# Skills Catalog

A pull-ready library of Claude Code skills and agent definitions. Browse, then copy what you need into any project.

## How to Use

**Skills** — drop into `.claude/skills/<skill-name>/SKILL.md` in your project. Claude Code auto-loads them and triggers based on description matching.

**Agents** — drop into `.claude/agents/<agent-name>.md` in your project. Reference them via `Agent` tool calls in your instructions.

```bash
# Example: add TDD workflow + code reviewer to a new project
cp -r ~/AI-Knowledgebase/skills-catalog/engineering/tdd-workflow /your-project/.claude/skills/
cp ~/AI-Knowledgebase/skills-catalog/agents/code-reviewer.md /your-project/.claude/agents/
```

---

## Skills by Category

### Workflow (11 skills) — Session orchestration, git, memory
*Source: Skills Master*

| Skill | Triggers On | Purpose |
|---|---|---|
| `brainstorming` | Before any new feature or task | Structured ideation before coding |
| `planning` | Multi-step work, architecture decisions | Build a plan before touching code |
| `smart-commit` | "commit", "save changes" | Staged commits with quality scan |
| `deslop` | "clean up", before committing | Remove AI-generated slop patterns |
| `wrap-up` | "wrap up", end of session | Session summary + handoff prep |
| `session-handoff` | "continue later", "next session" | Context file for seamless resumption |
| `parallel-worktrees` | Waiting on tests/builds | Run parallel work in git worktrees |
| `pro-workflow` | "set up", AI coding best practices | Configure the full agentic workflow |
| `learn-rule` | "remember this", after a mistake | Codify lessons into persistent rules |
| `replay-learnings` | "before I start", "remind me" | Load prior session learnings into context |
| `insights` | "show stats", "analytics", "how am I doing" | Session performance metrics |

---

### Design (6 skills) — UI/UX, visual systems
*Source: Skills Master*

| Skill | Triggers On | Purpose |
|---|---|---|
| `frontend-taste` | Any frontend UI generation | Enforces premium design standards (dials: variance/motion/density) |
| `ui-ux-pro-max` | UI/UX requests, design systems | Data-driven design via 14 CSV style databases |
| `web-design-patterns` | Design systems, component architecture | Design-system-first component workflow |
| `redesign-skill` | "upgrade", "improve", "redesign" | Audits + elevates existing UI |
| `brand-identity` | Styling, copywriting, brand consistency | Applies brand tokens across UI/copy |
| `optimizing-seo` | "SEO", "ranking", "meta tags" | Technical + content SEO workflow |

---

### Engineering (11 skills) — Code quality, patterns, security
*Sources: Skills Master (2) + ECC (9)*

| Skill | Triggers On | Purpose | Source |
|---|---|---|---|
| `tdd-workflow` | Writing features, fixing bugs, refactoring | Red-Green-Refactor with git checkpoints, 80% coverage target | ECC |
| `verification-loop` | Before PRs, after completing features | 6-phase quality gate: build → types → lint → test → security → diff | ECC |
| `git-workflow` | Branching, commits, merges, conflicts | Branching strategies, commit conventions, conflict resolution | ECC |
| `api-design` | Building APIs, REST endpoints | REST patterns, status codes, pagination, versioning | ECC |
| `backend-patterns` | Backend architecture, service layers | Repository/service/middleware patterns, caching, auth, rate limiting | ECC |
| `frontend-patterns` | React components, hooks, state | React patterns, custom hooks, performance, accessibility | ECC |
| `security-scan` | Pre-deploy, security audit | AgentShield scan — A-F grading, 1,282 tests, 102 rules | ECC |
| `security-review` | Code review, pre-PR | 10-section security checklist + pre-deploy verification | ECC |
| `database-migrations` | Schema changes, DB work | PostgreSQL, Prisma, Drizzle, Kysely, golang-migrate patterns | ECC |
| `error-handling-patterns` | Implementing error handling, API design | Cross-language patterns (Python, TS, Rust, Go) + universal strategies | Skills Master |
| `cloning-protocol` | "clone this site", "brand swap", "re-skin" | 6-phase discovery + 8-step implementation for site clones | Skills Master |

---

