# Quiz: Reproducible Dev Environments

## An agent loosens an image test's assertions because laptops and CI run different library versions. What's the real fix?

- [x] A dev container with pinned versions, built from CI's definition.
- [ ] A rule in the instruction file forbidding changes to assertions.
- [ ] Updating every laptop by hand so its libraries match CI's versions.
- [ ] Skipping the image tests whenever they run on a laptop instead of CI.

**Why:** Pin versions and build CI from the same definition, so local and CI runs agree. If laptops and CI use different processor architectures, the "same" image is two builds, so test both. See [[reproducible-dev-environments]].

## What should a locked-down agent profile include?

- [x] Only the repository mounted, with network limited to what builds need.
- [ ] The full image plus your cloud credentials, since it's already a container.
- [ ] Production database access, so the agent's tests stay realistic.
- [ ] Unrestricted network access, so package installs never fail mid-task.

**Why:** A container with your credentials and open network is reproducible, not safe; isolation depends on what you mount and allow. See [[reproducible-dev-environments]] and [[agent-guardrails]].

## When is a container-based dev environment probably overkill?

- [x] A small single-language project with a lockfile and standard tools.
- [ ] A service whose setup guide has grown to fourteen manual steps.
- [ ] A team whose CI runs and laptop runs keep disagreeing.
- [ ] A repository where agents regularly run unattended.

**Why:** Some projects are already reproducible enough. Hardware-dependent work, like mobile simulators, may need scripted setup instead. See [[reproducible-dev-environments]].
