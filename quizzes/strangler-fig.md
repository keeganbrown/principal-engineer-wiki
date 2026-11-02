# Quiz: Strangler Fig

## What is the first step in a strangler fig migration?

- [x] Put a routing layer, such as a proxy, in front of the old system.
- [ ] Copy the old database into the new system so both share the data.
- [ ] Rewrite the riskiest part of the system first, to retire risk early.
- [ ] Freeze the old system so its behavior stops changing under you.

**Why:** The routing layer lets you move one slice of traffic at a time to the new code. See [[strangler-fig]].

## A team wants to run a new payment-capture slice in shadow mode next to the old one. What must they do?

- [x] Stub the new slice's side effects, or customers get charged twice.
- [ ] Nothing special; shadow mode only copies traffic, so it's safe.
- [ ] Route all live traffic to the new slice first, then compare results.
- [ ] Run the shadow for a single day at most, so the cost stays low.

**Why:** Comparing outputs on real traffic catches differences before users see them, but only for reads and calculations. On a write path, shadowing would send every email and charge twice. See [[strangler-fig]].

## A strangler fig migration has moved most traffic, and then priorities shift. What's the risk?

- [x] Two systems run side by side indefinitely, and nobody deletes the old one.
- [ ] The new system gets slower, because the routing layer adds a network hop.
- [ ] The first slices have to be redone, because the old code has changed.
- [ ] The routing layer starts sending traffic to the old system on its own.

**Why:** Plan to delete the old code. In the example, the last two slices, which touched shared data, took as long as the first ten. See [[strangler-fig]].

## A slice moved to the new system is failing. When can you safely route it back?

- [x] When the old system can read whatever the new one wrote.
- [ ] Whenever the routing layer supports switching traffic.
- [ ] Only within the first hour or so after the slice moved over to it.
- [ ] Only if the new system's database has been deleted.

**Why:** Routing back limits risk only while data stays compatible both ways. Plan the data path before the switch. See [[strangler-fig]] and [[expand-and-contract]].
