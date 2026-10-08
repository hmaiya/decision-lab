#!/usr/bin/env python3
"""
bench.py: run one Decision Library template on every implementation, same cases.

  python3 bench.py action-gate                       # full run, all implementations
  python3 bench.py action-gate --limit 5             # quick check
  python3 bench.py action-gate --llm-confidence      # ask LLMs to state a confidence too
  python3 bench.py action-gate --models anthropic/claude-sonnet-5.5
  python3 bench.py action-gate --dry-run             # show requests, call nothing

Implementations are read from templates/<name>/implementations/:
  jev.yaml        kind: jev        one Choice question carries the whole policy
  jev_facts.yaml  kind: jev_facts  Jev answers fact questions, rules.py decides
  llm.yaml        kind: llm        frontier models with the policy as a prompt

Writes templates/<name>/results/<run-id>/results.json and results.md.
Every number used later (reports, posts) must come from these files.
"""
import argparse
import importlib.util
import json
import os
import re
import statistics
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import yaml

def _find_templates(here):
    # Step 1: an explicit folder wins (DECISIONS_DIR=/path/to/decisions).
    if os.environ.get("DECISIONS_DIR"):
        return os.environ["DECISIONS_DIR"]
    # Step 2: public repo layout: decision-lab/runner/ next to decision-lab/decisions/.
    repo = os.path.join(os.path.dirname(here), "decisions")
    if os.path.isdir(repo):
        return repo
    # Step 3: agents layout: agents/decision-bench/scripts/ and agents/decision-library/templates/.
    return os.path.join(os.path.dirname(os.path.dirname(here)), "decision-library", "templates")


HERE = os.path.dirname(os.path.abspath(__file__))
AGENTS = os.path.dirname(os.path.dirname(HERE))
TEMPLATES = _find_templates(HERE)
# openrouter.py sits next to this script in the repo, or in agents/shared/.
sys.path.insert(0, os.path.join(AGENTS, "shared"))
sys.path.insert(0, HERE)
import openrouter  # noqa: E402

JEV_PRICE_PER_M = 0.042   # USD per million input tokens (TypeSafe list price)
BANDS = (("0.9+", 0.9, 1.01), ("0.6-0.9", 0.6, 0.9), ("<0.6", -1, 0.6))


# ---------- Step 1: load the template and its implementations ----------
def load(name):
    folder = os.path.join(TEMPLATES, name)
    decision = yaml.safe_load(open(os.path.join(folder, "decision.yaml")))
    cases = [json.loads(l) for l in open(os.path.join(folder, "cases.jsonl")) if l.strip()]
    policy = open(os.path.join(folder, decision.get("policy_file", "policy.md"))).read()
    impl_dir = os.path.join(folder, "implementations")
    impls = []
    for fname in sorted(os.listdir(impl_dir)):
        if not fname.endswith(".yaml"):
            continue
        cfg = yaml.safe_load(open(os.path.join(impl_dir, fname)))
        cfg["_dir"] = impl_dir
        if cfg.get("kind") == "jev_facts":
            # Load the rules module that turns facts into an outcome.
            spec = importlib.util.spec_from_file_location("rules", os.path.join(impl_dir, cfg["rules"]))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            cfg["_decide"] = mod.decide
        impls.append(cfg)
    return folder, decision, cases, impls, policy


# ---------- Step 2: one call per implementation ----------
def run_jev(case, cfg):
    """Whole policy in one Choice question."""
    r = openrouter.jev(case["input"], {cfg["question_key"]: cfg["question"]}, model=cfg["model"])
    if not r["ok"]:
        return {"outcome": "error", "error": f"{r.get('status')}: {r['error'][:300]}", "ms": r["ms"]}
    ans = r["data"]["answers"][cfg["question_key"]]
    usage = r["data"].get("usage", {})
    return {"outcome": ans.get("choice"), "confidence": ans.get("confidence"),
            "probabilities": ans.get("probabilities"), "ms": r["ms"],
            "input_tokens": usage.get("input_tokens", 0), "cost": usage.get("cost") or 0,
            "model_version": r["data"].get("model")}


