---
title: Hero Culture
category: antipatterns
summary: A team that depends on a few people to rescue it, which feels heroic but hides broken systems and leaves the team stuck when those people are away.
tags: [teams, knowledge-sharing, reliability]
---

# Hero Culture

> **In one sentence:** A team that depends on a few people to rescue it, which feels heroic but hides broken systems and leaves the team stuck when those people are away.

## The idea

Every team has someone who knows where everything is. They fix the outage at 2 a.m., know why the deploy script has that flag, and answer questions nobody else can. Hero culture is when the team comes to depend on that person instead of fixing the systems that keep needing them.

It's comfortable for everyone. The hero is valued and needed; the team ships; managers reward visible rescues. But each rescue hides a missing runbook, a confusing system, or an alert that should never have fired. The *bus factor* measures the risk: the number of people who would need to be unavailable before a project stalls. A bus factor of one means one vacation can halt the team. Gene Kim and colleagues' 2013 novel *The Phoenix Project* made the pattern famous through Brent, the engineer every crisis waits on.

## Why it matters

- **The hero becomes a bottleneck.** Work queues behind one person, so the team's speed is that person's speed.
- **Problems stay hidden.** When someone always saves the day, the system that needed saving never gets fixed ([[blameless-postmortems]]).
- **People burn out and leave.** Being on call for everything is exhausting. When the hero quits, their knowledge leaves with them.
- **Others stop growing.** Engineers who never handle the hard problems never learn to.

## How to apply it

- **Measure the bus factor.** For each critical system, ask "who else could debug this tonight?" Tools that count distinct recent committers per directory give a rough first answer.
- **Make the hero a teacher, not a fixer.** During incidents, the expert advises while someone else drives. It's slower the first few times and spreads knowledge every time.
- **Turn every rescue into a fix.** After each save, ask what change would mean nobody needs to be a hero next time: a runbook, a better alert, a simpler system.
- **Reward prevention, not just rescue.** Praise the engineer who removed a class of incidents as loudly as the one who fixed one at 2 a.m.
- **Rotate ownership.** Pair newer engineers on the hero's systems and rotate on-call so knowledge stays spread.

## Example

Priya is the only person who understands the payment reconciliation job. It fails roughly monthly, and she fixes it in an hour. The team sees this as fine — until she's on a two-week holiday, it fails, and two engineers spend three days on a fix she would have made in an hour.

When she's back, the team makes a change: next time it fails, someone else drives the fix and Priya only answers questions. The first time takes four hours instead of one. They write a runbook from those notes, and the second engineer adds an alert that names the usual cause.

The hard part is Priya's own reluctance. Fixing things fast is how she has earned respect, and being made a teacher feels like losing status. Her manager makes the shift explicit: her goal for the quarter is that two others can handle the job alone, and that's what her review will measure.

## Common traps

- **Blaming the hero.** Heroes are usually responding to a system that needs them. The fix is to the system and the incentives, not the person.
- **Writing docs nobody reads.** A wiki page written once and never tested is not knowledge transfer. Test it by having someone else follow it during a real failure.
- **Making everyone a generalist.** Deep expertise is valuable. The goal is that expertise isn't the *only* way to keep a system running.
- **Celebrating long hours.** Praising late-night saves in public tells everyone that's how to get noticed.

## When it doesn't apply

Small teams and early startups can't spread every piece of knowledge, and one person owning an area is normal. The point isn't zero dependency on anyone; it's knowing where your bus factor is one and choosing which of those risks you'll live with. A specialist in a rarely changed area is fine. A specialist on the critical path for every release is the risk worth fixing.

## Related

- [[blameless-postmortems]] — fix the system that made the rescue necessary.
- [[observability]] — systems that explain themselves need fewer heroes.
- [[influencing-without-authority]] — senior engineers lead by spreading knowledge.
- [[paved-roads]] — the easy, documented way replaces tribal knowledge.
- [[big-ball-of-mud]] — tangled systems are where heroes grow.
