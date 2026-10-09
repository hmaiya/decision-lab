# Decision Lab

**Open tests of AI decision engines on real business decisions.** One decision definition, one case set, several engines, results by slice.

Decision models (TypeSafe Jev, OpenAI's Decisions API) and LLMs now approve, route and judge things inside agents. The question that matters is narrow: **when the engine is sure, is it right, on my decision, on each slice of it?**

## Reports

| # | Decision | Finding | Status |
|---|---|---|---|
| [1](reports/01-refund-eligibility/) | Refund eligibility, 40 cases, Jev 1.13 vs Claude Sonnet 5.5 vs GPT-6 Astra | Jev at ≥ 0.9 confidence: 35 of 35 correct. Routing the rest to Sonnet: 40 of 40 at about 87% lower cost than Sonnet alone. Both misses were approvals on vague requests | Published 6 Oct 2026 |
| [2](reports/02-action-gate/) | Action gate (approve / review / deny on an agent's proposed action), 46 cases with bypass attempts. Jev 1.13, Sonnet 5.5, GPT-6 Astra | Jev with facts from the model and policy in code: 46 of 46, no wrong approves, both runs. Policy in the prompt: 44 to 45 of 46. Two of four pre-registered expectations failed | Published 8 Oct 2026. LLM facts mode next |

## Agent Workflow Readiness Index

[V0 maps how 12 agent platforms publicly demonstrate workflow readiness](readiness-index/). It covers model and configuration comparison, trace evaluation, action validation, human acceptance, workflow simulation, and business outcomes. It is an evidence map, not a vendor ranking.

## What's here

```text
decisions/<name>/
  decision.yaml        the contract: outcomes, inputs, costly error, slices
  policy.md            the policy in plain words
  cases.jsonl          one case per line: input, expected outcome, slice
  build_cases.py       how the cases were made (synthetic decisions)
  implementations/     one file per engine setup (Jev, LLM, facts + rules)
  results/<run-id>/    results.json, results.md, calibration.md
runner/
  bench.py             run every implementation on every case
  calibration.py       accuracy and confidence by slice, routing result, chart
  openrouter.py        one small client for Jev and chat models via OpenRouter
```

## Run it

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY=...                      # or ~/.config/openrouter/key
python3 runner/bench.py action-gate --dry-run      # check setup, no API calls
python3 runner/bench.py action-gate --limit 5      # smoke test
python3 runner/bench.py action-gate --llm-confidence
python3 runner/calibration.py action-gate
```

## Bring your own decision

If you run an approve / review / deny, routing, tiering or judge decision, [open a "Submit a decision" issue](../../issues/new?template=submit-a-decision.md). Five free calibration runs are open now: we write the contract and 30 to 100 cases with you, run them across engines in both modes, and you keep everything. Published findings are anonymized and you see them first.

Or copy `decisions/action-gate/`, change the policy and cases, and run it yourself.

## Rules for every report

- Synthetic cases and unreviewed labels are disclosed.
- Numbers come from a `results.json` in this repo.
- Community findings are credited with links.
- One decision is a method, not a verdict on a model.

Maintained by Arti.
