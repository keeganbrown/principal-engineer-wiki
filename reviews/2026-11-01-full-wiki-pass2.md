# Wiki review — full wiki, pass 2, 2026-11-01

This review covers all 37 articles plus `index.md`, after the fixes on branch
`review-fixes-1`. The reviewers were the same as in pass 1:

- **NR** newcomer-reader
- **TA** technical-accuracy
- **PS** principal-skeptic
- **SE** style-editor
- **WG** wiki-gardener

Each reviewer checked its pass-1 findings against the new text. Tags such as
`[PS TA NR]` show which reviewers raised the same point.

## At a glance

| Severity | Count |
| --- | --- |
| must-fix | 2 |
| should-fix | 99 |
| consider | 82 |

### How pass 1 held up

- **Pass-1 must-fix items:** all 4 are fixed and verified (idempotency, backpressure, cap-theorem, dry).
- **NR findings:** every one is fixed, with no regressions.
- **PS and TA findings:** fixed in the 30 original articles, except the items listed in the next section.
- **WG findings:** most are resolved. All 7 proposed articles now exist, api-versioning went from 1 to 7 inbound links, and every index finding is done.

### Unfixed from pass 1, or new problems caused by a pass-1 fix

1. **Abstraction threshold is still inconsistent.** yagni's example abstracts at two formats while linking to "the rule of three". solid still says "second case". `[WG SE]`
2. **The saga ↔ CAP link was not reworded.** Sagas lose *isolation*, which none of CAP's replica-consistency models describe. `[WG TA]`
3. **feature-flags fallback fails open for permission flags.** Falling back to "on" would give every user paid features. `[TA NR]`
4. **backpressure overflow storage is unbounded**, which breaks the article's own first rule. `[PS TA NR]`
5. **The functional-core-imperative-shell conditional write means at-most-once delivery.** A crash between marking and sending loses the reminder, and the article doesn't say so. `[PS TA NR]`
6. **paved-roads brings back "adoption happens on its own"**, the claim pass 1 removed from influencing-without-authority. `[PS]`
7. **A few bold lead-ins in feature-flags and the ADR status line** are still not in house style. `[SE]`

### Must-fix

1. **expand-and-contract: "every step can be rolled back."** The contract step can't be undone. Once you stop writing the old shape, rolling back means reading stale data. The article contradicts itself here. `[PS must · TA SE NR should]`
2. **contract-testing: "If no contract mentions a field, it can be removed safely."** That is only true if *every* consumer publishes a contract. Old mobile releases, pipelines and analysts usually don't. `[PS must · TA SE should]`

**Should-fix items that are close to must-fix**, because they teach a real bug:

- **dry:** refunds must use the tax rate *charged on the original order*, not today's rate. `[TA]`
- **feature-flags:** the permission-flag fallback fails open (item 3 above). `[TA]`
- **idempotency:** the pseudocode never stores the request, so the sweeper can't redo the charge and the "same key, different payload" check can't run. `[TA SE]`

### Raised by two or more reviewers

- **retries-and-timeouts arithmetic.** "Retry three times" means four attempts, so five layers is 4⁵ = 1,024, not 3⁵. Also "fivefold/400%" doesn't follow from the setup, and "10%" depends on a retry budget the example never mentions. `[NR TA PS SE]`
- **"This article owns…" sentences** in cap-theorem, coupling, dry, ddd and hexagonal are maintainer notes leaking into the text. Delete them. `[WG SE NR]`
- **Duplicate example.** api-versioning and expand-and-contract use the same Ada Lovelace example. `[WG SE PS]`
- **backpressure copies the retry/timeout traps** that retries-and-timeouts owns. `[WG SE]`
- **Acronyms not expanded in each article** (the "every article stands alone" rule): CI (contract-testing, paved-roads, api-versioning, testing-pyramid, modular-monolith), CRUD (cqrs, ddd), DBA, MADR, IETF. `[NR SE]`
- **"Trace ID" undefined outside observability:** paved-roads, influencing, event-driven. `[NR SE]`
- **Terms of art left undefined:** span, unit of work, seam, repository, spike, port, fake, saga (in modular-monolith). `[NR SE]`
- **expand-and-contract says 3 phases but shows 5 steps.** `[NR SE]`
- **strangler-fig "roll back instantly"** ignores data the new system has already written. `[WG SE]`

---

## Convention rulings needed before the next fix pass

The style-editor flagged these patterns about 100 times. Most of those flags go away once the rules are settled:

