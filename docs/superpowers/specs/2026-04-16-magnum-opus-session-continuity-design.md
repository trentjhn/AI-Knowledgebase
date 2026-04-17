# Magnum Opus Session Continuity — Design Spec
**Date:** 2026-04-16  
**Status:** Approved  
**Scope:** Forward-looking only — new projects scaffolded by Cook after this change. Existing projects are out of scope.

---

## Problem Statement

When a new Claude Code session opens on a project scaffolded by Cook/Magnum Opus, four things fail:

1. **Agent fleet not discovered** — `.claude/agents/` contents are not surfaced during context exploration, even when git log signals their existence (e.g., commit: "add agent definitions").
2. **Workflow chain invisible** — there is no document that tells a cold-start session which skills to invoke, in what order, for this specific project.
3. **Phase state lost** — session handoffs capture completed/pending tasks but not the current workflow phase or which skills to invoke next.
4. **Skill-to-agent routing undocumented** — when executing-plans dispatches subagents, there is no authoritative mapping from task type to agent. The routing lives only in the user's head.

**Root cause:** Two types of knowledge are missing from the scaffold:
- **Structural knowledge** (workflow chain, agent fleet, routing) — changes rarely, should be static in always-loaded documents
- **State knowledge** (current phase, next invocations) — changes every session, should live in handoffs

---

## Architecture: Five Touch Points

| Touch Point | Failure Mode Fixed | Mechanism |
|---|---|---|
| CLAUDE.md `## Development Workflow` section | Workflow chain invisible to cold-start | Always-loaded static document |
| CLAUDE.md `## Session Start Protocol` (replaces old rules 1+2) | Agent fleet not discovered; git log not checked; handoff-enforcement missing | Ordered protocol with Glob discovery |
| AGENTS.md `## Role Directory` section | Skill dispatch ignores agent fleet; routing lives only in user's head | Authoritative routing table, also written into implementation plan tasks |
| Session-handoff skill update | Phase state lost; next invocations not captured | Three new required output sections |
| Magnum Opus done-gate + maintenance contract update | Scaffold ships without these sections; fleet drifts post-scaffold | Checklist enforcement + update rules |

---

## Change 1: CLAUDE.md Template (Magnum Opus Phase 4 + Cook Phase 4)

### What changes

Every Cook-generated `CLAUDE.md` gets two structural changes:

**Replace required rules (1) and (2)** with a unified `## Session Start Protocol` section. Rule (3) (self-review before reporting complete) is kept as a standalone required rule. Do NOT append the new protocol alongside the old rules — replace them entirely.

**Add a `## Development Workflow` section** populated from Phase 3 skill selections.

### New CLAUDE.md Required Rules (exact structure Cook must generate)

