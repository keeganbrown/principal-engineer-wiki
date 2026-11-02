# Principal Engineer Wiki — maintainer guide

An LLM-maintained knowledge base of principles, practices, and architecture
patterns a Principal Software Engineer should know. Plain Markdown, readable
on GitHub or in Obsidian. The LLM writes and maintains the articles; humans
read them, ask questions, and point at new topics.

## Commands

| Task | Command |
| --- | --- |
| Test the Python (linter, site build) | `python3 -m unittest discover -s tests` |
| Test the site's JS logic | `node --test 'tests/web/*.test.js'` |
| Lint the wiki | `python3 scripts/lint_wiki.py` |
| Build the reader site into `_site/` | `python3 scripts/build_site.py` |
| Preview the site | build, then open `_site/index.html` (or `python3 -m http.server -d _site`) |
| All checks (run before every commit) | `python3 -m unittest discover -s tests && node --test 'tests/web/*.test.js' && python3 scripts/lint_wiki.py` |

Python 3.9+ standard library and Node 18+ (tests only). No install step.

**Publishing:** `.github/workflows/pages.yml` runs all checks on every PR
and push; pushes to `main` also build and deploy the site to GitHub Pages
(repo Settings → Pages → Source: GitHub Actions).

## Layout

```
index.md              Entry point. Every article must be linked from here.
glossary.md           One-line definitions of terms, linked to owning articles.
log.md                Append-only history of wiki changes (newest at top).
templates/article.md  Copy this to start a new article.
wiki/principles/      Timeless design rules (KISS, coupling, ...).
wiki/practices/       Things teams do (TDD, code review, ADRs, ...).
wiki/architecture/    Structural patterns (hexagonal, CQRS, ...).
wiki/technology/      Kinds of technology (databases, brokers, LLMs, ...).
wiki/leadership/      Influence, communication, and the non-code skills.
wiki/coding-with-ai/  Working with coding agents, as an engineer and a team.
wiki/antipatterns/    Pitfalls: tempting moves that reliably make things worse.
quizzes/<slug>.md     3+ multiple-choice questions per article (see Quiz rules).
scripts/lint_wiki.py  Enforces the rules below.
scripts/quizzes.py    Parses and lints the quiz banks.
scripts/build_site.py Builds the reader site: wiki → _site/wiki-data.js + web/.
scripts/markdown_html.py  The Markdown subset the articles use → HTML.
web/                  Reader site: index.html, style.css, app.js (DOM shell),
                      core.js (pure logic, tested in tests/web/), sw.js
                      (offline cache; the build fills in its file list and
                      a content-hash version), manifest + icons (installable).
docs/review-guide.md  Shared rules + output format for reviewer agents.
docs/sources/         Research notes and citations behind fast-moving topics.
.claude/agents/       Reviewer agents, one perspective each.
.claude/skills/       /review-wiki — runs the reviewers and merges results.
reviews/              Saved review reports.
tests/                Tests for the linter, site build, and site logic.
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
- Use only the Markdown the site renders: headings, paragraphs, lists
  (one nesting level, two-space indent), `>` quotes, tables, fenced code,
  `**bold**`, `*italic*`, `` `code` ``, and wikilinks. No images or raw HTML.
  (Not linted, but a test fails if Markdown syntax leaks into the built HTML.)

## Glossary rules (enforced by the linter)

- Entries live under `## A`, `## B`, … (`## #` for terms starting with a
  digit or symbol), alphabetical within each letter, case-insensitive.
- Each entry is one line: `- **Term** — Definition. See [[slug]].`
- One or two plain sentences. Link to the owning article when there is
  one; the glossary defines, articles explain.
- No duplicate terms. When an article introduces an important term,
  add it here in the same change.

## Quiz rules (enforced by the linter)

- Every article has `quizzes/<slug>.md`; no quiz without an article.
- At least 3 questions. Each is a `## Question ending in?`, then 3–4
  options as `- [x]` (exactly one) / `- [ ]`, then `**Why:** …` with a
  link to the article. No duplicate options, no stray lines.
- The answer may be at most 1.3× the average wrong option's length, and
  across the whole bank it may be neither the longest nor the shortest
  option in more than 40% of questions. Readers learn to pick by shape.
- No "the wiki" (ask about the reader's situation) and no "listed trap"
  (give the reason) in quizzes.

Also, by you:

- The site shuffles questions and options, and the Quiz tab mixes
  questions from every article. Write options in any order, and make each
  question stand alone: name the pattern and the setup in the question
  itself, never "the same team" or "the table" from another question.
- Test judgment with scenarios, not trivia or recall of the example ("What
  did the team do?" becomes "What should they do?"). Give each quiz at
  least one question whose answer is "not yet" or "it depends", drawn from
  the article's costs or "When it doesn't apply".
- Make wrong options plausible near-misses, ideally the article's own
  traps. Don't let absolutes ("Never;", "always", "Whenever") mark the
  wrong ones or hedges mark the right one; use an absolute in the answer
  where the article is absolute.
- Base every answer and **Why:** line on what the article says, keeping its
  caveats; a wrong option the article only partly refutes is a second
  answer. When you change an article, check its quiz.

## Site copy comes from the wiki (enforced by tests)

The reader site in `web/` is a shell: it renders data, it doesn't restate
content. Interface labels ("Start quiz", "Check yourself") are fine; anything
that describes the wiki — categories, counts, topics, terms, the tagline —
comes from the Markdown at build time.

- The site description (page meta, app manifest, home page) is the first
  paragraph of `index.md`. It must name every category; a test checks this.
- The site title is `index.md`'s H1 without "— Index". Categories are the
  `index.md` sections, in order: the H2 is the label, and the folder of the
  section's entries (list items that start with a link) is the slug. A test
  checks that every `wiki/` folder is exactly one section.
- A test fails if `web/` contains any article title, glossary term,
  category name, or the site title. Paraphrases slip past it, so
  `wiki-gardener` checks for them.

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
  `Command Query Responsibility Segregation (CQRS)`. Exceptions: acronyms
  of lists (CAP, SOLID) keep the acronym; a well-known alias may go in
  parentheses (`Hexagonal Architecture (Ports and Adapters)`). No leading
  "The", no trailing "Pattern".
- **Bullets:** a bold lead-in is a short, complete clause ending in a
  period (`**Bound every queue.** An unbounded…`), or no bold at all.
  Never end a bold lead-in at a colon, comma, or mid-sentence.
  Two allowed exceptions:
  - *Definition lists* may use `**Term** — definition.`
  - A term of art may be bolded once, mid-sentence, where it is defined.
- **Paragraphs:** at most four sentences, including in Examples.
- **Pseudocode:** Python-like, colon-and-indent, no braces —
  `interface Clock:` / `    now()`. Identifiers in camelCase; constants
  and enum values may be UPPER_CASE (`IN_PROGRESS`, `MAX_RETRIES`).
  Comments with `#`.
- **Recovery jobs state their limits.** Any sweeper, reconciler, relay,
  replay, or backfill says (1) its time window or age threshold, (2) how
  it stays idempotent and handles ordering, and (3) who owns it. If it
  races with the normal path, the article says how the race resolves.
- **Re-read the example after changing a rule.** Examples must obey the
  article's own guidelines.
- **Acronyms that never need expanding:** API, HTTP, URL, SQL, JSON, UI, ID.
  Everything else (CI, CRUD, PR, ADR, CDC, …) is expanded once per article.
- **No maintainer notes in reader text.** Never write "this article owns…";
  ownership lives only in the table below.
- **Every fix gets its own cost check.** When adding a mechanism to fix a
  problem (a buffer, a retry, a fallback), say what it costs or where it
  stops working.
- **New owner → trim neighbours.** When an article becomes a concept's
  owner, cut other articles' copies to one sentence and a link.
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
  - *coding agent* — define it at first use in every `coding-with-ai`
    article: an AI tool that reads code, runs commands, and edits files
    in a loop toward a goal.
- **Coding-agent evidence is early and mixed — say so.** That is the
  wiki's position in `coding-with-ai`. Studies are small, short,
  observational, or from one firm, and they disagree. Treat a finding as a
  signal of what to watch, never a forecast; never rest advice on one
  study; and steer readers to measure their own team.
  - Every research claim names who, when, and the caveat (sample, design,
    what wasn't measured), next to the number, and has an entry in
    `docs/sources/`.
  - Use non-causal wording ("after adoption, X rose"; "the authors point
    to…") unless the study was randomized. Keep counter-findings.
  - Bold lead-ins state what to watch, not a proven effect.
  - Re-check claims at each review; prefer principles that survive tool
    churn over tool features.
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
  | Agent instruction files (AGENTS.md, CLAUDE.md) | `agent-instruction-files` |
  | Feedback loops for agents | `feedback-loops-for-agents` |
  | Plan-first agent workflow, task sizing | `spec-first-agent-tasks` |
  | Ownership and review of agent output | `reviewing-ai-generated-code` |
  | Agent permissions, sandboxing, prompt injection | `agent-guardrails` |
  | Dev containers, environment as code | `reproducible-dev-environments` |
  | Hooks, reusable commands, tool connections (MCP) | `shared-agent-configuration` |
  | Unattended agent runs: stop condition, budget, handoff | `feedback-loops-for-agents` (sandboxing them: `agent-guardrails`) |
  | Codebase layout and discoverability for agents | `navigable-codebases` |
  | Team rollout, AI working agreement, measuring AI impact | `adopting-coding-agents` |
  | ACID, constraints, indexes, replicas, sharding | `relational-databases` |
  | Cache patterns, TTLs, invalidation, stampedes | `caching` |
  | Queue vs log, delivery guarantees, DLQs, consumer lag | `message-brokers` |
  | Health checks, connection draining, CDN caching | `load-balancers-and-cdns` |
  | LLM properties, RAG, embeddings, evaluation sets | `large-language-models` |
  | Distributed monolith | `distributed-monolith` |
  | Why not to rewrite from scratch | `big-bang-rewrite` (how to replace instead: `strangler-fig`) |
  | Bus factor, knowledge silos | `hero-culture` |
  | Goodhart's law, metrics as targets | `metric-fixation` |

## Workflows

**Technology articles** describe a *kind* of technology, not a product.
Name products only as examples, and put "how to choose" ahead of "how to
configure." "When it doesn't apply" says what to pick instead.

**Antipattern articles** use the same sections with these meanings:
"The idea" says what it is *and why it's tempting*; "How to apply it" has
two labeled groups, `Spotting it:` and `Climbing out:`; "Example" shows the escape, including
its cost; "When it doesn't apply" says when the antipattern is the right
call. Never blame the people who fell into it.

**Add an article:** copy `templates/article.md` → fill it in → add it to
`index.md` under the right heading → add `[[links]]` from 1–3 related
existing articles back to it → write `quizzes/<slug>.md` → run lint → add a line to `log.md` → commit.

**Ingest a source** (book, talk, blog post): summarize what's new, then
update existing articles or create new ones. Note the source in `log.md`.
Don't paste copyrighted text; paraphrase and credit.

**Answer a question:** read `index.md`, open the relevant articles, answer
with `[[links]]`. If the answer is reusable, offer to file it as an article.

**Health check:** run lint; also look for contradictions between articles,
stale claims, concepts mentioned in several articles that deserve
their own page, quizzes that no longer match their articles, and site copy
that restates content instead of deriving it.

**Content review:** run `/review-wiki [slugs…] [reviewers…]`. It fans out to
five read-only reviewer agents in `.claude/agents/` — `newcomer-reader`,
`technical-accuracy`, `principal-skeptic`, `style-editor`, `wiki-gardener` —
and merges their findings into `reviews/YYYY-MM-DD-<scope>.md`. Shared rules
and output format live in `docs/review-guide.md`; change them there, not in
each agent. Reviewers never edit articles; fixes are applied after the user
picks which to take.
