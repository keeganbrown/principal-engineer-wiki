# Quiz: Expand and Contract

## What are the three phases of expand and contract?

- [x] Add the new shape, move every reader and writer over, then remove the old.
- [ ] Freeze writes, migrate the data, then unfreeze writes.
- [ ] Deploy the new code, roll back if needed, then deploy again.
- [ ] Copy the table, swap the names, then drop the copy.

**Why:** Splitting a breaking change into backward-compatible phases means old and new versions can run side by side. See [[expand-and-contract]].

## While renaming `name` to `fullName`, why must the backfill wait until the dual write is fully deployed?

- [x] Servers still on old code write only `name`, leaving rows the backfill already copied stale.
- [ ] Backfills run faster once the dual write has been deployed everywhere.
- [ ] The database locks the table while the dual write is rolling out.
- [ ] The new column doesn't exist until every server runs the new code.

**Why:** Writes during the change are the hard part. A row copied at 10:00 and edited on an old server at 10:01 stays stale for good. See [[expand-and-contract]].

## When can you skip the full dance?

- [x] Adding a new optional field, which is already "expand" with nothing to contract.
- [ ] Renaming a column used by a mobile app.
- [ ] Changing a column's type in a busy production table.
- [ ] Splitting one table into two that other services read.

**Why:** Additive changes don't need it. So does a change where you control every reader and writer and can take short downtime. See [[expand-and-contract]].
