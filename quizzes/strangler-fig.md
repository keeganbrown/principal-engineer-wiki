# Quiz: Strangler Fig

## What is the first step in a strangler fig migration?

- [x] Put a routing layer, such as a proxy or gateway, in front of the old system.
- [ ] Freeze the old system and start a full rewrite.
- [ ] Copy the old database into the new system.
- [ ] Rewrite the riskiest part of the system first.

**Why:** The routing layer lets you move one slice of traffic at a time to the new code. See [[strangler-fig]].

## How did the billing team check that new tax calculation matched the old one?

- [x] Ran both versions in shadow mode for a month and compared outputs.
- [ ] Asked the original authors to review the new code.
- [ ] Switched all traffic at once and watched for complaints.
- [ ] Wrote unit tests based on the tax documentation.

**Why:** Comparing outputs on real traffic catches differences before users see them. See [[strangler-fig]].

## What is the most common way a strangler fig migration fails?

- [x] Never finishing, so two systems run side by side indefinitely.
- [ ] Moving too slowly on the first slice.
- [ ] Choosing a low-risk slice to start with.
- [ ] Deleting the old code once traffic has moved.

**Why:** Actually delete the old code. In the example, the last two slices, which touched shared data, took as long as the first ten. See [[strangler-fig]].
