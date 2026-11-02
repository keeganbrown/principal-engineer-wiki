# Quiz: Metric Fixation

## A director sets an 80% coverage target. Teams hit it, but incidents don't drop. Why?

- [x] Many new tests ran code without asserting anything, the cheapest way to move the number.
- [ ] 80% is too low; the target should have been 100%.
- [ ] Coverage tools count lines incorrectly.
- [ ] Teams deleted their old tests to make room.

**Why:** Goodhart's law: when a measure becomes a target, it ceases to be a good measure. See [[metric-fixation]].

## What makes metrics harder to game?

- [x] Pairing metrics that pull against each other, like deploy frequency and change failure rate.
- [ ] Adding 40 metrics so no single one matters.
- [ ] Ranking individuals by their output each month.
- [ ] Dropping measurement entirely.

**Why:** Gaming one shows up in the other. More metrics or no metrics are both listed traps. See [[metric-fixation]].

## When can a metric work as a target?

- [x] When it's defined tightly, such as the slowest 1% of requests measured from the user's side, and audited.
- [ ] When it's simple enough to report in one number upward.
- [ ] When it counts activity, such as commits or tickets closed.
- [ ] When engineers are rewarded individually for moving it.

**Why:** Latency budgets or cost ceilings are close to the outcome, but even they get gamed at the edges without tight definitions. See [[metric-fixation]].
