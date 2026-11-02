import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from quizzes import load_quizzes, lint_quizzes, parse_quiz  # noqa: E402

QUESTION = """## Which design does KISS prefer?

- [ ] The most flexible one available.
- [x] The simplest one that works.
- [ ] The one with the most layers.

**Why:** Flexibility you don't need is cost you pay now. See [[yagni]].
"""


def quiz(*questions):
    return "# Quiz: KISS\n\n" + "\n".join(questions)


def question(heading="Which design does KISS prefer?", options=None, why="**Why:** Because. See [[yagni]]."):
    options = options if options is not None else ["- [x] Simple.", "- [ ] Clever.", "- [ ] Layered."]
    return f"## {heading}\n\n" + "\n".join(options) + f"\n\n{why}\n"


VALID = quiz(QUESTION, question("What does YAGNI warn against?"), question("When is extra flexibility worth it?"))


class ParseQuizTest(unittest.TestCase):
    def test_reads_question_options_answer_and_why(self):
        q = parse_quiz(quiz(QUESTION))[0]
        self.assertEqual(q.question, "Which design does KISS prefer?")
        self.assertEqual(q.options, [
            "The most flexible one available.",
            "The simplest one that works.",
            "The one with the most layers.",
        ])
        self.assertEqual(q.answers, [1])
        self.assertEqual(q.why, "Flexibility you don't need is cost you pay now. See [[yagni]].")
        self.assertEqual(q.links, {"yagni"})

    def test_reads_every_question_in_order(self):
        headings = [q.question for q in parse_quiz(VALID)]
        self.assertEqual(headings, [
            "Which design does KISS prefer?",
            "What does YAGNI warn against?",
            "When is extra flexibility worth it?",
        ])


