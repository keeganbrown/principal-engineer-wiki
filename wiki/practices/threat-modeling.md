---
title: Threat Modeling
category: practices
summary: Before you build, map where data crosses into more-trusted parts of the system, ask what could go wrong at each crossing, and decide what you'll do about each threat — while the design is still cheap to change.
tags: [security, design, risk, staff-plus]
---

# Threat Modeling

> **In one sentence:** Before you build, map where data crosses into more-trusted parts of the system, ask what could go wrong at each crossing, and decide what you'll do about each threat — while the design is still cheap to change.

## The idea

Threat modeling is a structured conversation about security at design time. It comes down to four questions:

1. What are we working on?
2. What can go wrong?
3. What are we going to do about it?
4. Did we do a good job?

To answer the first, sketch how data flows through the system and mark the **trust boundaries**: places where data crosses between parts of the system trusted at different levels, in either direction. The internet calling your API is one; a third-party webhook, a file a user uploads, and an email leaving your system are others, and so is a batch job that mixes many customers' data, where one customer's records could leak into another's output. Most attacks cross a boundary, so that's where you look.

To answer the second, walk each boundary with **STRIDE**, a checklist of six kinds of threat:

| Threat | Question to ask |
| --- | --- |
| Spoofing | Can someone pretend to be another user or service? |
| Tampering | Can someone change data in transit or at rest? |
| Repudiation | Could someone deny doing something, with no record to prove it? |
| Information disclosure | Can someone see data they shouldn't? |
| Denial of service | Can someone exhaust a resource and take it down? |
| Elevation of privilege | Can someone do more than they're allowed to? |

Loren Kohnfelder and Praerit Garg created STRIDE at Microsoft in 1999. The four questions were first published in Adam Shostack's *Threat Modeling: Designing for Security* (2014); the wording here is his current one.

## Why it matters

- **Design flaws are the expensive ones.** Scanners and code review find bugs in code; they rarely notice a control the design never had, like checking that a user owns the record they request. Broken access control is first in the OWASP Top 10, the Open Worldwide Application Security Project's list of the most serious web application risks, in both the 2021 edition and the 2025 list.
- **The builders know the weak spots.** An hour with the team that designed the system finds things an outside audit would need a week for. But builders share the design's blind spots, so bring one outsider, such as a security engineer, to question the assumptions.
- **It ranks risk.** Writing threats down shows which few deserve real work and which you can accept.

## How to apply it

- **Do it at design time, in about an hour.** Add a threat model section to the design doc template ([[design-docs]]), and revisit it when the design changes, not on a calendar.
- **Draw the data flow, then mark the boundaries.** Boxes for processes and data stores, arrows for data, dashed lines where trust changes, all on one page.
- **Walk each boundary with STRIDE.** Write each threat as a sentence: "A logged-in user changes the account ID in the export request and downloads another customer's invoices."
- **Decide something for every threat.** Mitigate it, remove the feature that creates it, transfer it (to a payment provider, say), or accept it. Accepted risks get an owner and a note of why.
- **Grant least privilege.** Each service, job, and person gets only the permissions it needs, for only as long as it needs them. The cost is more roles to manage, and a permission that's too narrow fails at a bad time, so automate granting and reviewing access.
- **Check authorization on the server, on every request.** Authentication says who someone is; authorization says what they may do. Check that the caller may touch *this* object, not just that they're logged in.
- **Keep secrets out of code and images.** Use a secrets manager and short-lived credentials, and rotate them ([[infrastructure-as-code]]).
- **Assume one layer fails.** Defense in depth means a second control catches what the first misses: an authorization check *and* storage that's private by default.
- **Count dependencies as attack surface.** Pin versions, scan them for known vulnerabilities, and review new ones before adding them.

## Example

A team adds "export your invoices": the API queues a job, a worker writes a CSV file (comma-separated values) to [[object-storage]], and an email sends the link. They spend 45 minutes on it. The boundaries are browser to API, API to queue, worker to storage, and email to recipient.

They find five threats:

- **Elevation of privilege** — the request carries `accountId`, so any user could export another account's invoices. Fix: take the account from the session.
- **Information disclosure** — the emailed link never expires. Fix: a pre-signed link (a URL carrying a signature that grants temporary access to one file) valid for 24 hours. The cost is that users who open the email later must request the export again.
- **Repudiation** — nothing records who exported what. Fix: log each export with the user and time.
- **Denial of service** — one account could request huge exports in a loop. Fix: cap rows and limit exports per hour.
- **Tampering** — a cell starting with `=`, `+`, `-`, or `@` (or a tab or carriage return) runs as a formula when the recipient opens the file in a spreadsheet. Fix: prefix such cells with a single quote.

They accept one risk: a forwarded email shares the link. The 24-hour expiry limits it, and the product owner signs off. The hard part was timeboxing: twenty minutes went on a far-fetched attacker before the facilitator steered back.

## Common traps

- **Boiling the ocean.** A forty-page model of every theoretical attack gets written once and never read.
- **Modeling once.** The design changes and the model doesn't. Tie updates to design changes.
- **Imagining only outside attackers.** Insiders, a compromised dependency, and a misconfigured storage bucket cause many real breaches.
- **Leaving it to the security team.** Specialists help, but the people who build the system must be in the room.
- **Listing threats without decisions.** A list with no owner or fix is a worry, not a plan.

## When it doesn't apply

A small change inside an already-modeled boundary, like a new field on an existing form, doesn't need its own session; a question in [[code-review]] is enough. A throwaway prototype with no real data and no real users can skip it, as long as it really is thrown away. At the other end, payments, health data, and other high-stakes systems need more than this lightweight approach: formal security review, penetration testing, and the controls their regulations require.

## Related

- [[design-docs]] — where the threat model lives and gets reviewed.
- [[agent-guardrails]] — the same thinking applied to coding agents and prompt injection.
- [[architecture-trade-offs]] — security is one quality attribute, weighed against others.
- [[object-storage]] — private-by-default buckets and pre-signed links.
- [[incident-response]] — what to do when a threat turns into a breach.
