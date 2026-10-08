# Calibration: refund-eligibility, run 20261006-052520

Cutoff 0.9. Fallback for cases below it: llm-v1:anthropic/claude-sonnet-5.5.

## jev-v1

- At or above 0.9: 34/34 right
- Below 0.9: 4/6 right
- Confident errors (wrong at or above 0.9): 0
- Route below-cutoff cases to llm-v1:anthropic/claude-sonnet-5.5: 40/40 right, 34/40 answered by jev-v1 alone

| Slice | Cases | Right | Mean confidence | Mean confidence when wrong |
|---|---|---|---|---|
| adversarial | 2 | 2 | 1.00 | n/a |
| change_of_mind | 9 | 9 | 0.99 | n/a |
| damaged | 10 | 10 | 1.00 | n/a |
| final_sale | 4 | 4 | 0.99 | n/a |
| not_delivered | 5 | 5 | 1.00 | n/a |
| over_500 | 3 | 3 | 1.00 | n/a |
| repeat_claimant | 3 | 3 | 1.00 | n/a |
| unclear | 6 | 4 | 0.65 | 0.54 |

