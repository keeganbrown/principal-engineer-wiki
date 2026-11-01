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

**Before proposing:**
- **Start by listening.** Understand each team's goals, constraints, and pain. People back solutions to problems *they* feel.
- **Frame it in their terms.** To a product manager: faster delivery. To a director: risk and cost. To engineers: fewer on-call alerts at 3 a.m. Same proposal, different "why."
- **Pre-wire key stakeholders.** Talk one-on-one with the people most affected before the big review, so no one is surprised. Use these conversations to surface objections early — not to settle the decision before the open review. Record what changed as a result.

**While driving it:**
- **Write it down.** A clear [[design-docs|design doc]] travels further than any meeting and lets people think on their own time.
- **Make the right path the easy one.** Build a [[paved-roads|paved road]] — a template, library, or automated check that makes the good way the default — instead of issuing a mandate. Then maintain it; an abandoned paved road costs more credibility than never building one.
- **Give credit and share ownership.** Ideas spread faster when others feel they co-own them.
- **Build sponsors.** Find leaders who care about the outcome and can provide the authority you don't have.

**Choosing your fights:**
- **Spend credibility on one-way doors.** Save your energy for decisions that are high-impact and hard to reverse ([[reversible-decisions]]). Let small things go.
- **Disagree and commit.** When a decision goes the other way, say so once, clearly — then help it succeed.

## Example

A principal engineer wants all services to adopt structured logging (logs as named fields, not free text) and trace IDs (one ID that follows a request across services, also called a correlation ID; see [[observability]]). A memo mandating it would be ignored.

Instead, they:
1. Interview on-call engineers and collect stories about painful incidents caused by missing logs.
2. Write a short design doc framing the problem as "incident time," with data from recent postmortems.
3. Build a drop-in logging library with one team that was eager for it, and measure how much faster that team resolves incidents.
4. Have that team present the results at an engineering all-hands.
5. Add the library to the service template, with a named owner, so new services get it for free.

Within two quarters, most teams have adopted it — and nobody was ordered to. The last few holdouts moved only after a sponsor added "trace ID present?" to the incident-review checklist: escalation, used legitimately.

## Common traps

- **Being right loudly.** Winning a debate in public often loses the person.
- **Borrowing authority too often.** "The VP wants this" works once and erodes your own credibility.
- **Influencing by exhaustion.** Out-argue people until they give up, and they'll comply, not commit.
- **Backchannel decisions.** Pre-wiring that turns the open review into theater loses the trust of everyone who wasn't consulted.
- **Only influencing upward.** Trust from the engineers doing the work matters as much as trust from leadership.
- **Never building anything.** Credibility needs occasional proof that your ideas work in practice.

## When it doesn't apply

Some situations call for direct authority: security incidents, legal compliance, or an outage in progress. Be clear about who's deciding and why, then return to collaborative influence afterward. And if influence repeatedly fails on something critical, escalating through your sponsors is legitimate, not a failure.

## Related

- [[paved-roads]] — influence that scales without meetings.
- [[design-docs]] — the primary tool for influence at scale.
- [[reversible-decisions]] — where to spend your credibility.
- [[conways-law]] — changing architecture often means changing how teams work together.
- [[blameless-postmortems]] — modeling blamelessness is a form of cultural influence.
