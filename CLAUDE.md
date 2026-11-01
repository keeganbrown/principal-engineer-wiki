# Principal Engineer Wiki — maintainer guide

An LLM-maintained knowledge base of principles, practices, and architecture
patterns a Principal Software Engineer should know. Plain Markdown, readable
on GitHub or in Obsidian. The LLM writes and maintains the articles; humans
read them, ask questions, and point at new topics.

## Commands

| Task | Command |
| --- | --- |
| Test the linter | `python3 -m unittest discover -s tests` |
| Lint the wiki | `python3 scripts/lint_wiki.py` |
| Both (run before every commit) | `python3 -m unittest discover -s tests && python3 scripts/lint_wiki.py` |

Python 3.9+, standard library only. No install step.

## Layout

```
index.md              Entry point. Every article must be linked from here.
log.md                Append-only history of wiki changes (newest at top).
templates/article.md  Copy this to start a new article.
wiki/principles/      Timeless design rules (KISS, coupling, ...).
wiki/practices/       Things teams do (TDD, code review, ADRs, ...).
wiki/architecture/    Structural patterns (hexagonal, CQRS, ...).
wiki/leadership/      Influence, communication, and the non-code skills.
scripts/lint_wiki.py  Enforces the rules below.
docs/review-guide.md  Shared rules + output format for reviewer agents.
.claude/agents/       Reviewer agents, one perspective each.
.claude/skills/       /review-wiki — runs the reviewers and merges results.
reviews/              Saved review reports.
tests/                Tests for the linter.
```

## Article rules (enforced by the linter)

- File name is the **slug**: lowercase-kebab-case, unique across all folders.
- Frontmatter has `title`, `category` (must equal the folder name), `summary`
  (one plain sentence), and `tags` (`[a, b]`).
- Body contains these `##` sections, in this order:
  `The idea`, `Why it matters`, `How to apply it`, `Example`,
  `Common traps`, `When it doesn't apply`, `Related`.
- Cross-link with `[[slug]]` or `[[slug|display text]]`. Every link must
  resolve, and every article links to at least one other article.
- Max 1,200 words. If it's longer, split it into two articles.

## Writing style (enforced by you)

The audience is a smart engineer who is new to *this* topic. Write so they
get it on the first read.

- Lead with the plain-English idea. Jargon comes after the intuition, and
  gets defined the first time it appears.
- Short paragraphs (≤ 4 sentences). Prefer bullets for lists of things.
- One concrete, realistic example per article — code, a scenario, or a
  diagram. Keep code short and language-neutral where possible.
- Be honest about trade-offs. "When it doesn't apply" is not optional;
  principal engineers are paid for judgment, not dogma.
- Second person, active voice, no filler ("It is important to note that…").
- Use the **In one sentence** callout under the H1 — it should match `summary`.

### House conventions

Decided after the first full review (`reviews/2026-11-01-full-wiki.md`):

- **Every article stands alone.** Expand every acronym and define every
  term of art at first use *in that article*, even if another article
  defines it. Link to the owning article where one exists.
- **Credit after the idea.** Attribution (who, where, when) goes at the end
  of "The idea", never as the opening sentence.
- **Titles:** `Full Name (ACRONYM)` when there's an acronym, e.g.
  `Command Query Responsibility Segregation (CQRS)`.
- **Bullets:** a bold lead-in is a short, complete clause ending in a
  period (`**Bound every queue.** An unbounded…`), or no bold at all.
  Don't bold mid-sentence.
- **Pseudocode:** Python-like, colon-and-indent, no braces —
  `interface Clock:` / `    now()`. Comments with `#`.
- **Examples show the hard part.** If the happy path hides a race, a
  partial failure, or a cost, the example says so.
- **Benefits come with their limits.** Every claimed benefit gets its
  caveat in the same article.
- **Canonical terms:**
  - *trace ID* (mention "also called a correlation ID" once) — follows one
    request. Distinct from an *idempotency key*, which follows one
    *intended action* across retries.
  - *group by domain* (not "feature" or "business capability").
  - *paved road* (not "golden path").
  - *eventual consistency*, *change-data-capture (CDC)*, *pull request (PR)*.
- **Concept owners.** One article explains a cross-cutting idea; the rest
  give one sentence and link:

  | Concept | Owner |
  | --- | --- |
  | When to abstract (rule of three) | `dry` |
  | Why group by domain | `coupling-and-cohesion` |
  | How to find domain boundaries | `domain-driven-design` |
  | Shared-database coupling | `coupling-and-cohesion` |
  | Consistency models, staleness UX | `cap-theorem` |
  | Ports, adapters, dependency inversion | `hexagonal-architecture` |
  | Timeouts, retries, backoff, jitter | `retries-and-timeouts` |
  | Outbox, CDC | `transactional-outbox` |
  | Expand-and-contract migrations | `expand-and-contract` |
  | Contract tests | `contract-testing` |
  | One-way vs two-way doors | `reversible-decisions` |
  | Design docs = deliberation; ADRs = the record | `design-docs` / `architecture-decision-records` |

## Workflows

**Add an article:** copy `templates/article.md` → fill it in → add it to
`index.md` under the right heading → add `[[links]]` from 1–3 related
existing articles back to it → run lint → add a line to `log.md` → commit.

**Ingest a source** (book, talk, blog post): summarize what's new, then
update existing articles or create new ones. Note the source in `log.md`.
Don't paste copyrighted text; paraphrase and credit.

**Answer a question:** read `index.md`, open the relevant articles, answer
with `[[links]]`. If the answer is reusable, offer to file it as an article.

**Health check:** run lint; also look for contradictions between articles,
stale claims, and concepts mentioned in several articles that deserve
their own page.

**Content review:** run `/review-wiki [slugs…] [reviewers…]`. It fans out to
five read-only reviewer agents in `.claude/agents/` — `newcomer-reader`,
`technical-accuracy`, `principal-skeptic`, `style-editor`, `wiki-gardener` —
and merges their findings into `reviews/YYYY-MM-DD-<scope>.md`. Shared rules
and output format live in `docs/review-guide.md`; change them there, not in
each agent. Reviewers never edit articles; fixes are applied after the user
picks which to take.
