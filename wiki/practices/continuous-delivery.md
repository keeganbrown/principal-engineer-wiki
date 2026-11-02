---
title: Continuous Delivery (CD)
category: practices
summary: Keep the main branch always releasable and move every change to production through one automated pipeline in small batches, rolling each one out to a small slice of users before everyone.
tags: [delivery, release, ci, risk]
---

# Continuous Delivery (CD)

> **In one sentence:** Keep the main branch always releasable and move every change to production through one automated pipeline in small batches, rolling each one out to a small slice of users before everyone.

## The idea

Shipping is risky in proportion to how much changes at once. A release with forty changes has forty suspects when it breaks; a release with one has one. Continuous delivery makes releases small and routine by automating the path from commit to production. It builds on three related practices:

- **Continuous integration (CI)** — everyone merges small changes into the main branch at least daily, and an automated build and test run checks every merge.
- **Continuous delivery** — every change that passes the pipeline *could* go to production at the push of a button.
- **Continuous deployment** — it goes automatically, with no button.

**Trunk-based development** is the branching style that goes with it: branches live for hours or a day or two, then merge into main (the "trunk"), with unfinished work hidden behind [[feature-flags]]. The last step is **progressive delivery**: release to a small slice of traffic first (a **canary release**), compare it with the rest, then widen or roll back. Continuous integration comes from Extreme Programming (Kent Beck, late 1990s). Jez Humble and David Farley's *Continuous Delivery* (2010) named the wider practice, and James Governor of RedMonk coined "progressive delivery" in 2018.

## Why it matters

- **Small batches are easier to debug and undo.** One change per deploy means the cause of a failure is obvious, and rolling back loses little.
- **Integration pain shrinks when it's frequent.** Merging a day's work is easy; merging a month-old branch is a project.
- **Speed and stability tend to go together.** The DevOps Research and Assessment (DORA) surveys, summarized in *Accelerate* (Forsgren, Humble, and Kim, 2018), found that teams deploying more often also tended to have fewer failed changes. That's a correlation from self-reported surveys, so it doesn't prove that deploying more makes you stabler, but it does show the assumed trade-off isn't inevitable.
- **Canaries limit the damage.** A bad change reaches a few percent of users for minutes, not everyone for an hour.

## How to apply it

- **Treat a red main branch as the team's top priority.** Fix it within minutes or revert the change. A main branch that's often broken can't be released, and people stop trusting it.
- **Merge small changes at least daily.** Hide unfinished work behind flags rather than on long branches.
- **Keep the pipeline fast.** If the commit checks take much more than ten minutes, people batch their changes to avoid waiting ([[testing-pyramid]]).
- **Build once, then promote the same artifact.** The package you tested is the package you deploy; only configuration differs between environments.
- **Make deploy and rollback one command each, and use both often.** A rollback path nobody exercises won't work when needed. Database changes must keep working with the previous version of the code, or rollback breaks ([[expand-and-contract]]).
- **Roll out in steps, with automatic checks.** Send a canary 1–5% of traffic (or one region), compare its error rate and latency with the rest for a set time, then widen in steps, rolling back automatically if the canary does worse. A canary has limits: at low traffic it may see too few requests to show a difference, it can't catch problems that appear only at full load or after hours (a slow memory leak, a nightly job), and old and new versions must run side by side safely.
- **Pause risky deploys when reliability is low.** When the error budget is spent, ship fixes, not features ([[service-level-objectives]]).

## Example

A team of eight releases its monolith every two weeks. Release day takes an afternoon, each release carries about 40 changes, and when one breaks, finding which change did it takes hours.

Over a quarter they cut the pipeline from 40 minutes to 12, switch to daily merges behind flags, and script the deploy. Then they add a canary: 5% of traffic for 20 minutes, with automatic rollback if errors or latency rise. They now deploy several times a day, and most failed changes are caught on the canary.

It wasn't smooth. Twice in the first month the canary rolled back healthy changes because the baseline was noisy at night, so they set a minimum request count before judging. One schema change couldn't be rolled back and had to be redone in expand-and-contract steps. Flags piled up until cleanup became part of each feature's definition of done. The cost was about one and a half engineers for a quarter.

## Common traps

- **Continuous integration in name only.** Running a build server on month-long feature branches still integrates late.
- **Living with a red build.** Once failures are normal, nobody notices the one that matters.
- **Approval boards that rubber-stamp.** A weekly board approving 40 changes adds days of delay without reading them. In the DORA surveys, approval by people outside the team was linked with slower delivery and showed no link to fewer failures; prefer peer review and automated checks ([[code-review]]).
- **Canaries judged by eye.** Someone glancing at a dashboard misses a 2% error rise. Compare canary and baseline numerically.
- **Deploying fast without seeing the result.** Frequent deploys are only safe with telemetry that shows what each one did ([[observability]]).

## When it doesn't apply

Software that users install — mobile apps behind app-store review, firmware, on-premises products — can't be deployed continuously. Still integrate continuously and keep main releasable, then release on a cadence. Regulated environments may require approvals; automate the evidence (who reviewed, which tests passed) rather than removing the gate. And a service with very little traffic gets little from canaries, so roll out customer by customer, or deploy plainly and keep rollback fast.

## Related

- [[feature-flags]] — hide unfinished work and separate deploying from releasing.
- [[testing-pyramid]] — what keeps the pipeline fast and trustworthy.
- [[expand-and-contract]] — schema changes that keep rollback possible.
- [[service-level-objectives]] — when the error budget is spent, slow down.
- [[load-balancers-and-cdns]] — rolling and blue-green deploys at the traffic layer.
