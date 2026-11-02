---
title: Navigable Codebases
category: coding-with-ai
summary: Structure code so a newcomer with only search tools can find the right place to change — predictable layout, consistent names, local docs, and no behavior wired up invisibly at runtime — because that's exactly how a coding agent explores.
tags: [ai, coding-agents, code-structure, naming, documentation]
---

# Navigable Codebases

> **In one sentence:** Structure code so a newcomer with only search tools can find the right place to change — predictable layout, consistent names, local docs, and no behavior wired up invisibly at runtime — because that's exactly how a coding agent explores.

## The idea

A **coding agent** is an AI tool that reads code, runs commands, and edits files in a loop toward a goal. It doesn't have a mental map of your system. Each session it explores like a very fast new hire: list folders, search for a name, open a few files, follow imports. Whatever it can't find, it guesses — or rebuilds from scratch next to the code it missed.

A **navigable codebase** is one where that kind of exploration works. The folder names say what's inside. One concept has one name everywhere. The rules for a module sit next to the module. And behavior is visible in the code, not wired up invisibly at runtime.

None of this is new: it's what makes a codebase easy for human newcomers too. Agents just make the cost of a confusing layout show up every day instead of once per hire.

## Why it matters

- **What the agent can't find, it duplicates.** A helper hidden in a `utils` file gets rewritten. Duplication then spreads, because the next agent finds both copies.
- **Context is limited.** An agent can only hold so much text at once (its *context window*, see [[large-language-models]]). Every file it opens to get oriented is attention not spent on the task.
- **Wrong guesses look plausible.** An agent that can't find how payments are validated will write its own validation — confident, tested, and different from the real one.

The limit: no structure makes a large system obvious. Navigability lowers the cost of exploring; it doesn't remove the need for a plan and a review ([[spec-first-agent-tasks]]).

## How to apply it

- **Group by domain.** `billing/`, `orders/`, `shipping/` tell an agent where a change belongs; `controllers/`, `services/`, `utils/` make it open three folders for every feature ([[coupling-and-cohesion]]).
- **Use one name per concept.** If the business says "subscription," don't call it `Plan` in one module and `Membership` in another. A search for one word should find all of it ([[domain-driven-design]] calls this the ubiquitous language). This holds within one bounded context; across contexts, different names can be right, so say so in each module's README and a search for one word points to the other.
- **Prefer names you can search for.** `calculateShippingCost` is findable; `calc` or a dynamically built method name isn't. Avoid code generated or registered at runtime by string, where a search finds nothing.
- **Put docs next to the code.** A short README or instruction file in each major module explains its purpose, rules, and entry points ([[agent-instruction-files]]). Architecture decisions live in the repository as [[architecture-decision-records]], not only in a wiki the agent can't see.
- **Keep tests easy to find.** Use a consistent pattern — beside the code or mirrored in a `tests/` folder — so finding the tests for a file is mechanical.
- **Mark generated and frozen code.** A header comment and a folder name like `gen/` stop agents from editing files that will be overwritten. Back it with a check or a hook so the rule holds ([[shared-agent-configuration]]).
- **Leave one good example of each common change.** A clean reference endpoint, migration, or test shows the house style better than a page of rules.
- **Delete dead code.** Unused modules look exactly like live ones to an agent. Commented-out code and stale feature flags are traps.

## Example

An agent is asked to add a discount type. The codebase has `services/pricing.ts`, `utils/money.ts`, `helpers/discounts.ts`, and an older `legacy/promo/` folder that's no longer used. Each discount registers itself at startup under a name assembled from strings (`"discount_" + kind`), so searching the code for a discount's name finds nothing.

The agent searches for "discount," finds `legacy/promo/` first, and adds the new type there. Tests pass, because the legacy folder still has tests. A reviewer catches it; the second attempt finds `helpers/discounts.ts` but misses the registration code and adds a `switch` statement beside it.

The team spends a sprint on navigability: delete `legacy/promo/`, move pricing into a `pricing/` domain folder with a short README, replace string-built registration with an explicit list, and add one reference discount with tests. The next agent task in that area lands correctly on the first try. The cost was a sprint of work with no new features, and the explicit list is slightly more typing each time someone adds a discount.

## Common traps

- **A big-bang reorganization.** Moving every file at once breaks history, open branches, and everyone's memory. Improve the areas where people and agents work most, a module at a time.
- **Docs that drift.** A module README that describes last year's design misleads agents with full confidence. Keep docs short enough that updating them is part of the change.
- **Over-splitting.** Fifty tiny files with one function each are as hard to navigate as one huge file. Group by what changes together.
- **Clever indirection.** Wiring that happens by naming convention or at runtime — a framework that finds `*Handler` classes automatically, code that generates methods on the fly — saves typing but hides the call graph from search. Use them where they pay, and document where they're used.
- **Layout by tooling, not meaning.** A structure that suits the build tool but not the domain makes every change a scavenger hunt.

## When it doesn't apply

A small codebase that fits in an agent's context in one go — a few thousand lines — is navigable almost regardless of layout. And some frameworks dictate structure; fighting them costs more than it saves. Follow the framework's conventions consistently, since a consistent convention is navigable even if it isn't your favorite.

## Related

- [[coupling-and-cohesion]] — why grouping by domain helps humans and agents alike.
- [[domain-driven-design]] — one consistent language for each concept.
- [[agent-instruction-files]] — per-module instruction files are part of the map.
- [[feedback-loops-for-agents]] — once the agent finds the right place, checks tell it whether the change is right.
- [[technical-debt]] — dead code and inconsistent names are debt agents pay interest on daily.
