# Agent Workflow Readiness Index V0

## How 12 agent platforms publicly demonstrate workflow readiness

Evidence reviewed 8 October 2026.

Agent platforms increasingly simulate complete workflows before production. Eleven of the twelve companies reviewed publicly describe end-to-end simulation. Several also validate tool behavior, compare agent versions, include domain experts, and connect results to production outcomes.

The remaining question is portability: can an enterprise apply one acceptance standard across vendors, models, and releases?

This index maps public evidence. It does not rank product quality.

## Evidence matrix

| Company | Model or configuration comparison | Trace or production evaluation | Action and tool validation | Human acceptance | Workflow simulation | Business outcome |
|---|---|---|---|---|---|---|
| [Ada](#ada) | Not found publicly | Partial | Partial | Shown | Partial | Shown |
| [Cresta](#cresta) | Shown | Shown | Shown | Shown | Shown | Shown |
| [Decagon](#decagon) | Shown | Shown | Partial | Shown | Shown | Shown |
| [Forethought](#forethought) | Partial | Shown | Shown | Partial | Shown | Shown |
| [Hippocratic AI](#hippocratic-ai) | Shown | Shown | Partial | Shown | Shown | Shown |
| [Intercom](#intercom) | Partial | Shown | Partial | Shown | Shown | Shown |
| [Maven AGI](#maven-agi) | Partial | Shown | Shown | Partial | Shown | Shown |
| [Parloa](#parloa) | Shown | Shown | Shown | Shown | Shown | Shown |
| [PolyAI](#polyai) | Shown | Shown | Shown | Partial | Shown | Shown |
| [Regal](#regal) | Partial | Shown | Shown | Shown | Shown | Partial |
| [Salesforce Agentforce](#salesforce-agentforce) | Partial | Shown | Shown | Shown | Shown | Partial |
| [Sierra](#sierra) | Shown | Shown | Shown | Shown | Shown | Shown |

`Shown` means a first-party source explicitly demonstrates the capability. `Partial` means the source shows an adjacent capability but leaves part of the criterion unclear. `Not found publicly` means the reviewed public material did not establish it. It does not mean the capability is absent.

No company has reviewed its row yet.

## What V0 shows

### Simulation is becoming part of the agent platform

Eleven companies publicly describe multi-turn or multi-step simulation. Sierra turns annotated conversations into regression tests against mock APIs. Parloa covers intents, tool calls, and handoffs. Salesforce tests action sequences in a sandbox. Hippocratic AI combines patient simulation with clinician review.

### Evaluation is moving toward operating outcomes

The stronger systems measure more than answer quality. Public evidence includes resolution, CSAT, safety events, action success, procedural correctness, cost, and real-world cross-validation.

### Enterprise ownership remains unclear

The reviewed material rarely answers four questions:

1. Can the same acceptance suite run outside the vendor's platform?
2. Can it compare two vendors, not only two versions inside one platform?
3. Can the enterprise own and version the scenarios and acceptance criteria?
4. Can the environment reproduce private systems, permissions, failures, and state transitions without touching production?

These are open questions. They are not claims about missing product capabilities.

## Company evidence

### Ada

GoFundMe describes three testing phases and human scores from Care Support, Trust and Safety, Security, and Strategy. Ada also shows API-backed customer workflows. The reviewed material does not establish persistent workflow simulation or configuration comparison.

- [GoFundMe case study](https://www.ada.cx/case-study/gofundme/)
- [Deezer case study](https://www.ada.cx/case-study/deezer/)

### Cresta

Cresta derives synthetic customers from conversation data, drafts binary criteria from enterprise documentation, calibrates evaluators against experts, and evaluates expected outcomes in tests and production.

- [AI agent test and deploy](https://cresta.com/ai-agent-test-and-deploy)
- [Production-grade AI agents](https://cresta.com/blog/building-and-deploying-production-grade-ai-agents-crestas-end-to-end-approach)

### Decagon

Decagon evaluates simulated environment flow and success criteria, calibrates judges against human labels, and compares offline evaluation with production outcomes.

- [DuetBench 2](https://decagon.ai/blog/duetbench-2)
- [Evaluation engine](https://decagon.ai/blog/evaluation-engine-ai-agents)

### Forethought

Forethought simulates complete interactions and asserts responses, actions, business logic, required information, and prohibited behavior. Agent QA evaluates production conversations.

- [Test Suite](https://forethought.ai/blog/say-hello-to-test-suite-simulating-real-conversations-verifying-outcomes)
- [Agent QA](https://forethought.ai/blog/introducing-assist-agent-and-agent-qa-a-new-era-of-human-ai-collaboration-in-cx)

### Hippocratic AI

Hippocratic AI combines patient simulation, safety models, clinician evaluation, a clinical review gate, and real-world cross-validation.

- [AI Certified Agent Builder](https://hippocraticai.com/ai-certified-agent-builder/)
- [Polaris evaluation](https://hippocraticai.com/polaris-1/)
- [Real-world evaluation](https://hippocraticai.com/real-world-evaluation-llm/)

### Intercom

Intercom Evals creates simulated scenarios from company conversations, applies pass or fail criteria, stores a release candidate, reruns tests after changes, and monitors production conversations.

- [Evals and Releases](https://www.intercom.com/blog/announcing-evals-and-releases)
- [Deploy Fin](https://www.intercom.com/help/en/articles/8286630-deploy-fin-ai-agent-over-chat)

### Maven AGI

Maven describes regression testing, simulation, action workflows, monitoring, and autonomous-resolution outcomes. The reviewed material does not show whether one case set compares external agents or model stacks.

- [Automating Tier-1 support](https://www.mavenagi.com/blog/automate-tier1-support-tickets)
- [Customer stories](https://www.mavenagi.com/customer-stories)

### Parloa

Parloa generates simulations from agent configuration, tests intents, tool calls, handoffs, and business boundaries, keeps drafts under human review, and compares agent versions on identical scenarios.

- [Performance Lab](https://www.parloa.com/platform/performance-lab/)
- [Automated simulations and A/B testing](https://www.parloa.com/blog/confidently-release-agent-improvements-faster-with-automated-testing/)

### PolyAI

PolyAI generates tests from flows, knowledge, and tools, runs simulated conversations, uses LLM judges, and compares live versions on containment, CSAT, and handle time.

- [Testing AI agents before deployment](https://poly.ai/blog/testing-ai-agents-before-deployment)
- [Self-learning AI agents](https://poly.ai/blog/self-learning-ai-agents-customer-service)

### Regal

Regal simulates full conversations, evaluates custom actions and function calls, stores transcripts, and combines automated testing with forward-deployed review. The public material defines test success criteria but does not show how simulated pass rates are calibrated to production operating outcomes.

- [Simulations](https://www.regal.ai/simulations)
- [Simulation testing documentation](https://developer.regal.ai/docs/test-cases-simulation)

### Salesforce Agentforce

Testing Center simulates multi-turn conversations in a sandbox, evaluates topics, actions, responses, and traces, and includes business users in validation.

- [Testing Center overview](https://help.salesforce.com/s/articleView?id=005228642&language=en_US&type=1)
- [Testing Center documentation](https://help.salesforce.com/s/articleView?id=ai.agent_testing_center.htm&language=en_US&type=5)

### Sierra

Sierra turns annotated conversations into persistent regression tests, runs them against mock APIs, traces tool calls, packages immutable releases, and supports A/B tests against business goals.

- [Agent development lifecycle](https://sierra.ai/blog/agent-development-life-cycle)
- [Simulations](https://sierra.ai/blog/simulations-the-secret-behind-every-great-agent)
- [Release governance](https://sierra.ai/fr/blog/release-governance-guardrails-for-agents-at-scale)

## Files

- [`data/companies.csv`](data/companies.csv): public matrix and verification status
- [`data/sources.csv`](data/sources.csv): source registry and evidence summaries
- [`METHODOLOGY.md`](METHODOLOGY.md): definitions and review rules
- [`CHANGELOG.md`](CHANGELOG.md): corrections and version history
- [`CONTRIBUTING.md`](CONTRIBUTING.md): how to submit a correction
- [`validate.py`](validate.py): data checks run on every pull request

## Correct a row

[Open an index correction issue](../../issues/new?template=correct-readiness-index.yml). Include a first-party public source and the exact field it changes. Corrections are credited in the changelog.
