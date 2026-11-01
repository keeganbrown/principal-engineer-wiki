---
title: Influencing Without Authority
category: leadership
summary: Principal engineers rarely get to order anyone to do anything, so they lead by building trust, framing problems in terms others care about, and making the right path the easy one.
tags: [leadership, communication, staff-plus]
---

# Influencing Without Authority

> **In one sentence:** Principal engineers rarely get to order anyone to do anything, so they lead by building trust, framing problems in terms others care about, and making the right path the easy one.

## The idea

As a principal engineer, your scope spans many teams — but none of those teams report to you. You can't assign their work or set their priorities. Yet you're expected to steer technical direction across all of them.

The way you do that is **influence**: getting people to *want* to go in a direction because they understand and agree with it. Influence is built from three things:

- **Credibility** — a track record of being right, being honest when wrong, and delivering.
- **Relationships** — people trust and listen to those who've helped them before.
- **Clarity** — a well-framed problem and a clear proposal are persuasive on their own.

## Why it matters

The best technical idea is worthless if nobody adopts it. Many senior engineers stall because they're right but unconvincing — they win arguments and lose outcomes. At the principal level, your impact is measured less by the code you write and more by the decisions you shape across the organization.

## How to apply it

- **Start by listening.** Before proposing a change, understand each team's goals, constraints, and pain. People back solutions to problems *they* feel.
- **Frame in their terms.** To a product manager: faster delivery. To a director: risk and cost. To engineers: fewer pages at 3 a.m. Same proposal, different "why."
- **Write it down.** A clear design doc travels further than any meeting and lets people think on their own time.
- **Socialize before you decide.** Talk one-on-one with key stakeholders before the big review. No one should be surprised in the meeting.
- **Give credit generously** and share ownership. Ideas spread faster when others feel they co-own them.
- **Make the right thing the easy thing.** Paved roads — templates, libraries, linters, golden paths — beat mandates. If the good way is also the convenient way, adoption takes care of itself.
- **Pick your battles.** Spend your credibility on decisions that are high-impact and hard to reverse. Let small things go.
- **Disagree and commit.** When a decision goes the other way, say so once, clearly — then help it succeed.
- **Build sponsors.** Find leaders who care about the outcome and can provide the authority you don't have.

## Example

A principal engineer wants all services to adopt structured logging and trace IDs. A memo mandating it would be ignored.

Instead, they:
1. Interview on-call engineers and collect stories about painful incidents caused by missing logs.
2. Write a short design doc framing the problem as "incident time," with data from recent postmortems.
3. Build a drop-in logging library with one team that was eager for it, and measure their faster incident resolution.
4. Share that team's results at an engineering all-hands — with that team presenting.
5. Add the library to the service template so new services get it for free.

Within two quarters, most teams have adopted it — and nobody was ordered to.

## Common traps

- **Being right loudly.** Winning a debate in public often loses the person.
- **Borrowing authority** ("the VP wants this") too often. It works once and erodes your own credibility.
- **Influence by exhaustion** — out-arguing people until they give up. They'll comply, not commit.
- **Only influencing upward.** Trust from the engineers doing the work matters as much as trust from leadership.
- **Never building anything.** Credibility needs occasional proof that your ideas work in practice.

## When it doesn't apply

Some situations call for direct authority: security incidents, legal compliance, or an outage in progress. In those cases, be clear about who's deciding and why, then return to collaborative influence afterward. And if influence repeatedly fails on something critical, escalating through your sponsors is a legitimate, not a failed, move.

## Related

- [[design-docs]] — the primary tool for influence at scale.
- [[conways-law]] — changing architecture often means changing how teams work together.
- [[architecture-decision-records]] — makes decisions transparent so people can trust the process.
- [[blameless-postmortems]] — modeling blamelessness is a form of cultural influence.
