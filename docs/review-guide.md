# Review guide

Shared rules for every reviewer agent in `.claude/agents/`. Each reviewer
has one lens; stay inside yours so reviews don't overlap.

## Ground rules

- Read `CLAUDE.md` first — it defines the article rules and writing style.
- **Do not edit files.** Report findings; a human or the main session applies them.
- Review only the articles you were given. If none were named, review them all.
- Quote the exact text you're commenting on so the fix is easy to place.
- Prefer a few high-value findings over many trivial ones. If an article is
  good, say so in one line and move on.
- Things the linter already checks (frontmatter, required sections, length,
  broken links) are out of scope.

## Severity

| Level | Meaning |
| --- | --- |
| **must-fix** | Wrong, misleading, or confusing enough that a reader would come away with the wrong idea. |
| **should-fix** | Noticeably weakens the article; worth fixing in the next pass. |
| **consider** | A judgment call or polish; fine to skip. |

## Output format

Return Markdown, grouped by article, most severe first:

```
## <slug>

- **must-fix** · <section> · "<quoted text>"
  Problem: <what's wrong, in one or two sentences>
  Suggestion: <a concrete rewrite or action>

Verdict: <one line overall assessment>
```

End with a **Summary** of at most five bullets: the patterns you saw across
articles, not a repeat of every finding.
