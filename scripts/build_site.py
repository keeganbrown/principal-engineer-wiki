#!/usr/bin/env python3
"""Build the static reader site into _site/.

site_data() is pure: wiki articles + index text in, JSON-ready dict out.
build_site() is the thin shell that writes files; main() wires up paths.
The front end in web/ only renders what site_data() produces.
"""
from __future__ import annotations

import json
import math
import os
import re
import shutil
import sys
from typing import Dict, List

from lint_wiki import WIKILINK, Article, load_wiki
from markdown_html import render_markdown

CATEGORIES = (
    ("principles", "Principles"),
    ("practices", "Practices"),
    ("architecture", "Architecture"),
    ("leadership", "Leadership"),
)
WORDS_PER_MINUTE = 230
H1 = re.compile(r"^# .*\n", re.MULTILINE)
STARTER_PATH = re.compile(r"\*\*New here\?\*\*(.*?)(?:\n\n|$)", re.DOTALL)
DATA_FILE = "wiki-data.js"


def _ordered_links(text: str, own_slug: str) -> List[str]:
    seen: List[str] = []
    for match in WIKILINK.findall(text):
        slug = match.strip()
        if slug != own_slug and slug not in seen:
            seen.append(slug)
    return seen


def _strip_h1(body: str) -> str:
    return H1.sub("", body, count=1)


def site_data(articles: Dict[str, Article], index_text: str) -> dict:
    titles = {slug: str(a.frontmatter.get("title", slug)) for slug, a in articles.items()}

    def is_known(slug: str) -> bool:
        return slug in articles

    out: Dict[str, dict] = {}
    for slug, a in articles.items():
        out[slug] = {
            "slug": slug,
            "title": titles[slug],
            "category": a.folder,
            "summary": a.frontmatter.get("summary", ""),
            "tags": a.frontmatter.get("tags", []),
            "html": render_markdown(_strip_h1(a.body), is_known, titles),
            "links": [s for s in _ordered_links(a.body, slug) if s in articles],
            "minutes": max(1, math.ceil(len(a.body.split()) / WORDS_PER_MINUTE)),
            "backlinks": [],
        }
    for slug in sorted(out):
        for target in out[slug]["links"]:
            out[target]["backlinks"].append(slug)

    edges = sorted({tuple(sorted((s, t))) for s in out for t in out[s]["links"]})

    starter = STARTER_PATH.search(index_text)
    path = _ordered_links(starter.group(1), "") if starter else []

    return {
        "articles": out,
        "edges": [list(edge) for edge in edges],
        "home": render_markdown(_strip_h1(index_text), is_known, titles),
        "path": [s for s in path if s in articles],
        "categories": [{"slug": s, "label": label} for s, label in CATEGORIES],
    }


def build_site(articles: Dict[str, Article], index_text: str, web_dir: str, out_dir: str) -> None:
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    shutil.copytree(web_dir, out_dir)
    data = json.dumps(site_data(articles, index_text), ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(out_dir, DATA_FILE), "w", encoding="utf-8") as f:
        f.write(f"window.WIKI = {data};\n")
    # GitHub Pages: serve files as-is, no Jekyll processing.
    open(os.path.join(out_dir, ".nojekyll"), "w").close()


def main() -> int:
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    articles = load_wiki(os.path.join(repo_root, "wiki"))
    with open(os.path.join(repo_root, "index.md"), encoding="utf-8") as f:
        index_text = f.read()
    out_dir = os.path.join(repo_root, "_site")
    build_site(articles, index_text, os.path.join(repo_root, "web"), out_dir)
    print(f"Built {len(articles)} articles into {os.path.relpath(out_dir, repo_root)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
