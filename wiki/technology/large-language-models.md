---
title: Large Language Models (LLMs)
category: technology
summary: Large language models predict likely text from patterns in their training data, which makes them capable but sometimes confidently wrong; design around their strengths, limits, and costs instead of treating them as oracles.
tags: [ai, llm, machine-learning, rag, product-design]
---

# Large Language Models (LLMs)

> **In one sentence:** Large language models predict likely text from patterns in their training data, which makes them capable but sometimes confidently wrong; design around their strengths, limits, and costs instead of treating them as oracles.

## The idea

A **large language model (LLM)** is a neural network trained on enormous amounts of text to predict what comes next. Given some input, it generates output one **token** at a time — a token is a chunk of text, roughly three-quarters of a word in English. From that objective, at large scale, come abilities like summarizing, translating, and writing code. A second training stage, on examples and human feedback, teaches the model to follow instructions and act as an assistant.

A few properties matter for anyone building with them:

- **Context window** — the model only "sees" the text sent with each request, up to a limit measured in tokens. It has no memory between requests unless you send history again.
- **Non-determinism** — the same input can produce different output, and small wording changes can shift results.
- **Hallucination** — the model can produce fluent, confident statements that are false, because it generates *likely* text, not *verified* text.
- **Cost and latency per token** — every token in and out costs money and time.
- **Tool use** — applications can let the model call functions, such as search, running code, or sending email. An LLM that calls tools in a loop toward a goal is an *agent*.

Modern LLMs build on the transformer, a network design that weighs every token against every other, from the 2017 Google paper "Attention Is All You Need."

## Why it matters

- **New products become possible.** Tasks that needed rigid rules or weren't possible — reading free-form documents, answering questions in natural language, generating code — are now practical.
- **Failures look different.** Errors are plausible rather than obvious, outputs vary, and text from users or documents can act as instructions to the model (**prompt injection**).
- **Costs scale with usage.** Usage-based pricing means a popular feature's cost grows with every request and every token.

## How to apply it

- **Give the model the facts it needs.** **Retrieval-augmented generation (RAG)** looks up relevant documents and includes them in the request, so answers draw on your data rather than the model's memory. Ask it to cite the sources it was given.
- **Use embeddings for meaning-based search.** An **embedding** turns text into a list of numbers so that similar meanings are close together; it powers semantic search (finding text by meaning, not exact words) and RAG retrieval.
- **Constrain the output.** Use the API's structured-output mode where available, which forces output to match a JSON schema, and still validate the values in code; retry or fall back on invalid results.
- **Build an evaluation set.** Collect real examples with known-good answers and score every prompt or model change against them — the equivalent of a test suite ([[test-driven-development]]). Keep some examples back that you never tune against, or the score measures how well you fit the set. Pin model versions where the provider allows it, and rerun the set before any model upgrade: a provider's update is a change you didn't write.
- **Keep humans on consequential decisions.** Drafts, suggestions, and triage are good fits; final calls on money, health, or access need review. Check that reviewers sometimes disagree; one who approves everything is not a control.
- **Treat model input as untrusted.** Anything the model reads might contain instructions. Limit what tools and data it can reach ([[agent-guardrails]]).
- **Budget and monitor tokens.** Cap request sizes, cache repeated work, and use smaller, cheaper models for simpler tasks.

## Example

A support team wants an assistant that answers customer questions from the help center. The first prototype sends questions straight to an LLM. It answers fluently — including inventing a refund policy the company doesn't have.

The second version uses RAG: it searches the help center using embeddings, sends the top five articles with the question, and instructs the model to answer only from them and cite which one it used. If nothing relevant is found, it says so and offers a human agent. A set of 300 real past questions with approved answers scores every change.

Accuracy on the set rises from 61% to 93%, and invented policies largely disappear. The costs: building and maintaining the evaluation set, keeping the search index current as articles change, and per-question token costs that the team tracks against support savings. The remaining 7% are wrong answers the system can't tell apart from right ones at run time. So the team keeps the "nothing relevant → human" fallback, samples live answers for review each week, and adds the bad ones to the evaluation set.

## Common traps

- **Treating output as fact.** Fluency isn't accuracy; check claims that matter.
- **Fixing hallucination with a bigger model or a sterner prompt.** Neither gives the model facts it doesn't have; retrieval does.
- **No evaluation.** Without a scored set of examples, every prompt change is a guess, and regressions go unnoticed.
- **Stuffing the context.** More text isn't always better; irrelevant context can make answers worse and costs more.
- **Ignoring injection.** A web page or email the model reads can say "ignore previous instructions" — and sometimes it works.
- **Sending sensitive data carelessly.** Know your provider's data retention and training terms before sending customer data.

## When it doesn't apply

If a deterministic rule, a regular expression, or a database query solves the problem, use it — it's cheaper, faster, and exactly repeatable. And where errors are unacceptable and can't be checked — legal commitments, safety-critical control — an LLM can assist a human but shouldn't decide alone.

## Related

- [[agent-guardrails]] — limiting what a model-driven agent can do.
- [[adopting-coding-agents]] — how a team rolls out LLM-based coding tools and measures the result.
- [[observability]] — log prompts, outputs, latency, and cost to understand behavior in production.
- [[nosql-databases]] — search stores can hold embeddings for semantic search.
- [[reversible-decisions]] — model vendors change fast, which is a real reason to keep a thin seam at the model call; prompts and evaluation results still won't transfer for free.
