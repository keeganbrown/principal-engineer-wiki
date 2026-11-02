# Quiz: Large Language Models (LLMs)

## A support assistant invents a refund policy the company doesn't have. What fixes this best?

- [x] Retrieve relevant help articles, tell the model to answer only from them, and offer a human when nothing fits.
- [ ] Ask the model to be more careful in the prompt.
- [ ] Switch to a larger model, which never invents facts.
- [ ] Lower the temperature to zero so answers are deterministic.

**Why:** Give the model the facts it needs (retrieval-augmented generation). Measured against an evaluation set, accuracy rose from 61% to 93%. See [[large-language-models]].

## What is an evaluation set for?

- [x] Scoring every prompt or model change against real questions with approved answers.
- [ ] Training the model on your company's data.
- [ ] Limiting how many tokens each request can use.
- [ ] Filtering harmful content from user input.

**Why:** Without evaluation, you can't tell whether a change helped. "No evaluation" is a listed trap. See [[large-language-models]].

## When should you not use an LLM?

- [x] When a regular expression or database query solves the problem exactly.
- [ ] When the text is longer than a few paragraphs.
- [ ] When users write in more than one language.
- [ ] When you need to summarize a long document.

**Why:** Deterministic tools are cheaper, faster, and exactly repeatable. Where errors can't be checked, an LLM shouldn't decide alone. See [[large-language-models]].
