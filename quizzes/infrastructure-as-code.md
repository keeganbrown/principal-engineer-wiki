# Quiz: Infrastructure as Code (IaC)

## An engineer opened a database port "temporarily" in the console and forgot. What fix prevents a repeat?

- [x] Bring the resources under IaC and remove console write access, so changes go through reviewed PRs.
- [ ] Send a reminder to all engineers to close ports after debugging.
- [ ] Run a weekly script that closes all open ports automatically.
- [ ] Give only senior engineers console access.

**Why:** Make code the only way to change infrastructure. The next "temporary" change then becomes a PR someone can question. See [[infrastructure-as-code]].

## What should reviewers read before an apply?

- [x] The plan, which shows what the tool will actually create, change, or destroy.
- [ ] Only the code diff, since the plan is generated.
- [ ] The cloud bill from the previous month.
- [ ] The tool's release notes.

**Why:** A small code change can produce a destructive plan. Applying without reading the plan is a listed trap. See [[infrastructure-as-code]].

## What does IaC not replace?

- [x] Application deploys, database migrations, and data backups.
- [ ] Clicking through the cloud console to create networks.
- [ ] Hand-written notes about how production was set up.
- [ ] Manual steps to rebuild staging after a failure.

**Why:** IaC manages infrastructure. Deploys, migrations, and backups need their own tooling. See [[infrastructure-as-code]].
