# Quiz: Continuous Delivery (CD)

## A team runs a build server on every branch, but feature branches live for a month before merging. Are they practicing continuous integration?

- [x] Not really; integration still happens late, when the branches finally merge.
- [ ] Yes; any team running automated builds on every push is doing it already.
- [ ] Yes, as long as every branch's build stays green before it gets merged.
- [ ] No, because continuous integration requires deploying automatically too.

**Why:** Continuous integration means merging small changes into main at least daily. A build server on month-long branches still integrates late. Deploying automatically is continuous deployment, a separate step. See [[continuous-delivery]].

## A canary at 5% of traffic is judged by an engineer glancing at a dashboard for a few minutes. What is the main risk?

- [x] A small rise in errors gets missed without a numeric comparison to baseline.
- [ ] Canaries should always start at 50% of traffic to give a fair comparison.
- [ ] Canaries can't catch any problems at all, so the step should be dropped.
- [ ] A dashboard is fine as long as the engineer watching is very experienced.

**Why:** Compare the canary's error rate and latency with the rest of traffic numerically, and roll back automatically if it does worse. Eyeballing misses a 2% error rise. See [[continuous-delivery]].

## A team wants fast rollback, but some deploys change the database schema. What keeps rollback safe?

- [x] Making each schema change work with the previous code version, step by step.
- [ ] Taking a database backup before every deploy and restoring it on rollback.
- [ ] Avoiding all schema changes until the next quarterly maintenance window.
- [ ] Rolling back only the code and fixing any database errors by hand later.

**Why:** Database changes must keep working with the previous version of the code, or rollback breaks; expand-and-contract does that in steps. Restoring a backup loses everything written since. See [[continuous-delivery]] and [[expand-and-contract]].

## A team ships a mobile app that goes through app-store review. Should they adopt continuous deployment?

- [x] They can't deploy continuously, but should still integrate continuously.
- [ ] Yes; push every merged change to the store as soon as it passes its checks.
- [ ] No; mobile teams gain nothing from continuous integration either.
- [ ] Yes, as long as they add a canary at 1% of app-store downloads.

**Why:** Software users install, like mobile apps behind store review, can't be deployed continuously. Keep integrating continuously and keep main releasable, then release on a cadence. See [[continuous-delivery]].
