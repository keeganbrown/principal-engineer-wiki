---
title: Service Level Objectives (SLOs)
category: practices
summary: Set a reliability target based on what users notice, measure it, and treat the gap between the target and perfect as an error budget you spend on change — and stop spending when it runs out.
tags: [reliability, operations, sre, staff-plus]
---

# Service Level Objectives (SLOs)

> **In one sentence:** Set a reliability target based on what users notice, measure it, and treat the gap between the target and perfect as an error budget you spend on change — and stop spending when it runs out.

## The idea

"How reliable should this be?" usually gets the answer "as reliable as possible." That can't be measured, can't be achieved, and quietly blocks every risky change. A service level objective replaces it with a number users would actually notice. Three terms, from narrowest to widest:

- **Service level indicator (SLI)** — what you measure, as good events over all events. For example, the share of checkout requests that succeed in under one second.
- **Service level objective (SLO)** — the target for that indicator over a time window: 99.9% of checkouts are good, over 28 days.
- **Service level agreement (SLA)** — a promise to customers with a penalty, such as refunds, if it's broken. Keep it looser than the SLO, so you hear about trouble before it costs money.

The gap between the SLO and 100% is the **error budget**. At 99.9% over 30 days, that's 0.1% of requests, or about 43 minutes of full outage. The budget is meant to be spent on deploys, experiments, and migrations; when it runs out, reliability work comes first until it recovers. The approach comes from Google's *Site Reliability Engineering* (2016) and *The Site Reliability Workbook* (2018).

## Why it matters

- **Perfect is the wrong target.** Each extra nine costs far more in redundancy and slower releases, while users' own phones and Wi-Fi fail more often than a 99.99% service does. Past a point, nobody notices the extra reliability you paid for.
- **It settles the features-versus-reliability argument in advance.** Product and engineering agree once, calmly, what happens when the budget is spent, instead of arguing during every incident.
- **It gives alerts a reason to exist.** You page when the budget is burning fast, not when a single server sneezes ([[observability]]).
- **It covers only what it measures.** An SLO says nothing about failures its indicator can't see, so choosing the indicator is most of the work.

## How to apply it

- **Start from what users notice.** Pick the few journeys that matter (log in, search, check out) and measure them as close to the user as you can: at the load balancer, or from the client. Server-side success rates miss requests that never arrived.
- **Define good and valid events precisely.** "Responses that aren't server errors and arrive within one second, divided by all requests except health checks and bots." Decide upfront whether client errors such as 404s count.
- **Set the target from history, not ambition.** Look at the last few months and set the SLO a little below what you achieved while users were content. Tighten it if users complain while you're meeting it.
- **Write the error budget policy before you need it.** Agree with the product owner what happens at 50% spent and at 100% (for example, a freeze on feature launches, with reliability and security fixes still allowed), and who can grant exceptions. Without an agreed policy, the budget is just a dashboard.
- **Alert on burn rate, not on every error.** **Burn rate** is how fast you're spending the budget; a burn rate of 1 uses exactly the budget over the window. The *Workbook* suggests paging when an hour's burn rate passes 14.4, which spends 2% of a 30-day budget in one hour, and opening a ticket for slow burns.
- **Don't promise more than your dependencies give.** If a request needs three services that each meet 99.9%, the chain is closer to 99.7%. Either add fallbacks or set a looser target.
- **Review SLOs every quarter.** Compare breaches with user complaints. If users complained while you met the SLO, the indicator is measuring the wrong thing.

## Example

A payments team sets a checkout SLO: 99.9% of checkout requests succeed in under two seconds over 28 days, measured at the load balancer. The policy, agreed with the product lead, says: below 25% budget left, every deploy needs a rollout plan with a canary; at zero, feature launches pause until the budget recovers.

Mid-month, a bad configuration change spends 60% of the budget in 40 minutes, and the burn-rate alert pages within five minutes. Two smaller incidents empty the budget a week later. The team spends the freeze adding automatic rollback to its deploy pipeline ([[continuous-delivery]]).

The hard part was the marketing launch scheduled inside the freeze. The policy named the vice president of engineering as the person who grants exceptions, so the argument took one meeting: the launch went ahead behind a [[feature-flags|feature flag]] at 5% of users, and the rest waited a week. The SLO also missed something: a bug that charged a few customers twice returned fast successes, so the team added a correctness check on payment totals.

## Common traps

- **Too many SLOs.** Twenty per service means nobody watches any of them. Start with one or two per user journey.
- **A budget with no consequences.** If an empty budget changes nothing, everyone learns the SLO is decoration.
- **Measuring what's easy instead of what users feel.** Host uptime and CPU tell you about machines, not about whether people can check out.
- **Fast, wrong answers count as good.** Wrong totals and duplicate charges look like successes. Add a correctness check where it matters.
- **Turning the SLO into a performance score.** Once teams are judged on it, incidents get reclassified and windows redefined ([[metric-fixation]]). Use it to make decisions, not to rank teams.

## When it doesn't apply

A young product with little traffic gains little: at a hundred requests a day, one failure is a 1% swing, and a couple of alerts on user-facing errors are enough. Batch jobs and data pipelines need different indicators, such as freshness (how old is the newest data?) and completeness, not request success rates. And if leadership won't honor the policy, an SLO is still useful for reporting, but say plainly that it isn't driving decisions yet.

## Related

- [[observability]] — the telemetry SLIs are built from, and which alerts should page.
- [[incident-response]] — what happens when the burn-rate alert fires.
- [[continuous-delivery]] — where an empty budget pauses risky deploys.
- [[metric-fixation]] — what happens when the SLO becomes a target for people.
- [[architecture-trade-offs]] — availability is one quality attribute among several.
