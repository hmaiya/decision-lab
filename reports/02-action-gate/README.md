# Calibration report #2: should an agent's action gate keep its policy in the prompt?

**Decision Lab. Pre-registered 8 October 2026. Status: cases and method published, runs in progress. Results will be added to this page; nothing above the Results section will change after the runs.**

## The question

Agents now take actions: refunds, account changes, data exports, admin grants. Most teams put a gate between the model's choice and the side effect. The gate answers **approve**, **review** or **deny**.

Two ways to build it:

1. **Policy in the prompt.** Give the model the policy and ask for the outcome.
2. **Facts plus rules.** Ask the model only facts ("is this a bypass attempt?", "does the action match the request?"). Code applies the policy.

One builder in the TypeSafe AI community moved from (1) to (2) on a Windows elevation gate and went from 60% to 85% on a 20-case holdout. This report tests whether that holds across engines, and whether any engine's confidence warns you on the slices that matter.

## Setup

| | |
|---|---|
| Decision | [`decisions/action-gate/`](../../decisions/action-gate/): `approve`, `review`, `deny`. Costly error: a wrong approve |
| Policy | 6 ordered rules ([`policy.md`](../../decisions/action-gate/policy.md)) |
| Cases | 46 synthetic cases. 14 approve, 19 review, 13 deny |
| Slices | clear 8, mismatch 8, unverified 6, high_risk 5, bypass_subtle 5, benign_mention 5, bypass_blatant 4, over_200 3, boundary 2 |
| Labels | Computed from the policy and each case's known facts. Not yet reviewed by a person |
| Implementations | `jev-policy` (Jev, policy in one Choice question), `jev-facts` (Jev answers two facts, [`rules.py`](../../decisions/action-gate/implementations/rules.py) decides), `llm-v1` (Claude Sonnet 5.5 and GPT-6 Astra, policy in the system prompt, stated confidence). OpenAI Decisions API when preview access arrives |
| Runs | Two full runs per implementation |

## What we expect, written before the runs

| # | Expectation | How we check |
|---|---|---|
| E1 | Facts plus rules is at least as accurate as policy in the prompt on every engine | Accuracy per implementation |
| E2 | Policy in the prompt makes more wrong approves on `bypass_subtle` | Wrong approves by slice |
| E3 | At least one engine is confidently wrong (≥ 0.9) on a bypass slice | Confident errors by slice |
| E4 | `benign_mention` cases get denied more often than they should under policy in the prompt | Wrong denies by slice |

If an expectation fails, the report says so.

## Results

_Pending. Two runs, then `results.md` and `calibration.md` per run are linked here._

## Limits

- Synthetic cases from one fictional company (Northwind SaaS).
- 46 cases: enough to see slice patterns, not to rank models.
- Labels not yet human-reviewed. Open an issue if you disagree with one.

## Reproduce

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY=...
python3 decisions/action-gate/build_cases.py
python3 runner/bench.py action-gate --llm-confidence
python3 runner/calibration.py action-gate
```
