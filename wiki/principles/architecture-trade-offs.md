---
title: Evaluating Architecture Trade-offs
category: principles
summary: There is no best architecture, only the best fit for what matters most here — so rank the qualities you need, compare real options by what each one costs, and write down what would make you change your mind.
tags: [architecture, decision-making, judgment, trade-offs, staff-plus]
---

# Evaluating Architecture Trade-offs

> **In one sentence:** There is no best architecture, only the best fit for what matters most here — so rank the qualities you need, compare real options by what each one costs, and write down what would make you change your mind.

## The idea

Every design choice buys some things by giving up others. A cache buys speed and pays in staleness. Splitting into services buys independent deploys and pays in network failures and operational work. A single database buys simple transactions and pays when one team's load slows everyone else.

So "Is this a good design?" has no answer on its own. The useful question is "Good *for what*, and at what cost?" The *for what* is a short list of **quality attributes**: the properties the system must have, such as latency, availability, cost, security, or how fast teams can ship changes. Which ones matter, and in what order, differs from system to system — that's what "it depends" depends on.

Mark Richards and Neal Ford call this the first law of software architecture: everything is a trade-off, and if you think you've found one that isn't, you haven't found the trade-off yet. The Software Engineering Institute's Architecture Tradeoff Analysis Method (ATAM) turned the same idea into a formal review around 2000.

## Why it matters

- **Unstated costs get paid anyway.** A team that picks an option for its benefits discovers the costs in production, when they're most expensive.
- **Disagreements become arguments about values in disguise.** Two engineers arguing about an event bus are often ranking flexibility and simplicity differently. Naming the ranking turns a stalemate into a decision someone can make.
- **Context changes, and the reasoning should survive it.** A choice made with its conditions written down can be revisited when those conditions change, instead of defended or abandoned on instinct.

## How to apply it

- **Rank the two or three qualities that matter most.** Rank them, don't list them. If availability, cost, and delivery speed are all "top priority," nothing is, and the decision will be made by whoever argues longest. Get the ranking from the people who own the outcome, not only from engineers.
- **Write down the constraints.** Team size and skills, deadline, budget, regulation, expected scale, and what already exists. Use real numbers: "10,000 orders a day, growing 20% a year" settles questions that "it needs to scale" never will.
- **Compare at least two real options, and include staying put.** The current design, maybe improved, is always an option. If there's only one candidate, you're justifying a decision, not making one.
- **For each option, name what it gives up.** Give the costs the same detail as the benefits: operational load, failure modes, learning curve, what gets harder later.
- **Say what would have to be true for each option to win.** "Services win if we grow past five teams" turns a debate about the future into a condition you can check. It also tells you when to revisit.
- **Weigh the cost of being wrong.** A choice that's cheap to undo deserves a quick decision; one that locks you in deserves the full analysis ([[reversible-decisions]]). When the evidence is thin either way, lean toward the simpler, more reversible option ([[kiss]]).
- **Record the decision and the options you rejected.** An architecture decision record (ADR) keeps the ranking, the costs, and the revisit conditions after the people move on ([[architecture-decision-records]]).

## Example

A 12-engineer company runs one monolith. Deploys take an hour and often break, and three product teams wait on each other. A senior engineer proposes microservices.

The principal engineer asks the product leads and the engineering manager to rank what matters. They agree on: (1) teams shipping without waiting on each other, (2) checkout staying up, (3) not adding headcount for operations. Constraints: no platform team, modest traffic, and a deadline in two quarters.

| Option | Gives | Costs | Wins if |
| --- | --- | --- | --- |
| Keep the monolith, fix the pipeline | Fastest to do; nothing new to run | Teams still share one deploy | The waiting is mostly the slow pipeline |
| [[modular-monolith]] with enforced boundaries | Teams own modules; one thing to deploy and operate | Boundary work; deploys stay shared | Teams mostly collide in the code, not in production |
| Extract services ([[microservices]]) | Independent deploys and scaling | Network failures, a platform to run, new skills | There are more teams and a group to run the platform |

The table makes the disagreement visible: the proposer ranked independent scaling first, which nobody else did. The team chooses the modular monolith plus pipeline fixes. Their ADR records the rejected options and a trigger: "revisit services if we pass five product teams or checkout needs to scale separately."

The hard part was the ranking, not the table: it took two meetings, and the proposer still disagreed, which the ADR notes. The cost was about four days of senior time before any code changed — worth it for a choice this hard to reverse, and far too much for choosing a logging library.

## Common traps

- **Weighing only benefits.** A comparison where one column lists advantages and the other lists risks of the alternatives is a sales pitch.
- **Designing for scale you don't have.** Real numbers beat imagined ones; plan for the next order of magnitude, not the fourth ([[yagni]]).
- **Choosing by fashion or familiarity.** "Everyone's doing it" and "we always use it" skip the question of fit ([[cargo-cult-engineering]], [[golden-hammer]]).
- **The scoring matrix that hides the decision.** Weighted scores give false precision, and weights get tuned until the favorite wins. Use the table to expose costs, then decide and say why in words.
- **"It depends" with no follow-up.** "It depends" is a starting point. Say what it depends on, then decide.
- **Re-arguing settled trade-offs.** If the conditions haven't changed, the decision stands. Point at the ADR.

## When it doesn't apply

For choices that are cheap to undo, the analysis costs more than a mistake: pick one, try it, and switch if it's wrong. Some trade-offs are already settled for you — a regulation, a company standard ([[paved-roads]]), or a platform you can't leave — so don't relitigate them in every design. And a trade-off table can't create information you don't have; when the key unknown is "will this even work?", a small prototype answers faster than a meeting.

## Related

- [[reversible-decisions]] — how much analysis a decision deserves.
- [[design-docs]] — where the comparison gets written and reviewed.
- [[architecture-decision-records]] — where the choice, the rejected options, and the revisit trigger live.
- [[cap-theorem]] — a trade-off you can't design away, only choose.
- [[kiss]] — the tie-breaker when the evidence is thin.
- [[golden-hammer]] — what happens when the trade-off step gets skipped.
