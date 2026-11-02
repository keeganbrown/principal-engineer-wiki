---
title: Large Language Models (LLMs)
category: technology
summary: Large language models predict likely text from patterns in vast training data — which makes them remarkably capable and also confidently wrong at times — so design systems around their strengths, limits, and costs rather than treating them as oracles.
tags: [ai, llm, machine-learning, rag, product-design]
---

# Large Language Models (LLMs)

> **In one sentence:** Large language models predict likely text from patterns in vast training data — which makes them remarkably capable and also confidently wrong at times — so design systems around their strengths, limits, and costs rather than treating them as oracles.

## The idea

A **large language model (LLM)** is a neural network trained on enormous amounts of text to predict what comes next. Given some input, it generates output one **token** at a time — a token is a chunk of text, roughly three-quarters of a word in English. From that simple objective, at large scale, come abilities like summarizing, translating, writing code, and following instructions.

A few properties matter for anyone building with them:

- **Context window** — the model only "sees" the text sent with each request, up to a limit measured in tokens. It has no memory between requests unless you send history again.
- **Non-determinism** — the same input can produce different output, and small wording changes can shift results.
- **Hallucination** — the model can produce fluent, confident statements that are false, because it generates *likely* text, not *verified* text.
- **Cost and latency per token** — every token in and out costs money and time.

Modern LLMs build on the **transformer** architecture from the 2017 Google paper "Attention Is All You Need."

## Why it matters

- **New product capabilities.** Tasks that needed rigid rules or weren't possible — reading free-form documents, answering questions in natural language, generating code — are now practical.
- **New failure modes.** Errors are plausible rather than obvious, outputs vary, and text from users or documents can act as instructions to the model (**prompt injection**).
- **New cost structure.** Usage-based pricing means a popular feature's cost grows with every request and every token.

## How to apply it

- **Give the model the facts it needs.** **Retrieval-augmented generation (RAG)** looks up relevant documents and includes them in the request, so answers draw on your data rather than the model's memory. Ask it to cite the sources it was given.
- **Use embeddings for meaning-based search.** An **embedding** turns text into a list of numbers so that similar meanings are close together; it powers semantic search and RAG retrieval.
- **Constrain the output.** Ask for structured output (a JSON schema), validate it in code, and retry or fall back on invalid results.
- **Build an evaluation set.** Collect real examples with known-good answers and score every prompt or model change against them — the equivalent of a test suite ([[test-driven-development]]).
- **Keep humans on consequential decisions.** Drafts, suggestions, and triage are good fits; final calls on money, health, or access need review.
- **Treat model input as untrusted.** Anything the model reads might contain instructions. Limit what tools and data it can reach ([[agent-guardrails]]).
- **Budget and monitor tokens.** Cap request sizes, cache repeated work, and use smaller, cheaper models for simpler tasks.

## Example

A support team wants an assistant that answers customer questions from the help center. The first prototype sends questions straight to an LLM. It answers fluently — including inventing a refund policy the company doesn't have.

The second version uses RAG: it searches the help center using embeddings, sends the top five articles with the question, and instructs the model to answer only from them and cite which one it used. If nothing relevant is found, it says so and offers a human agent. A set of 300 real past questions with approved answers scores every change.

Accuracy on the set rises from 61% to 93%, and invented policies largely disappear. The costs: building and maintaining the evaluation set, keeping the search index current as articles change, and per-question token costs that the team tracks against support savings. The remaining 7% are handed to humans.

## Common traps

- **Treating output as fact.** Fluency isn't accuracy; check claims that matter.
- **No evaluation.** Without a scored set of examples, every prompt change is a guess, and regressions go unnoticed.
- **Stuffing the context.** More text isn't always better; irrelevant context can make answers worse and costs more.
- **Ignoring injection.** A web page or email the model reads can say "ignore previous instructions" — and sometimes it works.
- **Sending sensitive data carelessly.** Know your provider's data retention and training terms before sending customer data.

## When it doesn't apply

If a deterministic rule, a regular expression, or a database query solves the problem, use it — it's cheaper, faster, and exactly repeatable. And where errors are unacceptable and can't be checked — legal commitments, safety-critical control — an LLM can assist a human but shouldn't decide alone.

## Related

- [[agent-guardrails]] — limiting what a model-driven agent can do.
- [[adopting-coding-agents]] — LLMs applied to software development itself.
- [[observability]] — log prompts, outputs, latency, and cost to understand behavior in production.
- [[nosql-databases]] — vector and search stores often hold the embeddings.
- [[reversible-decisions]] — model vendors change fast; keep the choice reversible behind an interface.
