# Quiz: Incident Response

## During an outage, the incident commander is the person who knows the failing service best and wants to dig into its logs. What should happen?

- [x] They hand the commander role to someone else, out loud, before digging in.
- [ ] They debug and coordinate at once, since they know the service best.
- [ ] They stay commander and the whole team waits until they find the cause.
- [ ] Nobody needs to coordinate while the best expert is working the problem.

**Why:** A commander who debugs leaves nobody coordinating, and changes start colliding. If the commander needs to debug, they hand off the role first. See [[incident-response]].

## Checkout errors spiked ten minutes after a deploy. The cause isn't known yet. What is the best first move?

- [x] Roll back the deploy if it's safe to, then diagnose once users recover.
- [ ] Find the root cause first, so that the fix addresses the real problem.
- [ ] Wait for the next scheduled deploy, which may include a fix already.
- [ ] Post a status update and hold any changes until the postmortem.

**Why:** Mitigate first, diagnose later: roll back, turn off a flag, fail over, or shed load. Rollback is safe only if the deploy's data changes are backward compatible, so know before deploying which changes can be undone. See [[incident-response]].

## An incident has run for an hour with no progress to report. How often should stakeholders hear from the team?

- [x] On a fixed schedule, such as every 30 minutes, even when there's no news.
- [ ] Only once the cause is found, so updates are accurate and not alarming.
- [ ] Whenever a stakeholder asks for an update in the responders' channel.
- [ ] Once at the start and once at the end, to avoid distracting responders.

**Why:** Silence costs trust, and people fill it with the worst case. Update on a clock in a separate stakeholder channel, saying what's affected, what's being done, and when the next update comes. See [[incident-response]].

## An internal dashboard has been broken since this morning, with no customer impact. Should the team declare an incident?

- [x] Not necessarily; a minor problem like this is cheaper to handle as a ticket.
- [ ] Yes; every problem gets an incident commander and a timed update schedule.
- [ ] Yes, at the top severity, so that it is guaranteed to get fixed quickly.
- [ ] No; internal tools are never allowed to become incidents of any kind.

**Why:** Declaring should be cheap, but full incident process for minor problems costs more than it saves. Severity is defined by user impact. See [[incident-response]].
