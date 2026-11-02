# Quiz: Containers and Kubernetes

## A 40-engineer company with 6 services has slow, scary deploys. What did the principal engineer recommend first?

- [x] Containerize the services and use a managed container platform, without running a cluster.
- [ ] Adopt self-hosted Kubernetes and build a platform team right away.
- [ ] Rewrite the six services as serverless functions.
- [ ] Keep the hand-run deploy scripts and add more documentation.

**Why:** The real pain was deploys and drift, not scheduling across hundreds of machines. Containerize first; orchestrate when you need it. See [[containers-and-kubernetes]].

## Where should secrets go?

- [x] Injected at runtime from a secrets store, never baked into the image.
- [ ] In the image, so every environment has the same values.
- [ ] In a config file committed next to the Dockerfile.
- [ ] In environment variables written into the image's build step.

**Why:** Anything in an image can be read by anyone who can pull it. "Secrets in images" is a listed trap. See [[containers-and-kubernetes]].

## Why set memory limits on containers?

- [x] So one leaking container can't starve others on the same machine.
- [ ] So containers start faster.
- [ ] So images stay small.
- [ ] So the container can be moved between clouds.

**Why:** Containers share machines. Without limits, one bad container takes down its neighbors. See [[containers-and-kubernetes]].
