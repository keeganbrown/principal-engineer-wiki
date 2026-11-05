---
title: Technical Strategy
category: leadership
summary: A technical strategy names the real problem, picks an approach that rules some options out, and lists a few concrete actions — so many teams can make consistent decisions without asking you each time.
tags: [leadership, strategy, planning, staff-plus]
---

# Technical Strategy

> **In one sentence:** A technical strategy names the real problem, picks an approach that rules some options out, and lists a few concrete actions — so many teams can make consistent decisions without asking you each time.

## The idea

When fifteen teams face the same kind of decision — which queue, which database, how to deploy — they'll make it fifteen different ways unless something guides them. A technical strategy is that guide: a short written plan that says what's actually going on, the approach the organization will take, and what happens next.

Richard Rumelt's *Good Strategy Bad Strategy* (2011) gives it three parts:

- **Diagnosis** — what's really going on, backed by evidence. This is the hard part.
- **Guiding policy** — the overall approach. A good one rules options out.
- **Coherent actions** — a few concrete steps that carry out the policy and support each other.

One of Rumelt's marks of bad strategy is a goal dressed up as a plan: "become cloud-native," "be world-class at reliability."

Will Larson (*Staff Engineer*, 2021) suggests writing strategy from the bottom up: look at several recent design docs, notice the decisions they share, and write those down as policy.

## Why it matters

- **It lets people decide without you.** A clear guiding policy answers the next ten questions before they're asked, which is how a principal engineer's judgment reaches teams they never meet.
- **It makes saying no possible.** "That doesn't fit the strategy" is a reason; "I don't like it" is a preference.
- **It connects technical work to business outcomes.** Investment in a platform gets funded when the diagnosis shows what the problem costs the business.
- **Its value depends on follow-through.** It changes nothing until someone revisits it and acts on it.

## How to apply it

- **Start with the diagnosis, and make it specific.** Gather evidence: incident reviews, delivery times, costs, interviews with teams. "Deploys are slow" is a symptom; "60% of lead time is waiting for the one shared staging environment" is a diagnosis.
- **Choose a guiding policy that excludes something.** "New services use our one supported database engine; exceptions need a written case" is a choice. The exit matters, or the default becomes a mandatory hammer ([[golden-hammer]]). "We'll use the right tool for each job" excludes nothing and guides nobody.
- **List a few coherent actions, with owners and dates.** Three to five, each traceable to the diagnosis. If an action doesn't follow from the diagnosis, it belongs somewhere else.
- **Say what you won't do.** Name the options you rejected and why ([[architecture-trade-offs]]). This is the part people will push back on.
- **Keep it short.** Two to five pages. A strategy people can't summarize after one read won't shape their decisions.
- **Build it with the teams it affects.** Interview them for the diagnosis and share drafts early ([[influencing-without-authority]]). Get an executive sponsor who will fund the actions.
- **Write down when to revisit it.** State what would change the diagnosis, and check on a schedule, perhaps every six months.

## Example

An online retailer has fifteen teams running four message brokers and three job frameworks. A principal engineer reviews the postmortems for the last twenty serious incidents ([[blameless-postmortems]]) and finds nine involved background jobs, each on a stack only one or two people understood ([[hero-culture]]).

The diagnosis: too many async stacks for the on-call knowledge available, plus patching work for each one. The guiding policy: one supported broker and job framework on the [[paved-roads|paved road]]; new async work uses it, and existing systems move only when they need major changes anyway. The actions: the platform team ships templates and runbooks in one quarter, and the two systems with the most incidents migrate the next.

They rejected a mandated full migration within six months (too costly for the risk it removed) and the status quo (the incident data ruled it out). One team runs a high-volume ordered event log the chosen broker handles poorly; the strategy records that exception rather than pretending one tool fits everything. The costs were half the platform team's time for two quarters, and legacy brokers that will linger for years and still need patching.

## Common traps

- **Goals posing as strategy.** An aspiration with no diagnosis tells nobody what to do differently on Monday.
- **A list of everything.** Twelve priorities is no priority; coherent actions support each other.
- **No staffing.** Engineering leaders must fund the actions, or the strategy becomes a document everyone agrees with and nobody follows.
- **Written in isolation.** A strategy drafted alone and published as a surprise gets ignored by the teams it was meant to guide.
- **Never revisited.** The diagnosis goes stale, and the strategy outlives the conditions that justified it.

## When it doesn't apply

One or two teams who talk every day don't need a strategy document; a handful of [[architecture-decision-records]] is enough. When the business itself is changing direction, a detailed technical strategy will be wrong within months, so keep options open and revisit the diagnosis once things settle ([[reversible-decisions]]). And don't write a strategy to justify a decision already made: readers can tell, and it spends credibility you'll need later.

## Related

- [[influencing-without-authority]] — how a strategy gets adopted without a mandate.
- [[architecture-trade-offs]] — how to compare the options the policy chooses between.
- [[paved-roads]] — a common way to carry out a guiding policy.
- [[design-docs]] — the raw material for a bottom-up strategy.
- [[architecture-decision-records]] — where individual decisions under the strategy get recorded.
- [[golden-hammer]] — why a standard needs a documented way out.
