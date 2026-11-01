---
title: Expand and Contract
category: practices
summary: Change a schema or interface in three backward-compatible steps — add the new, move everyone over, then remove the old — so nothing breaks mid-change.
tags: [migration, compatibility, databases]
---

# Expand and Contract

> **In one sentence:** Change a schema or interface in three backward-compatible steps — add the new, move everyone over, then remove the old — so nothing breaks mid-change.

## The idea

In a running system, you can't change everything at once. During a deploy, old and new versions of your code run side by side. Other services, mobile apps, and batch jobs keep using the old shape until they're updated. If you rename a database column or an API field in one step, something breaks.

**Expand and contract** (also called a *parallel change*) splits a breaking change into safe steps:

1. **Expand** — add the new thing *alongside* the old. Both work.
2. **Migrate** — move every reader and writer to the new thing, and copy existing data across.
3. **Contract** — once nothing uses the old thing, remove it.

At every point between steps, the system is fully working and every step can be rolled back.

## Why it matters

- **Zero-downtime changes.** No "maintenance window" to rename a column.
- **Safe rolling deploys.** A rolling deploy updates servers a few at a time, so old and new code briefly coexist; expand and contract makes that harmless.
- **Independent teams.** Consumers move on their own schedule instead of in a coordinated big-bang release.
- **Easy rollback.** Until the contract step, going back is just redeploying the old code.

## How to apply it

For a database column rename (`name` → `full_name`):

1. **Expand.** Add the `full_name` column. Deploy code that *writes both* columns and still *reads* `name`.
2. **Backfill.** Copy `name` into `full_name` for existing rows, in batches to avoid locking the table.
3. **Switch reads.** Deploy code that reads `full_name`. Keep writing both, so you can roll back.
4. **Stop writing the old.** Deploy code that writes only `full_name`.
5. **Contract.** Drop the `name` column.

General guidelines:

- **One deploy per step.** Don't combine steps "to save time" — that recreates the breaking change.
- **Measure before contracting.** Use logs, query stats, or API usage metrics to confirm nothing still touches the old thing.
- **Set a deadline for the contract step.** Otherwise you'll keep both forever.
- **Make backfills idempotent and resumable,** so a failure halfway can be restarted safely.

## Example

An API returns `{ "name": "Ada Lovelace" }` and needs separate first and last names.

- **Expand:** return `name`, `firstName`, and `lastName`. Mark `name` deprecated.
- **Migrate:** watch usage of `name` fall as clients update; contact the stragglers.
- **Contract:** six months later, usage is zero. Remove `name`.

No client broke, and no release had to be coordinated across teams.

## Common traps

- **Never contracting.** Old columns and fields pile up and confuse everyone.
- **Skipping the dual-write step,** so data written during the migration is lost from one side.
- **Huge backfills in one transaction** that lock tables and cause an outage.
- **Forgetting non-code readers:** reports, data pipelines, and analysts' queries also use the old column.

## When it doesn't apply

If you control every reader and writer and can take a short downtime — an internal tool, a prototype, an empty table — a direct change is simpler. Additive changes (a new optional field, a new table) don't need the full dance; they're already "expand" with nothing to contract.

## Related

- [[api-versioning]] — expand and contract is the default way to evolve an API.
- [[feature-flags]] — flags can switch reads from old to new during the migrate step.
- [[strangler-fig]] — the same idea, applied to replacing a whole system.
- [[contract-testing]] — tells you when a change would break a consumer.
- [[reversible-decisions]] — expand and contract keeps a change reversible until the last step.
