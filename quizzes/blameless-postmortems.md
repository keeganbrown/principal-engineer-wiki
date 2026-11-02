# Quiz: Blameless Postmortems

## An engineer ran a cleanup script against production instead of staging. Which conclusion is blameless?

- [x] Credentials for both environments sat in one file and the script had no guard, so the mistake was easy.
- [ ] The engineer was careless and has been reminded to double-check next time.
- [ ] The root cause was human error, so no system change is needed.
- [ ] The engineer's manager should now approve every script they run.

**Why:** Blameless analysis asks how the system made the mistake easy and its impact large. "Human error" is a starting point, not a conclusion. See [[blameless-postmortems]].

## Which action item is strongest?

- [x] Separate credentials so the script can't reach production from a laptop.
- [ ] Remind everyone to be more careful with production.
- [ ] Add a line to the onboarding wiki about checking environments.
- [ ] Require a manager to approve every script run.

**Why:** Removing the hazard beats reminders. Adding approval steps everywhere is process accretion that slows everyone for a rare risk. See [[blameless-postmortems]].

## What does "blameless" not cover?

- [x] Deliberate misconduct or malicious acts.
- [ ] Mistakes made by senior engineers.
- [ ] Incidents that caused customer data loss.
- [ ] Errors made during an on-call shift at night.

**Why:** Blamelessness covers honest mistakes. It isn't the same as being free of accountability, and misconduct is handled differently. See [[blameless-postmortems]].
