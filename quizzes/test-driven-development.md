# Quiz: Test-Driven Development (TDD)

## Why do you watch a new test fail before making it pass?

- [x] It proves the test can actually catch the problem.
- [ ] It confirms the build system is working.
- [ ] It measures how long the test takes to run.
- [ ] It's required for code coverage tools to count it.

**Why:** A test that never failed might be passing for the wrong reason. Red, then green, then refactor. See [[test-driven-development]].

## You need to change untested legacy code with no seams. Where do you start?

- [x] Write characterization tests that pin down what the code does today.
- [ ] Rewrite the module from scratch with tests.
- [ ] Mock every dependency the code touches.
- [ ] Skip tests until the module is refactored.

**Why:** Characterization tests record current behavior so you can change it safely, then test-drive the new work. See [[test-driven-development]].

## Which situation is often better done without TDD?

- [x] An exploratory spike where you don't yet know what you're building.
- [ ] A bug fix in a well-tested module.
- [ ] Pricing rules with many edge cases.
- [ ] A new pure function with clear inputs and outputs.

**Why:** Spikes answer a question and get thrown away. Rebuild the real thing with TDD once you know what it is. See [[test-driven-development]].