def run_jev_facts(case, cfg):
    """Jev answers narrow fact questions; the rules module makes the policy call."""
    r = openrouter.jev(case["input"], cfg["questions"], model=cfg["model"])
    if not r["ok"]:
        return {"outcome": "error", "error": f"{r.get('status')}: {r['error'][:300]}", "ms": r["ms"]}
    answers = r["data"]["answers"]
    facts = {k: answers[k].get("choice") for k in cfg["questions"]}
    confs = [answers[k].get("confidence") for k in cfg["questions"] if answers[k].get("confidence") is not None]
    usage = r["data"].get("usage", {})
    return {"outcome": cfg["_decide"](facts, case["input"]), "facts": facts,
            # The decision is only as sure as its least sure fact.
            "confidence": min(confs) if confs else None,
            "fact_confidence": {k: answers[k].get("confidence") for k in cfg["questions"]},
            "ms": r["ms"], "input_tokens": usage.get("input_tokens", 0), "cost": usage.get("cost") or 0,
            "model_version": r["data"].get("model")}


def run_llm(case, model, system, outcomes, ask_confidence):
    """Frontier model with the policy as a prompt. Answer read from the last ANSWER: line."""
    tail = f"\n\nEnd your reply with one line: ANSWER: {', '.join(outcomes)}."
    if ask_confidence:
        tail += " Then one more line: CONFIDENCE: a number from 0 to 1 for how likely your answer is correct."
    msgs = [{"role": "system", "content": system + tail},
            {"role": "user", "content": json.dumps(case["input"])}]
    r = openrouter.chat(model, msgs, max_tokens=600)
    if not r["ok"]:
        return {"outcome": "error", "error": f"{r.get('status')}: {r['error'][:300]}", "ms": r["ms"]}
    text = (r["data"]["choices"][0]["message"].get("content") or "").strip().lower()
    m = re.findall(r"answer:\s*([a-z_]+)", text)
    found = [w for w in re.findall(r"[a-z_]+", text) if w in outcomes]
    word = m[-1] if m else (found[-1] if found else "")
    conf = re.findall(r"confidence:\s*([01](?:\.\d+)?)", text)
    usage = r["data"].get("usage", {})
    # With BYOK, OpenRouter bills $0 and the provider bills directly. Count both.
    cost = usage.get("cost") or 0
    if usage.get("is_byok"):
        cost += (usage.get("cost_details") or {}).get("upstream_inference_cost") or 0
    return {"outcome": word if word in outcomes else "invalid", "raw": text[-80:],
            "confidence": float(conf[-1]) if conf else None, "confidence_kind": "stated" if conf else None,
            "ms": r["ms"], "input_tokens": usage.get("prompt_tokens", 0),
            "output_tokens": usage.get("completion_tokens", 0), "cost": cost,
            "byok": bool(usage.get("is_byok")), "model_version": r["data"].get("model")}


