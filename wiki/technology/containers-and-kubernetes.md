---
title: Containers and Kubernetes
category: technology
summary: Containers package an app with everything it needs so it runs the same everywhere, and orchestrators like Kubernetes run many containers across many machines — powerful, but a platform you adopt deliberately, not by default.
tags: [containers, kubernetes, deployment, infrastructure, platforms]
---

# Containers and Kubernetes

> **In one sentence:** Containers package an app with everything it needs so it runs the same everywhere, and orchestrators like Kubernetes run many containers across many machines — powerful, but a platform you adopt deliberately, not by default.

## The idea

A **container** bundles an application with its runtime, libraries, and settings into one **image**. The image runs the same on a laptop, in continuous integration (CI), and in production. Unlike a virtual machine, a container shares the host's operating system kernel, so it starts in seconds and adds little overhead.

Running one container is easy. Running hundreds — restarting crashed ones, spreading them across machines, rolling out new versions, connecting them to each other — needs an **orchestrator**. **Kubernetes** is the dominant one.

In Kubernetes, you describe the **desired state** — "run three copies of this image, with this much memory, behind this address" — and background processes called controllers continuously work to make reality match. If a machine dies, its containers are rescheduled elsewhere. Docker (2013) made containers mainstream; Google open-sourced Kubernetes in 2014, drawing on its internal Borg system.

## Why it matters

- **"Works on my machine" mostly goes away.** The image *is* the environment.
- **Deploys become routine.** Rolling updates, health checks, and rollbacks are built in.
- **Machines are used efficiently.** Many small services share a cluster instead of each owning idle servers.
- **One way to run everything.** A platform team can offer a [[paved-roads|paved road]]: logging, metrics, secrets, and deploys handled the same way for every service.

The cost is large: Kubernetes has many concepts, many failure modes, and needs people who understand it. Operating it well is a real job, often a team's job.

## How to apply it

- **Containerize first; orchestrate when you need it.** Containers pay off in most places, but someone must own rebuilding images when their base images get security fixes; an unpatched image is a vulnerability you shipped on purpose. Kubernetes pays off when you have many services, teams, or machines to coordinate.
- **Prefer managed options.** A managed Kubernetes service, or a simpler container platform (Cloud Run, AWS Fargate, Fly.io), removes much of the operating burden.
- **Keep images small and pinned.** Small base images start faster and carry fewer vulnerabilities. Pin versions so builds are reproducible.
- **Set resource requests and memory limits.** A *request* is what the scheduler reserves; a *limit* is the most a container may use. Without them, one memory-hungry container can starve its neighbors or cause surprise evictions. A sensible default is to set CPU requests and add CPU limits only where you must cap a noisy workload, because limits throttle bursts and can hurt latency-sensitive services.
- **Define readiness and liveness checks.** **Readiness** says "send me traffic"; **liveness** says "restart me if I'm stuck." If the liveness check tests readiness, a container that's still warming up fails it and is restarted before it's ever ready, again and again. Slow starters can also use a **startup probe**, which holds off the other checks until the app has started.
- **Treat containers as disposable.** Anything that must survive a restart goes in a database, object storage, or a persistent volume (storage the platform attaches to a container and keeps across restarts) — never in the container's own filesystem.
- **Keep configuration in version control.** Manifests (files describing the desired state) and Helm charts (templated bundles of manifests) are code; review them ([[infrastructure-as-code]]).

## Example

A company of 40 engineers runs six services on virtual machines with hand-run deploy scripts. Deploys are scary and take an afternoon. Someone proposes Kubernetes.

The principal engineer asks what problem it solves. The real pain is deploys and environment drift, not scheduling across hundreds of machines. They containerize all six services and move them to a managed container platform that runs images, scales on traffic, and does rolling deploys — without the team operating a cluster.

Deploys drop to ten minutes and become a non-event. Two years later, with 30 services, several teams, and needs for custom networking and batch jobs, they move to managed Kubernetes and fund a small platform team. The images move unchanged, though health checks, configuration, and secrets wiring take a few weeks of rework. The earlier step still made the later one cheaper, and they avoided running Kubernetes for two years when they didn't need it.

## Common traps

- **Kubernetes as a resume item.** Adopting it for three services adds a full-time operating burden for little gain.
- **Treating containers like pets.** Containers should be identical and replaceable, not unique and hand-tended. Logging in to patch a running container means the next restart loses the fix. Rebuild the image.
- **Secrets in images.** Anything baked into an image is readable by anyone who can pull it. Inject secrets at run time.
- **Copy-pasted configuration.** Fifty services with fifty slightly different manifests is drift at scale. Use shared templates.

## When it doesn't apply

A single app with modest traffic often runs best on a platform-as-a-service (a hosted service that runs your code without you managing servers) or a couple of virtual machines. Some workloads — heavy stateful databases, specialized hardware, very latency-sensitive systems — need extra care or are better outside containers. And serverless functions (small pieces of code the provider runs on demand, billed per call) may fit spiky, event-driven work better than a cluster.

## Related

- [[infrastructure-as-code]] — how clusters and their configuration are defined and reviewed.
- [[paved-roads]] — a container platform is a classic paved road.
- [[microservices]] — many services is the main reason to orchestrate.
- [[load-balancers-and-cdns]] — how traffic reaches the containers.
- [[reproducible-dev-environments]] — the same container idea applied to development.
