#!/usr/bin/env python3
"""Check that every wiki article follows the conventions in CLAUDE.md.

Pure checks live in parse_article / lint_article / lint_wiki; main() is the
thin shell that reads files and prints problems.
"""
from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Set

REQUIRED_FIELDS = ("title", "category", "summary", "tags")

# The shared skeleton keeps articles predictable: a reader always knows
# where to find the "why", the "how", and the caveats.
REQUIRED_SECTIONS = (
    "The idea",
    "Why it matters",
    "How to apply it",
    "Example",
    "Common traps",
    "When it doesn't apply",
    "Related",
)

# Articles are meant to be read in one sitting (~5 minutes).
MAX_WORDS = 1200

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
HEADING = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
CODE_BLOCK = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
BULLET_LEAD_IN = re.compile(r"^\s*(?:[-*]|\d+\.)\s+(\*\*.+?\*\*)(.*)$", re.MULTILINE)
CLAUSE_ENDINGS = (".", "?", "!")
CLOSING_QUOTES = "\"'”’"
DEFINITION_SEPARATOR = " — "
MAINTAINER_NOTES = ("this article owns", "the wiki's rule")
RELATED_OWNS = re.compile(r"\bowns\b", re.IGNORECASE)


def _related_section(body: str) -> str:
    _, _, after = body.partition("\n## Related")
    return after


def _bad_lead_ins(body: str) -> List[str]:
    """Bold bullet lead-ins must be complete clauses, except in definition lists."""
    prose = CODE_BLOCK.sub("", body)
    bad = []
    for lead_in, rest in BULLET_LEAD_IN.findall(prose):
        is_clause = lead_in[2:-2].rstrip().rstrip(CLOSING_QUOTES).endswith(CLAUSE_ENDINGS)
        is_definition = rest.startswith(DEFINITION_SEPARATOR)
        if not (is_clause or is_definition):
            bad.append(lead_in)
    return bad


@dataclass
class Article:
    slug: str
    folder: str
    frontmatter: Dict[str, object]
    body: str
    links: Set[str] = field(default_factory=set)
    sections: List[str] = field(default_factory=list)


def _parse_value(raw: str) -> object:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        return [item.strip() for item in raw[1:-1].split(",") if item.strip()]
    return raw


def _split_frontmatter(text: str):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    frontmatter = {}
    for line in text[4:end].splitlines():
        key, sep, value = line.partition(":")
        if sep:
            frontmatter[key.strip()] = _parse_value(value)
    return frontmatter, text[end + len("\n---\n"):]


def parse_article(slug: str, folder: str, text: str) -> Article:
    frontmatter, body = _split_frontmatter(text)
    return Article(
        slug=slug,
        folder=folder,
        frontmatter=frontmatter,
        body=body,
        links={match.strip() for match in WIKILINK.findall(body)},
        sections=HEADING.findall(body),
    )


def lint_article(article: Article) -> List[str]:
    problems = []
    for name in REQUIRED_FIELDS:
        if not article.frontmatter.get(name):
            problems.append(f"{article.slug}: missing frontmatter field '{name}'")

    category = article.frontmatter.get("category")
    if category and category != article.folder:
        problems.append(
            f"{article.slug}: category '{category}' does not match folder '{article.folder}'"
        )

    for section in REQUIRED_SECTIONS:
        if section not in article.sections:
            problems.append(f"{article.slug}: missing section '## {section}'")

    present_in_order = [s for s in article.sections if s in REQUIRED_SECTIONS]
    expected_order = [s for s in REQUIRED_SECTIONS if s in article.sections]
    if present_in_order != expected_order:
        problems.append(f"{article.slug}: required sections are out of order")

    for lead_in in _bad_lead_ins(article.body):
        problems.append(f"{article.slug}: bold lead-in must end with a period: '{lead_in}'")

    for note in MAINTAINER_NOTES:
        if note in article.body.lower():
            problems.append(f"{article.slug}: maintainer note in reader text ('{note}')")
    if RELATED_OWNS.search(_related_section(article.body)):
        problems.append(f"{article.slug}: maintainer note in Related ('owns')")

    words = len(article.body.split())
    if words > MAX_WORDS:
        problems.append(f"{article.slug}: too long ({words} words, max {MAX_WORDS})")
    return problems


