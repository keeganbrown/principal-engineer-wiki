# Quiz: You Aren't Gonna Need It (YAGNI)

## You're building CSV export. A teammate proposes a pluggable `Exporter` for CSV, JSON, XML, and Parquet. What does YAGNI suggest?

- [x] Write `exportCsv(rows)` with tests now, and add other formats when someone asks.
- [ ] Build the pluggable interface now, since adding formats later is always costly.
- [ ] Skip tests on the CSV export, since you might replace it with the plugin later.
- [ ] Build CSV and JSON now, and leave XML and Parquet as stubs for later.

**Why:** Guesses about the future are often wrong and always cost something now. Good tests make the later change cheap. See [[yagni]].

## Why does YAGNI work at all?

- [x] Tests and clean code make later changes cheap, so there's little reason to pay for them now.
- [ ] Most products are retired before anyone asks for a second feature.
- [ ] Customers rarely change their requirements once a feature ships.
- [ ] Flexible code is always slower, so skipping it improves performance.

**Why:** YAGNI depends on code being easy to change. Using it as an excuse to skip quality defeats it. See [[yagni]].

## Where does YAGNI apply least?

- [x] A public API shape that ten partner teams will build on.
- [ ] An internal helper function used by one module.
- [ ] A configuration option nobody has asked for yet.
- [ ] A second export format with no customer request.

**Why:** One-way doors — public APIs, large schemas, shared formats — are expensive to change later. Spend more thought up front there. See [[yagni]] and [[reversible-decisions]].
