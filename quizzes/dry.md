# Quiz: Don't Repeat Yourself (DRY)

## Two functions have identical code, but one validates shipping addresses and the other billing addresses, owned by different teams. What does DRY suggest?

- [x] Wait; they look alike but may represent different rules that change for different reasons.
- [ ] Merge them right away, because identical code always means duplicated knowledge.
- [ ] Move them into a shared library that both teams must release together.
- [ ] Delete one and have both teams call the other team's function directly.

**Why:** DRY is about knowledge, not code. Look-alike code waits for the third copy; a known shared rule gets one home at the second. See [[dry]].

## The sales-tax rate is hard-coded in checkout, invoicing, and refunds. What is the best fix?

- [x] One service owns the rate, and each order stores the rate it applied.
- [ ] Put the rate in a shared library constant that every service imports.
- [ ] Copy the new rate into all three places whenever it changes.
- [ ] Have refunds always use today's rate, so the numbers stay consistent.

**Why:** One owner holds the fact, and the order records the rate used, so refunding a 2025 purchase doesn't use a 2026 rate. A shared constant would tie separate services' releases together. See [[dry]].

## Which of these is a sound exception to DRY?

- [x] Two teams deliberately keep separate copies of similar logic so they can evolve independently.
- [ ] Two modules in one service compute the same discount rule in slightly different ways.
- [ ] A configuration value is copied into four files because a shared config felt like extra work.
- [ ] A business rule is restated in the UI and the API so each can be read without the other.

**Why:** Prototypes, generated code, and deliberate independence are legitimate reasons to repeat. Copying the same business rule within one system is what DRY warns against. See [[dry]].
