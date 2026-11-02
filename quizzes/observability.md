# Quiz: Observability

## Checkout is slow. What is the fastest path to the cause?

- [x] Dashboard shows when p99 jumped, traces show which service is slow, the span points to the query.
- [ ] Search all logs for the word "error" across every service.
- [ ] Add new log lines, deploy, and wait for the problem to happen again.
- [ ] Restart each service one by one until latency drops.

**Why:** Metrics show *when*, traces show *where*, and spans or logs show *why*. Good telemetry answers new questions without shipping new code. See [[observability]].

## What should alerts fire on?

- [x] Symptoms users feel, such as error rate or latency against a service level objective.
- [ ] Every cause that might lead to a problem, such as high CPU on any host.
- [ ] Every log line written at the warning level or above.
- [ ] Any change in traffic, up or down, greater than 5%.

**Why:** Cause-based alerts fire constantly and train people to ignore them. Alert on what users feel. See [[observability]].

## Why are user IDs a bad label on a metric?

- [x] High-cardinality labels create a time series per value, which explodes cost.
- [ ] Metrics can't store string values at all.
- [ ] User IDs change every time a user logs in.
- [ ] Labels are only allowed on log lines, not metrics.

**Why:** Per-user detail belongs in logs and traces. High-cardinality metric labels are a listed trap. See [[observability]].
