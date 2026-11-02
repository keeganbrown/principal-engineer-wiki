---
title: Infrastructure as Code (IaC)
category: technology
summary: Define servers, networks, databases, and permissions in version-controlled files that a tool applies, so infrastructure changes are reviewed, repeatable, and recoverable instead of clicked by hand.
tags: [infrastructure, automation, terraform, cloud, operations]
---

# Infrastructure as Code (IaC)

> **In one sentence:** Define servers, networks, databases, and permissions in version-controlled files that a tool applies, so infrastructure changes are reviewed, repeatable, and recoverable instead of clicked by hand.

## The idea

Without **infrastructure as code (IaC)**, infrastructure is built by clicking through a cloud console or running one-off commands. Nobody knows exactly how production was set up, staging quietly differs from it, and rebuilding after a disaster means guessing.

With IaC, you describe the infrastructure you want in files — "a database of this size, a bucket with these permissions, a network with these rules" — and a tool makes the real world match. Terraform (and its open-source fork OpenTofu), Pulumi, AWS CloudFormation, and Kubernetes manifests all work this way.

Most IaC tools are **declarative**: you describe the end state, not the steps. The tool compares what exists with what you described, shows a **plan** of the differences, and applies them when you approve.

## Why it matters

- **Changes get reviewed.** An infrastructure change is a pull request (PR) with a plan attached, not a click someone forgot to mention.
- **Environments match.** Staging and production come from the same code with different settings.
- **Disaster recovery becomes realistic.** You can rebuild an environment from the code, rather than from memory.
- **History explains the present.** Version control shows who changed a firewall rule and why.

The cost: IaC tools have their own languages, state files, and failure modes, and a bad apply can destroy real resources quickly.

## How to apply it

- **Make code the only way to change infrastructure.** If people still click in the console, the code drifts from reality. Restrict console write access in production.
- **Review the plan, not just the code.** The plan shows what will actually be created, changed, or *destroyed*. A plan that deletes a database should stop everyone.
- **Apply from a pipeline, not laptops.** CI (continuous integration) runs the plan on every PR and applies after merge, with credentials no individual holds.
- **Protect the state.** Tools like Terraform keep a **state file** mapping code to real resources. Store it remotely, locked, encrypted, and backed up.
- **Split by blast radius.** Separate the network, shared databases, and each service's resources, so one change can't touch everything.
- **Guard critical resources.** Use deletion protection on databases and buckets that hold data.
- **Detect drift.** Run the plan on a schedule; any difference means someone changed things by hand.

## Example

A team's production network rules were set up by hand three years ago. An engineer clicks to "temporarily" open a database port for debugging and forgets. Months later, a security scan finds the database reachable from the internet.

They import the existing resources into Terraform, review the code to make sure it describes exactly what exists (the plan should show no changes), and then remove console write access. All changes now go through PRs where the plan is posted as a comment.

The next "temporary" change is a PR that a reviewer questions. The hard part was the import: two weeks of matching code to reality, discovering resources nobody remembered, and one tense apply where the plan wanted to *replace* a load balancer because of a naming difference — caught in review, fixed in code before applying.

## Common traps

- **Applying without reading the plan.** "Destroy 1 database" is in the output; it's easy to miss in a long plan.
- **Leaving incident hotfixes out of the code.** A manual fix that's never written back gets silently reverted by the next apply.
- **Secrets in code or state.** State files often contain secrets in plain text; treat them as sensitive.
- **One giant configuration.** A single change becomes slow to plan and dangerous to apply.
- **Copy-paste environments.** Duplicated code for each environment drifts; use modules with per-environment settings.

## When it doesn't apply

A short-lived experiment or a personal sandbox can be clicked together, as long as it's thrown away rather than promoted to production. And IaC manages *infrastructure*; it doesn't replace application deploys, database migrations, or data backups, which need their own tooling.

## Related

- [[containers-and-kubernetes]] — Kubernetes manifests are IaC for workloads.
- [[code-review]] — infrastructure PRs deserve the same review, plus the plan.
- [[paved-roads]] — shared IaC modules make the secure setup the easy one.
- [[reversible-decisions]] — the plan shows which changes are one-way doors.
- [[blameless-postmortems]] — drift and manual changes are system problems, not personal ones.
