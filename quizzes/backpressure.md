# Quiz: Backpressure

## A marketing campaign triples uploads to an image service. Which design survives without losing accepted jobs?

- [x] A bounded, durable queue, with `503` and `Retry-After` when it's full.
- [ ] An unbounded in-memory queue, so that every upload is accepted immediately.
- [ ] Clients retrying instantly on any error until their upload is finally accepted.
- [ ] Doubling every timeout so that slow requests get the time to finish.

**Why:** Unbounded queues grow until the service runs out of memory and loses everything. Bound the queue and reject early and clearly. See [[backpressure]].

## An upload API rejects work with `503` when its queue is full. A browser upload form can't hold the photo and retry. What should the team do for it?

- [x] Accept its uploads into a larger store with its own cap and an age alert.
- [ ] Nothing; a `503` is a clear signal, and the user can retry later.
- [ ] Remove the queue's bound for the web form so its uploads are never rejected.
- [ ] Make the browser retry instantly in a loop until the upload is accepted.

**Why:** Rejection doesn't make the work disappear; it hands the waiting back to the client. The overflow store is still a queue, so it needs a cap, and an alert on its oldest item. See [[backpressure]].

## Why is "just add a queue" not a fix for overload on its own?

- [x] Without a bound and a signal upstream, it grows until it fails.
- [ ] Queues lose messages once the load passes a certain level.
- [ ] Queues make every request slower, even when load is low.
- [ ] A queue hides the load from the autoscaler, so it never scales.

**Why:** Backpressure means telling producers to slow down. A queue smooths bursts but can't absorb a sustained overload. See [[backpressure]].

## The autoscaler adds workers based on queue depth. Where does that stop helping?

- [x] When the database behind the workers is the bottleneck.
- [ ] Only once the cloud provider runs out of spare capacity.
- [ ] When the queue holds more than a few hundred waiting items.
- [ ] As soon as clients start receiving `503` responses from the API.

**Why:** Scaling one layer pushes load onto the next, so more workers just move the overload. Backpressure has to reach the real constraint. See [[backpressure]].
