# Quiz: Backpressure

## A marketing campaign triples uploads to an image service. Which design survives without losing accepted jobs?

- [x] A bounded, durable queue; when it's full, the API returns `503` with `Retry-After`.
- [ ] An unbounded in-memory queue, so every upload is accepted immediately.
- [ ] Clients retrying instantly on any error until their upload is accepted.
- [ ] Doubling every timeout so slow requests eventually finish.

**Why:** Unbounded queues grow until the service runs out of memory and loses everything. Bound the queue and reject early and clearly. See [[backpressure]].

## Why is "just add a queue" not a fix for overload on its own?

- [x] A queue only delays the problem; without a bound and a signal upstream it grows until it fails.
- [ ] Queues always lose messages under heavy load.
- [ ] Queues make every request slower, even when load is low.
- [ ] A queue prevents autoscaling from seeing the load.

**Why:** Backpressure means telling producers to slow down. A queue smooths bursts but can't absorb a sustained overload. See [[backpressure]].

## The autoscaler adds workers based on queue depth. Where does that stop helping?

- [x] When the database behind the workers is the bottleneck; more workers just move the overload.
- [ ] Never, as long as the cloud provider has spare capacity.
- [ ] When the queue holds more than 100 items.
- [ ] As soon as clients start receiving `503` responses.

**Why:** Every fix has a limit. Scaling one layer pushes load onto the next, so backpressure has to reach the real constraint. See [[backpressure]].
