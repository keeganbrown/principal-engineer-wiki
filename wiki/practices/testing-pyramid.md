---
title: Testing Pyramid
category: practices
summary: Have many fast unit tests, fewer integration tests, and only a handful of slow end-to-end tests, so your suite is both trustworthy and quick.
tags: [testing, quality, ci]
---

# Testing Pyramid

> **In one sentence:** Have many fast unit tests, fewer integration tests, and only a handful of slow end-to-end tests, so your suite is both trustworthy and quick.

## The idea

Tests trade **speed and precision** against **realism**:

```
        /\        End-to-end   — few; slow; test whole user journeys
       /  \
      /----\      Integration  — some; test real pieces working together
     /      \
    /--------\    Unit         — many; fast; test small pieces of logic
```

- **Unit tests** — check one unit of *behavior* — often several real objects working together — isolated only from slow or unpredictable things like the network, the clock, or the database. Milliseconds each. When one fails, you know where to look.
- **Integration tests** — check that your code works with real infrastructure or other modules: a real database, a real queue, a real HTTP client.
- **End-to-end (E2E) tests** — drive the whole system like a user would, through the UI or public API.

The pyramid shape says: most of your confidence should come from the cheap, fast layer at the bottom.

Mike Cohn popularized the pyramid in *Succeeding with Agile* (2009).

## Why it matters

A suite that's mostly E2E tests (the "ice-cream cone" anti-pattern) is slow, flaky, and hard to debug. Developers stop running it, continuous integration (CI) takes an hour, and a red build tells you *something* broke but not *what*.

A suite that's *only* unit tests misses the bugs that live between components: wrong SQL, mismatched JSON fields, misconfigured auth.

## How to apply it

- **Put business logic where unit tests can reach it.** Keep it free of I/O, then test it thoroughly there.
- **Write integration tests for each boundary.** Cover database queries, message formats, and external API clients.
- **Keep E2E tests for a few critical user journeys.** Sign up, checkout, login — not every edge case.
- **Use contract tests between services.** Each side verifies the API without running the other ([[contract-testing]]).
- **Track suite time.** If CI is creeping past ~10 minutes, find the slow tests and push them down the pyramid.
- **Fix flaky tests fast.** A flaky test teaches people to ignore red builds.

## Example

Testing a discount feature:

- **Unit (20 tests)** — `calculateDiscount` with every coupon type, expiry, stacking rule, and rounding edge case.
- **Integration (2 tests)** — the coupon repository saves and loads correctly against a real test database; the checkout API returns the discounted total in its JSON.
- **E2E (1 test)** — a user applies a coupon in the browser and sees the new total.

The first 22 run in a few seconds; the last takes about 30 seconds.

## Common traps

- **Mocking so much the unit tests lie.** They pass while the real integration is broken.
- **Duplicating every unit case at the E2E level.** Test each behavior at the lowest level that can catch it.
- **Treating coverage as the goal.** 90% coverage of trivial getters says little; focus on risky logic and boundaries ([[metric-fixation]]).
- **Sharing stateful test environments.** Tests start depending on each other's leftovers.

## When it doesn't apply

The ideal shape depends on where your risk lives:

- **Spotify's "testing honeycomb" (2018)** — for microservices with little internal logic, most risk is in how the service talks to its database and neighbors, so integration tests form the bulk.
- **Kent C. Dodds' "testing trophy" (2018)** — for frontend apps, a base of static checks (types, linting), a thick middle of integration tests, and fewer pure unit tests. Here, "integration" often means **component tests** — rendering one UI component with its real children and checking what the user sees.

The principle holds in every shape: prefer the fastest test that gives you real confidence.

## Related

- [[test-driven-development]] — produces a strong base of unit tests.
- [[contract-testing]] — replaces many slow E2E tests between services.
- [[hexagonal-architecture]] — makes it easy to unit-test logic and integration-test adapters separately.
- [[functional-core-imperative-shell]] — pushes most logic into the cheap-to-test layer.
- [[feature-flags]] — let you test both code paths, and test in production safely.
- [[continuous-delivery]] — the pipeline a fast suite keeps moving.
