# Principal Engineer Wiki

A reader-friendly knowledge base of the principles, practices, and
architecture patterns a Principal Software Engineer should know.

**Start reading at [index.md](index.md).**

## What makes it an "LLM wiki"

The wiki is plain Markdown that an LLM writes and keeps up to date, guided
by the rules in [CLAUDE.md](CLAUDE.md). You read it, ask questions, and
suggest topics or sources; the LLM adds articles, updates cross-links, and
runs the linter so the wiki stays consistent as it grows.

## Reading it

- On GitHub, or any Markdown viewer.
- In [Obsidian](https://obsidian.md): open this folder as a vault. The
  `[[wikilinks]]` become clickable and the graph view shows how ideas connect.

Every article has the same shape, so you always know where to look:

1. **The idea** — plain-English intuition
2. **Why it matters**
3. **How to apply it**
4. **Example**
5. **Common traps**
6. **When it doesn't apply** — the honest trade-offs
7. **Related** — where to go next

## Checking it

```sh
python3 -m unittest discover -s tests   # test the linter
python3 scripts/lint_wiki.py            # lint the wiki
```

The linter checks frontmatter, required sections, article length, that every
`[[link]]` resolves, and that every article appears in the index.
