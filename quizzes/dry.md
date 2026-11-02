# Quiz: DRY (Don't Repeat Yourself)

## Two functions have identical code, but one validates shipping addresses and the other billing addresses, owned by different teams. What does DRY suggest?

- [x] Keep them separate until the rules prove to be the same.
- [ ] Merge them right away, since identical code is duplicated knowledge.
- [ ] Move them into a shared library that both teams must release together.
- [ ] Delete one, and have both teams call the other team's function directly.

**Why:** DRY is about knowledge, not code. They look alike, but billing may have to match the card issuer's format while shipping supports PO boxes. Look-alike code waits for the third copy. See [[dry]].

## The sales-tax rate is hard-coded in checkout, invoicing, and a separately deployed refunds service. What is the best fix?

- [x] Give the pricing service the rate, and store the applied rate on each order.
- [ ] Put the rate in a shared library constant that every service imports.
- [ ] Copy the new rate into all three places whenever it changes.
- [ ] Have refunds use today's rate, so they match current invoices.

**Why:** Refunding a 2025 purchase at a 2026 rate would be wrong. A shared constant would tie refunds' releases to everyone else's. The cost is a runtime dependency: checkout needs pricing up, or a cached rate. See [[dry]].

## Which of these is a sound exception to DRY?

- [x] Two teams keep separate copies of similar logic to evolve independently.
- [ ] Two modules in one service compute the same discount rule slightly differently.
- [ ] A configuration value is copied into four files so each service can start alone.
- [ ] A discount rule is pasted into a second module because importing it felt awkward.

**Why:** Prototypes, generated code, and deliberate independence are legitimate reasons to repeat. Copying the same business rule within one system is what DRY warns against. See [[dry]].
