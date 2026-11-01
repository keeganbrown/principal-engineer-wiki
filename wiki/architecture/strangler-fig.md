---
title: Strangler Fig Pattern
category: architecture
summary: Replace a legacy system gradually by routing one piece of functionality at a time to new code, until the old system can be switched off — no big-bang rewrite.
tags: [architecture, migration, legacy]
---

# Strangler Fig Pattern

> **In one sentence:** Replace a legacy system gradually by routing one piece of functionality at a time to new code, until the old system can be switched off — no big-bang rewrite.

## The idea

Martin Fowler named this after the strangler fig tree, which grows around a host tree, slowly replacing it until the original is gone and the fig stands on its own.

Instead of rewriting a legacy system from scratch and switching over on one risky day, you:

1. **Put a routing layer in front** of the old system (a proxy, API gateway, or facade).
2. **Build one slice** of functionality in the new system.
3. **Route that slice's traffic** to the new system. Everything else still goes to the old one.
4. **Repeat** until nothing is left in the old system.
5. **Decommission** the legacy code.

```
             ┌──► /invoices  ──► New system
 Users ─► Router
             └──► everything else ──► Legacy system
```

## Why it matters

Big-bang rewrites are famously risky. They take longer than planned, the old system keeps changing during the rewrite, and the cutover day reveals hundreds of forgotten behaviors. Many are abandoned.

The strangler fig approach:

- **Delivers value continuously** — each migrated slice is in production.
- **Limits risk** — if a slice fails, route it back.
- **Keeps learning** — each slice teaches you more about the legacy system's hidden behaviors.
- **Can stop anytime** — if priorities change, you still have a working system.

## How to apply it

- **Start with a slice that's valuable but low-risk** — high change rate, clear boundaries, moderate traffic.
- **Find the seams.** URLs, message types, or modules make natural cut points.
- **Handle data carefully.** Decide which system owns each piece of data during the transition; sync with events or change-data-capture if both need it.
- **Use feature flags or percentage routing** to shift traffic gradually and roll back instantly.
- **Compare outputs.** For critical logic, run old and new side by side ("shadow mode") and diff results before switching.
- **Actually delete the old code.** Track progress by what's been turned off, not just what's been built.

## Example

A company's 15-year-old billing monolith is slowing every product launch. They place an API gateway in front of it. First, they rebuild the read-only "view invoice PDF" endpoint and route 5% of traffic, then 100%. Next, they migrate tax calculation, running both versions in shadow mode for a month to catch discrepancies. Eighteen months and twelve slices later, the last legacy endpoint is switched off.

## Common traps

- **Never finishing.** The last 20% is the hardest. Without commitment, you end up running two systems forever.
- **Shared database coupling.** If the new system writes directly to the legacy database, you've rebuilt the old coupling.
- **Rebuilding bugs faithfully.** Decide deliberately which legacy behaviors to keep; some are features users rely on, others are bugs.
- **Slices too big.** If a slice takes six months, it's a mini big-bang. Cut thinner.

## When it doesn't apply

If the legacy system is small, well understood, and has no way to intercept calls, a direct replacement may be faster. Systems with no clear seams (e.g., a single batch job) may need other techniques. And sometimes the right answer is not to replace the legacy system at all — just to stop it from growing.

## Related

- [[technical-debt]] — strangler fig is a way to pay down large debt safely.
- [[feature-flags]] — a common way to control routing between old and new.
- [[modular-monolith]] — a good target shape for the new system.
- [[architecture-decision-records]] — document the migration plan and the slice order.
