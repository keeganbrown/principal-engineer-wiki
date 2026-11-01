---
title: Paved Roads
category: leadership
summary: Make the recommended way of building things the easiest way — with templates, libraries, and automated checks — and maintain it like a product, instead of relying on mandates.
tags: [leadership, platform, developer-experience]
---

# Paved Roads

> **In one sentence:** Make the recommended way of building things the easiest way — with templates, libraries, and automated checks — and maintain it like a product, instead of relying on mandates.

## The idea

Imagine a park where people keep cutting across the grass. You can put up "Keep off" signs, or you can pave the path people actually want to walk. The second works better.

In engineering, a **paved road** is a supported, ready-made way to do a common job: a service template that already has logging, metrics, CI, and security scanning wired in; a library that handles retries correctly; a one-command deploy. Teams *can* go off-road, but the paved road is so much easier that most don't.

Netflix popularized the term "paved road"; Spotify calls the same idea a "golden path."

## Why it matters

Principal engineers often know the right way to build things across an organization, but can't order teams to follow it. Mandates get ignored, worked around, or followed grudgingly. Documentation goes unread.

A paved road changes the default. When the good way is also the fastest way, adoption happens on its own — and standards spread without a single meeting. It's one of the most powerful forms of [[influencing-without-authority]].

## How to apply it

- **Pave where people already walk.** Look at what teams are building repeatedly and painfully — new services, deploy pipelines, auth integration — and start there.
- **Build it with a real team.** Pair with one team that needs it now. Their feedback makes it usable; their success makes it credible.
- **Make it faster than the alternative.** If the paved road takes longer to set up than doing it by hand, nobody will use it.
- **Bake standards in, don't bolt them on.** Logging, trace IDs, security checks, and dashboards come for free with the template.
- **Allow exits.** Teams with genuinely different needs should be able to leave the road — and you should learn from why they did.
- **Treat it as a product.** It needs an owner, a roadmap, versioned upgrades, documentation, and support. Measure adoption and time-to-first-deploy.
- **Automate the guardrails.** Linters and CI checks enforce the few things that truly must be consistent, so humans don't have to police them.

## Example

Every new service at a company takes two weeks to set up: CI, deploy scripts, logging, metrics, alerts, secrets. Each team does it differently, and half forget trace IDs.

A principal engineer and one product team build a service template. Running one command creates a repo with all of that wired in, deployed to staging in 20 minutes. A small platform team owns it and ships monthly upgrades that existing services can pull in.

Within a year, 90% of new services use it. Nobody was required to. Incidents get easier to debug because every service now logs the same way.

## Common traps

- **Build it and walk away.** An unmaintained paved road decays into the thing teams route around — and costs more credibility than never building it.
- **Paving for imagined needs.** A platform built without real users usually solves the wrong problems.
- **Paving a cow path that shouldn't exist.** Make sure what you're standardizing is actually good.
- **No exits.** A paved road that's mandatory and inflexible is just a mandate with extra steps.
- **Too many roads.** Three competing templates is no standard at all.

## When it doesn't apply

In a small organization where everyone already talks daily, a short shared doc may be enough — the overhead of a maintained platform isn't worth it yet. And some rules (security, legal compliance) really must be mandatory; for those, pave the road *and* enforce it.

## Related

- [[influencing-without-authority]] — paved roads are influence that scales without meetings.
- [[observability]] — a classic thing to bake into every template.
- [[code-review]] — let automated checks handle style so reviewers can focus on design.
- [[modular-monolith]] — boundaries need tooling to enforce them, not just good intentions.
