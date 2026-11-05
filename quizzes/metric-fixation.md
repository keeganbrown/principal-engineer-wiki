# Quiz: Metric Fixation

## A director sets an 80% coverage target. Teams hit it, but incidents don't drop. Why?

- [x] Many new tests ran code without asserting anything.
- [ ] 80% is too low; the target should have been 100%.
- [ ] Coverage tools count lines incorrectly.
- [ ] Teams deleted their old tests to make room for faster new ones.

**Why:** Coverage counts lines run, not behavior checked, so tests without assertions raise it cheaply. Goodhart's law: when a measure becomes a target, it ceases to be a good measure. See [[metric-fixation]].

## What makes metrics harder to game?

- [x] Pairing metrics that pull against each other.
- [ ] Tracking 40 metrics so no single number dominates.
- [ ] Ranking individuals by their output each month.
- [ ] Dropping measurement entirely in favor of judgment.

**Why:** Gaming one shows up in the other, as with deploy frequency and change failure rate. Too many metrics dilute attention, and dropping them all leaves you guessing. See [[metric-fixation]].

## When can a metric work as a target?

- [x] When it's close to the outcome, tightly defined, and audited.
- [ ] When it's simple enough to report upward to leadership as a single number.
- [ ] When it counts activity, such as commits or tickets closed.
- [ ] When engineers are rewarded individually for moving it.

**Why:** A latency budget is mostly moved by improving latency. Even so it gets gamed at the edges, so define it tightly (the slowest 1%, measured from the user's side) and audit how it's collected. See [[metric-fixation]].
