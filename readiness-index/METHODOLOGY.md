# Methodology

## Research question

What public evidence shows that an agent can complete the customer's business workflow before production?

The index measures public evidence, not product quality or company readiness.

## Evidence states

- `shown`: a first-party source explicitly demonstrates the capability.
- `partial`: the source demonstrates an adjacent capability but leaves part of the criterion unclear.
- `not_found_publicly`: the reviewed public material does not establish the capability.

Silence is not evidence of absence. Company non-response is not confirmation.

## Dimensions

### Model or configuration comparison

The same cases compare models, prompts, agent versions, or configurations.

### Trace or production evaluation

Traces or live conversations are evaluated systematically.

### Action and tool validation

Tool calls, API behavior, state changes, or action order are checked.

### Human acceptance

Business, risk, clinical, or domain owners review or approve cases.

### Workflow simulation

A multi-turn or multi-step workflow runs end to end against expected outcomes before production.

### Business outcome

A production result such as resolution, completion, safety, CSAT, cost, or ROI closes the loop.

## Source rules

1. Use first-party product pages, documentation, engineering posts, research, or named customer stories.
2. Keep fact, interpretation, and unknown separate.
3. Do not infer a capability from company size, funding, hiring, or general reliability claims.
4. Record the evidence date and direct URL.
5. Prefer two sources when one page does not support the complete row.
6. Remove a classification when the source is ambiguous.

## Verification

Every row carries one status:

- `not_contacted`
- `fact_check_sent`
- `confirmed_by_company`
- `corrected_by_company`
- `not_reviewed_by_company`

Companies receive five business days for pre-publication fact-checking. Publication does not depend on a response. A correction must include public evidence or be labeled as private company context.

## Publication

- Companies remain in alphabetical order.
- V0 publishes no total score or rank.
- Aggregate findings appear before company-level evidence.
- Every release includes the evidence date, sources, verification status, and correction path.
- Material changes appear in `CHANGELOG.md`.

