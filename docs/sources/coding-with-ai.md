# Sources: Coding with AI

Research behind the `wiki/coding-with-ai/` articles, checked 2026-11-01.
This field moves fast: re-verify these at every review and update the
articles when newer evidence lands.

| Claim | Source | Caveats |
| --- | --- | --- |
| Experienced OSS developers were 19% slower with early-2025 AI tools, predicted 24% faster, believed 20% faster afterwards. | METR, "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity" (July 2025). <https://metr.org/> | 16 developers, 246 tasks, mature repos they knew well. |
| Follow-up: returning devs −18% time (CI −38% to +9%), new devs −4% (CI −15% to +9%); METR calls the signal unreliable and is redesigning. | METR, "We are Changing our Developer Productivity Experiment Design" (2026-02-24). <https://metr.org/blog/2026-02-24-uplift-update/> | CIs include zero; selection effects (developers declining no-AI tasks). |
| AI is an "amplifier" of existing strengths and weaknesses; ~90% adoption. | DORA, *State of AI-assisted Software Development* (2025). <https://dora.dev/research/2025/dora-report/> | Survey of ~5,000 professionals. |
| Seven capabilities amplify AI's benefits, incl. clear and communicated AI stance, healthy data ecosystems, working in small batches, user-centric focus, quality internal platforms. | DORA AI Capabilities Model (2025). <https://dora.dev/ai/capabilities-model> | Full list of seven not verified from the primary PDF; articles only name the ones confirmed. |
| Adopters of CLI coding agents merged +24.0% PRs/engineer/day (95% CI +14.5% to +33.7%); adoption spread through peers (skip-level peers +216% odds of trying). | Murphy-Hill, Butler, Savelieva (Microsoft), arXiv:2607.01418 (July 2026). <https://arxiv.org/abs/2607.01418> | One company, 16 weeks; quality, reverts, review time not measured; merged-PR counts reward small PRs; authors' employer owns GitHub. |
| AI-assisted learners of a new library scored 50% vs 67% on a quiz; largest gap on debugging; conceptual-question users scored higher. | Anthropic, "How AI assistance impacts the formation of coding skills" (2026-01-29). <https://www.anthropic.com/research/AI-assistance-coding-skills> | 52 developers, one library (Trio), quiz immediately after. |
| Explore → plan → code → commit; keep CLAUDE.md short and prune it; give the agent a way to verify its work. | Anthropic, Claude Code best practices. <https://code.claude.com/docs/en/best-practices> | Vendor guidance. |
| AGENTS.md is an open format, contributed to the Linux Foundation's Agentic AI Foundation (Dec 2025). | OpenAI, "Agentic AI Foundation". <https://openai.com/index/agentic-ai-foundation/> | Adoption figures are vendor-reported. |
| "Prompt injection" (term coined 2022) and the "lethal trifecta": private data + untrusted content + external communication. | Simon Willison, simonwillison.net (June 2025 post; "Living dangerously with Claude", Oct 2025). <https://simonwillison.net/2025/Oct/22/living-dangerously-with-claude/> | — |
| Permissions stop the agent trying; sandboxing stops an attempt succeeding. | Claude Code docs, Sandboxing. <https://code.claude.com/docs/en/sandboxing> | Vendor docs; specifics vary by tool. |
