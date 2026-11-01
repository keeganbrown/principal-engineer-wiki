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

Between steps, the system is always fully working. Until you stop writing the old shape, any step can be rolled back by redeploying the previous version. Stopping writes to the old shape (step 4) is the real [[reversible-decisions|one-way door]], so measure before you take it. Dropping the old thing (step 5) just makes that permanent.

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

2. **Backfill.** Once step 1 is on every server, copy `name` into `fullName` in batches, each one a single in-database statement: `UPDATE users SET fullName = name WHERE fullName IS NULL AND id BETWEEN …`.
3. **Switch reads.** Deploy code that reads `fullName`. Keep writing both, so you can still roll back.
4. **Stop writing the old.** Deploy code that writes only `fullName`. From here, rolling back would read stale data from `name`.

**Contract**

5. Drop the `name` column.

Guidelines:

- **Don't merge two steps into one deploy.** That recreates the breaking change.
- **Measure before you stop writing the old.** Use query logs or usage metrics to confirm nothing still reads it; after step 4, anything that does reads stale data.
- **Make backfills safe to rerun.** Each batch should be [[idempotency|idempotent]] — running it twice has the same effect as once — and resumable after a failure.
- **Decide on purpose whether to contract.** For a public API, usage of an old field may never reach zero. Keeping a cheap deprecated field forever is a legitimate choice — make it deliberately and record it.

## Example

The hard part of the rename isn't the steps — it's the writes that happen *during* them.

Suppose the team starts the backfill before step 1 has reached every server. The backfill copies row 42's `name` at 10:00. At 10:01, a user edits their profile on a server still running *old* code, which writes only `name` — and row 42's `fullName` is now stale for good. That's why the backfill waits until the dual write is fully deployed.

The backfill's form matters too. If it read `name` in application code and wrote `fullName` a moment later, it could overwrite a dual-written edit made in between. A single `UPDATE … WHERE fullName IS NULL` per batch is atomic per row, safe to rerun, and never touches a value the dual write already set.

The team also finds a nightly report, owned by the finance team, that queries `name` directly; it isn't in any codebase they own. They spot it in database query logs *before* step 4. Had they found it after, the report would already have been showing stale names.

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
- [[reversible-decisions]] — every step before you stop writing the old shape is reversible.
