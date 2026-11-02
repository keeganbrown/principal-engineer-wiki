# Quiz: Observability

## Checkout is slow. What is the fastest path to the cause?

- [x] Use metrics to see when it slowed, then traces to find the slow call.
- [ ] Alert on CPU for every host and check whichever one is running high.
- [ ] Add new log lines, deploy them, and wait for the slowdown to return.
- [ ] Restart each service one by one until checkout latency finally drops again.

**Why:** Metrics show when, traces show where, and spans or logs show why. Good telemetry answers new questions without shipping new code. See [[observability]].

## Which condition should page someone?

- [x] Checkout errors rising against its service level objective (SLO).
- [ ] CPU on any host passing 80%, since it may lead to a slowdown.
- [ ] A circuit breaker opening on a call that has a working fallback.
- [ ] Any change in overall traffic, up or down, of more than five percent.

**Why:** Page on symptoms users feel, and send most cause signals to dashboards; non-actionable pages teach people to ignore alerts. The exception is a near-certain failure, like a disk about to fill. See [[observability]].

## Why are user IDs a bad label on a metric?

- [x] Each unique value creates its own time series, so cost explodes.
- [ ] Metrics can't store string values of any kind, only numbers.
- [ ] User IDs change every time a user logs in again.
- [ ] Labels are allowed only on log lines, never on metric data points.

**Why:** Millions of users means millions of series. Per-user detail belongs in logs and traces. See [[observability]].