### Production (6 skills + reference) — Operations, cost, observability
*Source: ECC*

| Skill | Triggers On | Purpose |
|---|---|---|
| `context-budget` | Before scaling, performance issues | Token cost audit across all context components |
| `strategic-compact` | Long sessions, context pressure | Safe `/compact` timing — what survives, what doesn't |
| `continuous-learning` | Session setup, pattern capture | Stop-hook extraction of error patterns + corrections |
| `cost-aware-llm-pipeline` | Cost optimization, model routing | 3-tier model routing, prompt caching, retry logic |
| `eval-harness` | Building evals, regression testing | EDD framework, capability/regression evals, pass@k metrics |
| `deployment-patterns` | Deploying, CI/CD setup | Rolling/blue-green/canary, Docker, GitHub Actions, rollback |
| `hooks-reference.md` | Reference doc | Full hooks architecture — all 6 types, profiles, custom hook contract |

---

### Agents (15 definitions) — Drop into `.claude/agents/`
*Source: ECC*

| Agent | Model | Role |
|---|---|---|
| `planner.md` | opus | Creates implementation plans from requirements |
| `architect.md` | opus | System design, architecture decisions |
| `chief-of-staff.md` | opus | Coordinates work across multiple agents |
| `loop-operator.md` | sonnet | Manages autonomous agent loop execution |
| `harness-optimizer.md` | sonnet | Optimizes agent harness configuration |
| `code-reviewer.md` | sonnet | Code review against project standards |
| `security-reviewer.md` | sonnet | Security-focused code review |
| `tdd-guide.md` | sonnet | Enforces TDD workflow across implementation |
| `build-error-resolver.md` | haiku | Diagnoses and fixes build failures |
| `performance-optimizer.md` | sonnet | Identifies and resolves performance bottlenecks |
| `doc-updater.md` | haiku | Keeps documentation in sync with code changes |
| `refactor-cleaner.md` | sonnet | Code cleanup and refactoring without behavior change |
| `python-reviewer.md` | sonnet | Python-specific review (Pythonic patterns, type hints) |
| `typescript-reviewer.md` | sonnet | TypeScript-specific review (types, generics, patterns) |
| `go-reviewer.md` | sonnet | Go-specific review (idiomatic Go, concurrency) |

---

### Meta (1 skill) — Skill creation
*Source: Skills Master*

| Skill | Triggers On | Purpose |
|---|---|---|
| `antigravity_skill_creator` | Creating or modifying a skill | The schema and workflow for building new skills |

---

## Quick Reference — Common Project Setups

**New web app:**
```bash
cp -r skills-catalog/workflow/brainstorming .claude/skills/
cp -r skills-catalog/workflow/planning .claude/skills/
cp -r skills-catalog/engineering/tdd-workflow .claude/skills/
cp -r skills-catalog/engineering/verification-loop .claude/skills/
cp -r skills-catalog/design/frontend-taste .claude/skills/
cp skills-catalog/agents/planner.md .claude/agents/
cp skills-catalog/agents/code-reviewer.md .claude/agents/
```

**API / backend project:**
```bash
cp -r skills-catalog/engineering/tdd-workflow .claude/skills/
cp -r skills-catalog/engineering/api-design .claude/skills/
cp -r skills-catalog/engineering/backend-patterns .claude/skills/
cp -r skills-catalog/engineering/security-review .claude/skills/
cp -r skills-catalog/engineering/database-migrations .claude/skills/
cp skills-catalog/agents/architect.md .claude/agents/
cp skills-catalog/agents/security-reviewer.md .claude/agents/
```

**Production hardening / pre-launch:**
```bash
cp -r skills-catalog/production/verification-loop .claude/skills/
cp -r skills-catalog/production/context-budget .claude/skills/
cp -r skills-catalog/production/deployment-patterns .claude/skills/
cp -r skills-catalog/engineering/security-scan .claude/skills/
```

**Long AI session / research:**
```bash
cp -r skills-catalog/workflow/pro-workflow .claude/skills/
cp -r skills-catalog/workflow/session-handoff .claude/skills/
cp -r skills-catalog/production/strategic-compact .claude/skills/
cp -r skills-catalog/production/continuous-learning .claude/skills/
```
