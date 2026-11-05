# Quiz: You Aren't Gonna Need It (YAGNI)

## You're building CSV export. A teammate proposes a pluggable `Exporter` for CSV, JSON, XML, and Parquet. What does YAGNI suggest?

- [x] Write `exportCsv(rows)` with tests, and add formats when asked.
- [ ] Build the pluggable interface now, so new formats are cheap to add.
- [ ] Skip tests on the CSV export, since the plugin may replace it later.
- [ ] Build CSV and JSON now, and leave XML and Parquet as stubs for later.

**Why:** Guesses about the future are often wrong and always cost something now. Good tests make the later change cheap. See [[yagni]].

## What makes YAGNI safe to follow?

- [x] Tests and clean code keep later changes cheap.
- [ ] Most products are retired before anyone asks for a second feature.
- [ ] Customers rarely change their requirements once a feature ships.
- [ ] Flexible code tends to be slower, so skipping it improves performance.

**Why:** YAGNI depends on code being easy to change. Using it as an excuse to skip quality defeats it. See [[yagni]].

## The signed contract says the product must run in two regions by Q2. Does YAGNI say to wait until Q2 to design for it?

- [x] No; a known, committed requirement isn't speculation.
- [ ] Yes; wait until the requirement is actually being built.
- [ ] Yes, because contracts often change before the deadline.
- [ ] No, and every other region should be designed in too.

**Why:** YAGNI targets imagined futures. Plan for what's committed, and still skip what nobody has asked for. See [[yagni]].
