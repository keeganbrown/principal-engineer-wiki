# Quiz: Expand and Contract

## A team adds `fullName` and switches every read to it in the same deploy as the new write. What goes wrong?

- [x] Rows not yet backfilled read as empty until the backfill catches up.
- [ ] Nothing; one deploy is safer than several, so merging the steps helps.
- [ ] The database rejects the deploy, since a column can't be read and written at once.
- [ ] Old servers start writing to `fullName` too, so its data is duplicated.

**Why:** Each step must be backward-compatible on its own: add, dual-write, backfill, switch reads, stop writing the old, remove it. Don't merge two steps into one deploy. See [[expand-and-contract]].

## While renaming `name` to `fullName`, why must the backfill wait until the dual write is fully deployed?

- [x] Old servers still write only `name`, so rows already copied go stale.
- [ ] Backfills run much faster once the dual write is deployed everywhere.
- [ ] The database locks the whole table while the dual write is rolling out.
- [ ] The new column doesn't exist until every server runs the new code.

**Why:** Writes during the change are the hard part. A row copied at 10:00 and edited on an old server at 10:01 stays stale for good. See [[expand-and-contract]].

## Which step of expand and contract can't be undone by redeploying the previous version?

- [x] Stopping writes to the old shape.
- [ ] Adding the new column.
- [ ] Backfilling the new column.
- [ ] Switching reads to the new shape.

**Why:** After that step, rolling back would read stale data from the old shape. Measure with query logs that nothing still reads it first. See [[expand-and-contract]].

## When can you skip the full expand-and-contract sequence?

- [x] When adding a new optional field, with nothing to contract.
- [ ] When renaming a column that a mobile app reads.
- [ ] When changing a column's type in a busy production table.
- [ ] When splitting one table into two that other services read.

**Why:** Additive changes don't need it, and neither does a change where you control every reader and writer and can take a short downtime. See [[expand-and-contract]].
