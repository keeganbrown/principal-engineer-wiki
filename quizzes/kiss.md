# Quiz: Keep It Simple, Stupid (KISS)

## A team needs a nightly report email and runs no queues yet. Which design does KISS favor?

- [x] A scheduled job that sends the email and alerts on failure.
- [ ] A new message queue, worker service, and retry scheduler, so it can scale later.
- [ ] A plugin framework that lets any team add new report types without code.
- [ ] A separate microservice per report, so one failure never affects another.

**Why:** When two designs both work, pick the one with fewer moving parts. The simple option ships in a day and has one place to look when it breaks. See [[kiss]].

## A team that already runs a monitored job queue in production needs a nightly report email. Which design does KISS favor?

- [x] Usually the existing queue, since it's already monitored and familiar.
- [ ] A new scheduled job with its own new alerting stack to watch it.
- [ ] Stand up a second queue, so the report can't affect other work.
- [ ] Build a plugin framework so other teams can add reports later.

**Why:** Simple is relative to what you already operate. One familiar system with existing monitoring can beat a one-off script nobody remembers. See [[kiss]].

## What is the difference between essential and accidental complexity?

- [x] Essential comes from the problem; accidental comes from your design.
- [ ] Essential is complexity users can see; accidental is hidden in the back end.
- [ ] Essential is required by regulation; accidental is everything else in the code.
- [ ] Essential appears in early versions; accidental appears after years of change.

**Why:** Fred Brooks's distinction: tax rules or distributed consensus are complex no matter what. KISS targets the complexity you add yourself. See [[kiss]].
