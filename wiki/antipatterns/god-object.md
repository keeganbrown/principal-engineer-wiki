---
title: God Object
category: antipatterns
summary: One class or service that knows and does too much, so every feature has to change it and every team has to queue up behind it.
tags: [structure, cohesion, design]
---

# God Object

> **In one sentence:** One class or service that knows and does too much, so every feature has to change it and every team has to queue up behind it.

## The idea

A god object is a single class, module, or service at the center of everything. It holds most of the data, makes most of the decisions, and every other part calls it. Typical names give it away: `OrderManager`, `UserService`, `Core`, `AppController`, `Helpers`.

It starts innocently. The class that handles orders is the obvious place to put "send the order email," then "apply the loyalty discount," then "sync to the warehouse." Each addition is a few lines. Two years later it is 6,000 lines with 80 methods, and nobody fully understands it.

Arthur Riel described the "god class" in 1996, in *Object-Oriented Design Heuristics*.

## Why it matters

- **Every change touches it.** When most features edit one file, pull requests (PRs) conflict and reviews slow down.
- **It has many reasons to change.** Pricing, email, and shipping rules change for different people at different times. Putting them in one place breaks the single-responsibility principle ([[solid-principles]]).
- **It's hard to test.** To test one rule, you construct the whole object and its dozen dependencies.
- **It becomes a team bottleneck.** In a service, the god object turns into a god *service* that every team must change and coordinate releases for ([[conways-law]]).

## How to apply it

Spotting it:

- **Look at size and churn together.** A file that is both among the largest and the most often changed is a *hotspot* and your candidate ([[technical-debt]]). `git log --since=1.year --format= --name-only -- src/ | sort | uniq -c | sort -rn | head` lists the most-changed files; ignore generated ones.
- **Read its method names.** If they span several business areas (`calculateTax`, `sendWelcomeEmail`, `exportToCsv`), it has several jobs.
- **Count its constructor's dependencies.** More than five or six usually means several objects are hiding inside one.

Climbing out:

- **Group the methods by the data they use.** Methods that touch the same fields belong together. Each cluster is a candidate class ([[coupling-and-cohesion]]).
- **Extract one cluster at a time behind the old interface.** The god object delegates to the new class, so callers don't change yet. Then move callers over and delete the delegation. Set a removal date and track remaining callers, or the delegating methods become permanent and new code calls whichever path it finds first.
- **Stop adding to it.** Make it a review rule: new behavior goes in a new, focused home, even while the old object still exists.

## Example

`OrderService` has 4,800 lines. It prices carts, takes payments, reserves stock, sends emails, and builds reports. Three teams edit it every sprint, and merge conflicts in it cost each team a few hours a week.

The team groups its methods by the fields they touch and finds four clusters: pricing, payment, fulfillment, and notification. They extract `Pricing` first, because it's pure calculation with no I/O (input and output, such as database calls) and is easiest to test. `OrderService.priceCart()` becomes a one-line call to `Pricing.quote()`.

The hard part comes next: payment and fulfillment both update a shared `status` field. Splitting them means deciding who owns the order's status. They make fulfillment the owner: payment calls `Fulfillment.paymentCaptured(orderId)` instead of setting the field, and fulfillment alone writes `status`. Both still live in one process, so a plain method call keeps it in one transaction.

That decision took a design review, not a refactoring tool. It's why god objects resist being split: the tangled part is usually an undecided question of who owns what. If payment later moves to its own service, the call becomes an event, and the status can briefly lag behind the payment. The event must also be saved in the same transaction as the payment, or a crash loses it ([[transactional-outbox]]).

## Common traps

- **Splitting by technical layer instead of by job.** Replacing `OrderService` with `OrderValidator`, `OrderRepository`, and `OrderHelper` leaves every feature still editing all three.
- **Creating many tiny classes.** Ten one-method classes that always change together are a god object spread across ten files. Split where reasons to change differ.
- **Replacing it with a god service.** Moving a god object into its own microservice keeps the bottleneck and adds a network hop.
- **Big-bang extraction.** Extracting all four clusters in one long-lived branch produces a merge nobody can review.

## When it doesn't apply

A central object is fine when it does one job that is genuinely central. A small app's `App` class that wires dependencies together is a *composition root* — the one place that creates objects and connects them ([[hexagonal-architecture]]). It's large because it lists things, not because it decides things.

Likewise, a 500-line module with one clear purpose and few changes isn't worth splitting. Size alone isn't the problem — size combined with many reasons to change is.

## Related

- [[solid-principles]] — the single-responsibility principle a god object violates.
- [[separation-of-concerns]] — the principle a god object abandons, one concern at a time.
- [[big-ball-of-mud]] — the same problem across a whole system.
- [[coupling-and-cohesion]] — how to find the natural seams.
- [[code-review]] — where the "don't add to it" rule is enforced.
