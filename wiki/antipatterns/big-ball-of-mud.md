---
title: Big Ball of Mud
category: antipatterns
summary: A system with no real structure, where everything calls everything, grows one reasonable shortcut at a time until every change is risky.
tags: [structure, coupling, legacy]
---

# Big Ball of Mud

> **In one sentence:** A system with no real structure, where everything calls everything, grows one reasonable shortcut at a time until every change is risky.

## The idea

A big ball of mud is a codebase with no boundaries you can rely on. Any module may call any other, read any table, or reach into another's internals. Nobody designed it that way; it accumulated. Each shortcut — "just import the billing helper here," "just read that table directly" — was quick and locally sensible.

It is the most common architecture in the world, because it is what you get by default. Structure has to be maintained; mud only has to be left alone. Brian Foote and Joseph Yoder named it in a 1997 paper, and noted, uncomfortably, that mud often wins because it ships.

## Why it matters

- **Every change has an unknown blast radius.** Blast radius is how much breaks when one change goes wrong. When anything can depend on anything, you can't tell what a change will break, so you test everything or ship and pray.
- **Knowledge concentrates in a few people.** Only the engineers who were there know which paths are safe ([[hero-culture]]).
- **It blocks every later move.** You can't extract a service, assign team ownership, or let a coding agent work safely in one area, because there are no areas.

The cost is slow and invisible at first. Teams usually notice it as "everything takes longer than it used to," long after the cheap fix has passed.

## How to apply it

Spotting it:

- **Ask "who owns this?" and get a shrug.** Folders exist, but nobody can say what a module is responsible for.
- **Count the cycles.** Module A imports B, B imports C, C imports A. A dependency graph tool will show you in minutes.
- **Watch small changes touch many folders.** A one-field change that edits eight directories means the field's knowledge is smeared across all eight.

Climbing out:

- **Draw the boundaries you want, then enforce one.** Pick a domain with clear edges, give it a public interface, and add a build check that fails on imports of its internals ([[modular-monolith]]).
- **Stop the bleeding before cleaning up.** A rule that blocks *new* violations is worth more than a plan to fix old ones. Record existing violations in an allow list and shrink it over time.
- **Move code toward its data.** Logic that reads a domain's tables belongs inside that domain ([[coupling-and-cohesion]]).
- **Refactor where you're already working.** Improve the module the next feature touches, not the whole system at once ([[technical-debt]]).

## Example

An online shop's `utils/` folder has 140 files. Checkout, catalog, and email all import from it, and `utils/pricing.js` reads the `orders` table directly. A team tries to change how discounts round, and three unrelated tests fail in the email module.

They don't rewrite. They create a `pricing` module with one public function, `quote(cart)`, and add a lint rule: nothing outside `pricing/` may import its internals. The rule starts with 37 known violations in an allow list. Each sprint, the team that touches a violating file fixes it.

The hard part is the allow list. Without a deadline it becomes permanent, and new code copies the old violations because "it's done that way already." The team reviews the count monthly and refuses to add entries. After two quarters it's down to four, and discount changes no longer surprise the email team.

## Common traps

- **Declaring bankruptcy and rewriting.** A rewrite usually rebuilds the mud with newer tools, because the forces that made the mud haven't changed ([[big-bang-rewrite]]).
- **Splitting it into services.** Network calls between tangled modules give you a [[distributed-monolith]], which is the same mud plus latency.
- **Drawing boundaries on a diagram only.** A boundary that no build check enforces will be crossed by the next deadline.
- **Blaming the people who made it.** Mud is what deadlines produce. Blame stops people from telling you where the worst parts are.

## When it doesn't apply

Mud is a reasonable choice for code you expect to throw away: a prototype, a one-off migration script, or a product still searching for its first customers. Structure is an investment that pays off when the code lives long and many people change it. If neither is true yet, ship, and add boundaries when the code proves it will survive ([[yagni]]).

## Related

- [[modular-monolith]] — the usual way out: boundaries without a network.
- [[coupling-and-cohesion]] — the forces that turn code into mud.
- [[god-object]] — the same problem inside one class or service.
- [[technical-debt]] — mud is accumulated, unmanaged debt.
- [[strangler-fig]] — replacing a muddy system one slice at a time.
