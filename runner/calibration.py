#!/usr/bin/env python3
"""
calibration.py: does each engine's confidence tell you when to trust it?

  python3 calibration.py action-gate                 # newest run
  python3 calibration.py action-gate --run <run-id>  # a specific run
  python3 calibration.py action-gate --cutoff 0.85

Reads results/<run-id>/results.json and writes, next to it:
  calibration.md   per engine: accuracy above and below the cutoff, per slice,
                   confident errors, and what routing below the cutoff would cost
  calibration.png  one strip chart per engine: every case placed by its
                   confidence, colored right or wrong, one row per slice
Only engines that returned a confidence are charted.
"""
import argparse
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

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
TEMPLATES = _find_templates(HERE)

# Colors and ink from the Decision Lab chart palette (light surface).
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
RIGHT, WRONG = "#2a78d6", "#eb6834"


def newest_run(folder):
    runs = sorted(d for d in os.listdir(os.path.join(folder, "results"))
                  if os.path.isfile(os.path.join(folder, "results", d, "results.json")) and "-" in d
                  and not any(tag in d for tag in ("smoke", "bug")))
    if not runs:
        sys.exit("No usable runs. Run bench.py first.")
    return runs[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template")
    ap.add_argument("--run")
    ap.add_argument("--cutoff", type=float, default=0.9)
    ap.add_argument("--fallback", help="implementation id to route low-confidence cases to")
    a = ap.parse_args()

    folder = os.path.join(TEMPLATES, a.template)
    run_id = a.run or newest_run(folder)
    out_dir = os.path.join(folder, "results", run_id)
    run = json.load(open(os.path.join(out_dir, "results.json")))
    rows = run["rows"]
    engines = [i for i in run["scores"] if any(r["results"][i].get("confidence") is not None for r in rows)]
    if not engines:
        sys.exit("No engine in this run returned a confidence.")
    # Default fallback: the most accurate engine.
    fallback = a.fallback or max(run["scores"], key=lambda i: run["scores"][i]["accuracy"])

    # Step 1: the written summary.
    L = [f"# Calibration: {a.template}, run {run_id}", "", f"Cutoff {a.cutoff}. Fallback for cases below it: {fallback}.", ""]
    for e in engines:
        above = [r for r in rows if (r["results"][e].get("confidence") or 0) >= a.cutoff]
        below = [r for r in rows if r not in above]
        right = lambda rs, impl: sum(r["results"][impl]["outcome"] == r["expected"] for r in rs)
        routed_right = right(above, e) + right(below, fallback)
        L += [f"## {e}", "",
              f"- At or above {a.cutoff}: {right(above, e)}/{len(above)} right",
              f"- Below {a.cutoff}: {right(below, e)}/{len(below)} right",
              f"- Confident errors (wrong at or above {a.cutoff}): {len(above) - right(above, e)}",
              f"- Route below-cutoff cases to {fallback}: {routed_right}/{len(rows)} right, "
              f"{len(above)}/{len(rows)} answered by {e} alone", "",
              "| Slice | Cases | Right | Mean confidence | Mean confidence when wrong |", "|---|---|---|---|---|"]
        slices = sorted({s for r in rows for s in r["slices"]})
        for s in slices:
            rs = [r for r in rows if s in r["slices"]]
            confs = [r["results"][e].get("confidence") or 0 for r in rs]
            wrong = [r["results"][e].get("confidence") or 0 for r in rs if r["results"][e]["outcome"] != r["expected"]]
            L.append(f"| {s} | {len(rs)} | {right(rs, e)} | {sum(confs) / len(confs):.2f} | "
                     + (f"{sum(wrong) / len(wrong):.2f}" if wrong else "n/a") + " |")
        L.append("")
    open(os.path.join(out_dir, "calibration.md"), "w").write("\n".join(L) + "\n")

    # Step 2: the chart, one panel per engine, one row per slice.
    slices = sorted({s for r in rows for s in r["slices"]})
    fig, axes = plt.subplots(len(engines), 1, figsize=(10, 1.0 + 0.45 * len(slices) * len(engines)), dpi=180, squeeze=False)
    fig.patch.set_facecolor(SURFACE)
    for ax, e in zip(axes[:, 0], engines):
        ax.set_facecolor(SURFACE)
        for y, s in enumerate(slices):
            rs = [r for r in rows if s in r["slices"]]
            for k, r in enumerate(rs):
                c = r["results"][e].get("confidence")
                if c is None:
                    continue
                ok = r["results"][e]["outcome"] == r["expected"]
                jitter = ((k % 5) - 2) * 0.07
                ax.scatter(min(c, 0.998), y + jitter, s=46, color=RIGHT if ok else WRONG,
                           edgecolor=SURFACE, linewidth=1.2, zorder=3)
        ax.axvline(a.cutoff, color=INK2, linestyle=(0, (4, 3)), linewidth=1.1)
        ax.set_yticks(range(len(slices)))
        ax.set_yticklabels(slices, fontsize=8.5, color=INK)
        ax.set_xlim(0, 1.02)
        ax.set_ylim(-0.6, len(slices) - 0.4)
        ax.set_title(e, loc="left", fontsize=10, color=INK)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        ax.tick_params(colors=INK2, length=0, labelsize=8)
        ax.grid(axis="x", color=GRID, linewidth=0.7, zorder=0)
    axes[-1, 0].set_xlabel("Confidence in its answer (blue = right, orange = wrong)", fontsize=9, color=INK2)
    fig.suptitle(f"{a.template}: where each engine is sure, and whether it is right", x=0.02, ha="left", fontsize=11.5, color=INK)
    fig.text(0.02, 0.005, f"Run {run_id}. Check results.md for label status before publishing.", fontsize=7, color=INK2)
    plt.tight_layout(rect=(0, 0.02, 1, 0.97))
    plt.savefig(os.path.join(out_dir, "calibration.png"), facecolor=SURFACE)
    print(open(os.path.join(out_dir, "calibration.md")).read())
    print("Saved:", os.path.join(out_dir, "calibration.png"))


if __name__ == "__main__":
    main()