```markdown
## Session Start Protocol
At the start of every session, in this exact order:
1. Read SOUL.md — load character before any work begins
2. Read AGENTS.md — load operational context, workflow chain, and role directory
3. Check `.sessions/handoffs/` for the most recent non-superseded handoff — read it to load phase state
4. Glob `.claude/agents/*` — discover the actual agent fleet (directory is authoritative; overrides any stale documentation)
5. Run `git log --oneline -5` — check for agent/config commits since last handoff (e.g., "add agent definitions" is a signal to read new files)
6. If handoff specifies "Next Session Invocations," invoke those skills via the Skill tool before proceeding. If no handoff exists, consult the Development Workflow section below and start from the beginning.
7. Before invoking any skill, invoke it via the Skill tool to read its current content — do not assume you know what it specifies.

## Development Workflow
[Cook writes this section in Phase 4, populated from Phase 3 skill selections. See Cook Phase 4 instructions.]

**First session (implementation plan already exists at docs/plans/implementation.md):**
Skip steps 1–2 below. Start at step 3 (Execute).

**Per-feature / new work:**
1. Brainstorm: invoke `brainstorming` skill → produces design doc in docs/superpowers/specs/
2. Plan: invoke `superpowers:writing-plans` → produces implementation plan with agent annotations
3. Execute: invoke `superpowers:executing-plans` → dispatches agents per AGENTS.md Role Directory and task annotations in the plan
4. Review: invoke `superpowers:requesting-code-review` → code-reviewer agent
5. Commit: invoke `smart-commit` skill → quality gate before push
6. Handoff: invoke `session-handoff` skill → REQUIRED before ending any session

When executing-plans or subagent-driven-development dispatches work, route tasks using the Role Directory in AGENTS.md. The implementation plan's agent annotations are authoritative for per-task routing.

## Required Rules
- After completing any meaningful chunk of work, read back what you produced against the acceptance criteria, check for rough edges and missing requirements, and fix any issues before reporting done. Self-review happens per artifact, not only at the final gate.
- Before ending any session — whether complete or interrupted — invoke the `session-handoff` skill. This is not optional.
```

### Cook Phase 4 execution instructions (new)

After copying agents to `.claude/agents/` and skills to `.claude/skills/`, Cook must:

1. **Write the Development Workflow section** using the exact skill names confirmed in Phase 3, in the order they apply to this project type. If the project is purely an engineering tool with no UI, omit frontend-specific skills. If it's an AI project, include eval-harness. Match the workflow to what was actually selected — do not use a generic template.

2. **Write the AGENTS.md Role Directory section** using the agents that were copied to `.claude/agents/` in Phase 3. Each row: agent filename (without .md), model tier, and a project-specific trigger condition (not a generic catalog description).

3. **Annotate every task in `docs/plans/implementation.md`** with the agent from the Role Directory that should execute it. Format: `**Agent: [agent-name]**` on the line after the task description. Tasks with no matching agent are executed inline by the orchestrating session. This annotation is what executing-plans reads to dispatch the correct `.claude/agents/` definition.

---

## Change 2: AGENTS.md Template (Magnum Opus Phase 4 + Cook Phase 4)

### What changes

Every Cook-generated `AGENTS.md` gets a new `## Role Directory` section.

**Important distinction:** The existing Sequential protocol ordering section describes phase sequencing — which agent *category* goes first, what it produces, what the next category receives. The Role Directory is different: it describes task-level dispatch during execution — when executing a specific task, which agent handles it. These are not the same thing and must be presented as distinct sections.

### New AGENTS.md structure (Cook must generate)

```markdown
# [Project Name] — AGENTS.md

## Mission
[One sentence: what problem this project solves for whom.]

## Sequential Protocol Ordering
[Only for multi-agent projects. Defines phase ordering — which category goes first, what it produces, what the next receives. Agents self-select within each phase based on what predecessors produced. This is NOT pre-assignment of tasks to agents.]

## Role Directory
When dispatching tasks, route by trigger condition. The implementation plan's **Agent:** annotations take precedence over this table for specific tasks.

| Agent | Model | Trigger — Use When |
|---|---|---|
| [agent-name] | [haiku/sonnet/opus] | [project-specific trigger condition] |
| ... | ... | ... |

If `.claude/agents/` contains files not listed here, Glob the directory, read those files, and add them before proceeding.

If no agent matches the trigger for a task, handle inline — do not force delegation.
```

---

## Change 3: Session-Handoff Skill Update

### What changes

Three new required sections added to the handoff output template. These are mandatory, not optional. A handoff without these sections is incomplete.

Insert after `## Key Decisions Made` and before `## Files Touched`:

```markdown
## Current Phase
- **Workflow phase**: [brainstorm / plan / execute / review / done]
- **Sub-step**: [e.g., "executing-plans — task 4 of 9 complete" or "plan written, not yet executing"]
- **Last verified checkpoint**: [last artifact confirmed correct]

## Active Agent Fleet
Run `Glob(".claude/agents/*")` and list results with one-line purpose:
- `[agent-filename].md` — [what it does / when to use it]
[List every file found. If new files appeared since last handoff, note them.]

## Next Session Invocations
Read the Development Workflow section of CLAUDE.md. Based on current phase, list the skills the next session should invoke first, in order:
1. [exact skill name, e.g., superpowers:executing-plans] — [one-line context, e.g., "resume from task 4, auth module"]
2. [next skill if applicable]
[If the session is complete, write: "No pending invocations — project is at [phase]."]
```

### Session-handoff skill discovery note

Do NOT add to the bash Commands block — Glob is a native Claude Code tool, not a bash command. Instead, add this note to the Workflow section after step 1 (Gather current state from git):

> After gathering git state, use the Glob tool with pattern `.claude/agents/*` to discover the active agent fleet. List every file found in the Active Agent Fleet section.

### Session-handoff skill instructions update

Add to the Workflow section after step 4 (Capture learnings):

> 5. To fill **Next Session Invocations**: read the `## Development Workflow` section of `CLAUDE.md`, identify the current phase, and list the remaining skills in sequence. Use exact skill names (e.g., `superpowers:executing-plans`, not "execute"). If mid-task, specify the sub-step (e.g., "task 4 of 9").

---

## Change 4: Magnum Opus Phase 4 Done-Gate

Add to the done-gate checklist:
```
- [ ] CLAUDE.md has ## Session Start Protocol section (not the old two-line rules)
- [ ] CLAUDE.md has ## Development Workflow section populated from actual Phase 3 skill selections (not a generic template)
- [ ] AGENTS.md has ## Role Directory section populated with all agents in .claude/agents/ — trigger conditions are project-specific, not generic catalog descriptions
- [ ] docs/plans/implementation.md tasks are annotated with **Agent:** from the Role Directory
```

---

## Change 5: Magnum Opus Maintenance Contract

Add row to the maintenance table:

| What changes | What to update |
|---|---|
| Agent added to `.claude/agents/` mid-project | AGENTS.md Role Directory + re-annotate affected implementation plan tasks |

---

## Change 6: Global Memory Entry

Write one feedback memory file to `~/.claude/projects/-Users-t-rawww-AI-Knowledgebase/memory/`.

**Content:**
- Rule: During context exploration for any project, always Glob `.claude/agents/*` to discover the agent fleet. Follow git log signals — a commit like "add agent definitions" means read `.claude/agents/`. The CLAUDE.md Development Workflow + AGENTS.md Role Directory are the authoritative references. Never rely on memory of what agents exist or what skills do — invoke and read.
- Why: Viridian session (2026-04-16) failed to discover six agents despite a direct git log signal. Context was reconstructed from scratch each session.
- How to apply: Session start → Glob `.claude/agents/*` → cross-reference with AGENTS.md Role Directory → check handoff for current phase → invoke skills from Next Session Invocations before any other work.

---

## Change 7: KB-INDEX.md Update

After all file edits are committed, update KB-INDEX.md with new line ranges and section descriptions for:
- `future-reference/playbooks/magnum-opus.md` — Phase 4 section expanded (new CLAUDE.md rules, AGENTS.md Role Directory, implementation plan annotation, done-gate items, maintenance contract row)
- `future-reference/skills-catalog/meta/cook/SKILL.md` — Phase 4 expanded (Development Workflow generation, Role Directory generation, implementation plan task annotation, done-gate items)
- `future-reference/skills-catalog/workflow/session-handoff/SKILL.md` — Three new required output sections (Current Phase, Active Agent Fleet, Next Session Invocations)

---

## Acceptance Criteria

**Given** a new project scaffolded by Cook after this change:

**Cold-start session:**
- When a new session opens, CLAUDE.md Session Start Protocol is present and instructs Glob `.claude/agents/*` as step 4
- When a new session follows the protocol, it discovers all agents without reading git history or handoff docs
- When no handoff exists (first session), the protocol falls back to Development Workflow cleanly

**Workflow routing:**
- When executing-plans dispatches a task, the implementation plan's **Agent:** annotation specifies which `.claude/agents/` definition to use
- When a task has no annotation, the agent handles it inline — no undirected guessing

**Session boundary:**
- When a session ends, CLAUDE.md required rule enforces session-handoff invocation
- When next session reads the handoff, it has exact phase, active fleet, and ordered skill invocations to resume from

**Maintenance:**
- When a new agent is added to `.claude/agents/` mid-project, AGENTS.md Role Directory is the documented update target (maintenance contract row)

---

## Files Changed (Implementation Targets)

1. `future-reference/playbooks/magnum-opus.md` — Phase 4 (CLAUDE.md rationale, AGENTS.md rationale + Role Directory, implementation plan annotation instruction, done-gate 4 new items, maintenance contract 1 new row)
2. `future-reference/skills-catalog/meta/cook/SKILL.md` — Phase 4 execution (Development Workflow generation, AGENTS.md Role Directory generation, implementation.md annotation, file list descriptions, done-gate 4 new items)
3. `future-reference/skills-catalog/workflow/session-handoff/SKILL.md` — Workflow step 5 added, Commands block updated, output template 3 new sections
4. `~/.claude/projects/-Users-t-rawww-AI-Knowledgebase/memory/feedback_agent_fleet_discovery.md` — new global feedback memory
5. `KB-INDEX.md` — updated line ranges for all 3 changed KB files

**Total issues resolved:** 11 (5 design + 3 deployment + 3 deep-review)
