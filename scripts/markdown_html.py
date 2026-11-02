"""Convert the Markdown subset the wiki uses into HTML.

Supported: headings, paragraphs, fenced code, blockquotes, tables, and
nested lists; inline code, bold, italic, and [[wikilinks]]. Anything else
renders as plain text. Pure functions only, standard library only.
"""
from __future__ import annotations

import html
import re
from typing import Callable, Dict, List, Optional

IsKnown = Callable[[str], bool]

CODE_SPAN = re.compile(r"`([^`]+)`")
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:\|([^\]]*))?\]\]")
BOLD = re.compile(r"\*\*(.+?)\*\*")
ITALIC = re.compile(r"(?<![\w*])\*(?=\S)([^*]+?)(?<=\S)\*(?![\w*])")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
LIST_ITEM = re.compile(r"^( *)([-*]|\d+\.)\s+(.*)$")
TABLE_SEPARATOR = re.compile(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?$")
PLACEHOLDER = "\x00{}\x00"
PLACEHOLDER_RE = re.compile("\x00(\\d+)\x00")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def render_inline(text: str, is_known: IsKnown, titles: Optional[Dict[str, str]] = None) -> str:
    """Render one line of inline Markdown. Code spans are protected first."""
    titles = titles or {}
    stash: List[str] = []

    def keep(fragment: str) -> str:
        stash.append(fragment)
        return PLACEHOLDER.format(len(stash) - 1)

    text = CODE_SPAN.sub(lambda m: keep(f"<code>{html.escape(m.group(1), quote=False)}</code>"), text)
    text = html.escape(text, quote=False)

    def link(match: re.Match) -> str:
        slug = match.group(1).strip()
        label = match.group(2)
        inner = _format(label) if label else html.escape(titles.get(slug, slug), quote=False)
        if not is_known(slug):
            return keep(f'<span class="wikilink broken">{inner}</span>')
        return keep(f'<a class="wikilink" href="#/a/{slug}" data-slug="{slug}">{inner}</a>')

    text = WIKILINK.sub(link, text)
    text = _format(text)
    while PLACEHOLDER_RE.search(text):
        text = PLACEHOLDER_RE.sub(lambda m: stash[int(m.group(1))], text)
    return text


def _format(text: str) -> str:
    text = BOLD.sub(r"<strong>\1</strong>", text)
    return ITALIC.sub(r"<em>\1</em>", text)


def _split_row(line: str) -> List[str]:
    line = line.strip().strip("|")
    cells, current, in_code = [], "", False
    i = 0
    while i < len(line):
        char = line[i]
        if char == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            current += "|"
            i += 2
            continue
        if char == "`":
            in_code = not in_code
        if char == "|" and not in_code:
            cells.append(current.strip())
            current = ""
        else:
            current += char
        i += 1
    cells.append(current.strip())
    return cells


def _is_block_start(line: str) -> bool:
    return bool(
        line.startswith("```")
        or HEADING.match(line)
        or LIST_ITEM.match(line)
        or line.startswith(">")
        or line.startswith("|")
    )


def _render_list(lines: List[str], inline) -> str:
    """Render consecutive list lines; deeper-indented items nest."""
    items: List[dict] = []  # each: {"indent", "ordered", "text", "children": [lines]}
    base = len(LIST_ITEM.match(lines[0]).group(1))
    for line in lines:
        match = LIST_ITEM.match(line)
        if match and len(match.group(1)) == base:
            items.append({
                "ordered": match.group(2)[0].isdigit(),
                "text": match.group(3).strip(),
                "children": [],
            })
        elif match:
            items[-1]["children"].append(line)
        elif items[-1]["children"]:
            items[-1]["children"].append(line)
        else:
            items[-1]["text"] += " " + line.strip()

    tag = "ol" if items[0]["ordered"] else "ul"
    out = [f"<{tag}>"]
    for item in items:
        body = inline(item["text"])
        if item["children"]:
            body += "\n" + _render_list(item["children"], inline)
        out.append(f"<li>{body}</li>")
    out.append(f"</{tag}>")
    return "\n".join(out)


def _render_table(lines: List[str], inline) -> str:
    header = _split_row(lines[0])
    rows = [_split_row(line) for line in lines[2:]]
    head = "".join(f"<th>{inline(cell)}</th>" for cell in header)
    body = "\n".join(
        "<tr>" + "".join(f"<td>{inline(cell)}</td>" for cell in row) + "</tr>" for row in rows
    )
    return (
        f'<div class="table-wrap"><table>\n<thead><tr>{head}</tr></thead>\n'
        f"<tbody>\n{body}\n</tbody>\n</table></div>"
    )


def render_markdown(
    text: str, is_known: IsKnown, titles: Optional[Dict[str, str]] = None
) -> str:
    def inline(fragment: str) -> str:
        return render_inline(fragment, is_known, titles)

    lines = text.strip("\n").split("\n")
    blocks: List[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        if line.startswith("```"):
            end = i + 1
            while end < len(lines) and not lines[end].startswith("```"):
                end += 1
            code = html.escape("\n".join(lines[i + 1:end]), quote=False)
            blocks.append(f"<pre><code>{code}</code></pre>")
            i = end + 1
            continue

        heading = HEADING.match(line)
        if heading:
            level, title = len(heading.group(1)), heading.group(2).strip()
            blocks.append(f'<h{level} id="{slugify(title)}">{inline(title)}</h{level}>')
            i += 1
            continue

        if line.startswith(">"):
            quoted = []
            while i < len(lines) and lines[i].startswith(">"):
                quoted.append(lines[i][1:].lstrip())
                i += 1
            inner = render_markdown("\n".join(quoted), is_known, titles)
            blocks.append(f"<blockquote>{inner}</blockquote>")
            continue

        if line.startswith("|") and i + 1 < len(lines) and TABLE_SEPARATOR.match(lines[i + 1].strip()):
            end = i
            while end < len(lines) and lines[end].startswith("|"):
                end += 1
            blocks.append(_render_table(lines[i:end], inline))
            i = end
            continue

        if LIST_ITEM.match(line):
            end = i
            while end < len(lines) and lines[end].strip() and (
                LIST_ITEM.match(lines[end]) or lines[end].startswith(" ")
            ):
                end += 1
            blocks.append(_render_list(lines[i:end], inline))
            i = end
            continue

        paragraph = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not _is_block_start(lines[i]):
            paragraph.append(lines[i].strip())
            i += 1
        blocks.append(f"<p>{inline(' '.join(paragraph))}</p>")
    return "\n".join(blocks)
