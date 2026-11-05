import json
import os
import re
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from build_site import build_site, short_title, site_data  # noqa: E402
from lint_wiki import load_wiki, parse_article, parse_glossary  # noqa: E402
from quizzes import load_quizzes  # noqa: E402

INDEX = """# Wiki — Index

A field guide to **principles** and [[kiss|simple]] things.

Second paragraph.

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

    def test_categories_are_the_index_sections_in_reading_order(self):
        articles = {
            "kiss": article("kiss", "KISS", "x"),
            "cqrs": article("cqrs", "CQRS", "x", category="architecture"),
            "ddd": article("ddd", "DDD", "x", category="architecture"),
        }
        index = "# W — Index\n\nIntro.\n\n## Architecture patterns\n\n- [[nope]]\n- See also [[kiss]]\n- [[cqrs]]\n- [[ddd]]\n\n## Principles\n\n- [[kiss]]\n\n## Empty\n\nNo links.\n"
        self.assertEqual(site_data(articles, index)["categories"], [
            {"slug": "architecture", "label": "Architecture patterns"},
            {"slug": "principles", "label": "Principles"},
        ])

    def test_link_text_uses_article_titles(self):
        self.assertIn(">KISS</a>", self.data["articles"]["yagni"]["html"])


class SiteCopyTest(unittest.TestCase):
    """Text about the wiki comes from the wiki, not from the front end."""

    def test_description_is_the_first_paragraph_of_the_index_as_plain_text(self):
        data = site_data(sample_articles(), INDEX)
        self.assertEqual(data["description"], "A field guide to principles and simple things.")

    def test_title_is_the_index_heading_without_its_index_suffix(self):
        self.assertEqual(site_data(sample_articles(), INDEX)["title"], "Wiki")


class ShortTitleTest(unittest.TestCase):
    def test_short_titles_are_kept_whole(self):
        self.assertEqual(short_title("Wiki"), "Wiki")

    def test_long_titles_abbreviate_all_but_the_last_word(self):
        self.assertEqual(short_title("Principal Engineer Wiki"), "PE Wiki")


class GlossaryDataTest(unittest.TestCase):
    GLOSSARY = "# Glossary\n\n## K\n\n- **KISS** — Keep it simple. See [[kiss]].\n"

    def test_glossary_entries_are_rendered_with_ids(self):
        data = site_data(sample_articles(), INDEX, self.GLOSSARY)
        self.assertEqual(len(data["glossary"]), 1)
        entry = data["glossary"][0]
        self.assertEqual(entry["term"], "KISS")
        self.assertEqual(entry["id"], "kiss")
        self.assertEqual(entry["letter"], "K")
        self.assertIn('href="#/a/kiss"', entry["html"])

    def test_glossary_is_optional(self):
        self.assertEqual(site_data(sample_articles(), INDEX)["glossary"], [])


class QuizDataTest(unittest.TestCase):
    QUIZ = (
        "# Quiz: KISS\n\n## Which design does `KISS` prefer?\n\n"
        "- [ ] The *clever* one.\n- [x] The simplest one.\n- [ ] The layered one.\n\n"
        "**Why:** See [[yagni]].\n"
    )

    def test_each_article_carries_its_rendered_questions(self):
        data = site_data(sample_articles(), INDEX, quizzes={"kiss": self.QUIZ})
        (q,) = data["articles"]["kiss"]["quiz"]
        self.assertEqual(q["question"], "Which design does <code>KISS</code> prefer?")
        self.assertEqual(q["options"], ["The <em>clever</em> one.", "The simplest one.", "The layered one."])
        self.assertEqual(q["answer"], 1)
        self.assertIn('href="#/a/yagni"', q["why"])

    def test_articles_without_a_quiz_get_an_empty_list(self):
        data = site_data(sample_articles(), INDEX, quizzes={"kiss": self.QUIZ})
        self.assertEqual(data["articles"]["yagni"]["quiz"], [])
        self.assertEqual(site_data(sample_articles(), INDEX)["articles"]["kiss"]["quiz"], [])


class RealWikiRenderTest(unittest.TestCase):
    """Every real article renders without Markdown syntax leaking through."""

    def test_no_markdown_syntax_leaks_into_html(self):
        repo = os.path.join(os.path.dirname(__file__), "..")
        with open(os.path.join(repo, "index.md"), encoding="utf-8") as f:
            index_text = f.read()
        with open(os.path.join(repo, "glossary.md"), encoding="utf-8") as f:
            glossary_text = f.read()
        quizzes = load_quizzes(os.path.join(repo, "quizzes"))
        data = site_data(load_wiki(os.path.join(repo, "wiki")), index_text, glossary_text, quizzes)
        pages = {slug: a["html"] for slug, a in data["articles"].items()}
        for slug, a in data["articles"].items():
            self.assertGreaterEqual(len(a["quiz"]), 3, f"{slug}: quiz missing from site data")
            for i, q in enumerate(a["quiz"]):
                pages[f"quiz {slug} #{i}"] = "\n".join([q["question"], q["why"], *q["options"]])
        pages["index.md"] = data["home"]
        for entry in data["glossary"]:
            pages[f"glossary: {entry['term']}"] = entry["html"]
        self.assertGreater(len(data["glossary"]), 50)
        for name, html in pages.items():
            prose = re.sub(r"<pre>.*?</pre>|<code>.*?</code>", "", html, flags=re.DOTALL)
            for token in ("**", "[[", "]]", "\n#", "\n|", "\n- ", "\n> "):
                self.assertNotIn(token, prose, f"{name}: leaked {token!r}")


class RealSiteConsistencyTest(unittest.TestCase):
    """Guards against the front end drifting from the wiki's content."""

    REPO = os.path.join(os.path.dirname(__file__), "..")

    def read(self, *parts):
        with open(os.path.join(self.REPO, *parts), encoding="utf-8") as f:
            return f.read()

    def real_data(self):
        return site_data(load_wiki(os.path.join(self.REPO, "wiki")), self.read("index.md"))

    def test_every_wiki_folder_is_an_index_section_and_vice_versa(self):
        folders = {d for d in os.listdir(os.path.join(self.REPO, "wiki")) if os.path.isdir(os.path.join(self.REPO, "wiki", d))}
        slugs = [c["slug"] for c in self.real_data()["categories"]]
        self.assertEqual(len(slugs), len(set(slugs)), "two index sections map to the same folder")
        self.assertEqual(set(slugs), folders)

    def test_index_description_names_every_category(self):
        data = self.real_data()
        description = data["description"].lower()
        for c in data["categories"]:
            first_word = c["label"].split()[0].lower()
            self.assertIn(first_word, description, f"index.md's first paragraph doesn't mention '{c['label']}'")

    def test_front_end_does_not_hard_code_wiki_content(self):
        articles = load_wiki(os.path.join(self.REPO, "wiki"))
        data = self.real_data()
        names = [c["label"] for c in data["categories"]] + [data["title"]]
        names += [str(a.frontmatter["title"]) for a in articles.values()]
        names += [e.term for e in parse_glossary(self.read("glossary.md"))]
        shell = {f: self.read("web", f) for f in ("app.js", "index.html", "manifest.webmanifest", "sw.js")}
        for name in names:
            pattern = re.compile(rf"(?<![\w-]){re.escape(name)}(?![\w-])")
            for filename, text in shell.items():
                self.assertIsNone(pattern.search(text), f"web/{filename} hard-codes '{name}'; derive it from the wiki")


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

    def build(self, tmp, articles=None, sw="const VERSION = __CACHE_VERSION__;\nconst FILES = __PRECACHE_FILES__;\n"):
        web = os.path.join(tmp, "web")
        out = os.path.join(tmp, "out")
        os.makedirs(os.path.join(web, "icons"), exist_ok=True)
        for name, text in {"index.html": "<html></html>", "app.js": "", "icons/icon.png": "png", "sw.js": sw}.items():
            with open(os.path.join(web, name), "w") as f:
                f.write(text)
        build_site(articles or sample_articles(), INDEX, web, out)
        with open(os.path.join(out, "sw.js")) as f:
            return f.read()

    def test_service_worker_precaches_every_site_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            sw = self.build(tmp)
        files = json.loads(re.search(r"FILES = (.*);", sw).group(1))
        self.assertEqual(sorted(files), ["./", "app.js", "icons/icon.png", "index.html", "wiki-data.js"])

    def test_service_worker_version_changes_with_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = self.build(tmp)
        with tempfile.TemporaryDirectory() as tmp:
            same = self.build(tmp)
        changed = sample_articles()
        changed["yagni"] = article("yagni", "YAGNI", "Edited. See [[kiss]].")
        with tempfile.TemporaryDirectory() as tmp:
            edited = self.build(tmp, changed)
        version = lambda sw: json.loads(re.search(r"VERSION = (.*);", sw).group(1))  # noqa: E731
        self.assertEqual(version(first), version(same))
        self.assertNotEqual(version(first), version(edited))
        self.assertRegex(version(first), r"^[0-9a-f]{12}$")

    def test_site_description_is_filled_into_page_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            web = os.path.join(tmp, "web")
            out = os.path.join(tmp, "out")
            os.makedirs(web)
            with open(os.path.join(web, "index.html"), "w") as f:
                f.write('<title>__SITE_TITLE__</title><meta name="description" content="__SITE_DESCRIPTION__">')
            with open(os.path.join(web, "manifest.webmanifest"), "w") as f:
                f.write('{"name": __SITE_TITLE_JSON__, "short_name": __SITE_SHORT_TITLE_JSON__, '
                        '"description": __SITE_DESCRIPTION_JSON__}')
            build_site(sample_articles(), INDEX.replace("principles", 'the "best" & <worst>'), web, out)
            with open(os.path.join(out, "index.html")) as f:
                page = f.read()
            with open(os.path.join(out, "manifest.webmanifest")) as f:
                manifest = json.load(f)
        expected = 'A field guide to the "best" & <worst> and simple things.'
        self.assertIn('content="A field guide to the &quot;best&quot; &amp; &lt;worst&gt; and simple things."', page)
        self.assertEqual(manifest["description"], expected)
        self.assertIn("<title>Wiki</title>", page)
        self.assertEqual(manifest["name"], "Wiki")
        self.assertEqual(manifest["short_name"], "Wiki")

    def test_build_without_service_worker_template_still_works(self):
        with tempfile.TemporaryDirectory() as tmp:
            web = os.path.join(tmp, "web")
            os.makedirs(web)
            build_site(sample_articles(), INDEX, web, os.path.join(tmp, "out"))
            self.assertFalse(os.path.exists(os.path.join(tmp, "out", "sw.js")))

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
