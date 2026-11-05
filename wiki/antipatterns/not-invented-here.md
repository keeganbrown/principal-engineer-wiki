---
title: Not Invented Here (NIH)
category: antipatterns
summary: Building your own version of something you could adopt, because outside solutions feel untrustworthy or inferior, and then maintaining it forever.
tags: [build-vs-buy, technology-choice, judgment]
---

# Not Invented Here (NIH)

> **In one sentence:** Building your own version of something you could adopt, because outside solutions feel untrustworthy or inferior, and then maintaining it forever.

## The idea

"Not invented here" (NIH) is the reflex to build rather than adopt. A team writes its own logging framework, job queue, feature-flag system, or authentication instead of using a well-tested library or service. Each choice feels justified: the existing option is too heavy, doesn't quite fit, or "we'd have to learn it anyway."

The cost shows up later. A homegrown tool needs its own documentation, bug fixes, security patches, and an engineer who understands it. When that engineer leaves, the tool becomes a mystery that nobody wants to own.

Ralph Katz and Thomas Allen studied the effect in 1982. Research and development groups whose members had worked together for about five years or more increasingly dismissed outside ideas, communicated less with outside sources, and performed worse. So long-stable teams are where the reflex is strongest, and where an outside review of build-versus-adopt decisions pays off.

## Why it matters

- **You pay for maintenance, not just the build.** Writing the first version is the cheap part. The years of upkeep are the real cost.
- **You rediscover solved problems.** Mature libraries encode years of edge cases — time zones, retries, encoding, concurrency. A new version learns them one incident at a time.
- **Security suffers most.** Homegrown cryptography, authentication, or input parsing is where NIH does the most damage.
- **It spends effort away from what's unique.** Every week on a custom job queue is a week not spent on what makes your product different.

## How to apply it

Spotting it:

- **Listen for "it's only a week of work."** The estimate covers the first version, never the years after it.
- **Look for homegrown plumbing with one maintainer.** Internal frameworks, queues, and config systems that only one person can change are the usual result ([[hero-culture]]).
- **Notice "doesn't fit" with no specifics.** If nobody can name the requirement the existing option fails, it's a preference.

Climbing out:

- **Separate your differentiators from your plumbing.** Build what makes your product unique. Adopt everything else unless there's a strong reason. Domain-driven design calls these core and generic subdomains ([[domain-driven-design]]).
- **Price the whole lifetime.** Compare adopting (learning, license, integration, living with its limits) against building (first version, plus maintenance, on-call, security fixes, and documentation, for years).
- **Wrap the adopted tool where replacing it is a real possibility.** A thin adapter keeps it *more* replaceable ([[hexagonal-architecture]]). The adapter is code you maintain, and semantics such as delivery guarantees leak through it, so a swap gets cheaper, not free ([[reversible-decisions]]).
- **Never build your own security primitives.** Use established libraries for cryptography, password hashing, and authentication protocols.

## Example

A team needs background jobs with retries. One engineer says existing job libraries are bloated and offers to write a simple one in a week. It works well for six months.

Then the incidents start. Jobs vanish when a deploy kills a worker mid-job, because the queue has no visibility timeout: a lease that hides a job from other workers while one processes it, and returns it to the queue if that worker dies. Retries hammer a failing partner, because there's no backoff ([[retries-and-timeouts]]). Each fix takes days, and only the original author understands the code.

The team migrates to a widely used job library behind a small adapter, which means running Redis, a datastore they hadn't operated before. Its visibility timeout stops the lost jobs but means a job can occasionally run twice, so they also make the jobs idempotent ([[idempotency]]). For a week, new jobs go to the new library while the old queue finishes the jobs already in it. Counting six months of incidents and the three-week migration, the "one-week" queue cost the team well over two months.

## Common traps

- **Swinging to adopting everything.** Pulling in a large dependency for a tiny function adds supply-chain risk: a compromised or abandoned dependency becomes your problem. A 10-line helper is better written than imported.
- **Adopting without checking health.** An abandoned library with one maintainer can be worse than your own code. Check activity, maintainers, and license before adopting.
- **Forking and forgetting.** A fork you modify is your own code from then on, with the original's complexity attached.
- **Mistaking "I'd enjoy building it" for a business case.** It's fine to enjoy building things. Choose where.

## When it doesn't apply

Building your own is right when the thing *is* your product, when no existing option meets a hard requirement (performance, compliance, or data residency), or when the existing options are so large that your one narrow need is simpler to write and own. A need isn't narrow if it includes failure behavior — crash recovery, retries, concurrency, or security — because that's where the libraries' "bloat" lives. Large companies also build internal tools that pay off across hundreds of teams ([[paved-roads]]). The test is the same each time: is the lifetime cost of owning it lower than the lifetime cost of adopting?

## Related

- [[golden-hammer]] — a sibling: the answer is picked before the problem is understood.
- [[cargo-cult-engineering]] — the opposite reflex: adopting without understanding.
- [[domain-driven-design]] — core vs generic subdomains: what to build and what to adopt.
- [[technical-debt]] — homegrown tools are a common source.
- [[hero-culture]] — the one person who understands the homegrown tool.
