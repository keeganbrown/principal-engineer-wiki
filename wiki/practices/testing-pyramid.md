---
title: The Testing Pyramid
category: practices
summary: Have many fast unit tests, fewer integration tests, and only a handful of slow end-to-end tests, so your suite is both trustworthy and quick.
tags: [testing, quality, ci]
---

# The Testing Pyramid

> **In one sentence:** Have many fast unit tests, fewer integration tests, and only a handful of slow end-to-end tests, so your suite is both trustworthy and quick.

## The idea

Not all tests are equal. They trade off **speed and precision** against **realism**:

```
        /\        End-to-end   — few; slow; test whole user journeys
       /  \
      /----\      Integration  — some; test real pieces working together
     /      \
    /--------\    Unit         — many; fast; test small pieces of logic
```

- **Unit tests** check one function or module in isolation. Milliseconds each. When one fails, you know exactly where.
- **Integration tests** check that components work together — your code against a real database, a real queue, or another module.
- **End-to-end (E2E) tests** drive the whole system like a user would, through the UI or public API.

The pyramid shape says: most of your confidence should come from the cheap, fast layer at the bottom.

## Why it matters

A suite that's mostly E2E tests (the "ice-cream cone" anti-pattern) is slow, flaky, and hard to debug. Developers stop running it, CI takes an hour, and a red build tells you *something* broke but not *what*.

A suite that's *only* unit tests misses the bugs that live between components: wrong SQL, mismatched JSON fields, misconfigured auth.

## How to apply it

- Put business logic where unit tests can reach it without I/O — then test it thoroughly there.
- Write integration tests for each **boundary**: database queries, message formats, external API clients.
- Keep E2E tests for a few **critical user journeys**: sign up, checkout, login. Not every edge case.
- Use **contract tests** between services so each side can verify the API without spinning up the other.
- Track suite time. If CI is creeping past ~10 minutes, find the slow tests and push them down the pyramid.
- Quarantine and fix flaky tests fast. A flaky test teaches people to ignore red builds.

## Example

Testing a discount feature:

- **Unit (20 tests):** `calculateDiscount` with every coupon type, expiry, stacking rule, and rounding edge case.
- **Integration (3 tests):** coupon repository saves and loads correctly against a real test database; the checkout API returns the discounted total in its JSON.
- **E2E (1 test):** a user applies a coupon in the browser and sees the new total.

Total runtime: a few seconds for the first 23, maybe 30 seconds for the last one.

## Common traps

- **Mock-heavy "unit" tests** that pass while the real integration is broken.
- **Duplicating every unit case at the E2E level.** Test each behavior at the lowest level that can catch it.
- **Treating coverage as the goal.** 90% coverage of trivial getters says little; focus on risky logic and boundaries.
- **Shared, stateful test environments** that make tests depend on each other's leftovers.

## When it doesn't apply

The ideal shape varies. A thin CRUD service with little logic may get more value from integration tests (sometimes called a "testing trophy"). A UI-heavy app may lean on component tests. The principle holds, though: prefer the fastest test that gives you real confidence.

## Related

- [[test-driven-development]] — produces a strong base of unit tests.
- [[hexagonal-architecture]] — makes it easy to unit-test logic and integration-test adapters separately.
- [[functional-core-imperative-shell]] — pushes most logic into the cheap-to-test layer.
- [[feature-flags]] — let you test in production safely, complementing the pyramid.
