---
title: Big-Bang Rewrite
category: antipatterns
summary: Stopping to rebuild a working system from scratch and switching over all at once, which usually takes far longer than planned and loses behavior nobody wrote down.
tags: [legacy, migration, risk]
---

# Big-Bang Rewrite

> **In one sentence:** Stopping to rebuild a working system from scratch and switching over all at once, which usually takes far longer than planned and loses behavior nobody wrote down.

## The idea

The old system is slow to change, written in a language nobody likes, and full of strange code. The proposal: build a clean new version beside it, then switch everything over on one day. It's tempting because the new code will be simpler — at first, because it doesn't do everything yet.

The trap is that the old system's strange code is often *knowledge*: a fix for a customer's edge case, a tax rule, a workaround for a partner's bug. A rewrite throws that knowledge away and has to rediscover it, usually in production. Joel Spolsky called rewriting from scratch "the single worst strategic mistake" a software company can make, in a 2000 essay about Netscape. Fred Brooks's 1975 *second-system effect* explains the other half: the replacement tends to be over-designed, because it carries every idea the first version left out.

## Why it matters

- **It takes longer than anyone estimates.** You're estimating the visible features; the hidden behaviors only appear during testing or after cutover.
- **The old system won't sit still.** Customers still need fixes, so the old system keeps changing, and the new one chases a moving target.
- **You deliver nothing for months.** The business pays two teams' worth of effort and sees no new value until cutover.
- **Cutover concentrates all the risk on one day.** Every difference between old and new shows up at once, and rolling back may mean losing data written to the new system.

Many rewrites are abandoned partway, leaving two systems to run instead of one.

## How to apply it

- **Ask what problem the rewrite solves.** "The code is ugly" isn't a business case. "We can't add payment methods in under a month" is, and it may have a smaller fix.
- **Replace incrementally instead.** Route one slice of functionality at a time to new code, so each step delivers value and can be rolled back ([[strangler-fig]]).
- **Capture behavior before changing it.** Characterization tests record what the old system actually does, including the odd parts, so you notice what you'd lose.
- **Run old and new side by side.** Send the same inputs to both and compare outputs before switching. Differences are either bugs in the new code or knowledge you didn't know you had.
- **Cut scope from the replacement.** The second system should do *less* at first, not more.

## Example

A company decides to rewrite its 12-year-old billing system and estimates nine months. At month nine, the new system handles 80% of invoices. The remaining 20% involves pro-rated upgrades, legacy discount codes, and three enterprise customers with custom terms that only exist as `if` statements in the old code.

Meanwhile the old system has had 40 changes for new tax rules, each now needed twice. The team instead switches strategy: put a routing layer in front of billing, send plain monthly invoices to the new system, and leave everything else on the old one.

They run both on the same invoices for a month and compare totals. The comparison finds 23 differences — 19 bugs in the new system and 4 old behaviors that customers relied on. The cost is that both systems now run in production for longer, and someone must own the routing layer until the old system is switched off.

## Common traps

- **Freezing the old system.** A feature freeze during the rewrite sounds disciplined and usually fails, because the business can't wait a year.
- **Rewriting and redesigning at once.** Changing language, data model, and product behavior together means you can't tell which change caused which bug.
- **No plan for the data.** The code is often the easy part; migrating years of data with inconsistent history is the hard part ([[expand-and-contract]]).
- **Underestimating the old system.** "It's only CRUD (create, read, update, delete)" is said about almost every system that turns out not to be.

## When it doesn't apply

Sometimes a rewrite is right. A small system — a few weeks of work — can be rewritten faster than it can be strangled. A system on a platform that is being shut down, or one with a security model that can't be fixed in place, may have no incremental path. Even then, rewrite in slices where you can, test against the old system's real behavior, and plan the cutover so it can be reversed ([[reversible-decisions]]).

## Related

- [[strangler-fig]] — the incremental alternative.
- [[technical-debt]] — pay down debt in steps, not all at once.
- [[big-ball-of-mud]] — the usual reason teams want to rewrite.
- [[feature-flags]] — switch traffic between old and new gradually.
- [[golden-hammer]] — a rewrite is often driven by a new favourite tool.
