# Quiz: Testing Pyramid

## Testing a discount feature, where should coupon stacking and rounding edge cases be tested?

- [x] In unit tests of the discount calculation.
- [ ] In end-to-end browser tests, one per edge case.
- [ ] In integration tests against a real database.
- [ ] In manual QA before each release.

**Why:** Put business logic where fast unit tests can reach it. Save end-to-end tests for a few critical journeys. See [[testing-pyramid]].

## A microservice has little internal logic and mostly talks to its database. What shape fits?

- [x] More integration tests than unit tests, as in the "testing honeycomb."
- [ ] Almost all end-to-end tests, since the service is simple.
- [ ] Only unit tests with every dependency mocked.
- [ ] No automated tests, since there's no logic to test.

**Why:** The right shape depends on where risk lives. The principle holds everywhere: prefer the fastest test that gives real confidence. See [[testing-pyramid]].

## Which is a listed testing-pyramid trap?

- [x] Mocking so much that unit tests pass while the real code fails.
- [ ] Writing one end-to-end test for a critical user journey.
- [ ] Running integration tests against a real test database.
- [ ] Tracking how long the test suite takes.

**Why:** Over-mocked unit tests lie. Pair them with integration tests at each boundary. See [[testing-pyramid]].
