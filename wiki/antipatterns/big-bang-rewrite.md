---
title: Big-Bang Rewrite
category: antipatterns
summary: Stopping to rebuild a working system from scratch and switching over all at once, which usually takes far longer than planned and loses behavior nobody wrote down.
tags: [legacy, migration, risk]
---

# Big-Bang Rewrite

> **In one sentence:** Stopping to rebuild a working system from scratch and switching over all at once, which usually takes far longer than planned and loses behavior nobody wrote down.

## The idea

The old system is slow to change, written in a language nobody likes, and full of strange code. The proposal: build a clean new version beside it, then switch everything over on one day. It's tempting because the new code will be simpler — at first, since it doesn't do everything yet.

The trap is that the old system's strange code is often *knowledge*: a fix for a customer's edge case, a pricing rule, a workaround for a partner's bug. A rewrite throws that knowledge away and has to rediscover it, usually in production.

Joel Spolsky called rewriting from scratch "the single worst strategic mistake" a software company can make, in a 2000 essay about Netscape. The rewrite eventually became Firefox, but only after Netscape had lost its market. Fred Brooks's 1975 *second-system effect* adds a warning: a designer's second system tends to be over-designed, loaded with every idea held back from the first. Rewrites invite exactly that.

## Why it matters

- **It takes longer than anyone estimates.** You're estimating the visible features; the hidden behaviors only appear during testing or after cutover (the moment traffic switches to the new system).
- **The old system won't sit still.** Customers still need fixes, so the old system keeps changing, and the new one chases a moving target.
- **You deliver nothing for months.** The business pays two teams' worth of effort and sees no new value until cutover.
- **Cutover concentrates all the risk on one day.** Every difference between old and new shows up at once, and rolling back may mean losing data written to the new system.

Many rewrites are abandoned partway, leaving two systems to run instead of one.

## How to apply it

Spotting it:

- **The plan has one cutover date.** Everything switches at once, and nothing ships before it.
- **The case is "the code is ugly."** That isn't a business case. "We can't add a new product line in under a month" is, and it may have a smaller fix.
- **The new design has more features than the old one.** That's the second-system effect at work.

Climbing out:

- **Replace incrementally instead.** Route one slice of functionality at a time to new code, so each step delivers value and can be rolled back ([[strangler-fig]]). This has its own cost: you run two systems for longer, and the last awkward slices may never move. Decide up front what "done" means, including retiring or freezing the leftovers.
- **Capture behavior before changing it.** Characterization tests record what the old system actually does, odd parts included — for example, feed last month's real requests through and save the outputs as expected results ([[test-driven-development]]).
- **Compare old and new outputs before switching.** Do this for reads and calculations only; on a write path, running both would act twice ([[strangler-fig]] covers this *shadow mode*).
- **Cut scope from the replacement.** The second system should do *less* at first, not more.

## Example

An insurer decides to rewrite its 12-year-old quoting engine and estimates nine months. At month nine, the new engine quotes 80% of policies correctly. The remaining 20% involves multi-car discounts, legacy loyalty rates, and three broker partners with custom terms that exist only as `if` statements in the old code.

Meanwhile the old engine has had 40 changes for new regulations, each now needed twice. The team switches strategy: a routing layer sends single-car quotes to the new engine and leaves everything else on the old one.

Because a quote is a calculation with no side effects, they can safely compute every quote in both engines for a month and compare. Most of the first week's differences are rounding and timing noise, which they have to filter out before the real ones show. What's left is 23 differences — 19 bugs in the new engine and 4 old behaviors that brokers relied on. The cost is that both engines now run in production for longer, and someone must own the routing layer until the old one is switched off.

## Common traps

- **Freezing the old system completely.** A total feature freeze during the rewrite usually fails, because the business can't wait a year. That's different from the strangler fig's rule, where new features keep shipping, just into the new system from the first slice onward ([[strangler-fig]]).
- **Rewriting and redesigning at once.** Changing language, data model, and product behavior together means you can't tell which change caused which bug.
- **No plan for the data.** The code is often the easy part; migrating years of data with inconsistent history is the hard part ([[expand-and-contract]]).
- **Underestimating the old system.** Teams say "it's only CRUD (create, read, update, delete)" about almost every system that turns out not to be.

## When it doesn't apply

Sometimes a rewrite is right. A small system — a few weeks of work — can be rewritten faster than it can be replaced piece by piece. A system on a platform that is being shut down, or one with a security model that can't be fixed in place, may have no incremental path. Even then, rewrite in slices where you can, test against the old system's real behavior, and plan the cutover so it can be reversed ([[reversible-decisions]]).

## Related

- [[strangler-fig]] — the incremental alternative.
- [[technical-debt]] — pay down debt in steps, not all at once.
- [[big-ball-of-mud]] — the usual reason teams want to rewrite.
- [[feature-flags]] — switch traffic between old and new gradually.
- [[golden-hammer]] — a rewrite is often driven by a new favorite tool.
