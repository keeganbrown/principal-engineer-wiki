# Quiz: Containers and Kubernetes

## A 40-engineer company with six services has slow, scary deploys. What should it do first?

- [x] Containerize the services and use a managed container platform.
- [ ] Adopt self-hosted Kubernetes and build a platform team right away.
- [ ] Rewrite all six services as serverless functions over the next year.
- [ ] Keep the hand-run deploy scripts and write more detailed documentation.

**Why:** The real pain was deploys and drift, not scheduling across hundreds of machines. Containerize first; orchestrate when you need it. See [[containers-and-kubernetes]].

## Where should a container's secrets come from?

- [x] Injected at run time.
- [ ] Baked into the image at build time.
- [ ] A config file next to the Dockerfile.
- [ ] Build arguments set during the image build.

**Why:** Anything baked into an image can be read by anyone who can pull it. See [[containers-and-kubernetes]].

## Why set memory limits on containers?

- [x] So one leaking container can't starve others.
- [ ] So the scheduler knows how much memory to reserve on each machine.
- [ ] So the image build stays small and pulls quickly on deploy.
- [ ] So the container can move between cloud providers unchanged.

**Why:** A limit is the most a container may use; a request is what the scheduler reserves. Without limits, one bad container takes down its neighbors. See [[containers-and-kubernetes]].

## A container keeps restarting while it warms up its cache, before it's ready for traffic. What's likely wrong?

- [x] Its liveness check is doing a readiness check's job.
- [ ] Its memory limit is set higher than its memory request.
- [ ] Its image is too large to start within the default timeout.
- [ ] Its secrets are injected at run time instead of build time.

**Why:** Readiness says "send me traffic"; liveness says "restart me if I'm stuck." Mixing them up causes restart loops. See [[containers-and-kubernetes]].
