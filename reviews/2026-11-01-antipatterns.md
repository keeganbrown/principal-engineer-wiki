# Review: Pitfalls and antipatterns (2026-11-01)

**Scope:** the 10 articles in `wiki/antipatterns/`, their index section, and
the new glossary entries. All five reviewers; `wiki-gardener` covered the
whole wiki.
**Outcome:** every must-fix and should-fix item applied, plus most
"consider" items. Lint, the Python tests, and the JavaScript tests pass.

## Must-fix (all applied)

| Where | Finding | Reviewers |
| --- | --- | --- |
| metric-fixation | "When it doesn't apply" claimed latency/error budgets and cost ceilings can only be hit by improving the outcome; each has cheap workarounds. Now: they hold up only when tightly defined and audited. | skeptic, accuracy |
| god-object | Example swapped a field write for an event with no mention of staleness or the outbox. Now a plain in-process call, with the event-based costs stated for when payment moves out. | skeptic, newcomer |
| big-bang-rewrite | Parallel run on billing would double-charge. Example changed to a side-effect-free quoting engine; comparison noise and shadow-mode limits stated. | skeptic, gardener |

## Should-fix, by theme (applied)

- **Escape routes without a cost check:** build-check friction and the next `shared/` folder (big-ball-of-mud); delegation removal dates (god-object); event copies and team ownership when merging (distributed-monolith); strangler long tail (big-bang-rewrite); adapters leak and cost upkeep, Redis as the adopted tool's price (not-invented-here); DORA metrics are gameable too (metric-fixation). *(skeptic, gardener)*
- **Accuracy:** visibility-timeout mechanism (lost jobs, not duplicates; at-least-once then needs idempotency); Spotify claim re-sourced to its authors and former staff; Brooks's second-system effect is about a designer's second system; McKinley's tokens are per company; Parkinson's 45 minutes on roofing; Feynman's huts, and "cargo cult" predates him; Katz & Allen's five-year finding; Goodhart was about monetary statistics; availability arithmetic assumes independent failures. *(accuracy)*
- **Structure:** every article now has `Spotting it:` / `Climbing out:` groups (7 lacked them); the rule is recorded in CLAUDE.md. *(style)*
- **House rules:** US spelling throughout; "group by domain" instead of "business capabilities"; NIH title gets its acronym; bikeshedding credit moved to the end of "The idea"; tense fixed in distributed-monolith. *(style, gardener)*
- **Undefined terms:** cutover, service mesh, lead time, change failure rate, error and latency budgets, access pattern, composition root, coding agent, canary release, trunk-based development, supply-chain risk, entity split ("by noun"). *(newcomer, style)*
- **Overlap:** golden-hammer no longer reuses kiss's report-email example; big-bang-rewrite no longer reuses strangler-fig's billing story and defers shadow mode to it; bikeshedding defers comment labels to code-review; the feature-freeze trap now explains how it differs from strangler-fig's rule. *(gardener)*
- **Links:** not-invented-here had no inbound links (now from domain-driven-design and technical-debt); back-links added from dry, testing-pyramid, technical-debt, kiss, code-review, coupling-and-cohesion, separation-of-concerns; index "See also" lines under Structuring systems, Evolving systems, and Leadership. Golden-hammer and NIH are now framed as siblings; NIH and cargo cult as opposites. *(gardener)*
- **Glossary:** added Hero culture and Metric fixation; Characterization test now points to test-driven-development; Second-system effect corrected; Antipattern points to an example.

## Deferred

- **Proposed articles:** `lava-flow` (dead code and stale flags nobody dares delete) and `long-lived-branches`.
- **Consider:** append "(signs of a distributed monolith)" to microservices' traps — already one sentence each.
