---
title: Expand and Contract
category: practices
summary: Change a schema or interface in backward-compatible phases — add the new, move everyone over, then remove the old — so nothing breaks mid-change.
tags: [migration, compatibility, databases]
---

# Expand and Contract

> **In one sentence:** Change a schema or interface in backward-compatible phases — add the new, move everyone over, then remove the old — so nothing breaks mid-change.

## The idea

In a running system, you can't change everything at once. During a deploy, old and new versions of your code run side by side. Other services, mobile apps, and batch jobs keep using the old shape until they're updated. If you rename a database column or an API field in one step, something breaks.

**Expand and contract** splits a breaking change into three phases:

1. **Expand** — add the new thing *alongside* the old. Both work.
2. **Migrate** — move every reader and writer to the new thing, and copy existing data across.
3. **Contract** — once nothing uses the old thing, remove it.

Between steps, the system is always fully working. Until you stop writing the old shape, any step can be rolled back by redeploying the previous version. The contract step deletes the old thing, so it's a [[reversible-decisions|one-way door]] — measure before you take it.

The technique is also called *parallel change*, a name from Danilo Sato's 2014 article on martinfowler.com.

## Why it matters

- **Changes need no downtime.** No "maintenance window" to rename a column.
- **Rolling deploys become safe.** A rolling deploy updates servers a few at a time, so old and new code briefly coexist; expand and contract makes that harmless.
- **Teams move on their own schedule.** Consumers update independently instead of in a coordinated big-bang release.
- **It costs time and temporary complexity.** One rename becomes five deploys, often spread over weeks, plus dual-write code someone must remember to delete.

## How to apply it

Renaming a database column `name` → `fullName`, in five deploys:

**Expand**
1. Run a migration that adds the `fullName` column. Then deploy code that *writes both* columns (a **dual write**) and still *reads* `name`.

**Migrate**

2. **Backfill.** Copy `name` into `fullName` for existing rows, in batches to avoid locking the table.
3. **Switch reads.** Deploy code that reads `fullName`. Keep writing both, so you can still roll back.
4. **Stop writing the old.** Deploy code that writes only `fullName`. From here, rolling back would read stale data from `name`.

**Contract**

5. Drop the `name` column.

Guidelines:

- **Don't merge two steps into one deploy.** That recreates the breaking change.
- **Measure before contracting.** Use query logs or usage metrics to confirm nothing still touches the old thing.
- **Make backfills safe to rerun.** Each batch should be [[idempotency|idempotent]] — running it twice has the same effect as once — and resumable after a failure.
- **Decide on purpose whether to contract.** For a public API, usage of an old field may never reach zero. Keeping a cheap deprecated field forever is a legitimate choice — make it deliberately and record it.

## Example

The hard part of the rename isn't the steps — it's the writes that happen *during* them.

The backfill copies row 42's `name` at 10:00. At 10:01, a user edits their profile, and the request lands on a server still running *old* code, which writes only `name`. Row 42's `fullName` is now stale. This is exactly why step 1 dual-writes: once every server writes both columns, edits during the backfill update both, and the backfill can't miss them.

The team also finds a nightly report, owned by the finance team, that queries `name` directly. It isn't in any codebase they own. They only spot it because they checked database query logs before step 5.

## Common traps

- **Skipping the dual write.** Data written mid-migration ends up in only one column.
- **Running huge backfills in one transaction.** They lock tables and cause an outage.
- **Forgetting non-code readers.** Reports, data pipelines, and analysts' queries also use the old column.
- **Never contracting by accident.** Old columns and fields pile up and confuse everyone when nobody decides.

## When it doesn't apply

If you control every reader and writer and can take a short downtime — an internal tool, a prototype, an empty table — a direct change is simpler. Additive changes (a new optional field, a new table) don't need the full dance; they're already "expand" with nothing to contract.

## Related

- [[api-versioning]] — expand and contract is the default way to evolve an API.
- [[feature-flags]] — a flag can control the read switch in step 3.
- [[strangler-fig]] — the same idea, applied to replacing a whole system.
- [[contract-testing]] — tells you when a change would break a consumer.
- [[reversible-decisions]] — every step but the last keeps the change reversible.