| Question | Recommendation |
| --- | --- |
| Are glossary bullets in the form "**Term** — definition" allowed? (41 uses) | **Allow** them in definition lists. They read well. |
| May a term of art be bolded at the point it's defined, mid-sentence (**projector**, **bulkhead**)? | **Allow**, for first-use definitions only. |
| Bullet lead-ins that end at a colon or comma | **Fix.** A lead-in is a short clause ending in a period. |
| Titles that are acronyms for a list (CAP, SOLID), and alias titles in parentheses | **Allow** as exceptions. |
| Acronyms that never need expanding | API, HTTP, URL, SQL, JSON, UI, ID |
| The "Pattern" suffix in titles, and the leading "The" | **Drop both** (Saga, Strangler Fig, Testing Pyramid). |
| Pseudocode identifiers | **camelCase**, which most blocks already use. |

---

## Per-article findings

Must-fix and close-to-must-fix items appear above and are not repeated here. Items marked SE-format are bullet lead-in fixes.

### Principles
- **kiss:** title loses the second S. Use "Keep It Simple, Stupid (KISS)" or explain it `[TA SE]`. Two lead-ins `[SE]`.
- **yagni:** threshold drift (unfixed). Mixed bold styles in the cost list. Trim the restated reversible-decisions point `[WG SE]`.
- **dry:** refund rate bug (above). Example runs to 5 sentences. Delete "this article owns" `[TA SE]`.
- **separation-of-concerns:** "Why it matters" lead-ins are nouns. Drop "Don't oversell this" and "One subtle point". Define fake and port `[SE NR]`.
- **coupling-and-cohesion:** the dependency-inversion link should point to hexagonal. Link "eventually consistent" to cap. Delete the owns-line. Credit Stevens/Myers/Constantine more fully `[SE WG TA]`.
- **solid-principles:** threshold drift (unfixed) `[WG SE]`.
- **conways-law:** the quote is Conway's later restatement, not the 1968 paper. Use "inverse Conway maneuver" (LeRoy & Simons, 2010). Expand DBA. Example runs to 5 sentences `[TA SE NR]`.
- **cap-theorem:** replace the Sequential example (use ZooKeeper follower reads). Define "primary" before first use. Delete the owns-line. Fix the saga Related line `[TA NR SE WG]`.
- **reversible-decisions:** reversibility has a cost ("each hedge is code you carry"). Add the trap "small doors add up" (link paved-roads). Say which of Type 1/2 is which. Cover disagreement over which door type applies `[PS NR]`.

### Practices
- **expand-and-contract:** rollback (must-fix). Map the 3 phases onto the 5 steps. Add the hard part to the example: write conflicts, a lossy split, stragglers (or use the column-rename example). "Never contracting" conflicts with api-versioning's "keep forever". Add the cost (five deploys over weeks). Define dual write and idempotent. Credit Danilo Sato's "ParallelChange" (2014). Fix the three lead-in styles `[PS TA SE NR WG]`.
- **contract-testing:** removal claim (must-fix). Verify against every consumer *version* in production, not just the latest. Add organizational costs (provider states, broker, who pays). Contracts check shape, not meaning. Credit Ian Robinson (2006). Expand CI, OpenAPI/Protobuf. SE-format `[PS TA SE NR]`.
- **api-versioning:** RFC 9413 is from the IAB, not the IETF. Give it its own example (a `/v2` break plus `Sunset`). Expand CI/IETF/RFC. Heaviest SE-format cluster. Link expand-and-contract for the "keep forever" choice `[TA SE PS WG]`.
- **feature-flags:** permission fallback (above). Rewrite the fallback in terms of what the feature does, not on/off. Explain the Knight Capital mechanism (a server missed the deploy). Combine with expand-and-contract rather than "instead". Example runs to 6 sentences. Define PR `[TA NR SE PS WG]`.
- **design-docs:** define spike. Related line → "one-way doors are the strongest reason". Retitle to "Design Docs". SE-format `[NR PS SE]`.
- **architecture-decision-records:** in the example, say which option was chosen and what an event bus is. Expand MADR. Move the status values out of the code block. "Most ADR habits fade" → "Many". Use "a page or two" consistently `[NR SE TA]`.
- **code-review:** credit ship/show/ask to Rouan Wilsenach (2021). SE-format `[TA SE]`.
- **blameless-postmortems:** two lead-ins `[SE]`.
- **observability:** define span and label. Credit the golden signals (Google SRE book). Give a concrete threshold for when to add tracing. Link circuit-breaker's alerting advice `[NR TA PS SE]`.
- **technical-debt:** the example should show the interest paid while the debt was recorded. One lead-in `[PS SE]`.
- **test-driven-development:** define seam. Fold the one-sentence paragraph into step 1. Two lead-ins `[NR SE]`.
- **testing-pyramid:** expand CI. Retitle to "Testing Pyramid". SE-format `[NR SE]`.

