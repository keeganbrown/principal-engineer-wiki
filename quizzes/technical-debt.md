# Quiz: Technical Debt

## In the debt metaphor, what is the "interest"?

- [x] The extra effort every future change costs because the code is harder to work with.
- [ ] The work needed to fix the shortcut properly once.
- [ ] The money spent on the original feature.
- [ ] The time spent writing the ticket that records the debt.

**Why:** The principal is the fix; the interest is the ongoing drag. Prioritize debt by its interest rate. See [[technical-debt]].

## A team hard-codes one currency to launch on time and records it in an ADR. What happens?

- [x] Interest still accrues, but when expansion comes they know what to search for and budget the fix.
- [ ] Recording it stops the interest, so the code stays as cheap to change as before.
- [ ] The debt disappears once the launch succeeds.
- [ ] They must rewrite the whole pricing system before the next release.

**Why:** Recording deliberate debt doesn't stop the interest, but it turns a mid-launch surprise into planned work. See [[technical-debt]].

## Which code does not accrue meaningful debt interest?

- [x] A prototype that will truly be thrown away.
- [ ] A core billing module changed every sprint.
- [ ] A shared library with unclear ownership.
- [ ] A prototype that quietly became production.

**Why:** Disposable code doesn't need polish. The danger is prototypes that become production without anyone deciding so. See [[technical-debt]].
