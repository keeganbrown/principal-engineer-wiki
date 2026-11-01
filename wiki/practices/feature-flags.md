---
title: Feature Flags
category: practices
summary: Wrap new behavior in a runtime switch so you can deploy code without releasing it, roll out gradually, and turn it off instantly if something goes wrong.
tags: [delivery, release, risk]
---

# Feature Flags

> **In one sentence:** Wrap new behavior in a runtime switch so you can deploy code without releasing it, roll out gradually, and turn it off instantly if something goes wrong.

## The idea

A feature flag (also called a feature toggle) is an `if` statement whose condition is controlled outside the code — by a config file, database, or flag service:

```
if flags.isEnabled("new-checkout", user):
    renderNewCheckout()
else:
    renderOldCheckout()
```

This separates two things that are usually bundled together:

- **Deploy** — putting code on servers (a technical event).
- **Release** — letting users see the change (a business event).

## Why it matters

- **Smaller, safer merges.** Unfinished work can merge to the main branch, hidden behind a flag. No long-lived branches.
- **Gradual rollouts.** Turn a feature on for 1% of users, watch the metrics, then 10%, 50%, 100%.
- **Instant rollback.** Flipping a flag takes seconds; redeploying takes minutes or more.
- **Experiments.** Show variants to different groups and measure which works better (A/B testing).

## How to apply it

Know which kind of flag you're making — they have different lifetimes:

| Type | Purpose | Lifetime |
| --- | --- | --- |
| Release | Hide unfinished work | Days to weeks |
| Experiment | A/B test a variant | Weeks |
| Ops / kill switch | Disable a costly or risky feature under load | Long-lived |
| Permission | Enable for certain customers or plans | Long-lived |

Guidelines:
- Give every release flag an **owner and an expiry date**. Delete it soon after full rollout.
- Keep flag checks at the **edges** (one decision point), not scattered through the code.
- **Test both paths** while the flag exists.
- Use a **default that's safe** if the flag service is unreachable — usually "off."
- Pair rollouts with dashboards so you can see the impact of each step.

## Example

A team rebuilds search. They merge small PRs behind `new-search` for three weeks, invisible to users. They enable it for internal staff, then 5% of users. Error rates stay flat, but latency rises 30%. They turn it off, fix a missing cache, and roll out again. At 100% for a week, they delete the flag and the old code path.

No big-bang release, no late-night rollback deploy.

## Common traps

- **Flag debt.** Hundreds of stale flags make code unreadable and untestable. Treat cleanup as part of the feature.
- **Nested flags.** Flags that depend on other flags create combinations nobody has tested.
- **Reusing an old flag name** for new behavior — this has caused real, expensive outages.
- **Using flags as a substitute for configuration management** or permissions systems without proper auditing.

## When it doesn't apply

Tiny, low-risk changes don't need a flag; the overhead isn't worth it. Some changes can't be flagged cleanly — database schema migrations, for example, need expand-and-contract techniques instead. Teams without good monitoring get less value from gradual rollouts, since they can't see the effect of each step.

## Related

- [[observability]] — you need metrics to know whether a rollout is healthy.
- [[strangler-fig]] — flags are a common way to route traffic from old code to new.
- [[technical-debt]] — stale flags are a classic form of debt.
- [[code-review]] — flags let you keep each PR small and reviewable.
