---
title: CAP Theorem and Consistency Models
category: principles
summary: When a network splits, a distributed system must choose between staying consistent and staying available, so decide per feature which one users actually need.
tags: [distributed-systems, data, trade-offs]
---

# CAP Theorem and Consistency Models

> **In one sentence:** When a network splits, a distributed system must choose between staying consistent and staying available, so decide per feature which one users actually need.

## The idea

Eric Brewer's CAP theorem talks about three properties of a system that stores data on multiple machines:

- **Consistency (C)** — every read sees the most recent write. Everyone sees the same data.
- **Availability (A)** — every request gets a (non-error) response.
- **Partition tolerance (P)** — the system keeps working even when the network between machines drops messages.

The popular phrase "pick two of three" is misleading. Network partitions *will* happen; you don't get to opt out of P. So the real rule is:

> **When a partition happens, you must choose: refuse some requests (stay consistent) or answer them with possibly stale data (stay available).**

When there's no partition, the trade-off is between **latency and consistency** — waiting for replicas to agree takes time. This extension is called **PACELC**: if Partition, choose A or C; Else, choose Latency or Consistency.

## Why it matters

Every distributed database, cache, and multi-service system makes this choice, whether you notice or not. Engineers who don't understand it build features that assume perfect consistency on top of systems that don't provide it — and get bugs like double-booked seats or disappearing cart items.

## How to apply it

Learn the common **consistency models**, from strongest to weakest:

| Model | Plain English | Typical use |
| --- | --- | --- |
| Linearizable (strong) | Behaves like one single copy | Bank balances, locks, inventory counts |
| Sequential / causal | Everyone sees related events in the same order | Comments and replies, chat |
| Read-your-writes | You always see your own changes | Profile edits, settings |
| Eventual | Replicas converge "soon" if writes stop | Like counts, feeds, analytics |

Then:

- **Decide per operation, not per system.** Checkout payment needs strong consistency; the "recommended for you" list doesn't.
- **Ask the business** what being wrong costs. Showing a stale like count costs nothing; overselling the last concert ticket costs a lot.
- **Know your tools' defaults.** Many databases and caches are eventually consistent unless configured otherwise.
- **Design the UX for staleness** where you choose availability: "updated a few seconds ago," optimistic updates, clear retry states.

## Example

An airline seat-booking system spans two data centers. The link between them fails.

- **Choose consistency:** one side stops accepting bookings until the link heals. Some users see errors, but no seat is sold twice.
- **Choose availability:** both sides keep selling. Users are happy — until two passengers hold boarding passes for seat 14C.

For seat booking, the airline chooses consistency. For the flight-status page, it chooses availability: slightly stale status beats an error page.

## Common traps

- **"We picked CA."** Partition tolerance isn't optional in a real network.
- **Treating the whole system as one choice.** Different data deserves different guarantees.
- **Confusing CAP consistency with ACID consistency.** ACID's "C" means data obeys rules (constraints); CAP's "C" means all copies agree.
- **Assuming partitions are rare.** Timeouts, GC pauses, and overloaded nodes all look like partitions to the rest of the system.

## When it doesn't apply

A single database on a single machine doesn't face CAP — there's nothing to partition. Many apps can live comfortably on one strongly consistent primary database plus replicas for reads, and that's often the right, simple choice.

## Related

- [[event-driven-architecture]] — choosing events usually means choosing eventual consistency.
- [[cqrs]] — read models are typically eventually consistent with the write side.
- [[saga-pattern]] — how to keep data correct across services without distributed transactions.
- [[idempotency]] — retries during partitions must be safe.
