# Quiz: Adopting Coding Agents

## A principal engineer is asked to "get the org using agents." What should they do first?

- [x] Run a pilot with willing teams, a metrics baseline, and a short agreement.
- [ ] Mandate daily agent use for every engineer, tracked by usage dashboards.
- [ ] Roll agents out to everyone at once and measure the rise in pull requests.
- [ ] Buy licenses for everyone and let good habits form on their own over time.

**Why:** Treat it as a change to how the team works. Pilot on real work with a baseline, and spread practice through peers; quotas measure compliance, not value. See [[adopting-coding-agents]].

## A team tracks a pilot to judge whether agents are helping. Which should it track?

- [x] Lead time and change failure rate, against a baseline.
- [ ] How many lines of code agents generated each month.
- [ ] How many engineers say they feel more productive now.
- [ ] How many agent sessions each engineer started each week.

**Why:** Feelings are a poor measure and activity is easy to game. With a small pilot, treat results as direction, not proof, and watch review time and spend too. See [[adopting-coding-agents]] and [[metric-fixation]].

## A team's delivery pipeline is badly broken. Should they roll out agents now?

- [x] No; fix the pipeline where agents will work, since agents amplify it.
- [ ] Yes; agents will fix the pipeline themselves as part of their work.
- [ ] No; wait until the whole codebase is clean before trying any agents.
- [ ] Yes, but only for the engineers who complain most about the pipeline.

**Why:** Agents amplify a team's existing strengths and weaknesses, so a broken pipeline gets broken faster. That doesn't mean a perfect codebase first; fix the loop where agents will work most. See [[adopting-coding-agents]] and [[feedback-loops-for-agents]].

## A firm's agent rollout raised pull requests opened by a third, but resolved issues rose far less. Where should it look first?

- [x] Code review, where changes may now wait longer and draw more comments.
- [ ] Agent quotas, since mandated use would turn more code into finished work.
- [ ] Usage dashboards, since more agent sessions would raise resolved work.
- [ ] Licenses, since more seats would push the new code through faster.

**Why:** Watch delivered work, not code volume. A 2026 Harvard working paper (observational, not yet peer reviewed) saw the same pattern across 655 firms, and its authors point to review: code waited longer and drew more comments. Check your own review wait times before trusting that diagnosis. See [[adopting-coding-agents]] and [[reviewing-ai-generated-code]].

## A vendor cites one study showing agents raise output by 40%. How should you use it in your rollout plan?

- [x] As a signal to test against your own baseline, not as a forecast.
- [ ] As the target, since a published study shows what teams can reach.
- [ ] As proof to skip the pilot, since the effect is already measured.
- [ ] Not at all, since studies of coding agents tell you nothing useful.

**Why:** The evidence on coding agents is early and mixed: small, short, observational, or one-company studies that disagree. Treat findings as signals of what to watch, and measure your own team against a baseline. See [[adopting-coding-agents]].
