# Quiz: Technical Debt

## A rarely touched module runs on a runtime that no longer gets security patches. Can it wait, since its interest is low?

- [x] No; it carries risk that comes due on someone else's schedule.
- [ ] Yes; prioritize debt by interest, and this module costs almost nothing.
- [ ] Yes, until the module needs a feature change; then fix it all at once.
- [ ] No; every piece of debt should be paid off before any new feature work.

**Why:** Interest is the extra effort each change costs, and it's the usual way to prioritize. Watch for debt that carries risk instead: an unsupported runtime, unpatched dependencies, or one person who understands it. See [[technical-debt]] and [[hero-culture]].

## A team hard-codes one currency to launch on time and records it in an architecture decision record. What does the record buy them?

- [x] They still pay interest, but the fix is easy to find and budget.
- [ ] It stops the interest, so the code stays as cheap to change as before.
- [ ] It lets them skip the fix, since the decision is now on record.
- [ ] It moves the debt to the team that owns the ADR process.

**Why:** Recording deliberate debt doesn't stop the interest, but it turns a mid-launch surprise into planned work. See [[technical-debt]].

## Which code does not accrue meaningful debt interest?

- [x] A prototype that will truly be thrown away.
- [ ] A core billing module changed every sprint.
- [ ] A shared library with unclear ownership.
- [ ] A prototype that quietly became production.

**Why:** Disposable code doesn't need polish. The danger is prototypes that become production without anyone deciding so. See [[technical-debt]].
