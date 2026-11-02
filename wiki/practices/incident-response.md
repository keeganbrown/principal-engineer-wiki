---
title: Incident Response
category: practices
summary: When production breaks, declare an incident early, put one person in charge of coordinating, restore service before hunting for the cause, and update people on a fixed schedule.
tags: [reliability, operations, on-call, staff-plus]
---

# Incident Response

> **In one sentence:** When production breaks, declare an incident early, put one person in charge of coordinating, restore service before hunting for the cause, and update people on a fixed schedule.

## The idea

An **incident** is an unplanned event that is hurting users, or about to, and needs a coordinated response now. Incident response is the agreed playbook for the first minutes and hours. Most incidents that go badly fail at coordination, not at debugging: five engineers chase the same log line, two of them make conflicting changes, and nobody tells support what's happening.

The fix is a few roles, each held by a named person:

- **Incident commander** — coordinates and decides. Keeps the overall picture, assigns work, and calls for rollbacks. Doesn't debug.
- **Operations lead** — the people investigating and changing the system.
- **Communications lead** — updates stakeholders and the status page on a schedule.
- **Scribe** — keeps a timestamped log of what was seen, decided, and done.

In a small incident one person may hold several roles, but someone always says out loud that they are the commander. The roles are adapted from the Incident Command System, which emergency services in California developed in the 1970s for coordinating crews at wildfires. Google's *Site Reliability Engineering* (2016) describes its use for software.

## Why it matters

- **Time to restore is what users feel.** A clear process can cut an hour of confusion to minutes, and a fast rollback often matters more than a fast diagnosis.
- **Silence costs trust.** Customers and executives fill silence with the worst case. Regular updates, even "no news yet," buy the responders room to work.
- **The record feeds learning.** A timeline written during the incident makes the postmortem accurate instead of reconstructed from memory ([[blameless-postmortems]]).

## How to apply it

- **Make declaring cheap.** Anyone can declare, and nobody is criticized for declaring something that turns out minor. Downgrading costs a message; declaring late costs the first half hour. Set clear triggers too: a [[service-level-objectives|service level objective]] burning its error budget fast, customer data at risk, or a suspected security breach.
- **Define severity by user impact.** For example, severity 1: many users can't do a core task, or data is lost or exposed; severity 2: a feature is degraded or some users are affected; severity 3: minor, with a workaround. Severity decides who gets paged and how often you update.
- **Keep the commander out of the logs.** If the commander needs to debug, they hand the role to someone else first, out loud.
- **Mitigate first, diagnose later.** Roll back the last deploy, turn off the [[feature-flags|feature flag]], fail over, or shed load. The root cause can wait until users are unblocked. Rollback isn't always safe, though: a deploy that changed the database schema or wrote data in a new format may not roll back cleanly unless it followed [[expand-and-contract]]. Know before deploying which changes can be undone.
- **Update on a clock.** For the worst incidents, every 30 minutes: what's affected, what you're doing, and when the next update comes. Use one channel for responders and another for everyone else.
- **End it explicitly.** Declare it resolved, list follow-ups with owners, and schedule the postmortem.
- **Keep on-call sustainable.** Spread the rotation so nobody is paged most weeks, compensate it, and track pages per shift. A rotation that pages every night burns people out and concentrates knowledge in one person ([[hero-culture]]).
- **Practice when nothing is broken.** Game days (planned drills with a simulated failure) test the runbooks and give newer engineers a turn as commander.

## Example

At 14:02 a burn-rate alert fires on checkout. The on-call engineer declares a severity 2 incident and takes the commander role; two engineers investigate, and a support lead takes communications. A deploy went out at 13:50, so at 14:10 the commander orders a rollback, which is safe because that deploy's schema change was additive.

Errors don't drop: the deploy wasn't the cause. That's the hard moment, when everyone wants to dig into code. The commander instead asks what else changed, and an engineer finds that the payment provider is degraded in one region. At 14:31 the team uses an existing kill switch to route payments to the backup provider, and errors fall.

Updates went out at 14:15 and 14:45, and the incident closed at 15:05 after half an hour of stable graphs. The costs: about 3% of checkouts failed, the backup provider charges higher fees, and the first rollback spent ten minutes on a wrong guess. The postmortem adds the provider's status to the checkout dashboard.

## Common traps

- **The commander starts debugging.** Nobody is coordinating, and changes start colliding.
- **Hunting the root cause while users wait.** An elegant diagnosis an hour later is worse than a crude rollback now.
- **A channel full of spectators.** Status questions interrupt responders. Point onlookers at the stakeholder channel.
- **Severity drift.** If everything is severity 1, pages stop meaning anything; if declaring feels risky, incidents start late.
- **Follow-ups nobody owns.** Action items without an owner and a date don't happen, and the same incident returns.

## When it doesn't apply

A team of three running one service doesn't need four named roles, but it still needs one person saying "I'm coordinating" and a habit of posting updates. Minor problems, like a broken internal dashboard, are cheaper to handle as a normal ticket than as an incident. Security incidents and data breaches need more than this playbook: bring in security and legal early, because evidence must be preserved and notification deadlines may apply.

## Related

- [[blameless-postmortems]] — the learning that happens after the incident ends.
- [[service-level-objectives]] — burn-rate alerts are a good trigger for declaring.
- [[observability]] — the telemetry responders use to see what's wrong.
- [[feature-flags]] — kill switches turn many incidents into a quick flip.
- [[hero-culture]] — what happens when one person handles every incident.
