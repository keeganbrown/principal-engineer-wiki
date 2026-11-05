---
title: Secrets Management
category: practices
summary: Keep credentials out of code, images, logs, and agent environments: deliver them at run time, scope each one narrowly, keep it short-lived, and make rotation routine.
tags: [security, credentials, operations]
---

# Secrets Management

> **In one sentence:** Keep credentials out of code, images, logs, and agent environments: deliver them at run time, scope each one narrowly, keep it short-lived, and make rotation routine.

## The idea

A **secret** is anything that grants access: a password, an API key, a database credential, a signing key, a token. Secrets management is how you store them, deliver them to the code that needs them, limit what each one can do, and replace them. Most leaks don't come from a broken vault. They come from copies: a key pasted into code, baked into an image, printed in a build log, or left on a laptop.

A **secrets manager** holds secrets encrypted, controls who may read each one, and logs every read. Examples are HashiCorp Vault and the stores built into each cloud provider. Better still is a secret you never store: **short-lived credentials** issued on demand to a workload that proves its identity, so there's nothing long-lived to leak.

## Why it matters

- **Leaked keys get found fast.** Automated scanners watch public repositories, and exposed cloud keys can be found and abused within minutes. A private repository only narrows who finds them.
- **Secrets copy themselves.** Every image, log line, backup, and clone that holds one is another place to leak from, and you can't recall a copy.
- **Rotation is the real test.** A secret you can't change without an outage is one you won't change after a leak.
- **Centralizing has a cost.** A secrets manager puts every key in one place: it becomes a critical dependency and the most valuable thing to attack, so lock down who can administer it.

## How to apply it

- **Deliver secrets at run time.** The service reads them from the secrets manager, or from a file or environment variable the platform fills in at startup. Never put them in the repository, an image, or infrastructure-as-code state in plain text ([[infrastructure-as-code]], [[containers-and-kubernetes]]).
- **Prefer identity over stored keys.** Let workloads and pipelines authenticate as themselves — cloud workload identity, or continuous integration (CI) trading a signed token for temporary cloud credentials — and get credentials that expire in minutes or hours. The cost is setup on each platform, and authentication failures are harder to debug.
- **Scope each secret narrowly.** Use one credential per service and environment, with only the permissions it needs ([[threat-modeling]] covers least privilege). A shared "production key" turns every leak into a total one.
- **Make rotation routine.** Automate it, and let old and new versions both work during a short overlap so callers can switch without an outage. A rotation you've never run is a plan, not a capability.
- **Scan for leaks.** Run a secret scanner as a pre-commit hook and in CI, and scrub tokens from logs ([[observability]]). Scanners miss custom formats and raise false alarms, so treat them as a net, not a guarantee.
- **Keep secrets out of agents' reach.** A coding agent can read environment variables and files in its workspace; give tool connections their own credentials outside it ([[agent-guardrails]]).
- **Plan for the manager being down.** Cache secrets at startup so running services survive an outage of the manager. Cached values don't pick up a rotation until they refresh, so keep the overlap longer than the refresh interval.

## Example

A scan of a company's repositories finds a database password committed three years ago in a config file. Deleting the line isn't enough: the password is still in the history, in every clone, and possibly in old build logs. The only fix is to rotate it.

Rotating it is the hard part, because nobody knows everything that uses it. The team finds the main service, a reporting job, and an analyst's notebook. They create a second credential, move each user over, and watch the database's connection logs until the old credential has been quiet for a week, then revoke it. A nightly export nobody had listed breaks that night and is moved over the next morning.

Afterward, each service gets its own credential from the secrets manager at startup, rotated every 30 days with a one-day overlap, and a pre-commit scanner blocks new commits that contain credentials. The cost: two weeks of one engineer's time, and a secrets manager that is now a critical dependency, so services cache the last value they fetched.

## Common traps

- **Deleting the commit and calling it fixed.** History and clones keep the secret. Treat any committed secret as leaked, and rotate it.
- **Real credentials "just for development."** A shared development key in an environment file spreads to every laptop and image. Use fakes or local services, with per-person credentials where real ones are needed ([[reproducible-dev-environments]]).
- **One credential for everything.** You can't tell which service leaked it, and you can't rotate it without touching all of them.
- **Secrets in error messages and build output.** A failed connection that prints its connection string publishes the password to everyone who can read the log.
- **Rotation that has never run.** The first rotation, done during an incident, is when you discover the forgotten consumer.

## When it doesn't apply

A local prototype that talks only to fakes, with no real credentials, needs none of this yet; add it before the first real credential appears. A small team on one platform can start with the platform's built-in secret store rather than running a separate manager. And where every platform you use offers workload identity, you may need very few stored secrets at all.

## Related

- [[threat-modeling]] — least privilege, and where secrets sit among the other threats.
- [[infrastructure-as-code]] — state files often hold secrets in plain text.
- [[containers-and-kubernetes]] — inject secrets at run time instead of baking them into images.
- [[agent-guardrails]] — keeping credentials away from coding agents.
- [[observability]] — scrub secrets from logs and traces at the source.
- [[reproducible-dev-environments]] — environments defined as code without credentials baked in.
