---
title: Object Storage
category: technology
summary: Store files and large blobs in a cheap, durable, nearly unlimited object store addressed by key, and keep only references to them in your database.
tags: [storage, files, cloud, durability]
---

# Object Storage

> **In one sentence:** Store files and large blobs in a cheap, durable, nearly unlimited object store addressed by key, and keep only references to them in your database.

## The idea

**Object storage** keeps files — called **objects** — in flat containers called **buckets**, each object addressed by a key like `invoices/2026/10/inv-4821.pdf`. You put, get, list, and delete whole objects over HTTP. There are no folders in the filesystem sense, and most object stores can't edit part of a file in place or append to it; a few specialized storage classes allow appends.

In exchange for that simple interface, you get storage that is very cheap per gigabyte, effectively unlimited, and highly durable: providers replicate each object across several machines and data centers. Amazon S3 (launched in 2006) defined the category, and its API became a de facto standard that many other products copy.

## Why it matters

- **Databases are poor file stores.** Large blobs bloat backups, slow replication, and cost far more per gigabyte in a database than in object storage.
- **Durability is built in.** Providers replicate every object across machines and sites, far beyond what a team gets from disks on its own servers.
- **It scales without planning.** You don't provision capacity; you pay for what you store and transfer.

The limits: each request has latency measured in milliseconds, there's no in-place editing, and listing millions of keys is slow. It's storage for whole files, not a database or a disk.

## How to apply it

- **Store the file in object storage, the reference in the database.** The database row holds the key, size, type, and checksum; the bytes live in the bucket.
- **Upload and download directly from clients.** Issue a short-lived **pre-signed URL** — a link that grants one operation on one object for a few minutes — so large files don't pass through your servers.
- **Keep buckets private by default.** Public buckets are a leading cause of data leaks. Serve public content through a CDN (content delivery network) in front of a private bucket ([[load-balancers-and-cdns]]).
- **Use lifecycle rules.** Move old objects to cheaper storage classes and delete what you no longer need automatically.
- **Turn on versioning for important data.** Keeping previous versions protects against accidental overwrites and deletes, at the cost of paying to store them.
- **Design keys for your access patterns.** Prefixes like `tenant-42/2026/10/` make listing and lifecycle rules per tenant or month easy.

## Example

An app stores user-uploaded photos as binary columns in PostgreSQL. The database grows to 2 TB, backups take nine hours, and a replica falls hours behind after a bulk upload.

The team moves photos to a private bucket. Uploads go straight from the mobile app via pre-signed URLs; the app then calls the API to record the key and checksum. Downloads go through a CDN that reads from the bucket. The database shrinks to 40 GB.

The hard part is the gap between upload and record: if the app uploads but crashes before calling the API, an orphaned object remains. A nightly cleanup job deletes objects older than 24 hours with no matching row. It's idempotent, because deleting an already-deleted object is harmless, and it skips anything newer than 24 hours, so it can't race an upload in progress. The storage team owns it.

## Common traps

- **Public buckets.** One misconfigured permission exposes everything. Many providers now block public access by default, so leaks come from exceptions made casually. Block public access at the account level and make exceptions deliberately.
- **Treating it like a filesystem.** Renaming a "folder" means copying every object under that prefix. Appending to a file means rewriting it.
- **Many tiny objects.** Request costs and latency dominate when objects are a few bytes. Batch small records into larger files.
- **Forgetting egress costs.** Storage is cheap; transferring data out of the provider often isn't. Check the bill model before serving heavy traffic from a bucket directly.
- **No cleanup.** Without lifecycle rules, buckets grow forever with temp files and old versions.

## When it doesn't apply

Small structured data that you query and update field by field belongs in a database. Workloads that need low-latency random reads and writes inside a file — a database's own data files, for example — need block storage (a raw virtual disk attached to one machine) or a real filesystem. Object storage is for whole files you write once and read many times.

## Related

- [[relational-databases]] — holds the references and metadata; the bucket holds the bytes.
- [[load-balancers-and-cdns]] — how stored files reach users quickly.
- [[idempotency]] — why cleanup and upload retries must be safe to repeat.
- [[infrastructure-as-code]] — define buckets and their access rules as reviewed code.
