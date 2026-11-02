---
title: Metric Fixation
category: antipatterns
summary: Turning a useful measurement into a target, so people optimize the number instead of the outcome it was meant to show.
tags: [metrics, incentives, teams]
---

# Metric Fixation

> **In one sentence:** Turning a useful measurement into a target, so people optimize the number instead of the outcome it was meant to show.

## The idea

A number is a proxy: test coverage stands in for "well-tested code," tickets closed stands in for "progress," uptime stands in for "users can rely on us." Proxies are useful while nobody is rewarded for moving them. Once they become targets, people find the cheapest way to move the number, which is often not the way that improves the outcome.

The principle is *Goodhart's law*: "When a measure becomes a target, it ceases to be a good measure." That phrasing is anthropologist Marilyn Strathern's (1997), generalizing a 1975 point by economist Charles Goodhart about monetary-policy statistics. The historian Jerry Muller named the wider habit "metric fixation" in his 2018 book *The Tyranny of Metrics*.

## Why it matters

- **The number improves while the outcome doesn't.** Coverage reaches 90% with tests that assert nothing ([[testing-pyramid]]).
- **People game it, often without meaning to.** Engineers split one change into five pull requests (PRs) to raise a PR count, or close tickets and open new ones.
- **The metric loses its value as a signal.** A gamed number no longer tells you anything, even to the people who want to use it honestly.
- **What isn't measured gets ignored.** Effort flows to whatever is counted. Mentoring, documentation, and design rarely are.

## How to apply it

Spotting it:

- **The number moves but the outcome doesn't.** Coverage is up and incidents aren't down; velocity is up and customers see nothing new.
- **People talk about hitting the number, not the goal.** "We need two more points this sprint" is a target talking.
- **Definitions start to shift.** Bugs get relabeled as feature requests; incidents get split or merged to fit a count.

Climbing out:

- **Measure outcomes, not activity.** Lead time (commit to production), change failure rate (the share of deploys that cause a failure), and recovery time say more than lines of code or commits. These are three of the DevOps Research and Assessment (DORA) delivery metrics ([[adopting-coding-agents]]). They can be gamed too — empty deploys, relabeled failures — which is why the next step pairs them.
- **Pair metrics that pull against each other.** Deployment frequency alongside change failure rate; speed alongside quality. Gaming one shows up in the other.
- **Use metrics to ask questions, not to grade people.** A drop in a team's numbers is a reason for a conversation, not a performance rating.
- **Never rank individuals by an output metric.** Software is a team activity; individual counts reward the wrong behavior and punish helping others.
- **Review the metrics themselves.** Every few months, ask: is this still telling us what we thought? Has anyone found a way around it?

## Example

An engineering director sets a target of 80% test coverage for every service by the end of the quarter. Most teams hit it. Incidents don't go down.

A review of the new tests shows why. Many call functions without checking results; some catch every exception, so the test passes even when the code crashes. The number measured lines executed, and the cheapest way to execute lines was to run them without asserting anything.

The director drops the target and keeps coverage as a team-level signal, paired with escaped defects (bugs found after release). Teams instead pick their two riskiest modules and test those thoroughly. Escaped defects can be gamed too, by reclassifying bugs, so a lead reviews a sample each month. The hard part is that leadership wanted one number to report upward; the team reports the paired signal anyway, with a sentence of context, because a reportable number that means nothing is worse than none.

## Common traps

- **Dropping measurement altogether.** Without numbers, decisions run on anecdote and the loudest voice. The fix is better metrics, used carefully, not none.
- **Adding more metrics to stop gaming.** A dashboard of 40 numbers is ignored or gamed 40 ways. Choose a few that matter.
- **Blaming people for gaming.** If the incentive rewards the number, people will move the number. Change the incentive.
- **Measuring what's easy instead of what matters.** Commits are easy to count; customer value isn't. That's not a reason to count commits.

## When it doesn't apply

Some metrics hold up better as targets because the number and the outcome are close to the same thing. A latency budget (say, the page must load in under two seconds), an error budget (the amount of failure a reliability target allows), or a cost ceiling for a cloud account is mostly moved by improving the thing measured.

Even these get gamed at the edges: averages instead of slow-request percentiles, timeouts left out of the count, spend moved to another account. They work as targets only when the measurement is defined tightly — the slowest 1% of requests, measured from the user's side — and someone audits how it's collected.

## Related

- [[adopting-coding-agents]] — measuring the impact of coding agents without rewarding volume.
- [[observability]] — metrics used as signals to investigate, not targets to hit.
- [[technical-debt]] — the unmeasured cost that metric targets often grow.
- [[cargo-cult-engineering]] — copying another company's metrics without their context.
- [[testing-pyramid]] — what good test coverage actually looks like.
