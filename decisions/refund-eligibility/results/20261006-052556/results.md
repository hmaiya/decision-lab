# Results: refund_eligibility v0.1

Run 20261006-052556 · 40 cases · labels: draft

> Draft labels. Not reviewed by a person yet. Say so if you publish these numbers.

| Implementation | Accuracy | Wrong approvals | Median latency | Cost per 1,000 | Errors |
|---|---|---|---|---|---|
| jev-v1 | 38/40 (95%) | 2 | 265 ms | $0.000 (list $0.0282) | 0 |
| llm-v1:anthropic/claude-sonnet-5.5 | 40/40 (100%) | 0 | 2659 ms | $3.014 | 0 |
| llm-v1:openai/gpt-6-astra | 40/40 (100%) | 0 | 2041 ms | $5.112 | 0 |

## By outcome (right / cases)

| Outcome | jev-v1 | llm-v1:anthropic/claude-sonnet-5.5 | llm-v1:openai/gpt-6-astra |
|---|---|---|---|
| approve | 15/15 (100%) | 15/15 (100%) | 15/15 (100%) |
| deny | 8/8 (100%) | 8/8 (100%) | 8/8 (100%) |
| request_evidence | 9/11 (82%) | 11/11 (100%) | 11/11 (100%) |
| escalate | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) |

## By slice (right / cases)

| Slice | jev-v1 | llm-v1:anthropic/claude-sonnet-5.5 | llm-v1:openai/gpt-6-astra |
|---|---|---|---|
| adversarial | 2/2 (100%) | 2/2 (100%) | 2/2 (100%) |
| change_of_mind | 9/9 (100%) | 9/9 (100%) | 9/9 (100%) |
| damaged | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| final_sale | 4/4 (100%) | 4/4 (100%) | 4/4 (100%) |
| not_delivered | 5/5 (100%) | 5/5 (100%) | 5/5 (100%) |
| over_500 | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) |
| repeat_claimant | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) |
| unclear | 4/6 (67%) | 6/6 (100%) | 6/6 (100%) |

## jev-v1: accuracy by confidence band

| Band | Cases | Right |
|---|---|---|
| 0.9+ | 35 | 35/35 (100%) |
| 0.6-0.9 | 3 | 2/3 (67%) |
| <0.6 | 2 | 1/2 (50%) |

## Agreement between implementations

- jev-v1 vs llm-v1:anthropic/claude-sonnet-5.5: 38/40 (95%)
- jev-v1 vs llm-v1:openai/gpt-6-astra: 38/40 (95%)
- llm-v1:anthropic/claude-sonnet-5.5 vs llm-v1:openai/gpt-6-astra: 40/40 (100%)

## Misses

| Case | Expected | jev-v1 | llm-v1:anthropic/claude-sonnet-5.5 | llm-v1:openai/gpt-6-astra | Message |
|---|---|---|---|---|---|
| refund-028 | request_evidence | approve | request_evidence | request_evidence | This isn't working out, what are my options? |
| refund-029 | request_evidence | approve | request_evidence | request_evidence | Please process a return on my last order. |

Cost: OpenRouter usage.cost plus the provider's upstream cost when the account uses its own provider key (BYOK). Jev is billed by TypeSafe; the list figure uses $0.042 per million input tokens.


Model versions: jev-v1=typesafe/jev-1.13-20260917, llm-v1:anthropic/claude-sonnet-5.5=anthropic/claude-sonnet-5.5, llm-v1:openai/gpt-6-astra=openai/gpt-6-astra
