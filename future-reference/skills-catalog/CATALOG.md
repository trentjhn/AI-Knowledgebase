# Skills Catalog — Flat Index

Read this to find the right skill for a task. Skills are reusable
procedures invoked during execution — distinct from agents (role
definitions) and prompts (templates).

---

## Workflow Skills

| Skill | Invoke when | What it does |
|---|---|---|
| [brainstorming](workflow/brainstorming/) | Starting any new feature, task, or creative work; requirements are vague | Explores intent and design before implementation; outputs design doc |
| [planning](workflow/planning/) | After design is approved; before writing code for multi-step tasks | Creates bite-sized implementation plan with exact file paths and commands |
| [smart-commit](workflow/smart-commit/) | Saying "commit" or ready to save changes | Quality gates, reviews staged changes, creates conventional commit |
| [deslop](workflow/deslop/) | Cleaning up code; removing boilerplate; simplifying before PR | Removes AI-generated slop, unnecessary comments, over-engineering |
| [session-handoff](workflow/session-handoff/) | Ending a session; "save progress"; "pick up later" | Structured handoff document capturing progress and context |
| [human-voice](workflow/human-voice/) | Drafting any email, message, Slack, or professional communication | Writes in TJ's voice — direct, warm, not corporate |
| [learn-rule](workflow/learn-rule/) | Capturing a correction or lesson; "remember this" | Saves persistent learning rule to memory |
| [insights](workflow/insights/) | Post-implementation review needed | Surfaces non-obvious patterns and lessons from the work |
| [parallel-worktrees](workflow/parallel-worktrees/) | Starting feature work needing isolation from current workspace | Creates isolated git worktrees with safety verification |
| [pro-workflow](workflow/pro-workflow/) | Professional development workflow needed | Full professional workflow with review gates |
| [replay-learnings](workflow/replay-learnings/) | Reviewing accumulated lessons; applying past corrections | Replays stored learning rules to current context |
| [wrap-up](workflow/wrap-up/) | Session complete; wrapping up work | Consolidates session output, updates docs, commits |

## Design Skills

| Skill | Invoke when | What it does |
|---|---|---|
| [ui-ux-pro-max](design/ui-ux-pro-max/) | Building any UI; design system needed; component library decisions | Full design system generator: tailwind config, globals.css, components |
| [frontend-taste](design/frontend-taste/) | Frontend code needs design quality lift; AI-generic aesthetics need removing | Applies design taste guidelines: DESIGN_VARIANCE:8, MOTION_INTENSITY:6 |
| [web-design-patterns](design/web-design-patterns/) | Web UI needs established patterns applied correctly | Pattern library: navigation, forms, cards, layouts, interactions |
| [brand-identity](design/brand-identity/) | Brand system needs definition or application | Brand tokens, voice, visual identity system |
| [redesign-skill](design/redesign-skill/) | Existing UI needs systematic redesign | Redesign methodology: audit → direction → execution |
| [optimizing-seo](design/optimizing-seo/) | Page SEO needs improvement | SEO audit and optimization recommendations |

## Engineering Skills

| Skill | Invoke when | What it does |
|---|---|---|
| [tdd-workflow](engineering/tdd-workflow/) | Writing code that needs tests; TDD discipline needed | Test-first development workflow |
| [verification-loop](engineering/verification-loop/) | Before claiming work is complete; before commits | Runs verification gates and confirms output |
| [api-design](engineering/api-design/) | API endpoints need design; REST/GraphQL patterns needed | API design patterns and review |
| [security-review](engineering/security-review/) | Code needs security audit; before production deploy | Security checklist and vulnerability scan |
| [security-scan](engineering/security-scan/) | Automated security scanning needed | Runs security scanning tools |
| [backend-patterns](engineering/backend-patterns/) | Backend code needs established patterns | Backend architecture patterns |
| [frontend-patterns](engineering/frontend-patterns/) | Frontend code needs established patterns | Frontend component and state patterns |
| [git-workflow](engineering/git-workflow/) | Git workflow needs structure; branching strategy needed | Git workflow guide |
| [database-migrations](engineering/database-migrations/) | Database schema changes needed | Safe migration patterns |
| [error-handling-patterns](engineering/error-handling-patterns/) | Error handling needs design; silent failures occurring | Error handling contract and patterns |
| [cloning-protocol](engineering/cloning-protocol/) | Project needs to be cloned or templated | Project cloning and setup protocol |

## Meta Skills

| Skill | Invoke when | What it does |
|---|---|---|
| [cook](meta/cook/) | Starting any new project; "new project", "let's build", "/cook" | Runs the full magnum-opus 9-phase scaffold workflow; writes complete project structure to disk |

## Production Skills

| Skill | Invoke when | What it does |
|---|---|---|
| [context-budget](production/context-budget/) | AI project needs token budget planning | Context budget allocation and compaction strategy |
| [strategic-compact](production/strategic-compact/) | Context is approaching limits; compaction needed | Strategic context compaction (50% threshold rule) |
| [eval-harness](production/eval-harness/) | AI system needs automated evaluation setup | Eval harness scaffolding and framework selection |
| [cost-aware-llm-pipeline](production/cost-aware-llm-pipeline/) | LLM costs need optimization; model routing needed | Cost optimization: Haiku/Sonnet/Opus routing |
| [deployment-patterns](production/deployment-patterns/) | Deployment architecture needed; CI/CD setup; Docker; blue-green/canary strategies | Deployment strategies, Dockerfiles, GitHub Actions pipeline, health checks, rollback commands |
| [pre-ship](production/pre-ship/) | "Ready to ship", "deploy to production", "going live", "launch" | Pre-deploy safety gate: security + database + infrastructure + code quality + monitoring checklist. Check-in first, never auto-runs. |
| [continuous-learning](production/continuous-learning/) | Agent needs to improve from interactions; instinct system needed | Continuous learning via micro-skills and confidence scoring |
