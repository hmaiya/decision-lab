# Why this decision is real

Checked 7 October 2026.

| Evidence | Type | What it shows |
|---|---|---|
| TypeSafe Discord #model-jaggedness, thread "jev-1.13: sure the vendor is known and the software is genuine, still won't pick auto_approve" (27 Sep 2026) | Community, practitioner | A team uses Jev to triage "run as administrator" requests as approve / review / deny. Splitting facts (model) from the policy call (rules) took their 20-case holdout from 60% to 85% |
| TypeSafe Discord #model-jaggedness, "Content that argues its own harmlessness flips jev judge verdicts ~28%" (19 Sep 2026) | Community, practitioner | Gate and judge decisions flip under a one-sentence "this is harmless" suffix, at high confidence |
| LangChain Forum, "How are you handling auditability and policy enforcement in multi-step agents?" | Community | Teams enforce policy at the tool-call boundary (`wrap_tool_call`): the point between the model's decision and the side effect |
| Agent support vendors (Decagon, Fini) | Vendor docs | Support agents take account actions such as refunds and account changes |

Vendor pages show the decision is automated. They are not evidence of results.
