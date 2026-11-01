---
title: Conway's Law
category: principles
summary: Systems end up shaped like the communication structure of the teams that build them, so design your teams and your architecture together.
tags: [organization, architecture, teams]
---

# Conway's Law

> **In one sentence:** Systems end up shaped like the communication structure of the teams that build them, so design your teams and your architecture together.

## The idea

Where teams talk easily, their components integrate tightly. Where teams rarely talk, you get a boundary — an API, a file handoff, or a wall. Over time, the system's structure comes to mirror the org chart.

Eric Raymond's well-known paraphrase: "If you have four groups working on a compiler, you'll get a four-pass compiler" — a compiler built in four separate stages, one per group.

This isn't a rule you choose to follow. It's a force, like gravity. You can only choose whether to work with it.

Melvin Conway made the argument in his 1968 paper "How Do Committees Invent?". He later summarized it as: "Any organization that designs a system (defined broadly) will produce a design whose structure is a copy of the organization's communication structure."

## Why it matters

Architecture problems are often **organization problems in disguise**:

- A service that every team must change for every feature usually reflects a missing team boundary.
- Two services that are constantly out of sync often belong to two teams that don't talk.
- A planned architecture that contradicts the org chart will quietly drift back toward the org chart.

## How to apply it

- **Use the inverse Conway maneuver.** Decide the architecture you want, then shape teams to match it. (Jonny LeRoy and Matt Simons named it in 2010; ThoughtWorks' Technology Radar spread it.)
- **Align most teams to domains.** Teams that own checkout, search, or payments end to end ship features without hand-offs. Teams split by technical layer (frontend, backend, database administration) force every feature through several queues.
- **Make ownership explicit.** Every service, repo, and on-call rotation should have exactly one owning team.
- **Mind team cognitive load.** A team can only own so much. If it owns too many systems, boundaries rot. Skelton and Pais's *Team Topologies* (2019) is the standard reference here.
- **Trace messy code boundaries to people.** When an interface between two components is a mess, look at the communication path between the teams that own them.

## Example

A company has a frontend team, a backend team, and a database team. Every feature needs all three, so every feature needs three backlogs, three priorities, and two hand-offs. The API between frontend and backend becomes a giant, chatty contract that changes weekly.

They reorganize into domain teams — Search, Checkout, Accounts — each with frontend, backend, and data skills. Within months, each domain's code becomes more self-contained, and cross-team APIs shrink to what the domains actually share.

It isn't free: the database experts are now spread thin across three teams, and schema quality starts to slip.

Shared infrastructure that the old DBA team ran has no obvious owner. The company responds by forming a small platform team for shared databases and standards. Domain teams trade hand-off cost for some duplication and thinner specialist depth — usually a good trade, but a trade.

## Common traps

- **Reorgs as a silver bullet.** Moving people without changing ownership, incentives, or architecture just reshuffles the problem.
- **Ignoring the law during design reviews.** A beautiful service diagram that needs five teams to coordinate on every change won't stay beautiful.
- **Too many tiny teams.** Very small teams owning very small services can create more coordination, not less.

## When it doesn't apply

For a single small team, the law has little bite — everyone talks to everyone.

More importantly, not every team should be a domain team. Platform teams and deep-specialty teams (security, search ranking, data infrastructure) are legitimate where expertise is scarce or a capability is shared by everyone. The goal is fewer hand-offs on the common path, not organizational purity.

## Related

- [[coupling-and-cohesion]] — team boundaries become coupling boundaries.
- [[domain-driven-design]] — bounded contexts give teams natural ownership boundaries.
- [[microservices]] — service boundaries that don't match teams need constant coordination.
- [[modular-monolith]] — module ownership lets multiple teams share one deployable.
- [[influencing-without-authority]] — reshaping team boundaries is mostly persuasion.
- [[architecture-decision-records]] — let teams that rarely talk read each other's decisions and reasons.
