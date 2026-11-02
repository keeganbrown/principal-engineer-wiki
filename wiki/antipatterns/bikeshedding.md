---
title: Bikeshedding
category: antipatterns
summary: Spending the most discussion on the small decisions everyone understands, while the big, hard decisions get little scrutiny.
tags: [decisions, meetings, review]
---

# Bikeshedding

> **In one sentence:** Spending the most discussion on the small decisions everyone understands, while the big, hard decisions get little scrutiny.

## The idea

A committee approves a nuclear power plant in a few minutes, because few members understand reactors well enough to question them. It then argues for 45 minutes about the roofing material for the staff bike shed, because everyone has an opinion on a bike shed. Small decisions are easy to have opinions about; big ones take effort to understand.

In engineering, the bike shed is the variable name, the brace style, the endpoint's URL wording, or the color of a dashboard. The reactor is the data model, the consistency choice, or the failure handling.

C. Northcote Parkinson called this the *law of triviality* (1957). Poul-Henning Kamp popularized "bikeshed" in software with a 1999 email to the FreeBSD developers' list.

## Why it matters

- **Big risks get the least scrutiny.** The decisions most likely to cause an outage or a costly migration slide through while time goes on trivia.
- **Small changes become slow.** A trivial pull request (PR) draws 30 comments; a large risky one gets "looks good to me" ([[code-review]]).
- **People stop contributing.** Engineers learn that any proposal draws endless debate and stop proposing.
- **Decisions don't stick.** Matters of taste get reopened every time someone new joins.

## How to apply it

Spotting it:

- **Compare comment counts to risk.** A rename with 30 comments next to a schema change with none is the signal.
- **Notice who talks.** When everyone weighs in on naming and two people on the data model, the room is on the bike shed.
- **Watch for decisions reopened.** The same style debate in three reviews means it was never settled.

Climbing out:

- **Automate the matters of taste.** A formatter and linter settle style once, so nobody discusses it in review. Adopt the tool's defaults to skip a debate over its settings, and reformat in one commit that `git blame` is told to ignore.
- **Sort decisions by how reversible they are.** Spend discussion on [[reversible-decisions|one-way doors]], decisions that are expensive to undo. Give two-way doors, which are cheap to reverse, a default owner and a short deadline.
- **Name a decider.** For each decision, one person decides after hearing input. Discussion has an end when someone is responsible for ending it.
- **Timebox small decisions.** "We'll pick a name in five minutes, then move on" works better than letting it run.
- **Point reviewers at the risky part.** In design docs and PRs, say where you most want scrutiny: "the retry logic is the part I'm unsure about" ([[design-docs]]). Label comment weight so small comments don't block merging ([[code-review]]).

## Example

A design review for a new internal orders API runs for an hour. Forty minutes go to whether the endpoint should be `/orders` or `/purchase-orders` and whether field names use camelCase. Nobody asks what happens when the payment call times out after the order is saved.

The next review is set up differently. The author opens with "decisions I need: idempotency on retries (a retried request must not create a second order, see [[idempotency]]), and whether stock is reserved before or after payment." Naming is delegated to the API style guide, with the author deciding anything it doesn't cover.

The hard part is that the risky questions are harder to discuss, and the room goes quiet when they come up. The reviewer leading the session asks specific questions — "what does a client see if we crash between saving and charging?" — which turns a vague worry into something people can answer.

The meeting ends early with two decisions recorded ([[architecture-decision-records]]). The cost moved, not vanished: the author spent an hour beforehand writing the decision list.

## Common traps

- **Calling everything a bike shed.** Some small-looking decisions are one-way doors: a public API field name, once customers depend on it, is expensive to change ([[api-versioning]]).
- **Dismissing people's concerns.** Saying "that's bikeshedding" can shut down someone who has spotted a real problem. Ask why it matters to them first.
- **Swinging to no discussion.** Fast decisions without input are their own failure. The goal is effort in proportion to stakes.
- **Relitigating decided matters.** Once a style decision is recorded, point to the record instead of debating again.

## When it doesn't apply

Sometimes the bike shed matters. Names in a public API, terms that become your domain's shared vocabulary, and user-facing wording all last a long time and are worth getting right ([[domain-driven-design]]). And a team that's newly formed may benefit from debating small things, because it's how people learn each other's judgment. The antipattern is debate out of proportion to the decision's cost, not debate about small things.

## Related

- [[reversible-decisions]] — match the effort to how hard the decision is to undo.
- [[code-review]] — where bikeshedding is most common.
- [[design-docs]] — say where you want scrutiny.
- [[architecture-decision-records]] — record decisions so they aren't relitigated.
- [[influencing-without-authority]] — steering a room toward the decisions that matter.
