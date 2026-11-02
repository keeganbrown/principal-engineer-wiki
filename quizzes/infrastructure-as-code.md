# Quiz: Infrastructure as Code

## An engineer opened a database port "temporarily" in the console and forgot. What fix prevents a repeat?

- [x] Manage it as code, and keep console writes to a logged break-glass role.
- [ ] Turn on scheduled drift detection, and alert when the plan shows differences.
- [ ] Run a weekly script that finds open ports and closes them automatically.
- [ ] Give only senior engineers console access, since they're more careful.

**Why:** Make code the only everyday way to change infrastructure, so the next "temporary" change is a pull request someone can question. Keep break-glass for incidents, and write its changes back to code within a day. Drift detection only finds the problem afterward. See [[infrastructure-as-code]].

## A small code change is ready to apply to production infrastructure. What should reviewers read first?

- [x] The plan of what will be created, changed, or destroyed.
- [ ] Only the code diff, since the plan is generated from it anyway.
- [ ] The state file, to see what currently exists in the account.
- [ ] Last night's scheduled drift report for the environment.

**Why:** A small code change can produce a destructive plan, such as replacing a database. Read the plan, not just the diff. See [[infrastructure-as-code]].

## During an incident, an engineer changes a firewall rule by hand with the break-glass role. What should happen next?

- [x] Write the change back to code within a day, or the next apply reverts it.
- [ ] Leave it as it is, since break-glass changes are already logged and that's sufficient.
- [ ] Revoke the engineer's access until a review of the change is complete.
- [ ] Wait for scheduled drift detection to update the code automatically.

**Why:** Manual changes left out of code drift from reality, and the next apply silently undoes them. See [[infrastructure-as-code]].
