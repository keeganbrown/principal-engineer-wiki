# Review: 2026 agent research ingest (2026-11-02)

Scope: commit 8c8ac3f — adopting-coding-agents, reviewing-ai-generated-code,
agent-instruction-files, feedback-loops-for-agents, their quizzes, and
`docs/sources/coding-with-ai.md`.

Reviewers: newcomer-reader (NR), principal-skeptic (PS), style-editor (SE),
wiki-gardener (WG). **technical-accuracy did not finish** (usage limit); its
pass is still owed. WG cross-checked every new number against the sources
file and found them matching, apart from the wording issues below.

Totals: 2 must-fix, 18 should-fix, 16 consider.

## reviewing-ai-generated-code

### must-fix

1. **Bot approval contradicts "first pass, not an approval."** [NR, PS, SE, WG — all four]
   The new bullet "write down which changes a bot may approve" contradicts the
   bullet above it. The new quiz question's answer contradicts its own Why line
   and makes the older question's wrong option ("required approver, but only
   for small agent changes") a second answer.
   Options:
   - (a) Scope it: a written list of low-risk changes that may merge on bot
     review alone, the *ship* tier of ship/show/ask in [[code-review]]. A named
     human still owns them. Soften the first-pass bullet to match.
   - (b) Keep bots non-approving: "write down which changes always need a
     careful human read."

   Then align quiz Q3 and Q5.

### should-fix

