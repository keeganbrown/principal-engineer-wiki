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

This approach comes from safety-critical fields like aviation and medicine, and was popularized in software by companies like Etsy and Google's SRE practice.

## Why it matters

- **Blame hides information.** If people fear punishment, they leave out details — and the details are where the real causes are.
- **"Human error" is a starting point, not a conclusion.** If one typo can take down production, the problem is the system that let one typo do that.
- **Learning compounds.** Teams that learn from every incident get steadily more reliable. Teams that blame repeat the same failures with different people.
- **Psychological safety** makes people report near-misses, which are free lessons.

## How to apply it

- **Hold one for every significant incident** (and interesting near-misses), within a few days while memory is fresh.
- **Build a timeline first.** What happened, when, what people saw, and what they did — using logs, chat history, and dashboards.
- **Ask "how" and "what," not "why did you."** "What did the dashboard show at that moment?" invites detail; "Why didn't you check?" invites defense.
- **Look for contributing factors, not one root cause.** Real incidents usually need several things to go wrong at once.
- **Write action items that change the system**: automation, guardrails, alerts, better defaults. "Be more careful" is not an action item.
- **Give every action item an owner and a due date,** and track them to completion.
- **Share widely.** Publish postmortems so other teams learn too.

A simple template: *Summary · Impact · Timeline · Contributing factors · What went well · What was hard · Action items.*

## Example

An engineer runs a cleanup script against the production database instead of staging and deletes customer data.

**Blameful conclusion:** "Engineer was careless. Reminded to double-check."

**Blameless analysis:** the staging and production credentials were in the same file; the script had no confirmation prompt; the terminal prompt looked identical for both environments; and backups had never been restore-tested, so recovery took six hours. **Action items:** separate credentials, require typed confirmation for destructive production commands, color-code production shells, and run monthly restore drills. Now *nobody* can make that mistake easily again.

## Common traps

- **Blameless in name only.** If a manager uses the postmortem in a performance review, trust is gone.
- **Stopping at "human error."** Keep asking what made the error possible and costly.
- **Action items that never get done.** An untracked list is a ritual, not a fix.
- **Too many action items.** Prioritize the few that most reduce risk.
- **Blameless doesn't mean accountability-free.** People are still accountable for participating honestly and following through on fixes.

## When it doesn't apply

Blamelessness covers honest mistakes, not deliberate misconduct or malicious acts — those are handled differently. Tiny incidents may need only a short note rather than a full meeting; scale the effort to the impact.

## Related

- [[observability]] — good telemetry makes the timeline accurate.
- [[technical-debt]] — postmortems often reveal debt that finally needs repaying.
- [[feature-flags]] — kill switches often appear as postmortem action items.
- [[influencing-without-authority]] — leading a blameless culture is a principal-engineer responsibility.
