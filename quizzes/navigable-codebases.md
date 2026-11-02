# Quiz: Navigable Codebases

## An agent adds a new discount type to an unused `legacy/promo/` folder. What change prevents this?

- [x] Delete dead code so search finds only the real implementation.
- [ ] Add a comment in the legacy folder asking agents not to use it.
- [ ] Rename the legacy folder so it starts with an underscore.
- [ ] Give the agent a bigger context window so it sees everything.

**Why:** What the agent can't find, it duplicates, and what it finds first, it uses. See [[navigable-codebases]].

## Discounts register at startup under names built from strings, like `"discount_" + kind`. Why is that a problem?

- [x] Searching for a discount's name finds nothing, so its wiring stays hidden.
- [ ] String concatenation at startup makes the service noticeably slower.
- [ ] Registration order becomes unpredictable from one startup to the next.
- [ ] Agents can't read any code that builds names out of strings.

**Why:** Prefer names you can search for. Indirection can pay for itself, but then document where it's used, so readers and agents can find it. See [[navigable-codebases]].

## When does layout matter least for navigability?

- [x] A codebase of a few thousand lines that fits in the agent's context.
- [ ] A large monorepo shared by dozens of teams with their own conventions.
- [ ] A service with several legacy folders that nobody has cleaned up.
- [ ] A framework app whose structure the team has chosen to work around.

**Why:** Small codebases are navigable almost regardless of layout. Where a framework dictates structure, follow it consistently rather than fighting it. See [[navigable-codebases]].
