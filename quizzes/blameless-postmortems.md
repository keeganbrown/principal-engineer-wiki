# Quiz: Blameless Postmortems

## An engineer ran a cleanup script against production instead of staging. Which conclusion is blameless?

- [x] Shared credentials and an unguarded script made the mistake easy.
- [ ] The script lacked a guard, which the engineer should have added first.
- [ ] The root cause was human error, so no system change is needed at all.
- [ ] The engineer was careless and has been reminded to double-check.

**Why:** Blameless analysis asks how the system made the mistake easy and its impact large. "Human error" is a starting point, not a conclusion. See [[blameless-postmortems]].

## A team's postmortem lists 14 action items, from new approval steps to wiki edits. What's the usual problem?

- [x] Too many to prioritize, and new approvals slow everyone down.
- [ ] Nothing; a long list shows the review was thorough.
- [ ] The list is too short to cover every contributing factor in full.
- [ ] Action items belong in a separate document, not the postmortem.

**Why:** Pick the few items that remove the hazard, like separating credentials so a script can't reach production. Adding approvals everywhere is process accretion. See [[blameless-postmortems]].

## An engineer deliberately deleted production data to cover up an earlier mistake. Does a blameless postmortem shield them?

- [x] No; blamelessness covers honest mistakes, not deliberate misconduct.
- [ ] Yes; a blameless culture means no one is ever held responsible.
- [ ] Yes, as long as the data can be restored from a recent backup.
- [ ] No, and no postmortem should be held for this incident at all.

**Why:** Blamelessness covers honest mistakes. It isn't the same as being free of accountability, and misconduct is handled differently. See [[blameless-postmortems]].
