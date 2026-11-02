import os
import sys
import tempfile
import textwrap
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lint_wiki import (  # noqa: E402
    REQUIRED_SECTIONS,
    lint_article,
    lint_glossary,
    parse_glossary,
    lint_wiki,
    load_wiki,
    parse_article,
)


def make_article(
    title="KISS",
    category="principles",
    summary="Keep it simple.",
    tags="[simplicity]",
    body_links="[[yagni]]",
    sections=REQUIRED_SECTIONS,
    extra_words=0,
):
    frontmatter = textwrap.dedent(
        f"""\
        ---
        title: {title}
        category: {category}
        summary: {summary}
        tags: {tags}
        ---
        """
    )
    body = f"# {title}\n\n"
    for section in sections:
        body += f"## {section}\n\nSome text. {body_links}\n\n"
    body += "word " * extra_words
    return frontmatter + "\n" + body


class ParseArticleTest(unittest.TestCase):
    def test_reads_frontmatter_fields(self):
        article = parse_article("kiss", "principles", make_article())
        self.assertEqual(article.frontmatter["title"], "KISS")
        self.assertEqual(article.frontmatter["tags"], ["simplicity"])

    def test_collects_wikilinks_including_aliased_ones(self):
        text = make_article(body_links="See [[yagni]] and [[dry|Don't Repeat Yourself]].")
        article = parse_article("kiss", "principles", text)
        self.assertEqual(article.links, {"yagni", "dry"})

    def test_collects_section_headings(self):
        article = parse_article("kiss", "principles", make_article())
        self.assertEqual(article.sections, list(REQUIRED_SECTIONS))

    def test_missing_frontmatter_yields_empty_dict(self):
        article = parse_article("kiss", "principles", "# Just a heading\n")
        self.assertEqual(article.frontmatter, {})


class LintArticleTest(unittest.TestCase):
    def test_well_formed_article_has_no_problems(self):
        article = parse_article("kiss", "principles", make_article())
        self.assertEqual(lint_article(article), [])

    def test_reports_missing_frontmatter_field(self):
        text = make_article().replace("summary: Keep it simple.\n", "")
        problems = lint_article(parse_article("kiss", "principles", text))
        self.assertIn("kiss: missing frontmatter field 'summary'", problems)

    def test_reports_category_that_does_not_match_folder(self):
        text = make_article(category="practices")
        problems = lint_article(parse_article("kiss", "principles", text))
        self.assertIn(
            "kiss: category 'practices' does not match folder 'principles'", problems
        )

    def test_reports_missing_required_section(self):
        text = make_article(sections=[s for s in REQUIRED_SECTIONS if s != "Example"])
        problems = lint_article(parse_article("kiss", "principles", text))
        self.assertIn("kiss: missing section '## Example'", problems)

    def test_reports_sections_out_of_order(self):
        swapped = list(REQUIRED_SECTIONS)
        swapped[0], swapped[1] = swapped[1], swapped[0]
        problems = lint_article(parse_article("kiss", "principles", make_article(sections=swapped)))
        self.assertIn("kiss: required sections are out of order", problems)

    def test_accepts_bold_lead_ins_that_are_complete_clauses(self):
        text = make_article(body_links=(
            "[[yagni]]\n\n"
            "- **Bound every queue.** Unbounded ones crash.\n"
            "- **Which framework?** A two-way door.\n"
            "1. **Red** — write a failing test.\n"
            "- Plain bullet with **a defined term** inside.\n"
            '- **"Just add a queue."** It only delays failure.\n'
            '- **Ask: "What would undoing this cost?"** Then decide.\n'
        ))
        self.assertEqual(lint_article(parse_article("kiss", "principles", text)), [])

    def test_reports_bold_lead_in_ending_mid_sentence(self):
        text = make_article(body_links="[[yagni]]\n\n- **Keep tests fast** so people run them.\n")
        problems = lint_article(parse_article("kiss", "principles", text))
        self.assertIn(
            "kiss: bold lead-in must end with a period: '**Keep tests fast**'", problems
        )

    def test_reports_bold_lead_in_ending_with_colon(self):
        text = make_article(body_links="[[yagni]]\n\n2. **Integration (2 tests):** the repo saves.\n")
        problems = lint_article(parse_article("kiss", "principles", text))
        self.assertIn(
            "kiss: bold lead-in must end with a period: '**Integration (2 tests):**'",
            problems,
        )

    def test_ignores_bold_lead_ins_inside_code_blocks(self):
        text = make_article(body_links="[[yagni]]\n\n```\n- **not markdown** here\n```\n")
        self.assertEqual(lint_article(parse_article("kiss", "principles", text)), [])

    def test_reports_maintainer_notes_in_reader_text(self):
        text = make_article(body_links="[[yagni]] This article owns the rule of three.")
        problems = lint_article(parse_article("kiss", "principles", text))
        self.assertIn("kiss: maintainer note in reader text ('this article owns')", problems)

    def test_reports_ownership_notes_in_related_lines(self):
        text = make_article(body_links="[[yagni]]").replace(
            "## Related\n\nSome text. [[yagni]]",
            "## Related\n\n- [[yagni]] — owns the rule for when to abstract.",
        )
        problems = lint_article(parse_article("kiss", "principles", text))
        self.assertIn("kiss: maintainer note in Related ('owns')", problems)

    def test_allows_owns_outside_related(self):
        text = make_article(body_links="[[yagni]] Each service owns its own data.")
        text = text.replace("## Related\n\nSome text. [[yagni]] Each service owns its own data.",
                            "## Related\n\n- [[yagni]] — scope.")
        self.assertEqual(lint_article(parse_article("kiss", "principles", text)), [])

    def test_reports_wikis_rule_phrasing(self):
        text = make_article(body_links="[[yagni]] The wiki's rule is three.")
        problems = lint_article(parse_article("kiss", "principles", text))
        self.assertIn("kiss: maintainer note in reader text ('the wiki's rule')", problems)

    def test_reports_article_that_is_too_long(self):
        text = make_article(extra_words=2000)
        problems = lint_article(parse_article("kiss", "principles", text))
        self.assertTrue(any("too long" in p for p in problems), problems)