# ---------- Step 3: score one implementation ----------
def score(rows, impl, decision):
    costly = decision.get("costly_outcome", "approve")
    exp = [r["expected"] for r in rows]
    got = [r["results"][impl]["outcome"] for r in rows]
    res = [r["results"][impl] for r in rows]
    n = len(rows)
    out = {"accuracy": sum(e == g for e, g in zip(exp, got)) / n,
           "correct": sum(e == g for e, g in zip(exp, got)), "n": n,
           "costly_outcome": costly,
           "costly_errors": sum(1 for e, g in zip(exp, got) if g == costly and e != costly),
           "errors": got.count("error"), "invalid": got.count("invalid")}
    out["per_outcome"] = {o: {"cases": sum(e == o for e in exp),
                              "right": sum(e == o and g == o for e, g in zip(exp, got))}
                          for o in decision["outcomes"]}
    by_slice = defaultdict(lambda: [0, 0])
    for r, g in zip(rows, got):
        for s in r["slices"]:
            by_slice[s][0] += 1
            by_slice[s][1] += (g == r["expected"])
    out["by_slice"] = {k: {"cases": v[0], "right": v[1]} for k, v in by_slice.items()}
    ms = [x["ms"] for x in res if x["outcome"] != "error"]
    out["median_ms"] = statistics.median(ms) if ms else None
    out["p90_ms"] = sorted(ms)[int(0.9 * (len(ms) - 1))] if ms else None
    cost = sum(x.get("cost", 0) for x in res)
    tokens = sum(x.get("input_tokens", 0) for x in res)
    out.update(billed_usd=cost, billed_per_1000=cost / n * 1000, input_tokens=tokens)
    if impl.startswith("jev"):
        out["list_per_1000"] = tokens / n * 1000 * JEV_PRICE_PER_M / 1e6
    # Confidence bands, for any implementation that returned a confidence.
    if any(x.get("confidence") is not None for x in res):
        out["confidence_bands"] = {}
        for name, lo, hi in BANDS:
            idx = [i for i, x in enumerate(res) if x.get("confidence") is not None and lo <= x["confidence"] < hi]
            out["confidence_bands"][name] = {"cases": len(idx), "right": sum(got[i] == exp[i] for i in idx)}
        # Wrong answers given with high confidence: the ones a cutoff cannot catch.
        out["confident_errors"] = sum(1 for i, x in enumerate(res)
                                      if x.get("confidence") is not None and x["confidence"] >= 0.9 and got[i] != exp[i])
    return out


# ---------- Step 4: write the report ----------
def pct(a, b):
    return f"{a}/{b} ({a / b:.0%})" if b else "0/0"


def report(run, decision):
    impls = list(run["scores"])
    costly = decision.get("costly_outcome", "approve")
    L = [f"# Results: {decision['id']} v{decision['version']}", "",
         f"Run {run['run_id']} · {run['n']} cases · labels: {decision.get('status', '?')}", ""]
    if decision.get("status") == "draft":
        L += ["> Draft labels. Not reviewed by a person yet. Say so if you publish these numbers.", ""]
    L += [f"| Implementation | Accuracy | Wrong {costly} | Confident errors (≥0.9) | Median latency | Cost per 1,000 | Errors |",
          "|---|---|---|---|---|---|---|"]
    for i in impls:
        s = run["scores"][i]
        billed = f"${s['billed_per_1000']:.3f}" + (f" (list ${s['list_per_1000']:.4f})" if "list_per_1000" in s else "")
        lat = f"{s['median_ms']:.0f} ms" if s["median_ms"] else "n/a"
        ce = s.get("confident_errors", "n/a")
        L.append(f"| {i} | {pct(s['correct'], s['n'])} | {s['costly_errors']} | {ce} | {lat} | {billed} | {s['errors'] + s['invalid']} |")
    L += ["", "## By outcome (right / cases)", "", "| Outcome | " + " | ".join(impls) + " |", "|---" * (len(impls) + 1) + "|"]
    for o in decision["outcomes"]:
        L.append(f"| {o} | " + " | ".join(pct(run['scores'][i]['per_outcome'][o]['right'], run['scores'][i]['per_outcome'][o]['cases']) for i in impls) + " |")
    L += ["", "## By slice (right / cases)", "", "| Slice | " + " | ".join(impls) + " |", "|---" * (len(impls) + 1) + "|"]
    for sl in sorted(run["scores"][impls[0]]["by_slice"]):
        L.append(f"| {sl} | " + " | ".join(pct(run['scores'][i]['by_slice'][sl]['right'], run['scores'][i]['by_slice'][sl]['cases']) for i in impls) + " |")
    for i in impls:
        if "confidence_bands" in run["scores"][i]:
            L += ["", f"## {i}: accuracy by confidence band", "", "| Band | Cases | Right |", "|---|---|---|"]
            for b, v in run["scores"][i]["confidence_bands"].items():
                L.append(f"| {b} | {v['cases']} | {pct(v['right'], v['cases'])} |")
    L += ["", "## Misses", "", "| Case | Slice | Expected | " + " | ".join(impls) + " | Text |", "|---" * (len(impls) + 4) + "|"]
    for r in run["rows"]:
        outs = [r["results"][i]["outcome"] for i in impls]
        if any(o != r["expected"] for o in outs):
            msg = r["message"][:70].replace("|", "/")
            L.append(f"| {r['id']} | {','.join(r['slices'])} | {r['expected']} | " + " | ".join(outs) + f" | {msg} |")
    L += ["", "Cost: OpenRouter usage.cost plus upstream cost under BYOK. Jev list figure uses $0.042 per million input tokens.",
          "", "Model versions: " + ", ".join(f"{i}={run['versions'].get(i)}" for i in impls)]
    return "\n".join(L) + "\n"


