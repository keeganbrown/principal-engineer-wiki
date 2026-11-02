---
title: Adopting Coding Agents as a Team
category: coding-with-ai
summary: Treat coding agents as a change to how the team works, not a tool install — agree on shared norms, spread practice through peers, share configuration as code, and measure delivery outcomes rather than usage or feelings.
tags: [ai, coding-agents, adoption, team-practices, metrics, leadership]
---

# Adopting Coding Agents as a Team

> **In one sentence:** Treat coding agents as a change to how the team works, not a tool install — agree on shared norms, spread practice through peers, share configuration as code, and measure delivery outcomes rather than usage or feelings.

## The idea

A **coding agent** is an AI tool that reads code, runs commands, and edits files in a loop toward a goal. Handing every engineer a license is easy. Getting a *team* to use agents well is harder, because agents change who writes code, how much of it arrives, and what review means.

Left alone, each engineer invents their own habits: different tools, different rules about what's safe, different ideas of what "done" means. The result is uneven quality and arguments in code review about things nobody agreed on.

Aligning a team means deciding a few things together and writing them down: what agents are for, who owns their output, what data they may see, how shared setup is maintained, and how you'll know whether it's working. Google's DORA (DevOps Research and Assessment) 2025 research lists a "clear and communicated AI stance" among seven capabilities that separate teams that benefit from AI from teams that don't.

## Why it matters

- **Feelings are a poor measure.** In a 2025 randomized trial by the research group METR, experienced open-source developers took 19% *longer* on tasks with AI tools, while believing they'd been about 20% faster. METR's 2026 follow-up points toward a speed-up with newer tools, but with uncertainty wide enough to include none. Either way, perception and measurement disagree.
- **AI amplifies what's already there.** DORA's 2025 report found AI magnifies a team's existing strengths and weaknesses. Teams with fast feedback and small batches gain; teams with slow, tangled systems mostly get more of the same.
- **Practice spreads through people.** A 2026 Microsoft study of its rollout of command-line coding agents found engineers mostly started using them because peers did. Adopters merged roughly 24% more pull requests (PRs); the study didn't measure quality.
- **Skills can erode quietly.** In a 2026 Anthropic trial, developers learning a new library with AI help scored 50% on a follow-up quiz versus 67% without, with the biggest gap on debugging. Those who asked the AI conceptual questions and follow-ups did much better than those who delegated the code.

## How to apply it

- **Write a one-page team agreement.** Cover approved tools, what data may be sent to them, the ownership rule ("you open the PR, you own it"), review expectations, and when agents must not run unattended. Keep it short enough that people read it.
- **Pilot on real work, with a baseline.** Pick a willing team and real tasks. Record delivery metrics for a few weeks *before* the pilot, or you'll have nothing to compare against.
- **Spread practice through peers, not mandates.** Run short demos of real sessions, pair on agent tasks, and give the engineers who are good at it time to help others. Usage quotas produce theater: people generate code to hit a number.
- **Share setup as code.** Instruction files, permission settings, sandbox configs, and reusable prompts live in the repository and get reviewed ([[agent-instruction-files]], [[agent-guardrails]]). This is the team's [[paved-roads|paved road]] for agents.
- **Measure outcomes, not activity.** Track lead time for changes, change failure rate, time to restore service, review time, and escaped defects — alongside a short developer survey. Lines of code, suggestion acceptance rates, and PR counts alone reward volume, not value.
- **Protect learning on purpose.** Expect people new to a codebase or language to explain agent-written code in review, ask the agent "why" as well as "write," and sometimes work without it. Make understanding, not output, the bar for juniors.
- **Revisit the agreement on a schedule.** Tools change every few months. A quarterly review keeps the agreement current, and most choices — which tool, which settings — are [[reversible-decisions|two-way doors]] you can change. Data policy deserves more care, since data sent out can't be recalled.

## Example

A principal engineer is asked to "get the org using agents." Six teams have already split: two use agents heavily with no shared rules, three barely use them, one has banned them after an agent-written migration broke staging.

Instead of a mandate, they run a six-week pilot with two volunteer teams:

- **Week 0.** Capture baseline lead time, change failure rate, and review time. Draft a one-page agreement with both teams and with security, who add a rule: no customer data in prompts.
- **Weeks 1–6.** Engineers share one recorded session a week. The teams fix their slowest test suites ([[feedback-loops-for-agents]]) and adopt [[spec-first-agent-tasks]].
- **Week 7.** Review the data. Lead time is down for well-tested services and flat for the team with a 40-minute flaky suite. Change failure rate is flat, and review time is *up*, because reviewers are reading more code.

The report to leadership says exactly that: real gains where feedback loops are good, a review bottleneck to fix, and a test-suite investment that should come before wider rollout. The team that banned agents joins the next cohort after its migration incident is reviewed blamelessly. The cost: two teams spent part of six weeks on process instead of features, and the honest results were less exciting than the vendor's slides.

## Common traps

- **Mandating usage.** Quotas measure compliance, not value, and push agent use into work where it doesn't help.
- **Measuring what's easy.** PR counts rise easily — split one change into five. Pair any volume metric with quality and stability metrics.
- **Skipping the security conversation.** Deciding later what data agents may see means deciding after it has already been sent.
- **Framing it as headcount reduction.** If engineers believe the goal is replacing them, you'll get quiet resistance and no honest feedback. Say plainly what the goal is.
- **Hollowing out the junior pipeline.** If juniors only prompt and merge, you'll have no seniors in five years. Protect time to learn the hard way.
- **One person's setup as the standard.** Agree the setup together, or it becomes one person's preferences enforced on everyone.

## When it doesn't apply

In some regulated environments, no external model may see the code; there the question is whether an approved, self-hosted option exists at all. A team of two doesn't need a formal pilot — a five-line agreement and an honest check-in after a month will do. And if your delivery pipeline is badly broken, fix that first: by DORA's evidence, agents will amplify the breakage.

## Related

- [[influencing-without-authority]] — adoption spreads through trust and examples, not memos.
- [[paved-roads]] — shared agent configuration is a paved road; maintain it like one.
- [[reviewing-ai-generated-code]] — the review norms the agreement should set.
- [[feedback-loops-for-agents]] — where the biggest gains come from.
- [[observability]] — measure outcomes in production, not activity in the editor.
