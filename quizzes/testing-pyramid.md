# Quiz: Testing Pyramid

## Testing a discount feature, where should coupon stacking and rounding edge cases be tested?

- [x] In unit tests of the discount calculation.
- [ ] In end-to-end browser tests, one per edge case.
- [ ] In integration tests against a real database.
- [ ] In manual QA before each release goes out.

**Why:** Put business logic where fast unit tests can reach it. Save end-to-end tests for a few critical journeys. See [[testing-pyramid]].

## A microservice has little internal logic and mostly talks to its database. What shape fits?

- [x] Mostly integration tests, with fewer unit and end-to-end tests.
- [ ] Almost all end-to-end tests, since the service itself is simple.
- [ ] Only unit tests, with every dependency mocked out.
- [ ] No automated tests, since there's no logic to test.

**Why:** Most of its risk is in how it talks to its database and neighbors, so that's where tests pay off (Spotify called this the "testing honeycomb"). Prefer the fastest test that gives real confidence. See [[testing-pyramid]].

## A team's unit tests mock the HTTP client and are all green, but checkout fails in staging because a JSON field was renamed. What went wrong?

- [x] The unit tests mocked the boundary, and no integration test covered it.
- [ ] The team ran too few end-to-end tests, so every journey needs one now.
- [ ] Staging is configured differently, so its failures can be ignored.
- [ ] The unit tests ran too fast to catch problems of this kind.

**Why:** Over-mocked unit tests pass while the real code fails. Pair them with integration tests at each boundary. See [[testing-pyramid]] and [[contract-testing]].
