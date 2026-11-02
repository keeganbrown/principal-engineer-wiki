# Quiz: Contract Testing

## The mobile app reads an order's `total`. The orders team renames it to `totalAmount` and all their tests pass. How does contract testing catch the break?

- [x] The orders team's CI runs the app's contract, which reads `total`.
- [ ] A full end-to-end environment runs both services together every night.
- [ ] The mobile app's unit tests fail as soon as the orders team merges.
- [ ] The API gateway rejects responses that don't match old field names.

**Why:** Consumers record what they use, and the provider verifies those contracts in its own fast suite, before release. See [[contract-testing]].

## No consumer contract mentions a field. Is it safe to remove?

- [x] Not yet; check usage metrics for consumers without contracts.
- [ ] Yes; a field no contract mentions is unused by definition.
- [ ] Yes, as long as the provider's own tests still pass after.
- [ ] No; published fields have to stay for at least a year.

**Why:** It's a strong signal, but only consumers that publish contracts are counted. See [[contract-testing]] and [[api-versioning]].

## What can contract tests not tell you?

- [x] Whether the provider's values are actually correct.
- [ ] Whether a field the consumer requires is missing.
- [ ] Whether a field changed type from number to string.
- [ ] Whether the provider renamed a field the consumer reads.

**Why:** Contracts check shape, not meaning: they confirm `total` is a number, not that it's the right total. Keep other tests for behavior. See [[contract-testing]].

## A public API has unknown outside consumers. What replaces consumer-driven contracts?

- [x] Schema checks and a strict versioning policy.
- [ ] Asking every customer to publish a contract first.
- [ ] More end-to-end tests run against each customer.
- [ ] Manual testing by partners before each release.

**Why:** You can't collect contracts from consumers you don't know. And if one team owns and deploys both sides, a few integration tests are usually enough. See [[contract-testing]] and [[api-versioning]].
