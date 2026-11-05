# Quiz: Test-Driven Development (TDD)

## Why do you watch a new test fail before making it pass?

- [x] It proves the test can actually catch the problem.
- [ ] It confirms that the build system is working as expected.
- [ ] It measures how long the new test takes to run.
- [ ] It's required for code coverage tools to count the test.

**Why:** A test that never failed might be passing for the wrong reason. Red, then green, then refactor. See [[test-driven-development]].

## You need to change untested legacy code with no place to swap in a test double. Where do you start?

- [x] Write tests that pin down what the code does today.
- [ ] Rewrite the module from scratch, with tests this time.
- [ ] Mock every dependency the code touches, then change it.
- [ ] Skip tests until the module has been fully refactored.

**Why:** Characterization tests record current behavior so you can change it safely, then test-drive the new work. See [[test-driven-development]].

## Which situation is often better done without TDD?

- [x] An exploratory spike where you don't yet know what to build.
- [ ] A bug fix in a module that already has a good test suite.
- [ ] Pricing rules with many tricky edge cases to cover.
- [ ] A new pure function with clear inputs and outputs.

**Why:** Spikes answer a question and get thrown away. Rebuild the real thing with TDD once you know what it is. See [[test-driven-development]].
