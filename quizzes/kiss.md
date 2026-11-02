# Quiz: Keep It Simple, Stupid (KISS)

## A team needs a nightly report email. Which design does KISS favor?

- [x] A scheduled job that renders a template and calls the email API, alerting on failure.
- [ ] A new message queue, worker service, and retry scheduler, so it can scale later.
- [ ] A plugin framework that lets any team add new report types without code changes.
- [ ] A microservice per report so failures in one never affect the others.

**Why:** When two designs both work, pick the one with fewer moving parts. The simple option ships in a day and has one place to look when it breaks. See [[kiss]].

## The same team already runs a job queue in production for other work. What changes?

- [x] Using the existing queue may now be simpler than a special-case scheduled job.
- [ ] Nothing; a scheduled job is always simpler than a queue.
- [ ] They should add a second queue so the report can't affect other work.
- [ ] KISS no longer applies, because the system is already complex.

**Why:** Simple is relative to what you already operate. One familiar system with existing monitoring can beat a one-off script nobody remembers. See [[kiss]].

## What is the difference between essential and accidental complexity?

- [x] Essential comes from the problem itself; accidental comes from your design choices.
- [ ] Essential is complexity users can see; accidental is hidden in the back end.
- [ ] Essential is required by regulation; accidental is everything else in the code.
- [ ] Essential appears in early versions; accidental appears only after years of change.

**Why:** Fred Brooks's distinction: tax rules or distributed consensus are complex no matter what. KISS targets the complexity you add yourself. See [[kiss]].
