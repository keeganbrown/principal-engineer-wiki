# Quiz: Feature Flags

## What is the difference between deploying and releasing?

- [x] Deploying puts code on servers; releasing turns behavior on for users.
- [ ] Deploying is for back-end code; releasing is for front-end code.
- [ ] Deploying happens daily; releasing happens only at the end of a quarter.
- [ ] They are the same step, named differently by different teams.

**Why:** Flags separate the two, so code can ship dark and be released gradually or turned off fast. See [[feature-flags]].

## A rollout at 5% shows flat errors but latency up 30%. What should the team do?

- [x] Turn the flag off, fix the cause, and roll out again.
- [ ] Push to 100% quickly so the latency averages out.
- [ ] Leave it at 5% indefinitely and move on to other work.
- [ ] Ship a rollback deploy of the whole service.

**Why:** Gradual rollouts are only useful if you watch each step and act on what you see. Turning a flag off is faster than a rollback deploy. See [[feature-flags]].

## Which practice best prevents flag debt?

- [x] Giving every release flag an owner and an expiry date.
- [ ] Reusing old flag names for new features to keep the list short.
- [ ] Nesting new flags inside existing ones.
- [ ] Keeping every flag forever in case you need to roll back.

**Why:** Release flags should be deleted once the rollout is done. Reused names and nested flags are listed traps. See [[feature-flags]].
