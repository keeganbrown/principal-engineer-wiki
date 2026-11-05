#!/usr/bin/env python3
"""Quiz question banks: one Markdown file per article in quizzes/<slug>.md.

Format (the H1, when checked against article titles, is "# Quiz: <title>"):

    ## A question that ends with a question mark?

    - [x] The correct option.
    - [ ] A plausible wrong option.
    - [ ] Another plausible wrong option.

    **Why:** One or two sentences explaining the answer. [[links]] allowed.

parse_quiz and lint_quizzes are pure; load_quizzes reads the folder.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from lint_wiki import WIKILINK

MIN_QUESTIONS = 3
OPTION_COUNTS = (3, 4)
# Readers learn to pick the longest (or shortest) option when it's usually right.
MAX_ANSWER_LENGTH_RATIO = 1.3
MAX_LENGTH_SHARE = 0.4
MIN_BANK_FOR_SHARE = 30
# Phrases that cite the wiki instead of testing or explaining the idea.
BOILERPLATE = {
    "the wiki": "ask about the reader's situation",
    "listed trap": "give the reason instead",
}
QUESTION_HEADING = re.compile(r"^## (.+?)\s*$")
OPTION = re.compile(r"^- \[( |x)\] (.+?)\s*$")
WHY = re.compile(r"^\*\*Why:\*\* (.+?)\s*$")


@dataclass
class Question:
    question: str
    options: List[str] = field(default_factory=list)
    answers: List[int] = field(default_factory=list)
    why: str = ""
    stray: List[str] = field(default_factory=list)

    @property
    def links(self) -> Set[str]:
        text = " ".join([self.question, self.why, *self.options])
        return {m.strip() for m in WIKILINK.findall(text)}


def parse_quiz(text: str) -> List[Question]:
    questions: List[Question] = []
    for line in text.splitlines():
        heading = QUESTION_HEADING.match(line)
        if heading:
            questions.append(Question(question=heading.group(1)))
            continue
        if not questions or not line.strip():
            continue
        current = questions[-1]
        option = OPTION.match(line)
        why = WHY.match(line)
        if option:
            if option.group(1) == "x":
                current.answers.append(len(current.options))
            current.options.append(option.group(2))
        elif why:
            current.why = why.group(1)
        else:
            current.stray.append(line.strip())
    return questions


def _lint_question(path: str, q: Question) -> List[str]:
    label = f"{path}: '{q.question}'"
    problems = []
    if not q.question.endswith("?"):
        problems.append(f"{label} must end with '?'")
    if len(q.options) not in OPTION_COUNTS:
        problems.append(f"{label} has {len(q.options)} options, need 3 or 4")
    if len(q.answers) != 1:
        problems.append(f"{label} needs exactly one correct option, has {len(q.answers)}")
    if len({o.lower() for o in q.options}) != len(q.options):
        problems.append(f"{label} repeats an option")
    if not q.why:
        problems.append(f"{label} has no **Why:** line")
    for line in q.stray:
        problems.append(f"{path}: unexpected line '{line}'")
    ratio = _answer_length_ratio(q)
    if ratio is not None and ratio > MAX_ANSWER_LENGTH_RATIO:
        problems.append(f"{label} answer is {ratio:.1f}x the average wrong option (max {MAX_ANSWER_LENGTH_RATIO}x)")
    text = " ".join([q.question, q.why, *q.options]).lower()
    for phrase, advice in BOILERPLATE.items():
        if phrase in text:
            problems.append(f"{label} says '{phrase}'; {advice}")
    return problems


def _answer_length_ratio(q: Question):
    if len(q.answers) != 1 or len(q.options) < 2:
        return None
    answer = len(q.options[q.answers[0]])
    wrong = [len(o) for i, o in enumerate(q.options) if i != q.answers[0]]
    return answer / (sum(wrong) / len(wrong))


def _answer_is_longest(q: Question) -> bool:
    answer = len(q.options[q.answers[0]])
    return all(answer > len(o) for i, o in enumerate(q.options) if i != q.answers[0])


def _answer_is_shortest(q: Question) -> bool:
    answer = len(q.options[q.answers[0]])
    return all(answer < len(o) for i, o in enumerate(q.options) if i != q.answers[0])


def _lint_length_shares(questions: List[Question]) -> List[str]:
    """Bank-wide: neither "pick the longest" nor "pick the shortest" should win."""
    scored = [q for q in questions if len(q.answers) == 1 and len(q.options) >= 2]
    if len(scored) < MIN_BANK_FOR_SHARE:
        return []
    problems = []
    for name, test in (("longest", _answer_is_longest), ("shortest", _answer_is_shortest)):
        count = sum(test(q) for q in scored)
        share = count / len(scored)
        if share > MAX_LENGTH_SHARE:
            problems.append(
                f"quizzes: the answer is the {name} option in {count} of {len(scored)} questions "
                f"({share:.0%}); keep it under {MAX_LENGTH_SHARE:.0%}"
            )
    return problems


def lint_quizzes(
    quizzes: Dict[str, str], slugs: Set[str], titles: Optional[Dict[str, str]] = None
) -> List[str]:
    """Every article has a quiz; every quiz is well formed and its links resolve.

    With `titles` (slug -> article title), each quiz's H1 must be "# Quiz: <title>".
    """
    problems = [f"quizzes: missing quiz for [[{s}]]" for s in sorted(slugs - set(quizzes))]
    everything: List[Question] = []
    for slug in sorted(quizzes):
        path = f"quizzes/{slug}.md"
        if slug not in slugs:
            problems.append(f"{path}: no article with this slug")
        if titles and slug in titles:
            expected = f"# Quiz: {titles[slug]}"
            if quizzes[slug].splitlines()[:1] != [expected]:
                problems.append(f"{path}: title should be '{expected}'")
        questions = parse_quiz(quizzes[slug])
        everything.extend(questions)
        if len(questions) < MIN_QUESTIONS:
            problems.append(f"{path}: {len(questions)} question(s), need at least {MIN_QUESTIONS}")
        for q in questions:
            problems.extend(_lint_question(path, q))
            for target in sorted(q.links - slugs):
                problems.append(f"{path}: broken link [[{target}]]")
    return problems + _lint_length_shares(everything)


def load_quizzes(quiz_root: str) -> Dict[str, str]:
    if not os.path.isdir(quiz_root):
        return {}
    quizzes = {}
    for filename in sorted(os.listdir(quiz_root)):
        if filename.endswith(".md"):
            with open(os.path.join(quiz_root, filename), encoding="utf-8") as f:
                quizzes[filename[: -len(".md")]] = f.read()
    return quizzes
