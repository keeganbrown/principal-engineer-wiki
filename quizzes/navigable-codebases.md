# Quiz: Navigable Codebases

## An agent adds a new discount type to an unused `legacy/promo/` folder. What change prevents this?

- [x] Delete dead code so search only finds the real implementation.
- [ ] Add a comment in the legacy folder asking agents not to use it.
- [ ] Rename the legacy folder to start with an underscore.
- [ ] Give the agent a bigger context window.

**Why:** What the agent can't find, it duplicates — and what it finds first, it uses. Delete dead code. See [[navigable-codebases]].

## Discounts register at startup under names built from strings, like `"discount_" + kind`. Why is that a problem?

- [x] Searching for a discount's name finds nothing, so explorers miss where it's wired up.
- [ ] String concatenation is slow at startup.
- [ ] The registry can only hold ten entries.
- [ ] Agents can't read code that uses string concatenation.

**Why:** Prefer names you can search for. Clever indirection hides behavior from anyone exploring with search tools. See [[navigable-codebases]].

## When does layout matter least for navigability?

- [x] A codebase of a few thousand lines that fits in the agent's context at once.
- [ ] A large monorepo with dozens of teams.
- [ ] A service with several legacy folders.
- [ ] A codebase where each concept has three names.

**Why:** Small codebases are navigable almost regardless of layout. Where a framework dictates structure, follow it consistently. See [[navigable-codebases]].
