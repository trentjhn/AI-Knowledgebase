---
name: cook
description: Complete project scaffold generator. Invokes the full magnum-opus workflow — traverses KB, selects agents and skills, asks targeted questions, and writes a production-ready project structure. Use when starting any new project. Trigger: "new project", "start building", "/cook", "scaffold a project for", "let's build", "I want to build".
---

# /cook — Project Scaffold Workflow

You are the executor of the magnum-opus workflow. Your job is to read
the decision hub, traverse the knowledge and capability layers, and
write a complete production-ready project scaffold.

## Configuration

```
KB_ROOT = /path/to/your/AI-Knowledgebase
```

**Before using this skill:** Replace every path below that starts with
`/path/to/your/AI-Knowledgebase` with the absolute path to your local
KB clone. This is the only change needed to make the skill functional
on a new machine.

## Before Anything Else

Read the full magnum-opus.md hub document:
`/path/to/your/AI-Knowledgebase/future-reference/playbooks/magnum-opus.md`

This is your decision engine. Follow its phases in order.
Do not skip phases. Do not advance past a gate until it passes.

## Execution Instructions

### Phase 0: Intake
1. Check `/path/to/your/AI-Knowledgebase/.sessions/` for prior notes on this topic
2. Ask: "Describe the project in one sentence — what problem does it solve for whom?"
3. Run CLAUDE.md pattern recognition — consult `/path/to/your/AI-Knowledgebase/CLAUDE.md` for the pattern rubric
4. Read `/path/to/your/AI-Knowledgebase/KB-INDEX.md` targeted sections based on patterns fired
5. Report: "Here are the KB domains relevant to this project: [list with file + line ranges]"

