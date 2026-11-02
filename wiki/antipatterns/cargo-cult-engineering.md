---
title: Cargo Cult Engineering
category: antipatterns
summary: Copying another team's or company's practices without the problems and conditions that made them work, so you get the rituals without the results.
tags: [judgment, process, technology-choice]
---

# Cargo Cult Engineering

> **In one sentence:** Copying another team's or company's practices without the problems and conditions that made them work, so you get the rituals without the results.

## The idea

A successful company does something visible — microservices, a team structure, daily stand-ups, monorepos, a particular interview process. Another team copies the visible part and expects the same results. They don't come, because the visible part was the *output* of conditions the copier doesn't have: thousands of engineers, a specific scaling problem, or years of tooling built to support it.

The name comes from Richard Feynman's 1974 "cargo cult science" speech. He described islanders who, after wartime airfields brought supplies, built runways and wooden control towers hoping planes would land again. The form was perfect; the planes didn't come.

## Why it matters

- **You inherit the costs without the problem they solved.** A company with 2,000 engineers splits into hundreds of services to reduce coordination. A team of 15 that copies it gets the operating cost and no coordination problem to solve ([[microservices]]).
- **Practices lose their purpose.** A stand-up copied without its reason becomes a status report. Code review copied without its reason becomes a rubber stamp ([[code-review]]).
- **It crowds out thinking.** "Google does it" ends a discussion that should have started with "what's our problem?"
- **It's hard to undo.** Once a practice is a ritual, removing it feels like lowering standards, even when it never helped.

## How to apply it

- **Find the problem the practice solved.** Read the original source, not the conference summary. Ask: what was hurting them, and how big were they at the time?
- **Check whether you have that problem.** If you don't, you're buying a solution in search of one.
- **Check the hidden supports.** Most famous practices rest on tooling, staffing, or culture that isn't in the blog post. Spotify's squads and tribes depended on things that Spotify itself later said didn't work as described.
- **Adopt the principle, then pick the practice.** "Small, safe deploys" is the principle; feature flags, canary releases, or trunk-based development are ways to get it. Choose the one that fits your scale ([[feature-flags]]).
- **Define what success looks like before you start.** Then check after a few months whether you got it, and drop the practice if not.

## Example

A 30-person company reads that a large tech firm requires a design doc for every change and adopts the same rule, with the same eight-page template. Within a month, engineers write docs after the code is done, reviewers skim them, and small changes wait a week for approval.

Asked what problem they were solving, the team says "we kept building the wrong thing on big projects." That is a real problem, but it applies to perhaps one project a month. They change the rule: a two-page doc for work longer than two weeks or that crosses teams, and none for anything else ([[design-docs]]).

The hard part is that the original rule felt safer, and loosening it got pushback: "what if something slips through?" They answer with data instead of opinion — tracking for a quarter whether any undocumented change caused a cross-team problem. None did, and the lighter rule stuck.

## Common traps

- **Dismissing every outside idea.** The opposite mistake is assuming nothing from elsewhere applies to you ([[not-invented-here]]). Learning from others is good; copying without understanding isn't.
- **Copying the vocabulary.** Renaming teams to "squads" or meetings to "ceremonies" changes nothing by itself.
- **Copying your own past.** A practice that worked at your last company was cargo at the time you joined it, too. Re-check the conditions.
- **Treating best practices as universal.** "Best practice" usually means "worked well somewhere, for someone." Ask where.

## When it doesn't apply

Copying without full understanding is reasonable when a practice is cheap to try and easy to reverse ([[reversible-decisions]]). Trying a weekly demo or a postmortem template for a month costs little, and you learn more by doing than by analysing. It's also fine to follow widely tested defaults — version control, automated tests, code review — without re-deriving their value each time. Save the scrutiny for practices that are expensive to adopt or hard to remove.

## Related

- [[golden-hammer]] — the tool-choice version of the same mistake.
- [[not-invented-here]] — the opposite reflex.
- [[microservices]] — the most commonly cargo-culted architecture.
- [[paved-roads]] — good defaults are explained, not just imposed.
- [[metric-fixation]] — copying metrics without knowing what they measured.