class LintQuizzesTest(unittest.TestCase):
    SLUGS = {"kiss", "yagni"}

    def lint(self, quizzes, slugs=None):
        return lint_quizzes(quizzes, slugs or self.SLUGS)

    def test_well_formed_quizzes_have_no_problems(self):
        self.assertEqual(self.lint({"kiss": VALID, "yagni": VALID}), [])

    def test_reports_article_without_a_quiz(self):
        self.assertIn("quizzes: missing quiz for [[yagni]]", self.lint({"kiss": VALID}))

    def test_reports_quiz_for_unknown_article(self):
        problems = self.lint({"kiss": VALID, "yagni": VALID, "nope": VALID})
        self.assertIn("quizzes/nope.md: no article with this slug", problems)

    def test_reports_too_few_questions(self):
        problems = self.lint({"kiss": quiz(QUESTION), "yagni": VALID})
        self.assertIn("quizzes/kiss.md: 1 question(s), need at least 3", problems)

    def test_reports_question_without_exactly_one_answer(self):
        none_right = question(options=["- [ ] A.", "- [ ] B.", "- [ ] C."])
        two_right = question(options=["- [x] A.", "- [x] B.", "- [ ] C."])
        problems = self.lint({"kiss": quiz(none_right, two_right, QUESTION), "yagni": VALID})
        self.assertEqual(
            [p for p in problems if "correct" in p],
            ["quizzes/kiss.md: 'Which design does KISS prefer?' needs exactly one correct option, has 0"] +
            ["quizzes/kiss.md: 'Which design does KISS prefer?' needs exactly one correct option, has 2"],
        )

    def test_reports_wrong_number_of_options(self):
        two = question(options=["- [x] A.", "- [ ] B."])
        five = question(options=["- [x] A.", "- [ ] B.", "- [ ] C.", "- [ ] D.", "- [ ] E."])
        problems = self.lint({"kiss": quiz(two, five, QUESTION), "yagni": VALID})
        self.assertIn("quizzes/kiss.md: 'Which design does KISS prefer?' has 2 options, need 3 or 4", problems)
        self.assertIn("quizzes/kiss.md: 'Which design does KISS prefer?' has 5 options, need 3 or 4", problems)

    def test_reports_duplicate_options(self):
        dup = question(options=["- [x] A.", "- [ ] B.", "- [ ] b."])
        problems = self.lint({"kiss": quiz(dup, QUESTION, QUESTION), "yagni": VALID})
        self.assertIn("quizzes/kiss.md: 'Which design does KISS prefer?' repeats an option", problems)

    def test_reports_missing_why(self):
        problems = self.lint({"kiss": quiz(question(why=""), QUESTION, QUESTION), "yagni": VALID})
        self.assertIn("quizzes/kiss.md: 'Which design does KISS prefer?' has no **Why:** line", problems)

    def test_reports_question_that_is_not_a_question(self):
        problems = self.lint({"kiss": quiz(question("Pick one."), QUESTION, QUESTION), "yagni": VALID})
        self.assertIn("quizzes/kiss.md: 'Pick one.' must end with '?'", problems)

    def test_reports_broken_link_in_why(self):
        bad = question(why="**Why:** See [[nowhere]].")
        problems = self.lint({"kiss": quiz(bad, QUESTION, QUESTION), "yagni": VALID})
        self.assertIn("quizzes/kiss.md: broken link [[nowhere]]", problems)

    def test_reports_stray_lines(self):
        stray = question() + "\nSome loose paragraph.\n"
        problems = self.lint({"kiss": quiz(stray, QUESTION, QUESTION), "yagni": VALID})
        self.assertIn("quizzes/kiss.md: unexpected line 'Some loose paragraph.'", problems)


    def test_reports_answer_much_longer_than_the_wrong_options(self):
        long_answer = question(options=["- [x] The one that is far longer than every other option here.", "- [ ] Short.", "- [ ] Brief."])
        problems = self.lint({"kiss": quiz(long_answer, QUESTION, QUESTION), "yagni": VALID})
        self.assertTrue(any("is 9.3x the average wrong option (max 1.3x)" in p for p in problems), problems)

    def test_reports_boilerplate_phrases(self):
        meta = question("What does the wiki suggest?", why="**Why:** Clever code is a listed trap. See [[yagni]].")
        problems = self.lint({"kiss": quiz(meta, QUESTION, QUESTION), "yagni": VALID})
        self.assertIn("quizzes/kiss.md: 'What does the wiki suggest?' says 'the wiki'; ask about the reader's situation", problems)
        self.assertIn("quizzes/kiss.md: 'What does the wiki suggest?' says 'listed trap'; give the reason instead", problems)

    def test_reports_bank_where_the_answer_is_usually_the_longest_option(self):
        tell = question(options=["- [x] Longest one.", "- [ ] Shorter.", "- [ ] Short."])
        fair = question(options=["- [x] Short.", "- [ ] Shorter.", "- [ ] Longest one."])
        bank = {f"s{i}": quiz(tell, tell, fair) for i in range(10)}
        problems = lint_quizzes(bank, set(bank))
        self.assertIn("quizzes: the answer is the longest option in 20 of 30 questions (67%); keep it under 40%", problems)

    def test_reports_bank_where_the_answer_is_usually_the_shortest_option(self):
        tell = question(options=["- [x] Short.", "- [ ] Shorter one.", "- [ ] Longest one."])
        fair = question(options=["- [x] Longest one.", "- [ ] Shorter.", "- [ ] Short."])
        bank = {f"s{i}": quiz(tell, tell, fair) for i in range(10)}
        problems = lint_quizzes(bank, set(bank))
        self.assertIn("quizzes: the answer is the shortest option in 20 of 30 questions (67%); keep it under 40%", problems)

    def test_small_banks_skip_the_longest_option_check(self):
        tell = question(options=["- [x] Longest one.", "- [ ] Shorter.", "- [ ] Short."])
        problems = lint_quizzes({"kiss": quiz(tell, tell, tell)}, {"kiss"})
        self.assertFalse(any("longest option" in p for p in problems))


class LoadQuizzesTest(unittest.TestCase):
    def test_loads_markdown_files_by_slug(self):
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "kiss.md"), "w", encoding="utf-8") as f:
                f.write(VALID)
            with open(os.path.join(root, "notes.txt"), "w", encoding="utf-8") as f:
                f.write("ignored")
            self.assertEqual(load_quizzes(root), {"kiss": VALID})

    def test_missing_folder_means_no_quizzes(self):
        self.assertEqual(load_quizzes("/nonexistent/quizzes"), {})


if __name__ == "__main__":
    unittest.main()
