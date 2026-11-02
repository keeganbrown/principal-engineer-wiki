# Quiz: Bikeshedding

## A review of a new internal orders API spends 40 minutes on endpoint naming and none on payment timeouts. What helps next time?

- [x] Open with the decisions needed and leave naming to the style guide.
- [ ] Ban all discussion of names in reviews so the design gets the time.
- [ ] Book a two-hour review next time so that every topic gets covered.
- [ ] Invite more reviewers so the risky parts get more eyes on them.

**Why:** Point reviewers at the risky part and delegate matters of taste. Expect to spend time beforehand writing the decision list. If the API were public, its names would be one-way doors worth real time. See [[bikeshedding]].

## Why do small decisions attract the most debate?

- [x] Everyone understands them well enough to have an opinion.
- [ ] Small decisions are usually the ones that matter most to users.
- [ ] Big decisions are usually settled in advance by managers.
- [ ] Small decisions are harder to reverse once they ship.

**Why:** Big decisions take effort to understand, so fewer people engage. It's Parkinson's law of triviality: the nuclear plant passes in minutes, and the bike shed takes 45 minutes. See [[bikeshedding]].

## When is a long debate about a name worth it?

- [x] When it's in a public API or becomes shared domain vocabulary.
- [ ] When it's a local variable in a private function that's hard to read.
- [ ] When the team decided it once but some people still disagree.
- [ ] Only when the team can't agree after the first short discussion.

**Why:** Long-lived names are expensive to change once others depend on them. Calling everything a bike shed hides those one-way doors. See [[bikeshedding]] and [[api-versioning]].
