#!/usr/bin/env python3
"""Build the static reader site into _site/.

site_data() is pure: wiki articles + index text in, JSON-ready dict out.
build_site() is the thin shell that writes files; main() wires up paths.
The front end in web/ only renders what site_data() produces.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import sys
from typing import Dict, List, Optional

from lint_wiki import WIKILINK, Article, load_wiki, parse_glossary
from markdown_html import render_inline, render_markdown, slugify
from quizzes import load_quizzes, parse_quiz

CATEGORIES = (
    ("principles", "Principles"),
    ("practices", "Practices"),
    ("architecture", "Architecture"),
    ("technology", "Technology"),
    ("leadership", "Leadership"),
    ("coding-with-ai", "Coding with AI"),
    ("antipatterns", "Pitfalls"),
)
WORDS_PER_MINUTE = 230
H1 = re.compile(r"^# .*\n", re.MULTILINE)
STARTER_PATH = re.compile(r"\*\*New here\?\*\*(.*?)(?:\n\n|$)", re.DOTALL)
DATA_FILE = "wiki-data.js"
SERVICE_WORKER = "sw.js"
# Files the browser fetches but the service worker shouldn't cache.
NOT_PRECACHED = {SERVICE_WORKER, ".nojekyll"}


def _ordered_links(text: str, own_slug: str) -> List[str]:
    seen: List[str] = []
    for match in WIKILINK.findall(text):
        slug = match.strip()
        if slug != own_slug and slug not in seen:
            seen.append(slug)
    return seen


def _strip_h1(body: str) -> str:
    return H1.sub("", body, count=1)


def site_data(
    articles: Dict[str, Article], index_text: str, glossary_text: str = "", quizzes: Optional[Dict[str, str]] = None
) -> dict:
    quizzes = quizzes or {}
    titles = {slug: str(a.frontmatter.get("title", slug)) for slug, a in articles.items()}

    def is_known(slug: str) -> bool:
        return slug in articles

    def inline(text: str) -> str:
        return render_inline(text, is_known, titles)

    def quiz(slug: str) -> List[dict]:
        return [
            {
                "question": inline(q.question),
                "options": [inline(o) for o in q.options],
                "answer": q.answers[0],
                "why": inline(q.why),
            }
            for q in parse_quiz(quizzes.get(slug, ""))
            if q.answers
        ]

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
            "quiz": quiz(slug),
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
        "glossary": [
            {
                "term": e.term,
                "id": slugify(e.term),
                "letter": e.letter,
                "html": inline(e.definition),
            }
            for e in parse_glossary(glossary_text)
        ],
    }


def build_site(
    articles: Dict[str, Article],
    index_text: str,
    web_dir: str,
    out_dir: str,
    glossary_text: str = "",
    quizzes: Optional[Dict[str, str]] = None,
) -> None:
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    shutil.copytree(web_dir, out_dir)
    data = json.dumps(site_data(articles, index_text, glossary_text, quizzes), ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(out_dir, DATA_FILE), "w", encoding="utf-8") as f:
        f.write(f"window.WIKI = {data};\n")
    # GitHub Pages: serve files as-is, no Jekyll processing.
    open(os.path.join(out_dir, ".nojekyll"), "w").close()
    write_service_worker(out_dir)


def _site_files(out_dir: str) -> List[str]:
    files = []
    for folder, _, names in os.walk(out_dir):
        for name in names:
            rel = os.path.relpath(os.path.join(folder, name), out_dir).replace(os.sep, "/")
            if rel not in NOT_PRECACHED:
                files.append(rel)
    return sorted(files)


def write_service_worker(out_dir: str) -> None:
    """Fill in sw.js with every site file and a version that changes with them.

    The version is a hash of the cached bytes, so a deploy that changes any
    file installs a fresh cache, and a deploy that changes nothing doesn't.
    """
    path = os.path.join(out_dir, SERVICE_WORKER)
    if not os.path.exists(path):
        return
    files = _site_files(out_dir)
    digest = hashlib.sha256()
    for rel in files:
        digest.update(rel.encode())
        with open(os.path.join(out_dir, rel), "rb") as f:
            digest.update(f.read())
    with open(path, encoding="utf-8") as f:
        template = f.read()
    # "./" is how the start page is requested; cache it alongside index.html.
    precache = (["./"] if "index.html" in files else []) + files
    script = template.replace("__CACHE_VERSION__", json.dumps(digest.hexdigest()[:12]))
    script = script.replace("__PRECACHE_FILES__", json.dumps(precache))
    with open(path, "w", encoding="utf-8") as f:
        f.write(script)


def main() -> int:
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    articles = load_wiki(os.path.join(repo_root, "wiki"))
    with open(os.path.join(repo_root, "index.md"), encoding="utf-8") as f:
        index_text = f.read()
    glossary_path = os.path.join(repo_root, "glossary.md")
    glossary_text = ""
    if os.path.exists(glossary_path):
        with open(glossary_path, encoding="utf-8") as f:
            glossary_text = f.read()
    out_dir = os.path.join(repo_root, "_site")
    quizzes = load_quizzes(os.path.join(repo_root, "quizzes"))
    build_site(articles, index_text, os.path.join(repo_root, "web"), out_dir, glossary_text, quizzes)
    print(f"Built {len(articles)} articles into {os.path.relpath(out_dir, repo_root)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
