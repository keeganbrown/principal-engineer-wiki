import json
import os
import re
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from build_site import build_site, site_data  # noqa: E402
from lint_wiki import load_wiki, parse_article  # noqa: E402

INDEX = """# Wiki — Index

Intro text.

**New here?** A good first path:
[[kiss]] → [[yagni]].

## Principles

- [[kiss]] — Simple.
- [[yagni]] — Later.
"""


def article(slug, title, body, category="principles"):
    text = (
        f"---\ntitle: {title}\ncategory: {category}\nsummary: About {title}.\n"
        f"tags: [a, b]\n---\n\n# {title}\n\n{body}\n"
    )
    return parse_article(slug, category, text)


def sample_articles():
    return {
        "kiss": article("kiss", "KISS", "> **In one sentence:** hi\n\nSee [[yagni]]. " + "word " * 400),
        "yagni": article("yagni", "YAGNI", "See [[kiss]] and [[kiss|again]] and [[yagni]]."),
    }


class SiteDataTest(unittest.TestCase):
    def setUp(self):
        self.data = site_data(sample_articles(), INDEX)

    def test_article_metadata(self):
        kiss = self.data["articles"]["kiss"]
        self.assertEqual(kiss["title"], "KISS")
        self.assertEqual(kiss["category"], "principles")
        self.assertEqual(kiss["summary"], "About KISS.")
        self.assertEqual(kiss["tags"], ["a", "b"])

    def test_article_html_drops_the_h1_but_keeps_the_callout(self):
        html = self.data["articles"]["kiss"]["html"]
        self.assertNotIn("<h1", html)
        self.assertIn("<blockquote>", html)

    def test_links_exclude_self_and_duplicates(self):
        self.assertEqual(self.data["articles"]["yagni"]["links"], ["kiss"])

    def test_backlinks_list_articles_that_link_here(self):
        self.assertEqual(self.data["articles"]["kiss"]["backlinks"], ["yagni"])
        self.assertEqual(self.data["articles"]["yagni"]["backlinks"], ["kiss"])

    def test_reading_time_is_at_least_one_minute(self):
        self.assertEqual(self.data["articles"]["yagni"]["minutes"], 1)
        self.assertEqual(self.data["articles"]["kiss"]["minutes"], 2)

    def test_edges_are_undirected_and_unique(self):
        self.assertEqual(self.data["edges"], [["kiss", "yagni"]])

    def test_home_html_comes_from_index_without_h1(self):
        self.assertNotIn("<h1", self.data["home"])
        self.assertIn('href="#/a/kiss"', self.data["home"])

    def test_starter_path_comes_from_new_here_paragraph(self):
        self.assertEqual(self.data["path"], ["kiss", "yagni"])

    def test_categories_are_listed_in_reading_order(self):
        slugs = [c["slug"] for c in self.data["categories"]]
        self.assertEqual(slugs, ["principles", "practices", "architecture", "leadership", "coding-with-ai"])

    def test_link_text_uses_article_titles(self):
        self.assertIn(">KISS</a>", self.data["articles"]["yagni"]["html"])


class RealWikiRenderTest(unittest.TestCase):
    """Every real article renders without Markdown syntax leaking through."""

    def test_no_markdown_syntax_leaks_into_html(self):
        repo = os.path.join(os.path.dirname(__file__), "..")
        with open(os.path.join(repo, "index.md"), encoding="utf-8") as f:
            index_text = f.read()
        data = site_data(load_wiki(os.path.join(repo, "wiki")), index_text)
        pages = {slug: a["html"] for slug, a in data["articles"].items()}
        pages["index.md"] = data["home"]
        for name, html in pages.items():
            prose = re.sub(r"<pre>.*?</pre>|<code>.*?</code>", "", html, flags=re.DOTALL)
            for token in ("**", "[[", "]]", "\n#", "\n|", "\n- ", "\n> "):
                self.assertNotIn(token, prose, f"{name}: leaked {token!r}")


class BuildSiteTest(unittest.TestCase):
    def test_writes_data_script_and_copies_static_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            web = os.path.join(tmp, "web")
            out = os.path.join(tmp, "out")
            os.makedirs(web)
            with open(os.path.join(web, "index.html"), "w") as f:
                f.write("<html></html>")
            build_site(sample_articles(), INDEX, web, out)

            self.assertTrue(os.path.exists(os.path.join(out, "index.html")))
            self.assertTrue(os.path.exists(os.path.join(out, ".nojekyll")))
            with open(os.path.join(out, "wiki-data.js")) as f:
                script = f.read()
        prefix = "window.WIKI = "
        self.assertTrue(script.startswith(prefix))
        data = json.loads(script[len(prefix):].rstrip().rstrip(";"))
        self.assertIn("kiss", data["articles"])

    def test_replaces_stale_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            web = os.path.join(tmp, "web")
            out = os.path.join(tmp, "out")
            os.makedirs(web)
            os.makedirs(out)
            stale = os.path.join(out, "old.html")
            with open(stale, "w") as f:
                f.write("old")
            build_site(sample_articles(), INDEX, web, out)
            self.assertFalse(os.path.exists(stale))


if __name__ == "__main__":
    unittest.main()