# ---------- Step 5: command line ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--models", nargs="*", help="override the LLM list in llm.yaml")
    ap.add_argument("--only", nargs="*", help="run only these implementation ids, e.g. jev-facts")
    ap.add_argument("--llm-confidence", action="store_true", help="ask LLMs to state a confidence")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()

    folder, decision, cases, impl_cfgs, policy = load(a.template)
    cases = cases[: a.limit] if a.limit else cases
    display = decision.get("display_field", "customer_message")

    # Build the list of (implementation id, function) to run on each case.
    runners = []
    for cfg in impl_cfgs:
        if cfg["kind"] == "jev":
            runners.append((cfg["id"], lambda c, cfg=cfg: run_jev(c, cfg)))
        elif cfg["kind"] == "jev_facts":
            runners.append((cfg["id"], lambda c, cfg=cfg: run_jev_facts(c, cfg)))
        elif cfg["kind"] == "llm":
            system = cfg["system"].replace("{policy}", policy)
            for m in (a.models if a.models is not None else cfg["models"]):
                runners.append((f"{cfg['id']}:{m}", lambda c, m=m, s=system:
                                run_llm(c, m, s, decision["outcomes"], a.llm_confidence)))
    if a.only:
        runners = [r for r in runners if r[0] in a.only or r[0].split(":")[0] in a.only]

    if a.dry_run:
        print("Implementations:", [r[0] for r in runners])
        print("First case input:", json.dumps(cases[0]["input"])[:400])
        return

    def one(case):
        return {"id": case["id"], "expected": case["expected"]["outcome"], "slices": case["metadata"]["slices"],
                "message": str(case["input"].get(display, "")),
                "results": {rid: fn(case) for rid, fn in runners}}

    started = time.time()
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        rows = list(pool.map(one, cases))
    ids = [r[0] for r in runners]
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run = {"run_id": run_id, "template": a.template, "n": len(rows), "seconds": time.time() - started,
           "llm_confidence": a.llm_confidence, "rows": rows,
           "scores": {i: score(rows, i, decision) for i in ids},
           "versions": {i: next((r["results"][i].get("model_version") for r in rows
                                 if r["results"][i].get("model_version")), None) for i in ids}}
    out = os.path.join(folder, "results", run_id)
    os.makedirs(out, exist_ok=True)
    json.dump(run, open(os.path.join(out, "results.json"), "w"), indent=1)
    md = report(run, decision)
    open(os.path.join(out, "results.md"), "w").write(md)
    print(md)
    for rid in ids:
        errs = [r["results"][rid].get("error") for r in rows if r["results"][rid]["outcome"] == "error"]
        if errs:
            print(f"ERRORS {rid}: {len(errs)}, first: {errs[0]}")
    print(f"Saved: {out}\nNext: python3 calibration.py {a.template} --run {run_id}")


if __name__ == "__main__":
    main()
