import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from markdown_html import render_inline, render_markdown  # noqa: E402


def no_links(slug):
    return False


def known(*slugs):
    return lambda slug: slug in slugs


class RenderInlineTest(unittest.TestCase):
    def test_escapes_html(self):
        self.assertEqual(render_inline("a < b & c", no_links), "a &lt; b &amp; c")

    def test_bold_italic_and_code(self):
        self.assertEqual(
            render_inline("**bold**, *it*, `x = 1`", no_links),
            "<strong>bold</strong>, <em>it</em>, <code>x = 1</code>",
        )

    def test_code_spans_are_not_formatted(self):
        self.assertEqual(
            render_inline("`a * b * c` and `**x**`", no_links),
            "<code>a * b * c</code> and <code>**x**</code>",
        )

    def test_code_spans_escape_html(self):
        self.assertEqual(render_inline("`<T>`", no_links), "<code>&lt;T&gt;</code>")

    def test_wikilink_to_known_article(self):
        self.assertEqual(
            render_inline("see [[yagni]]", known("yagni")),
            'see <a class="wikilink" href="#/a/yagni" data-slug="yagni">yagni</a>',
        )

    def test_aliased_wikilink_uses_alias_text(self):
        html = render_inline("[[design-docs|design doc]]", known("design-docs"))
        self.assertEqual(
            html,
            '<a class="wikilink" href="#/a/design-docs" data-slug="design-docs">design doc</a>',
        )

    def test_wikilink_with_formatting_in_alias(self):
        html = render_inline("[[dry|*DRY*]]", known("dry"))
        self.assertIn(">", html)
        self.assertIn("<em>DRY</em>", html)

    def test_broken_wikilink_renders_as_marked_text(self):
        self.assertEqual(
            render_inline("[[ghost]]", no_links),
            '<span class="wikilink broken">ghost</span>',
        )

    def test_title_lookup_supplies_link_text(self):
        html = render_inline("[[kiss]]", known("kiss"), titles={"kiss": "KISS"})
        self.assertIn(">KISS</a>", html)

    def test_asterisk_between_spaces_is_not_italic(self):
        self.assertEqual(render_inline("3 * 4 * 5", no_links), "3 * 4 * 5")


class RenderMarkdownTest(unittest.TestCase):
    def render(self, text, is_known=no_links):
        return render_markdown(text, is_known)

    def test_paragraphs_join_wrapped_lines(self):
        self.assertEqual(self.render("one\ntwo\n\nthree"), "<p>one two</p>\n<p>three</p>")

    def test_headings_get_ids(self):
        self.assertEqual(
            self.render("## Why it matters"),
            '<h2 id="why-it-matters">Why it matters</h2>',
        )

    def test_h1_is_rendered(self):
        self.assertEqual(self.render("# KISS"), '<h1 id="kiss">KISS</h1>')

    def test_fenced_code_is_escaped_and_untouched(self):
        html = self.render("```\nif a < b: **x**\n    [[kiss]]\n```")
        self.assertEqual(html, "<pre><code>if a &lt; b: **x**\n    [[kiss]]</code></pre>")

    def test_unordered_list(self):
        self.assertEqual(
            self.render("- one\n- **two.** more"),
            "<ul>\n<li>one</li>\n<li><strong>two.</strong> more</li>\n</ul>",
        )

    def test_ordered_list(self):
        self.assertEqual(
            self.render("1. one\n2. two"),
            "<ol>\n<li>one</li>\n<li>two</li>\n</ol>",
        )

    def test_nested_list(self):
        html = self.render("- outer\n  - inner a\n  - inner b\n- next")
        self.assertEqual(
            html,
            "<ul>\n<li>outer\n<ul>\n<li>inner a</li>\n<li>inner b</li>\n</ul></li>\n"
            "<li>next</li>\n</ul>",
        )

    def test_list_item_continuation_line(self):
        self.assertEqual(
            self.render("- one\n  continues\n- two"),
            "<ul>\n<li>one continues</li>\n<li>two</li>\n</ul>",
        )

    def test_blockquote(self):
        self.assertEqual(
            self.render("> **In one sentence:** hi\n> there"),
            "<blockquote><p><strong>In one sentence:</strong> hi there</p></blockquote>",
        )

    def test_table(self):
        html = self.render("| A | B |\n| --- | --- |\n| `x` | y |")
        self.assertEqual(
            html,
            '<div class="table-wrap"><table>\n<thead><tr><th>A</th><th>B</th></tr></thead>\n'
            "<tbody>\n<tr><td><code>x</code></td><td>y</td></tr>\n</tbody>\n</table></div>",
        )

    def test_pipes_inside_code_do_not_split_table_cells(self):
        html = self.render("| A |\n| --- |\n| `a \\| b` |")
        self.assertIn("<td><code>a | b</code></td>", html)

    def test_list_directly_after_paragraph(self):
        self.assertEqual(
            self.render("Then:\n- one"),
            "<p>Then:</p>\n<ul>\n<li>one</li>\n</ul>",
        )

    def test_wikilinks_resolve_in_blocks(self):
        html = self.render("- [[kiss]] — simple", known("kiss"))
        self.assertIn('href="#/a/kiss"', html)


if __name__ == "__main__":
    unittest.main()