def lint_wiki(articles: Dict[str, Article], index_text: str) -> List[str]:
    problems = []
    for article in articles.values():
        problems.extend(lint_article(article))
        for target in sorted(article.links - set(articles)):
            problems.append(f"{article.slug}: broken link [[{target}]]")
        if not article.links - {article.slug}:
            problems.append(f"{article.slug}: links to no other articles")

    index_links = {match.strip() for match in WIKILINK.findall(index_text)}
    for slug in sorted(set(articles) - index_links):
        problems.append(f"index.md: missing link to [[{slug}]]")
    for target in sorted(index_links - set(articles)):
        problems.append(f"index.md: broken link [[{target}]]")
    return problems


GLOSSARY_LETTER = re.compile(r"^## (.+?)\s*$")
GLOSSARY_ENTRY = re.compile(r"^- \*\*(.+?)\*\* — (.+)$")


@dataclass
class GlossaryEntry:
    term: str
    letter: str
    definition: str
    links: Set[str] = field(default_factory=set)


def _glossary_letter(term: str) -> str:
    first = term[0].upper()
    return first if first.isalpha() else "#"


def _glossary_lines(text: str):
    """Yield (letter heading, line) for each bullet line under a ## heading."""
    letter = None
    for line in text.splitlines():
        heading = GLOSSARY_LETTER.match(line)
        if heading:
            letter = heading.group(1)
        elif letter and line.startswith("- "):
            yield letter, line


def parse_glossary(text: str) -> List[GlossaryEntry]:
    entries = []
    for letter, line in _glossary_lines(text):
        match = GLOSSARY_ENTRY.match(line)
        if match:
            definition = match.group(2).strip()
            entries.append(GlossaryEntry(
                term=match.group(1).strip(),
                letter=letter,
                definition=definition,
                links={m.strip() for m in WIKILINK.findall(definition)},
            ))
    return entries


def lint_glossary(text: str, slugs: Set[str]) -> List[str]:
    """Entries are `- **Term** — definition.`, alphabetical, under the right letter."""
    problems = []
    for _, line in _glossary_lines(text):
        if not GLOSSARY_ENTRY.match(line):
            problems.append(f"glossary.md: malformed entry '{line}'")

    seen: Set[str] = set()
    previous: Dict[str, str] = {}
    for entry in parse_glossary(text):
        key = entry.term.lower()
        if key in seen:
            problems.append(f"glossary.md: duplicate term '{entry.term}'")
        seen.add(key)
        if _glossary_letter(entry.term) != entry.letter:
            problems.append(f"glossary.md: '{entry.term}' is under '## {entry.letter}'")
        if key < previous.get(entry.letter, ""):
            problems.append(f"glossary.md: '{entry.term}' is out of alphabetical order")
        previous[entry.letter] = key
        for target in sorted(entry.links - slugs):
            problems.append(f"glossary.md: '{entry.term}' has broken link [[{target}]]")
    return problems


def load_wiki(wiki_root: str) -> Dict[str, Article]:
    articles: Dict[str, Article] = {}
    for folder in sorted(os.listdir(wiki_root)):
        folder_path = os.path.join(wiki_root, folder)
        if not os.path.isdir(folder_path):
            continue
        for filename in sorted(os.listdir(folder_path)):
            if not filename.endswith(".md"):
                continue
            slug = filename[: -len(".md")]
            if slug in articles:
                raise ValueError(
                    f"duplicate slug '{slug}' in '{folder}' and '{articles[slug].folder}'"
                )
            with open(os.path.join(folder_path, filename), encoding="utf-8") as f:
                articles[slug] = parse_article(slug, folder, f.read())
    return articles


def main() -> int:
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    articles = load_wiki(os.path.join(repo_root, "wiki"))
    with open(os.path.join(repo_root, "index.md"), encoding="utf-8") as f:
        index_text = f.read()

    problems = lint_wiki(articles, index_text)
    glossary_path = os.path.join(repo_root, "glossary.md")
    if os.path.exists(glossary_path):
        with open(glossary_path, encoding="utf-8") as f:
            problems.extend(lint_glossary(f.read(), set(articles)))
    from quizzes import lint_quizzes, load_quizzes  # quizzes imports this module

    titles = {slug: str(article.frontmatter.get("title", "")) for slug, article in articles.items()}
    problems.extend(lint_quizzes(load_quizzes(os.path.join(repo_root, "quizzes")), set(articles), titles))
    for problem in problems:
        print(problem)
    print(f"{len(articles)} articles checked, {len(problems)} problem(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