class LintWikiTest(unittest.TestCase):
    def test_reports_link_to_missing_article(self):
        kiss = parse_article("kiss", "principles", make_article(body_links="[[nope]]"))
        problems = lint_wiki({"kiss": kiss}, index_text="[[kiss]]")
        self.assertIn("kiss: broken link [[nope]]", problems)

    def test_reports_article_missing_from_index(self):
        kiss = parse_article("kiss", "principles", make_article(body_links="[[yagni]]"))
        yagni = parse_article(
            "yagni", "principles", make_article(title="YAGNI", body_links="[[kiss]]")
        )
        problems = lint_wiki({"kiss": kiss, "yagni": yagni}, index_text="[[kiss]]")
        self.assertIn("index.md: missing link to [[yagni]]", problems)

    def test_reports_broken_link_in_index(self):
        kiss = parse_article("kiss", "principles", make_article(body_links="[[kiss]]"))
        problems = lint_wiki({"kiss": kiss}, index_text="[[kiss]] [[ghost]]")
        self.assertIn("index.md: broken link [[ghost]]", problems)

    def test_reports_article_with_no_links_to_other_articles(self):
        kiss = parse_article("kiss", "principles", make_article(body_links=""))
        problems = lint_wiki({"kiss": kiss}, index_text="[[kiss]]")
        self.assertIn("kiss: links to no other articles", problems)


GLOSSARY = """# Glossary

Intro.

## A

- **ACID** — Atomicity, consistency, isolation, durability. See [[kiss]].
- **At-least-once delivery** — Every message arrives, maybe more than once.

## B

- **Backpressure** — Pushing back on fast producers.
"""


class GlossaryTest(unittest.TestCase):
    def test_parses_entries_with_letter_and_links(self):
        entries = parse_glossary(GLOSSARY)
        self.assertEqual([e.term for e in entries], ["ACID", "At-least-once delivery", "Backpressure"])
        self.assertEqual(entries[0].letter, "A")
        self.assertEqual(entries[0].links, {"kiss"})
        self.assertEqual(entries[2].definition, "Pushing back on fast producers.")

    def test_well_formed_glossary_has_no_problems(self):
        self.assertEqual(lint_glossary(GLOSSARY, {"kiss"}), [])

    def test_reports_broken_link(self):
        problems = lint_glossary(GLOSSARY, set())
        self.assertIn("glossary.md: 'ACID' has broken link [[kiss]]", problems)

    def test_reports_entries_out_of_order(self):
        text = GLOSSARY.replace("- **ACID**", "- **Azure**").replace("- **At-least", "- **At-least")
        problems = lint_glossary(text, {"kiss"})
        self.assertIn("glossary.md: 'At-least-once delivery' is out of alphabetical order", problems)

    def test_reports_entry_under_wrong_letter(self):
        text = GLOSSARY.replace("- **Backpressure**", "- **Circuit breaker**")
        problems = lint_glossary(text, {"kiss"})
        self.assertIn("glossary.md: 'Circuit breaker' is under '## B'", problems)

    def test_reports_duplicate_terms(self):
        text = GLOSSARY + "- **backpressure** — Again.\n"
        problems = lint_glossary(text, {"kiss"})
        self.assertIn("glossary.md: duplicate term 'backpressure'", problems)

    def test_reports_malformed_entry_line(self):
        text = GLOSSARY + "- **Bulkhead**: isolating failures.\n"
        problems = lint_glossary(text, {"kiss"})
        self.assertIn("glossary.md: malformed entry '- **Bulkhead**: isolating failures.'", problems)

    def test_digits_and_symbols_sort_under_hash(self):
        text = GLOSSARY.replace("## A\n", "## #\n\n- **2PC** — Two-phase commit.\n\n## A\n")
        self.assertEqual(lint_glossary(text, {"kiss"}), [])


class LoadWikiTest(unittest.TestCase):
    def test_loads_articles_by_slug_with_folder_as_category(self):
        with tempfile.TemporaryDirectory() as root:
            folder = os.path.join(root, "principles")
            os.makedirs(folder)
            with open(os.path.join(folder, "kiss.md"), "w") as f:
                f.write(make_article())
            articles = load_wiki(root)
        self.assertEqual(list(articles), ["kiss"])
        self.assertEqual(articles["kiss"].folder, "principles")

    def test_rejects_duplicate_slugs_across_folders(self):
        with tempfile.TemporaryDirectory() as root:
            for folder in ("principles", "practices"):
                os.makedirs(os.path.join(root, folder))
                with open(os.path.join(root, folder, "kiss.md"), "w") as f:
                    f.write(make_article())
            with self.assertRaises(ValueError):
                load_wiki(root)


if __name__ == "__main__":
    unittest.main()
