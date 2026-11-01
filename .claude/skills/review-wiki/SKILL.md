---
name: review-wiki
description: Run the wiki's reviewer agents in parallel over some or all articles and merge their findings into one prioritized report. Use when asked to review wiki content.
---

# Review the wiki

**Arguments:** optional article slugs (e.g. `kiss cqrs`) and/or reviewer
names (e.g. `newcomer-reader style-editor`). With no slugs, review every
article. With no reviewer names, use all five.

Reviewers live in `.claude/agents/`:

| Agent | Lens |
| --- | --- |
| `newcomer-reader` | Would this land on a first read? |
| `technical-accuracy` | Is it correct and well-sourced? |
| `principal-skeptic` | Are the trade-offs honest and complete? |
| `style-editor` | Is it tight and consistent with house style? |
| `wiki-gardener` | Does the wiki hang together as a whole? |

## Steps

1. Resolve the article list (check each slug exists under `wiki/`).
2. Launch the chosen reviewers **in parallel**, one Agent call each, passing
   the article paths. For more than ~15 articles, split the per-article
   reviewers into batches of about 15 articles each (articles are short, so
   bigger batches keep the agent count down); `wiki-gardener` always gets
   one run over the whole wiki.
   If the agent types above aren't loaded in the session, launch
   general-purpose agents told to read `.claude/agents/<name>.md` and adopt
   that role, with an explicit read-only instruction.
3. When all have returned, merge into a single report:
   - Group by article, then by severity (`must-fix` → `should-fix` → `consider`).
   - Tag each finding with the reviewer that raised it.
   - Merge duplicates raised by several reviewers and note the agreement —
     agreement is a signal of priority.
   - Put `wiki-gardener` findings in their own section at the end.
4. Save the report to `reviews/YYYY-MM-DD-<scope>.md` and show the user the
   `must-fix` items plus a count of the rest.
5. **Don't apply fixes** until the user says which to take. When applying,
   run the linter and tests afterwards and add a line to `log.md`.
