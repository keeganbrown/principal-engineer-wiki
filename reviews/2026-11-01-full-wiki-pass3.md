# Wiki review — pass 3, 2026-11-01

**Scope:** articles whose content changed on branch `review-fixes-2`. The whole-wiki and style checks covered all 37 articles.

**Reviewers:**
- **TA** technical-accuracy (16 articles)
- **PS** principal-skeptic (22 articles, 2 batches)
- **NR** newcomer-reader (16 articles)
- **SE** style-editor (all 37; only checks the linter can't do)
- **WG** wiki-gardener (whole wiki)

## Trend

| Pass | Must-fix | Unfixed from previous pass | Notes |
| --- | --- | --- | --- |
| 1 | 4 | — | 30 articles, broad problems |
| 2 | 2 | 7 | Mostly in 7 new articles |
| 3 | **1** | **4** (all minor) | Mostly new problems introduced by pass-2 fixes |

- **TA:** every pass-2 finding is fixed, and every attribution checked out against primary sources.
- **PS:** every pass-2 finding is fixed in all 22 articles.
- **NR:** fixed except two items (RFC not expanded; "partition" only partly defined).
- **WG:** almost everything resolved. It proposes no new articles and no index changes, and calls the wiki "structurally healthy."
- **SE:** 15 articles came back fully clean. Only two paragraphs exceed four sentences.

## Must-fix

1. **expand-and-contract: measure before step 4, not step 5.** Stopping writes to the old column (step 4) is the real one-way door. In the example, the finance report has been reading stale names since step 4. The example therefore presents the mistake as the success. The guideline and the Related line both name the wrong step. `[PS · WG agrees on the Related line]`

## Unfixed from pass 2

- **circuit-breaker:** the example says "an alert fires," but the fallback works, so by the article's own rule nothing should page. The "No fallback" trap also conflicts with "a clear, fast failure" being a valid fallback. `[WG PS]`
- **solid-principles:** a "…owns ports, adapters, and dependency inversion" note is back in Related. The linter only matched "this article owns". `[WG]`
- **api-versioning:** RFC is still not expanded. `[NR SE]`
- **transactional-outbox:** "partition" is still only partly defined. `[NR SE]`

## Pass-2 fixes that brought a new race or an unstated cost

These are the main theme of this pass. Each pass-2 fix added a recovery mechanism, but the mechanism's own limits weren't stated.

| Article | Mechanism | Gap | Raised by |
| --- | --- | --- | --- |
| hexagonal | Caller-supplied key + reconciler | A retry can overwrite a completed order. A late retry can revive and charge a cancelled order. Needs `find` first, a conditional insert, and a conditional cancel. Also, "ask the provider by key" isn't a real Stripe lookup. | TA PS |
| idempotency | Sweeper | The provider's key expires (Stripe: about 24h). Needs an age threshold. A provider timeout also leaves the key `IN_PROGRESS`. | PS TA |
| expand-and-contract | Dual-write backfill | A read-then-write backfill can overwrite a dual-written edit. Use one `UPDATE … WHERE fullName IS NULL` per batch. The example timeline is also confusing. | TA PS NR |
| transactional-outbox | `SKIP LOCKED`, one relay per partition | Neither guarantees order. Lead with per-entity sequence numbers or entity-row locks. CDC replication slots can fill the database's disk. The example orders by ID without any caveat. | TA PS NR |
| retries-and-timeouts | One-layer rule + example | In the example, both the user and payment retry, which breaks the article's own rule. The retry budget has no stated cost. | PS WG |
| feature-flags | Cached-value fallback | You can't flip a kill switch while the flag service is down. Give critical switches an independent path. | PS |
| contract-testing | Verify every live version | The set only grows. Needs a published support window. | PS |
| dry | Pricing API owns the rate | Swaps release coupling for a runtime dependency. Checkout needs pricing up, or a cached rate. | PS |
| functional-core-imperative-shell | Outbox for must-happen effects | Brings back duplicates, so the sender must be idempotent. The conditional write doesn't re-check `paid`. | PS TA |
| event-driven-architecture | Dead-letter replay | Late replays can overwrite newer state. Consumers need version checks. | PS |
| saga | Semantic lock, workflow engine | A pending lock needs a timeout and an owner. The engine is a critical dependency with its own constraints (e.g., determinism). | PS |
| conways-law | Platform team | Becomes the old queue unless it ships self-service tools. | PS |
| paved-roads | Versioned libraries | Infrastructure only, never domain logic (see dry). Supporting several versions costs effort. | PS |
| strangler-fig | Shadow mode | Runs side effects twice on write paths. | PS |

**Proposed convention:** any recovery job (sweeper, reconciler, relay, replay) must state three things: its time window, how it stays idempotent or ordered, and who owns it.

## Other findings

- **api-versioning:** `Sunset: Sat, 31 Oct 2027` is wrong; that date is a Sunday (checked). `[TA]`
- **microservices ≈ modular-monolith:** both tell the same payments, PCI and saga extraction story. The "reasons to extract" list has also drifted between the two. Make microservices the owner of the list. `[WG]`
- **Link text isn't a definition.** "Two-way door" and "eventually consistent" appear only as link text in saga, feature-flags and retries. `[NR]`
- **Undefined terms and acronyms:**
  - Introduced by fixes: at-most-once, reconcile, leader election, `SKIP LOCKED`, fail open, guardrails (used before defined), lead time for changes, two-phase commit, exponential backoff, fault injection, test double. `[NR SE]`
  - Unexpanded acronyms, mostly in Related lines: UX, CLI, DBA, TDD, ADR, YAGNI. `[SE]`
  - Trace ID is undefined in microservices and saga; the correlation-ID alias is missing in event-driven-architecture and idempotency. `[SE]`
- **Paragraphs over four sentences:** domain-driven-design (Example) and architecture-decision-records (The idea). `[SE]`
- **Open convention question:** may constants and enum values be UPPER_CASE (`IN_PROGRESS`, `FREE_SHIPPING_THRESHOLD`)? `[SE]`
- **Missing links:** paved-roads → reversible-decisions, and conways-law → paved-roads. `[WG]`
- **Wording that reads like maintainer notes:** "The wiki's rule" in yagni and solid. `[WG]`

## Lessons

- **Each fix creates the next round's findings.** A mechanism added to fix one problem needs its own limits stated in the same edit. Adopting the recovery-job convention above would prevent most of this pass's findings.
- **Re-read the example after changing a rule.** Several examples drifted from their articles' rules: expand-and-contract, outbox, retries and circuit-breaker.
- **Widen the maintainer-note lint.** It should match "owns" in Related lines, not just "this article owns".
