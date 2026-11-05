# Quiz: Feature Flags

## What is the difference between deploying and releasing?

- [x] Deploying puts code on servers; releasing turns behavior on for users.
- [ ] Deploying is reversible in seconds; releasing can't be undone at all.
- [ ] Deploying happens daily; releasing happens only at the end of a quarter.
- [ ] They are the same step, named differently by different teams.

**Why:** Flags separate the two, so code can be merged and deployed hidden behind a flag, then released gradually or turned off fast. See [[feature-flags]].

## A feature-flagged rollout at 5% of users shows flat errors but latency up 30%. What should you do?

- [x] Turn the flag off, fix the cause, and roll out again.
- [ ] Push to 100% quickly so the latency averages out.
- [ ] Leave it at 5% indefinitely and move on to other work.
- [ ] Wait a week at 5% to see whether latency recovers.

**Why:** Watch each step and act on it: flipping a flag off takes seconds, so fix the cause before rolling out again. See [[feature-flags]].

## The flag service is unreachable and there's no cached value. What should a permission flag default to?

- [x] Access denied; never fail open.
- [ ] Access granted, so users aren't blocked.
- [ ] Whatever the flag was set to yesterday.
- [ ] The new path, since it's the one being tested.

**Why:** Granting access because the check couldn't run would fail open. A release flag falls back to the old path, and a kill switch to the feature still running. See [[feature-flags]].

## Which practice best prevents flag debt?

- [x] Giving every release flag an owner and an expiry date.
- [ ] Reusing old flag names for new features to keep the list short.
- [ ] Nesting new flags inside existing ones so they're grouped.
- [ ] Keeping every flag forever in case you need to roll back.

**Why:** Release flags should be deleted once the rollout is done. Reused names can switch on old behavior by surprise, and nested flags multiply the states to test. See [[feature-flags]].

## You're fixing a typo in a help-page string. Should the change go behind a release flag?

- [x] Not usually; for a tiny, low-risk change the flag costs more than it saves.
- [ ] Yes; every change should ship behind a flag so it can be turned off.
- [ ] Yes, and roll it out to 1% of users first to watch the metrics.
- [ ] No; flags are only for changes to the database schema.

**Why:** Tiny, low-risk changes don't need a flag; the overhead isn't worth it. Flags pay off for risky or unfinished work. See [[feature-flags]].
