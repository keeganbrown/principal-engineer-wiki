# Quiz: Large Language Models

## A support assistant invents a refund policy the company doesn't have. What reduces this most?

- [x] Answer only from retrieved help articles, with a human fallback.
- [ ] Ask the model in the prompt to be more careful about facts.
- [ ] Switch to a larger model, since bigger models invent less.
- [ ] Send the whole help center along with every single question asked.

**Why:** Give the model the facts it needs (retrieval-augmented generation); a bigger model or a sterner prompt doesn't supply facts it lacks. Some wrong answers remain that the system can't detect at run time, so keep a fallback and review a sample each week. See [[large-language-models]].

## What is an evaluation set for?

- [x] Scoring every prompt or model change against approved answers.
- [ ] Training the model on your company's own internal documents.
- [ ] Limiting how many tokens each request is allowed to use.
- [ ] Filtering harmful content out of user input before it's sent.

**Why:** Without evaluation, you can't tell whether a change helped. See [[large-language-models]].

## When should you not use an LLM?

- [x] When a regular expression or query solves it exactly.
- [ ] When the input text is longer than a few paragraphs.
- [ ] When users write in more than one language.
- [ ] When you need a quick summary of a long internal document.

**Why:** Deterministic tools are cheaper, faster, and exactly repeatable. See [[large-language-models]].

## A human reviews every refund the model approves, and has approved all 2,000 so far. What does that suggest?

- [x] The review may not be a real control.
- [ ] The model has reached perfect accuracy on refunds.
- [ ] The human reviewer can now be safely removed.
- [ ] Refunds are a good fit for full automation now.

**Why:** Keep humans on consequential decisions, and check that reviewers sometimes disagree; one who approves everything is not a control. See [[large-language-models]].