### Phase 0.5: Domain Research
1. Run last30days skill for the project domain: HN + YouTube, 30 days
   (Install last30days from: https://github.com/mvanhorn/last30days-skill)
2. Note findings in session context only — do not write to files
3. Surface: "Recent practitioner findings relevant to this project: [2-3 points]"

### Phase 1: Project Classification
Ask one question at a time:
1. "Is this primarily AI/agentic, product/UI, engineering infrastructure, or a combination?"
2. "Greenfield (new repo) or adding to an existing codebase?"
3. "Will this need a single agent, hierarchical multi-agent, or an agent team (peer agents with shared task list)?"

If agent teams are under consideration, reference:
`/path/to/your/AI-Knowledgebase/LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agent-teams.md`

Report: "Classification: [type]. Playbook(s): [list]. Topology: [single/hierarchical/team]."

### Phase 1.5: Specification + Pre-flight
1. Walk through the 7-property spec framework — reference:
   `/path/to/your/AI-Knowledgebase/LEARNING/PRODUCTION/specification-clarity/specification-clarity.md`
2. For each property, ask a targeted question until the property is satisfied
3. Write at least one BDD Given/When/Then scenario for each key behavior
4. Run the 4 failure mode pre-flight check — reference:
   `/path/to/your/AI-Knowledgebase/future-reference/playbooks/building-ai-saas.md`
5. Present the completed spec and get explicit confirmation before advancing

Gate check: "Does this spec satisfy all 7 properties? Can a developer implement it without asking questions?" Do not advance until the answer is yes.

### Phase 2: Harness Design
Present decisions one at a time with KB-grounded options:
1. Four Pillars — fill each explicitly (Prompt / Model / Context / Tools)
   Reference: `/path/to/your/AI-Knowledgebase/LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md` §1
2. Context window architecture — what loads, what stays out, token budget
   Reference: `/path/to/your/AI-Knowledgebase/LEARNING/FOUNDATIONS/context-engineering/context-engineering.md` lines 132-204
3. Memory architecture — short-term / episodic / semantic
4. RAG needed? → If yes, reference:
   `/path/to/your/AI-Knowledgebase/future-reference/playbooks/building-rag-pipelines.md`
5. MCP needed? → If yes, reference:
   `/path/to/your/AI-Knowledgebase/LEARNING/AGENTS_AND_SYSTEMS/mcp/mcp.md`
6. Execution topology (multi-agent or agent teams)
7. Loop pattern — ReAct / Plan-Build-Review / Sequential / Event-driven
8. HITL gates — list every point where human approval is required
9. Model and cost tier — with ceiling per request
10. Error handling contract — explicit behavior for every failure type
11. SOUL.md character — ask: "What is this agent's project-specific character?"
    Template at: `/path/to/your/AI-Knowledgebase/future-reference/agent-catalog/SOUL-TEMPLATE.md`

Gate: present a summary of all Phase 2 decisions and get explicit confirmation before proceeding.

### Phase 2.5: Build Methodology
1. Present methodology options — reference:
   `/path/to/your/AI-Knowledgebase/LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md` lines 2865-2935
2. Recommend BMAD for complex/multi-agent, plan-first for everything else
3. Confirm git workflow approach

### Phase 3: Capability Selection
1. Read `/path/to/your/AI-Knowledgebase/future-reference/agent-catalog/CATALOG.md` — present relevant agent pool for this project type
2. Read `/path/to/your/AI-Knowledgebase/future-reference/skills-catalog/CATALOG.md` — present relevant skills
3. Read `/path/to/your/AI-Knowledgebase/future-reference/prompt-catalog/CATALOG.md` — present relevant templates if applicable
4. Confirm selections with user
5. For multi-agent or agent teams: establish Sequential protocol ordering

### Phase 4: Scaffold Output
Write all files to the specified project directory.

**Required files (every project):**
- `CLAUDE.md` — project-specific; must include Session Start Protocol (7-step ordered list), Development Workflow (from Phase 3 skill selections), and Required Rules (self-review + session-handoff enforcement)
- `AGENTS.md` — mission + Role Directory (all projects with agents) + Sequential Protocol Ordering (multi-agent only)
- `SOUL.md` — from SOUL-TEMPLATE.md with [PROJECT CHARACTER] customized for this project
- `README.md` — project overview, what was scaffolded, next steps
- `.gitignore`
- `.claude/agents/` — selected agent definitions (copied from `/path/to/your/AI-Knowledgebase/future-reference/agent-catalog/`)
- `.claude/skills/` — selected skills (copied from `/path/to/your/AI-Knowledgebase/future-reference/skills-catalog/`)
- `.claude/settings.json` — hook configurations
- `docs/kb-references.md` — KB section pointers only (never content copies)
- `docs/plans/design.md` — all Phase 2 decisions captured with rationale
- `docs/plans/implementation.md` — ordered build plan grounded in KB
- `.sessions/[project-name]/` — local workspace directory (not committed)

**AI projects additionally:**
- `docs/prompts/` — system prompts designed in Phase 2, one file per prompt

**After copying agents to `.claude/agents/` and skills to `.claude/skills/`, execute these three generation steps before writing any other file:**

**Generation Step A — Populate CLAUDE.md Session Start Protocol and Development Workflow:**
Write these two sections using the exact skill names confirmed in Phase 3, in the order they apply to this project. Do not use a generic template — the workflow must reflect actual Phase 3 selections. The Development Workflow section must include the "First session (implementation plan exists): skip to Execute" conditional. The Required Rules section must include the session-handoff enforcement rule ("Before ending any session — whether complete or interrupted — invoke the `session-handoff` skill. This is not optional."). Remove the old rules (1) and (2) — they are replaced by the Session Start Protocol section entirely.

**Generation Step B — Populate AGENTS.md Role Directory:**
Add a `## Role Directory` section to AGENTS.md. One row per agent in `.claude/agents/`. Each row: agent filename without .md extension, model tier (haiku/sonnet/opus), and a project-specific trigger condition written for this project's context — not a generic catalog description. Add this self-healing note below the table: "If `.claude/agents/` contains files not listed here, Glob the directory, read those files, and add them before proceeding."
Add this fallback row below the note: "If no agent matches the trigger for a task, handle inline — do not force delegation."

**Generation Step C — Annotate implementation.md tasks with Agent:**
For every task in `docs/plans/implementation.md`, add `**Agent: [agent-name]**` on the line after the task description, using the Role Directory to assign. Tasks with no matching agent get: `**Agent: inline — no delegation.**` This annotation is what executing-plans reads to dispatch `.claude/agents/` definitions.

**Done-gate — verify every item before reporting scaffold complete:**
- [ ] All required files exist and are non-empty
- [ ] `docs/kb-references.md` has entries for every load-bearing KB section from Phase 0
- [ ] `docs/plans/design.md` captures all Four Pillars, topology, error contract, and character design with rationale
- [ ] `SOUL.md` [PROJECT CHARACTER] section is customized — not left as the default template text
- [ ] Eval criteria defined in `docs/plans/design.md`
- [ ] Security threat model started in `docs/plans/design.md`
- [ ] `CLAUDE.md` Session Start Protocol and Development Workflow sections are populated with project-specific content — not generic template text
- [ ] `CLAUDE.md` Required Rules section includes the session-handoff enforcement rule
- [ ] `AGENTS.md` Role Directory section is populated with all agents in `.claude/agents/` — trigger conditions are project-specific
- [ ] `docs/plans/implementation.md` tasks are annotated with `**Agent:**` from the Role Directory

### Phase 5: Eval + Security Baseline
1. Write initial eval criteria to docs/plans/design.md
   Reference: `/path/to/your/AI-Knowledgebase/LEARNING/PRODUCTION/evaluation/evaluation.md`
2. Write first-pass threat model to docs/plans/design.md
   Reference: `/path/to/your/AI-Knowledgebase/LEARNING/PRODUCTION/ai-security/ai-security.md` lines 63-145
3. Note observability signals for this project type
4. If AI project: note when to run harness optimization (after 50-100 production interactions)
5. Remind: update `/path/to/your/AI-Knowledgebase/builds-log.md` when this project ships

## After Scaffold Complete

Report:
"Scaffold complete. Files written to [path].

Load-bearing KB references: [list from docs/kb-references.md]

Next step: Open [path] in a new Claude Code session. The scaffold is ready.
Implementation plan is at docs/plans/implementation.md."
