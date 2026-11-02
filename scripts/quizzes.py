#!/usr/bin/env python3
"""Quiz question banks: one Markdown file per article in quizzes/<slug>.md.

Format (the H1 is optional and ignored):

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
from typing import Dict, List, Set

from lint_wiki import WIKILINK

MIN_QUESTIONS = 3
OPTION_COUNTS = (3, 4)
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
    return problems


def lint_quizzes(quizzes: Dict[str, str], slugs: Set[str]) -> List[str]:
    """Every article has a quiz; every quiz is well formed and its links resolve."""
    problems = [f"quizzes: missing quiz for [[{s}]]" for s in sorted(slugs - set(quizzes))]
    for slug in sorted(quizzes):
        path = f"quizzes/{slug}.md"
        if slug not in slugs:
            problems.append(f"{path}: no article with this slug")
        questions = parse_quiz(quizzes[slug])
        if len(questions) < MIN_QUESTIONS:
            problems.append(f"{path}: {len(questions)} question(s), need at least {MIN_QUESTIONS}")
        for q in questions:
            problems.extend(_lint_question(path, q))
            for target in sorted(q.links - slugs):
                problems.append(f"{path}: broken link [[{target}]]")
    return problems


def load_quizzes(quiz_root: str) -> Dict[str, str]:
    if not os.path.isdir(quiz_root):
        return {}
    quizzes = {}
    for filename in sorted(os.listdir(quiz_root)):
        if filename.endswith(".md"):
            with open(os.path.join(quiz_root, filename), encoding="utf-8") as f:
                quizzes[filename[: -len(".md")]] = f.read()
    return quizzes