### Architecture
- **retries-and-timeouts:** arithmetic and retry budget (above). The user clicking Pay again is a retry and needs the same idempotency key. "Retry at one layer" vs the client retrying in backpressure. 404 *is* sometimes retryable (read-after-write lag). Soften "almost every outage" `[NR TA PS SE WG]`.
- **idempotency:** store the request and its hash. Show what the losing insert does (409). Explain what to do when the downstream system has no key support (query its status, or accept at-most-once) `[TA SE PS]`.
- **functional-core-imperative-shell:** state the at-most-once cost and link the outbox. Add a limit to the portability claim. Fix mixed casing `[PS TA NR SE]`.
- **hexagonal-architecture:** delete the owns-line and split the 6-sentence paragraph. Define unit of work. `order.id` doesn't protect against a *client* retry (the key must come from the caller). Explain who recovers stuck pending orders. Add one bridging sentence explaining "core". SE-format `[SE NR TA PS WG]`.
- **modular-monolith:** expand CI, define saga. Explain how the paved-roads link relates. SE-format `[SE NR]`.
- **microservices:** the example hides the platform cost, and the module boundaries did most of the work. Add how to measure whether the split worked. Mention eventual consistency and link cap. Downplay "different technology need". Bullets are the furthest from house style. Make the PCI wording consistent `[PS WG SE TA]`.
- **domain-driven-design:** delete the owns-line. Expand CRUD. Define repository. Explain why large aggregates block each other. Credit Brandolini for Event Storming `[SE NR TA]`.
- **event-driven-architecture:** example says five services but shows four consumers. The broker becomes critical infrastructure, and dead-letter queues need an owner. Define trace ID and orchestrated saga. Expand SNS/SQS `[TA PS SE]`.
- **transactional-outbox:** two relays double-publish (use leader election or `SKIP LOCKED`). ID order is not commit order. Point CDC at the outbox table. State the costs of the outbox. Explain "partition". SE-format `[PS TA NR SE]`.
- **cqrs:** expand CRUD. Try replicas and caching before reaching for CQRS. Bridge the jump to multiple services. Link cap for read-your-writes. Make the bullets parallel `[NR SE PS WG]`.
- **saga-pattern:** loses isolation, not atomicity, and needs a CAP fix (above). Explain "command" next to EDA. Link retries-and-timeouts and reversible-decisions. Expand atomicity/isolation. Italicize authorize/capture `[TA WG NR SE]`.
- **circuit-breaker:** "no fallback" advice contradicts itself. Paging when the breaker opens conflicts with observability's "alert on symptoms". Link the retry trap to its owner. SE-format `[PS SE]`.
- **backpressure:** the unbounded overflow (above). Adding workers stops helping at the database's limit. Collapse the retry/timeout traps into a link `[PS TA NR WG SE]`.
- **strangler-fig:** rollback caveat for data the new system wrote. The last slices should be shown as the hardest. Retitle to "Strangler Fig". SE-format `[SE WG PS]`.

### Leadership
- **paved-roads:** "spreads on its own" is back (unfixed). Show the cost of migrating existing services and the permanent platform team. Going off-road isn't free. Expand CI and define trace ID. Swap the "cow path" metaphor `[PS NR SE]`.
- **influencing-without-authority:** define trace ID and structured logging. Its example nearly duplicates paved-roads, so vary it or show the holdouts. Change "pages" to "on-call alerts". SE-format `[NR PS SE]`.

---

## Whole-wiki findings (WG)

- **Missing links.** Add: microservices → cap (eventual consistency). dry ↔ microservices (shared libraries). saga → retries-and-timeouts and reversible-decisions. feature-flags → reversible-decisions. reversible-decisions → expand-and-contract. expand-and-contract → idempotency. transactional-outbox → strangler-fig.
- **Proposed articles (consider):**
  - `spikes-and-prototypes` (practices)
  - `progressive-delivery` (practices: canaries, percentage rollout, shadow traffic)
  - `event-sourcing` (architecture)
- **Index (consider).**
  - Give reversible-decisions its own "Judgment" subgroup.
  - Add it to the "New here?" path after yagni, and put separation-of-concerns before coupling.
  - Under "Evolving systems", add "see also expand-and-contract".

## Lessons for the next fix pass

- **Every fix needs its own cost check.** Several pass-1 fixes introduced a new unstated trade-off: the overflow store, at-most-once delivery, and the fail-open default.
- **New articles repeat old weaknesses.** The pass-1 lessons (benefits without limits, happy-path examples) came back in the 7 new articles.
- **A new owner article means trimming its neighbours.** When an article becomes the owner of a concept, cut the neighbouring articles' copies down to one sentence and a link.
- **Settle style conventions before rewriting.** A mechanical sweep for bullet lead-ins and acronyms should follow the rulings above.
