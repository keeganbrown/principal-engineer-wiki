---
title: Blameless Postmortems
category: practices
summary: After an incident, study how the system and process allowed it to happen — not who to blame — so people share the full truth and the same failure doesn't repeat.
tags: [reliability, culture, learning]
---

# Blameless Postmortems

> **In one sentence:** After an incident, study how the system and process allowed it to happen — not who to blame — so people share the full truth and the same failure doesn't repeat.

## The idea

When something breaks in production, there's a natural urge to find the person who "caused" it. A blameless postmortem resists that. It assumes that everyone involved acted reasonably given what they knew, the tools they had, and the pressure they were under. The question isn't "who messed up?" but "**how did our system make this mistake easy and its impact large?**"

The approach comes from safety-critical fields like aviation and medicine. In software, it was popularized by Etsy (John Allspaw's 2012 writing on blameless postmortems) and by Google's Site Reliability Engineering (SRE) practice.

## Why it matters

- **Blame hides information.** If people fear punishment, they leave out details — and the details are where the real causes are.
- **"Human error" is a starting point, not a conclusion.** If one typo can take down production, the problem is the system that let one typo do that.
- **Learning compounds.** Teams that learn from every incident get steadily more reliable. Teams that blame repeat the same failures with different people.
- **Safety surfaces near-misses.** When people aren't afraid, they report near-misses — free lessons.

## How to apply it

- **Hold one for every significant incident.** Include interesting near-misses, and meet within a few days while memory is fresh.
- **Build a timeline first.** What happened, when, what people saw, and what they did — from logs, chat history, and dashboards ([[observability]]).
- **Ask "how" and "what," not "why did you."** "What did the dashboard show at that moment?" invites detail; "Why didn't you check?" invites defense.
- **Look for contributing factors, not one root cause.** Real incidents usually need several things to go wrong at once.
- **Write action items that change the system.** Think automation, safer defaults, removed hazards. "Be more careful" is not an action item.
- **Give every action item an owner and a due date.** Track them to completion.
- **Share widely.** Publish postmortems so other teams learn too.

A simple template: *Summary · Impact · Timeline · Contributing factors · What went well · What was hard · Action items.*

## Example

An engineer runs a cleanup script against the production database instead of staging and deletes customer data.

**Blameful conclusion:** "Engineer was careless. Reminded to double-check."

**Blameless analysis:** staging and production credentials were in the same file; the script had no confirmation prompt; the terminal looked identical for both environments; and backups had never been restore-tested, so recovery took six hours.

**Action items:** separate the credentials so the script *can't* reach production from a laptop (removes the hazard); color-code production shells; and run monthly restore drills. The team deliberately skips adding a manager approval step for every script — it would slow every normal day for a rare event. Now the mistake is much harder to make and much cheaper to recover from.

## Common traps

- **Blameless in name only.** If a manager uses the postmortem in a performance review, trust is gone.
- **Stopping at "human error."** Keep asking what made the error possible and costly.
- **Action items that never get done.** An untracked list is a ritual, not a fix.
- **Too many action items.** Prioritize the few that most reduce risk.
- **Process accretion.** Every postmortem adds an approval, a checklist, or a confirmation prompt, and over years the system gets slow and people learn to click through warnings. Prefer fixes that *remove* a hazard over fixes that *add friction*; every guardrail has a cost paid on every normal day.
- **Confusing blameless with accountability-free.** People are still accountable for participating honestly and following through on fixes.

## When it doesn't apply

Blamelessness covers honest mistakes, not deliberate misconduct or malicious acts — those are handled differently. Tiny incidents may need only a short note rather than a full meeting; scale the effort to the impact.

## Related

- [[observability]] — good telemetry makes the timeline accurate.
- [[technical-debt]] — postmortems often reveal debt that finally needs repaying.
- [[feature-flags]] — kill switches often appear as postmortem action items.
- [[influencing-without-authority]] — leading a blameless culture is a principal-engineer responsibility.
- [[hero-culture]] — every rescue hides a system that needs fixing.
