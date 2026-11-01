---
title: Technical Debt
category: practices
summary: Shortcuts in code are like a loan — they buy speed now but charge interest on every future change, so take them deliberately and pay them down on purpose.
tags: [maintainability, planning, communication]
---

# Technical Debt

> **In one sentence:** Shortcuts in code are like a loan — they buy speed now but charge interest on every future change, so take them deliberately and pay them down on purpose.

## The idea

Ward Cunningham coined the metaphor. When you ship code that isn't quite right — to hit a deadline, or because you didn't yet understand the problem — you're borrowing. The **principal** is the work needed to fix it. The **interest** is the extra effort every future change costs because the code is harder to work with.

Debt isn't automatically bad. Like a mortgage, it can be a smart investment. The problem is debt you didn't know you took on, or never pay back.

Martin Fowler's **debt quadrant** is a helpful lens:

| | Reckless | Prudent |
| --- | --- | --- |
| **Deliberate** | "We don't have time for design." | "Ship now, fix after launch — we've noted it." |
| **Inadvertent** | "What's layering?" | "Now we know how we *should* have built it." |

Prudent debt is normal. Reckless debt is a problem to address.

## Why it matters

Interest compounds. A codebase with heavy debt gets slower to change every quarter, until simple features take weeks and nobody wants to touch certain files. Velocity collapses gradually, so it's easy to miss until it's severe.

For principal engineers, a key skill is **translating debt into business terms** — risk, delay, cost — so it can be prioritized alongside features.

## How to apply it

- **Make it visible.** Keep a debt register (tickets labeled `tech-debt`, or a short doc) with the *impact* of each item.
- **Pay interest where you work.** Follow the "boy scout rule": leave the code a bit better than you found it.
- **Prioritize by interest rate.** Fix debt in code that changes often. Debt in a stable, rarely touched module can wait forever.
- **Budget for it.** Many teams reserve ~10–20% of capacity for paying down debt continuously.
- **Record deliberate debt** at the time you take it: what shortcut, why, and the trigger for repaying it.
- **Frame it in outcomes.** Not "refactor the order module," but "cut time-to-ship for checkout features from 2 weeks to 3 days."

## Example

A team hard-codes support for one currency to launch in the US on time — a prudent, deliberate choice, noted in an ADR with the trigger "before any international launch."

A year later, international expansion is on the roadmap. Because the debt was recorded and scoped, the team can estimate the payoff work accurately and schedule it before the launch, rather than discovering it mid-project.

## Common traps

- **"Debt" as a label for code you don't like.** Debt should have measurable interest: bugs, slowness, risk.
- **The big rewrite.** Halting features to rewrite everything usually fails. Pay down incrementally instead.
- **Invisible debt.** If only engineers know about it, it will never be prioritized.
- **Never taking any.** Refusing all shortcuts can be its own waste. Speed sometimes really matters.

## When it doesn't apply

Code that will be thrown away — a prototype, an experiment, a one-time migration — doesn't accrue meaningful interest. Don't spend effort polishing it. Just be honest about which code is disposable, and don't let prototypes quietly become production.

## Related

- [[kiss]] — unchecked complexity is the most common form of debt.
- [[strangler-fig]] — a safe way to pay down large debt without a rewrite.
- [[architecture-decision-records]] — a place to record deliberate debt.
- [[code-review]] — a natural checkpoint for spotting and naming new debt.
- [[blameless-postmortems]] — incidents are often where hidden debt surfaces.
