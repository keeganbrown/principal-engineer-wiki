---
title: CAP Theorem and Consistency Models
category: principles
summary: When a network splits, a distributed system must choose between staying consistent and staying available, so decide per feature which one users actually need.
tags: [distributed-systems, data, trade-offs]
---

# CAP Theorem and Consistency Models

> **In one sentence:** When a network splits, a distributed system must choose between staying consistent and staying available, so decide per feature which one users actually need.

## The idea

The CAP theorem names three properties of a system that stores data on multiple machines:

- **Consistency (C)** — every read sees the most recent write. Everyone sees the same data.
- **Availability (A)** — every request gets a (non-error) response.
- **Partition tolerance (P)** — the system keeps running, without corrupting data, when the network between machines drops messages. It may still have to turn some requests away.

The popular phrase "pick two of three" is misleading. Network partitions *will* happen; you don't get to opt out of P. So the real rule is:

> **When a partition happens, you must choose: refuse some requests (stay consistent) or answer them with possibly stale data (stay available).**

When there's no partition, there's still a trade-off, between **latency and consistency**: waiting for copies to agree takes time. This extension is called **PACELC** — if Partition, choose A or C; Else, choose Latency or Consistency.

The same "else" trade-off shows up in application design. When a service publishes an event and doesn't wait for consumers to process it, it has chosen low latency, and the consumers' copies lag behind. That lag is **eventual consistency**.

Eric Brewer stated CAP as a conjecture in 2000; Seth Gilbert and Nancy Lynch proved it in 2002. Daniel Abadi proposed PACELC (published 2012).

## Why it matters

Every distributed database, cache, and multi-service system makes this choice, whether you notice or not. Engineers who don't understand it build features that assume perfect consistency on top of systems that don't provide it — and get bugs like double-booked seats or disappearing cart items.

## How to apply it

Consistency models, from strongest to weakest:

| Model | Plain English | Typical use |
| --- | --- | --- |
| Linearizable (strong) | Behaves like one single copy, in real time. | Locks, leader election, unique usernames |
| Sequential | Everyone sees all operations in the same order, though maybe not instantly. | Reads from replicas that apply one shared log in order (e.g., ZooKeeper followers) |
| Causal | If B depends on A (a reply to a comment), everyone sees A before B. Unrelated events may appear in different orders. | Comments and replies, chat |
| Read-your-writes | You always see your own changes. | Profile edits, settings |
| Eventual | Copies converge "soon" if writes stop. | Like counts, feeds, analytics |

Then:

- **Default to one strong store.** Every extra consistency model is something every engineer must remember, and bugs live at the seams. Relax consistency only where latency, availability, or cost forces it.
- **Decide per operation when you do relax.** Checkout payment needs strong consistency; "recommended for you" doesn't.
- **Ask the business what being wrong costs.** A stale like count costs nothing; overselling the last concert ticket costs a lot.
- **Know your tools' defaults.** Many databases and caches are eventually consistent unless configured otherwise.
- **Design the user experience (UX) for staleness where you choose availability.** Show "updated a few seconds ago," use optimistic updates (show the change immediately, reconcile later), and read from the **primary** — the main copy that takes writes — right after a user's own write.

## Example

An airline seat-booking system spans two data centers. The link between them fails.

- **Choose consistency** — one side stops accepting bookings until the link heals. Some users see errors, but no seat is sold twice.
- **Choose availability** — both sides keep selling. Users are happy — until two passengers hold boarding passes for seat 14C.

For seat booking, the airline chooses consistency. For the flight-status page, it chooses availability: slightly stale status beats an error page.

## Common traps

- **Claiming "we picked CA."** Partition tolerance isn't optional in a real network.
- **Treating the whole system as one choice.** Different data deserves different guarantees.
- **Confusing CAP consistency with ACID consistency.** ACID (Atomic, Consistent, Isolated, Durable) describes database transactions; its "C" means data obeys rules like constraints. CAP's "C" means all copies agree.
- **Assuming partitions are rare.** Timeouts, overloaded nodes, and garbage-collection pauses that freeze a process for seconds all look like partitions to the rest of the system.

## When it doesn't apply

A single database on one machine doesn't face CAP — there's nothing to partition.

Adding read replicas is often the right, simple next step, but it brings back a small version of the choice: replica reads can be seconds stale. Send reads that must be fresh — like "show me the profile I just saved" — to the primary.

## Related

- [[event-driven-architecture]] — choosing async events means choosing eventual consistency for consumers.
- [[cqrs]] — read models are usually eventually consistent with the write side.
- [[saga-pattern]] — multi-service workflows end up eventually consistent; the isolation they lose is a separate problem that article covers.
- [[idempotency]] — retries during partitions must be safe.
