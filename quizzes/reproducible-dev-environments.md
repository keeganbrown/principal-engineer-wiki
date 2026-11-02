# Quiz: Reproducible Development Environments

## An agent "fixes" an image-resizing test by loosening its assertions, because laptops have a different library version than CI. What's the real fix?

- [x] A dev container with pinned versions, built from the same definition CI uses.
- [ ] A rule in the instruction file forbidding changes to assertions.
- [ ] Updating every laptop by hand to match CI.
- [ ] Skipping the image tests when running locally.

**Why:** Pin versions and build CI from the same definition, so local and CI runs agree. See [[reproducible-dev-environments]].

## What should a locked-down agent profile include?

- [x] Only the repository mounted, and network access limited to what's needed, such as the package registry.
- [ ] The engineer's home directory, so the agent can find credentials.
- [ ] Production database access, so tests are realistic.
- [ ] Unrestricted network access, so installs never fail.

**Why:** A reproducible environment is the easiest path to a sandbox, but not a complete one on its own. See [[reproducible-dev-environments]] and [[agent-guardrails]].

## When is a container-based dev environment probably overkill?

- [x] A small single-language project with a lockfile and a standard toolchain.
- [ ] A service whose setup guide has 14 steps.
- [ ] A team whose CI and laptops keep disagreeing.
- [ ] A repository where agents run unattended.

**Why:** Some projects are already reproducible enough. Hardware-dependent work, like mobile simulators, may need scripted setup instead. See [[reproducible-dev-environments]].