2. **Split the "Review becomes the bottleneck" bullet.** [NR, SE, WG] It has
   about 90 words, four sentences and six statistics. Use one bullet per study.
   Say what "careful" (the source's "substantive") review means.
3. **"Neither found more bugs or reverts" reads as reassurance.** [PS, WG]
   Harvard measured bug reports and CMU/Stanford measured reverts, both over a
   short horizon. Meanwhile, human review halved. Say "in the short term" and
   note that defects may surface later. Add "one firm" for CMU/Stanford and
   "working paper" for Harvard.
4. **"Check what humans have stopped reading" isn't actionable.** [NR] Give
   one concrete action, e.g. "sample bot-cleared PRs monthly and read them in
   full."

### consider

- Use "alongside authoring", not "with authoring". [SE]
- Merge the "Review fatigue" trap into the new capacity bullet, or have the
  trap point to it. [WG]

## adopting-coding-agents

### must-fix

5. **The student study is misdescribed.** [PS, WG; SE flagged the missing
   "who"] "Found the same" implies AI versus no AI, but the comparison was
   agent versus *chatbot* users. The bullet also drops a counter-finding: on a
   later task done without AI, both groups did about equally well. Name the
   source (UMD-led preprint, in progress) and its caveats (short tasks,
   short-term only).

### should-fix

6. **Quiz Q4 stem and distractors.** [NR, SE, WG] "Barely moved" overstates a
   14% rise; use "rose far less". The "ticket sizing" option is partly backed
   by the article's own PR-splitting trap, and "prompting skill" is never
   refuted, so replace both with options the article clearly refutes (e.g.
   usage dashboards). The Why line should keep the caveats ("observational
   working paper") and say the study *points to* review.
7. **"Change requests" vs "comments".** [SE, WG, NR] The source says comments
   per change rose 38.6%. Use "drew more review comments" in the article, the
   Why line and the quiz answer ("draw more comments").
8. **The mandate bullet lacks its caveats and cost.** [PS, WG, SE] It is one
   firm, not randomized, with uncapped AI budgets, so the figure is a ceiling.
   In the same firm, reviewer load doubled and careful human review roughly
   halved. The lead-in "A mandate doesn't set the pace" claims more than a
   study with no comparison can show; consider "A target doesn't set the pace."
9. **The Harvard bullet uses causal verbs.** [PS] It says "agents raised" and
   "Review was the bottleneck". Say "after adoption…", "the authors point to
   review", and note it is not peer reviewed and that the firms all use one
   analytics vendor. Optionally add "rule out gains above ~31%".
10. **Statistics jargon.** [NR] Gloss the phrases: "borderline result" means
    "may be noise"; "margin of error includes zero" means "too uncertain to
    rule out no speed-up".

### consider

- Restore "METR itself calls the result unreliable". [PS, WG]
- Restore "one library" for the Anthropic trial. [WG]
- Restore the examples in "each engineer invents their own habits". [NR]
- Resolve or drop the team-that-banned-agents thread in the Example. [NR, PS]
- Restore "longer if you release slowly" for the baseline. [PS]
- Explain why agents inflate deployment frequency. [NR]

The article is at 1,200 words, so every addition needs a matching cut.

## agent-instruction-files

### should-fix

11. **"Rules file" vs "instruction file".** [NR, SE, WG] Use the article's
    term throughout, in the article and the quiz. The study measured committed
    AI configuration generally, so the "three-quarters never edited" figure
    should say "agent config files".
12. **"Either way" points back at a choice not yet given.** [NR, SE] Write
    "whether or not the repository had an instruction file."
13. **The lead-in "linked to cleaner agent code" oversells.** [PS] Complexity
    still rose 27%. Use "linked to slower decay", and say it was measured by a
    static-analysis tool.

### consider

- In the trap, write "The Stanford and Carnegie Mellon study…" instead of
  "The same 2026 study…". [SE]
- Reword the quiz stem: "halves the rise in code complexity in repositories
  that use agents heavily". [NR, SE]
- The benefit appeared even in files nobody touched again, so a short,
  correct first version may matter more than ritual upkeep. [PS]

## feedback-loops-for-agents

### should-fix

14. **"Loop" now means two things.** [NR, SE, WG] The article's term is
    *feedback loop* (the checks). Call the new thing an *unattended agent run*
    (or "scheduled agent run"), defined once.
15. **Undefined and drifting terms.** [NR, SE] "Saved progress" vs "saved
    state" are undefined and drift. Define the term once (a record of what's
    done, so the next run doesn't start over) and use one word. Keeping it
    durable doesn't have to mean committing it to Git. [PS]
16. **Say the decision.** [PS] "If you can't write the stop condition, don't
    run it unattended." The paper's list of parts comes from practitioner
    blogs and posts, not measured results.
17. **The quiz has no "not yet / it depends" question.** [PS should-fix, SE
    consider] This was already the case before this change. Add one drawn
    from "When it doesn't apply" or from the unattended-run bullet.

### consider

- Define "token budget" or link [[large-language-models]], and give an
  example stop condition. [NR, SE]
- Split the bullet; it is the longest in the article. [NR, SE]

## Wiki-gardener: whole-wiki findings

### should-fix

18. **Unattended agent runs have no owner.** [WG, PS] They are covered in
    four articles (adopting, guardrails, reproducible-dev-environments, and
    now feedback-loops). Add a row to the CLAUDE.md concept-owner table
    (suggested: `agent-guardrails`). Then cut the feedback-loops bullet to
    the stop-condition point plus a link, and add a glossary entry once an
    owner is chosen. No new article yet; the evidence is a workshop paper.

### consider

- agent-guardrails' "Run unattended agents in a sandbox" should link back to
  where the stop condition and budget are described. [WG]
- code-review's "waiting at that gate is often the biggest delay" could point
  to [[reviewing-ai-generated-code]]. [WG]
- In adopting, trim the review clause to "Review was the bottleneck
  ([[reviewing-ai-generated-code]])", so the owner carries the detail. [WG]
- The feedback-loops index line no longer covers the loop content. Moving it
  to guardrails solves this. [WG]
- The manifest `short_name` and `apple-mobile-web-app-title` ("PE Wiki")
  could be derived from the site title. [WG]

Clean: every new number matches the sources file. Acronym expansion, bold
lead-ins, paragraph length and lint (66 articles, 0 problems) are all fine,
and no site copy restates content.

## Applied (2026-11-02)

All must-fix and should-fix items, with bot approval resolved as option (b):
bots are a first pass, and a human approves every merge. Following the user's
direction that the evidence is early and mixed, claims too thin to build on
were cut rather than caveated: the (Im)Paired comprehension result, and the
mandate study's throughput range. Consider items applied: METR redesign note,
"one library", the habit examples, the banned-team thread, the
deployment-frequency explanation, the guardrails back-link, the stop-condition
example. Not applied: the "Review fatigue" pointer (word limit), the
code-review back-link, and deriving `short_name` from the site title.

## technical-accuracy (completed after the limit reset, against 0d70370)

Every number matches its source. No must-fix. Should-fix, all applied:

- Harvard's agent effects are measured *on top of* AI-assistant adoption, not
  against no AI. Added to both articles and the sources row.
- Restored Harvard's counter-finding: the authors read the longer reviews and
  extra comments as lower-quality submitted code. Neither study's
  bug-report or revert null is precise enough to rule out a rise.
- Removed causal lead-ins and quiz stems: "AI amplifies…" (DORA is a
  self-report survey about AI tools, not agents), "It may slow the decay",
  "agents raised", "the rise … that agents cause".
- Sources row: opted-in Jellyfish sample, imprecise bug-report estimate.

Consider items applied: CMU "observational", "fix the checks first" in
Related, DORA "AI tools", the 14-month window, the glossary handoff, and the
CMU revert wording ("stayed flat, suggestive").
