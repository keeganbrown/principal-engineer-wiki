# Quiz: Contract Testing

## The orders team renames `total` to `totalAmount` and all their tests pass. How does contract testing catch the break?

- [x] Their CI runs the mobile app's contract, which says it reads `total`, and fails.
- [ ] A full end-to-end test environment runs both services together nightly.
- [ ] The mobile app's unit tests fail as soon as the orders team merges.
- [ ] The API gateway rejects responses that don't match the old field names.

**Why:** Consumers record what they use, and the provider verifies those contracts in its own fast suite, before release. See [[contract-testing]].

## What should a consumer's contract specify?

- [x] Only the fields and behavior that consumer actually uses.
- [ ] Every field in the provider's full response schema.
- [ ] The provider's internal database schema.
- [ ] The exact response times the consumer expects.

**Why:** Over-specified contracts break on harmless changes. Consumers specify only what they rely on, which also shows providers what's used. See [[contract-testing]].

## What can contract tests not tell you?

- [x] Whether the provider's values are correct — they check shape, not meaning.
- [ ] Whether a field the consumer reads has been removed.
- [ ] Whether a field changed type from a number to a string.
- [ ] Which consumers depend on a given field.

**Why:** A contract test confirms `total` is a number, not that it's the right total. Keep other tests for behavior. See [[contract-testing]].
