---
title: Test-Driven Development (TDD)
category: practices
summary: Write a small failing test first, make it pass with the simplest code, then clean up — repeating in tight loops so design and safety grow together.
tags: [testing, design, workflow]
---

# Test-Driven Development (TDD)

> **In one sentence:** Write a small failing test first, make it pass with the simplest code, then clean up — repeating in tight loops so design and safety grow together.

## The idea

TDD flips the usual order. Instead of writing code and then testing it, you:

1. **Red** — write a test for one small behavior. Run it and watch it fail, which proves the test can catch a problem.
2. **Green** — write the simplest code that makes it pass. Don't polish.
3. **Refactor** — now that it works and is protected by a test, improve the design.

Each loop takes minutes. Over a day, you build up working code *and* a test suite that describes exactly what it does.

Kent Beck popularized TDD as part of Extreme Programming in the late 1990s.

## Why it matters

- **Design feedback.** If something is hard to test, it's often too [[coupling-and-cohesion|coupled]]. TDD surfaces that while it's cheap to fix. But don't add interfaces and indirection *only* to make testing possible — if testability demands a layer the design doesn't otherwise need, test through a real boundary with a fake, or test at a higher level.
- **Confidence to change.** A good suite lets you refactor boldly and deploy often.
- **Living documentation.** Tests show how the code is meant to be used.
- **Focus.** You build only what a test demands, which keeps scope tight.

## How to apply it

- **Start with the simplest meaningful case.** Then add edge cases one at a time.
- **Test behavior through public interfaces.** Tests that know about private methods or internal structure break on every refactor.
- **Keep tests fast.** Milliseconds each. Slow tests stop being run.
- **Name tests as sentences.** For example, `"rejects expired tokens"` or `"applies discount to orders over 100"`.
- **Start every bug fix with a failing test.** Reproduce the bug in a test, then fix it, so it can never silently return.
- **Wrap what's hard to test.** For UI, hardware, or third-party APIs, put a thin layer around them and test-drive everything behind it ([[hexagonal-architecture]]).

## Example

Requirement: orders over $100 get free shipping; others pay a flat $5.

```
test "orders over 100 ship free":
    assert shippingCost(order(total=101)) == 0      # red: function doesn't exist

function shippingCost(order):
    return 0           # green: deliberately naive — the next test forces real logic

test "orders at or under 100 pay flat 5":
    assert shippingCost(order(total=100)) == 5      # red again

function shippingCost(order):                       # green
    return 0 if order.total > 100 else 5

# refactor: name the magic numbers, tests still pass
FREE_SHIPPING_THRESHOLD = 100
FLAT_SHIPPING_FEE = 5

function shippingCost(order):
    return 0 if order.total > FREE_SHIPPING_THRESHOLD else FLAT_SHIPPING_FEE
```

Each step is tiny, and the boundary case (`100`) is pinned down by a test.

## Common traps

- **Testing implementation details.** Asserting that a private helper was called makes tests brittle.
- **Skipping refactor.** Red-green without refactor produces passing tests and messy code.
- **Giant steps.** Writing ten tests then a hundred lines of code isn't TDD; you lose the feedback loop.
- **Mocking everything.** A **mock** checks *which calls were made*; a **fake** is a simple working stand-in, like an in-memory database. Heavy mocking tests your mocks, not your system. Many practitioners (the "classicist" school) prefer fakes and real objects for your own code; others ("mockists") use mocks more freely. Either way, mock only at real boundaries.

## When it doesn't apply

Exploratory spikes — where you don't yet know what you're building — are often better done without tests, then thrown away and rebuilt with TDD. Visual design, performance tuning, and integration with poorly documented systems may need other feedback loops (screenshots, benchmarks, [[contract-testing|contract tests]]).

In untested legacy code, TDD often stalls because there are no **seams** — places where you can swap in a test double (a mock, fake, or stub) without editing the code. Start with **characterization tests** that pin down what the code does today, then test-drive your changes.

## Related

- [[testing-pyramid]] — how to balance the kinds of tests TDD produces.
- [[functional-core-imperative-shell]] — an architecture that makes TDD easy.
- [[yagni]] — TDD naturally limits code to what tests require.
- [[code-review]] — tests make reviews faster and more trustworthy.
