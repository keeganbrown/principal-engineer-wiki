---
title: Not Invented Here
category: antipatterns
summary: Building your own version of something you could adopt, because outside solutions feel untrustworthy or inferior, and then maintaining it forever.
tags: [build-vs-buy, technology-choice, judgment]
---

# Not Invented Here

> **In one sentence:** Building your own version of something you could adopt, because outside solutions feel untrustworthy or inferior, and then maintaining it forever.

## The idea

"Not invented here" (NIH) is the reflex to build rather than adopt. A team writes its own logging framework, job queue, feature-flag system, or authentication instead of using a well-tested library or service. Each choice feels justified: the existing option is too heavy, doesn't quite fit, or "we'd have to learn it anyway."

The cost shows up later. A homegrown tool needs its own documentation, bug fixes, security patches, and an engineer who understands it. When that engineer leaves, the tool becomes a mystery that nobody wants to own. Ralph Katz and Thomas Allen studied the effect in 1982, finding that research teams that stayed together for years increasingly ignored outside ideas.

## Why it matters

- **You pay for maintenance, not just the build.** Writing the first version is the cheap part. The years of upkeep are the real cost.
- **You rediscover solved problems.** Mature libraries encode years of edge cases — time zones, retries, encoding, concurrency. A new version learns them one incident at a time.
- **Security suffers most.** Homegrown cryptography, authentication, or input parsing is where NIH does the most damage.
- **It spends effort away from what's unique.** Every week on a custom job queue is a week not spent on what makes your product different.

## How to apply it

- **Separate your differentiators from your plumbing.** Build what makes your product unique. Adopt everything else unless there's a strong reason.
- **Price the whole lifetime.** Compare adopting (learning, licence, integration, living with its limits) against building (first version, plus maintenance, on-call, security fixes, and documentation, for years).
- **Write down what "doesn't fit" means.** "It's too heavy" should become a specific requirement the existing option can't meet. Often it turns out to be a preference.
- **Wrap the adopted tool.** A thin adapter around a library keeps it replaceable, which answers the fear of being locked in ([[hexagonal-architecture]]).
- **Never build your own security primitives.** Use established libraries for cryptography, password hashing, and authentication protocols.

## Example

A team needs background jobs with retries. One engineer says existing job libraries are bloated and offers to write a simple one in a week. It works well for six months.

Then the incidents start. Jobs run twice after a deploy, because the homegrown queue has no visibility timeout (a lease that hides a job from other workers while one is processing it). Retries hammer a failing partner, because there's no backoff ([[retries-and-timeouts]]). Each fix takes days, and only the original author understands the code.

The team migrates to a widely used job library behind a small adapter. The hard part is jobs already in flight: they drain the old queue before switching, which means a week of running both. The migration costs three weeks in total — far more than the "week" the homegrown version was supposed to take, and part of the hidden lifetime cost of building it.

## Common traps

- **Swinging to adopting everything.** Pulling in a large dependency for a tiny function adds supply-chain risk and upgrade work. A 10-line helper is better written than imported.
- **Adopting without checking health.** An abandoned library with one maintainer can be worse than your own code. Check activity, maintainers, and licence before adopting.
- **Forking and forgetting.** A fork you modify is your own code from then on, with the original's complexity attached.
- **Mistaking "I'd enjoy building it" for a business case.** It's fine to enjoy building things. Choose where.

## When it doesn't apply

Building your own is right when the thing *is* your product, when no existing option meets a hard requirement (performance, compliance, or data residency), or when the existing options are so large that your one narrow need is simpler to write and own. Large companies also build internal tools that pay off across hundreds of teams ([[paved-roads]]). The test is the same each time: is the lifetime cost of owning it lower than the lifetime cost of adopting?

## Related

- [[golden-hammer]] — the opposite failure: one tool for everything.
- [[cargo-cult-engineering]] — adopting without understanding.
- [[hexagonal-architecture]] — adapters keep adopted tools replaceable.
- [[technical-debt]] — homegrown tools are a common source.
- [[hero-culture]] — the one person who understands the homegrown tool.
