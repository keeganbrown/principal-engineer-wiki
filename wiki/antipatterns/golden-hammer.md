---
title: Golden Hammer
category: antipatterns
summary: Using a familiar or fashionable tool for every problem, whether or not it fits, because the choice is made before the problem is understood.
tags: [technology-choice, judgment, tools]
---

# Golden Hammer

> **In one sentence:** Using a familiar or fashionable tool for every problem, whether or not it fits, because the choice is made before the problem is understood.

## The idea

"If the only tool you have is a hammer, everything looks like a nail." The golden hammer is a tool a team knows well, or is excited about, and reaches for by default. Kubernetes for a single small app; a graph database because the team just learned one; microservices for a three-person startup; an event bus for what could be a function call.

There are two flavors. The *comfortable* hammer is the tool you already know, used even where it fits badly — say, a relational table polled every second as a high-volume job queue. The *shiny* hammer is the new tool you want to learn, sometimes called résumé-driven development. Both skip the same step: describing the problem before picking the solution.

The saying is usually credited to psychologist Abraham Maslow (1966), though Abraham Kaplan made a similar point in 1964. The antipattern name comes from the 1998 book *AntiPatterns* by William Brown and colleagues.

## Why it matters

- **Bad fits cost forever.** A store that doesn't match your access pattern (how the data is read and written, such as by key, range, or relationship) makes every query harder for the life of the system ([[nosql-databases]]).
- **Shiny tools carry unknown failure modes.** A tool nobody on the team has run in production will teach you its limits during an incident.
- **Every new tool is a permanent operating cost.** Someone must patch it, monitor it, and know how to debug it at 3 a.m.
- **The comfortable hammer hides better options.** Teams that always use one tool never learn when another is simpler.

## How to apply it

Spotting it:

- **The tool is named before the problem is.** A design doc that opens with "we'll use X" and describes the need later has chosen first.
- **The same tool appears in every design.** One team's last five proposals all use it, whatever the problem.
- **Workarounds keep growing.** Custom locking, hand-built indexes, and retry hacks around a tool are signs it doesn't fit.

Climbing out:

- **Write the problem down before the solution.** State the access pattern, scale, latency, and consistency you need, in plain words, before naming any product.
- **Make the boring option the default.** Choose the tool your organization already runs well unless the problem clearly needs something else ([[paved-roads]]). Dan McKinley's "Choose Boring Technology" (2015) suggests each company gets about three "innovation tokens" to spend. Each unfamiliar technology you adopt uses one, so spend them where they make your product different.
- **Ask "what would we use if this tool didn't exist?"** If the answer is simpler and works, use it.
- **Price the operating cost, not just the build cost.** Include on-call knowledge, upgrades, and the second engineer who must understand it.
- **Try new tools where failure is cheap.** An internal tool or a prototype is a good place to learn; the payment path is not.

## Example

A team is adding "customers who bought this also bought" recommendations. An engineer who has just learned a graph database proposes adding one, since purchases are naturally a graph.

The written problem is short: once a night, compute the top 10 related products for each product; at request time, look them up by product ID; a day stale is fine. Against that, a nightly batch job writing to one table in the existing Postgres database does it, with lookups by key that any database handles well ([[relational-databases]]).

The hard part is that the engineer's underlying point is real — a planned fraud project will need to follow chains of shared cards and addresses several hops deep, which is what graph databases are for. So they record that need in a design doc and plan to evaluate one there. The batch approach has its own cost: a new nightly job to own, and recommendations up to a day old. Saying "not here" is easier when you can say where.

## Common traps

- **Overcorrecting into never trying anything new.** Boring isn't the goal; fit is. Sometimes the new tool is the right one, and refusing it is its own hammer.
- **Mistaking popularity for fit.** "Everyone uses it" describes the market, not your problem ([[cargo-cult-engineering]]).
- **Standardizing too hard.** One approved database for every use case makes the comfortable hammer mandatory. Paved roads should document how to get an exception when the default doesn't fit.
- **Judging the person instead of the proposal.** Wanting to learn is healthy. Give engineers safe places to try tools, so the production path doesn't become the training ground.

## When it doesn't apply

Using one tool for many jobs is often the right call. A small team that runs Postgres well should probably use it for queues, search, and caching until a real limit appears, because one well-understood tool beats four half-understood ones ([[kiss]]).

It becomes a hammer when the workarounds — custom locking for the queue, hand-rolled ranking for search — cost more each quarter than running a fitting tool would. The antipattern is choosing without looking at the problem, not reusing a tool that fits well enough.

## Related

- [[cargo-cult-engineering]] — copying a tool because others succeeded with it.
- [[not-invented-here]] — a sibling: "we'll build it" is also an answer picked before the problem is understood.
- [[paved-roads]] — a deliberate default, with a way to ask for exceptions.
- [[reversible-decisions]] — tool choices vary a lot in how hard they are to undo.
- [[design-docs]] — where the problem gets written down first.
