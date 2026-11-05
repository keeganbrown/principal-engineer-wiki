---
title: Technical Debt
category: practices
summary: Shortcuts in code are like a loan — they buy speed now but charge interest on every future change, so take them deliberately and pay them down on purpose.
tags: [maintainability, planning, communication]
---

# Technical Debt

> **In one sentence:** Shortcuts in code are like a loan — they buy speed now but charge interest on every future change, so take them deliberately and pay them down on purpose.

## The idea

When you ship code that isn't quite right — to hit a deadline, or because you didn't yet understand the problem — you're borrowing:

- The **principal** is the work needed to fix it properly.
- The **interest** is the extra effort every future change costs because the code is harder to work with.

Debt isn't automatically bad. Like a mortgage, it can be a smart investment. The problem is debt you didn't know you took on, or never pay back.

Martin Fowler's **debt quadrant**:

| | Reckless | Prudent |
| --- | --- | --- |
| **Deliberate** | "We don't have time for design." | "Ship now, fix after launch — we've noted it." |
| **Inadvertent** | "We didn't know about separating layers." | "Now we know how we *should* have built it." |

*Deliberate* means you knew you were borrowing; *inadvertent* means you didn't. *Prudent* debt is a reasonable trade and normal; *reckless* debt comes from ignoring good practice, and it's what to stamp out.

Ward Cunningham coined the metaphor in 1992.

## Why it matters

Interest compounds. A codebase with heavy debt gets slower to change every quarter, until simple features take weeks and nobody wants to touch certain files. Velocity collapses gradually, so it's easy to miss until it's severe.

As a principal engineer, your job is to **translate debt into business terms** — risk, delay, cost — so the business can weigh it against features.

## How to apply it

- **Make it visible.** Keep a debt register (tickets labeled `tech-debt`, or a short doc) with the *impact* of each item.
- **Pay down principal where you work.** Follow the "boy scout rule": leave the code a bit better than you found it.
- **Prioritize by interest rate.** Fix debt in code that changes often first.
- **Watch for debt that carries risk, not interest.** A rarely touched module can wait — *unless* it runs on an unsupported runtime, has unpatched dependencies, or only one person understands it ([[hero-culture]]). That debt comes due on someone else's schedule: a security advisory, a forced upgrade, a resignation.
- **Find the debt nobody recorded.** Look for **hotspots**: files with high churn (edited very often) and frequent bug fixes. Measure lead time for changes (from commit to production; see [[continuous-delivery]]) there before and after paying debt down, to show it worked.
- **Budget for it.** Many teams reserve roughly 10–20% of capacity for paying down debt continuously. Hold that allocation to the same rules — hotspots and outcomes — or it turns into a fund for whatever someone dislikes.
- **Record deliberate debt when you take it.** Note the shortcut, the reason, and the trigger for repaying it.
- **Frame it in outcomes.** Not "refactor the order module," but "cut time-to-ship for checkout features from 2 weeks to 3 days."

## Example

A team hard-codes support for one currency to launch in the US on time — a prudent, deliberate choice. They note it in an architecture decision record ([[architecture-decision-records|ADR]]) with the trigger "before any international launch."

Recording it didn't stop the interest. Over the year, about 30 places in the code quietly assumed USD, and every pricing feature took a little longer because of it.

When international expansion reached the roadmap, though, the team knew exactly what to search for and budgeted a quarter for the fix — instead of discovering it mid-launch.

## Common traps

- **"Debt" as a label for code you don't like.** Debt should have measurable interest or risk: bugs, slowness, exposure.
- **The big rewrite.** Halting features to rewrite everything usually fails ([[big-bang-rewrite]]). Pay down incrementally instead ([[strangler-fig]]).
- **Invisible debt.** If only engineers know about it, it will never be prioritized.
- **Never taking any.** Refusing all shortcuts can be its own waste. Speed sometimes really matters.
- **Forgotten scaffolding.** Stale [[feature-flags]], dead code paths, and abandoned migrations are debt too.

## When it doesn't apply

Code that will be thrown away — a prototype, an experiment, a one-time migration — doesn't accrue meaningful interest. Don't spend effort polishing it. Just be honest about which code is disposable, and don't let prototypes quietly become production.

A system you'll replace within a year, for example through a [[strangler-fig]], should get only its risk debt paid: security fixes and unsupported runtimes. Paying down its interest is paying off a loan you're about to walk away from.

## Related

- [[kiss]] — unchecked complexity is the most common form of debt.
- [[strangler-fig]] — a safe way to pay down large debt without a rewrite.
- [[architecture-decision-records]] — a place to record deliberate debt.
- [[code-review]] — a natural checkpoint for spotting and naming new debt.
- [[blameless-postmortems]] — incidents are often where hidden debt surfaces.
- [[feedback-loops-for-agents]] — slow, flaky checks are debt that coding agents make more expensive.
- [[big-ball-of-mud]] — what debt becomes when nobody manages it.
- [[not-invented-here]] — homegrown plumbing is debt with an owner of one.
