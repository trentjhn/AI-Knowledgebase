# Magnum Opus Session Continuity — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Patch five files so every Cook-scaffolded project automatically surfaces its agent fleet, communicates its workflow chain, enforces session handoffs, and carries phase state across sessions.

**Architecture:** Text/markdown edits only — no code. Each task targets one section of one file with exact old→new strings. No placeholders, no interpretation required. Commit after each file is fully patched.

**Tech Stack:** Edit tool (old_string → new_string), Glob tool for fleet discovery, Write tool for the new memory file.

**Spec:** `docs/superpowers/specs/2026-04-16-magnum-opus-session-continuity-design.md`

---

### Task 1: magnum-opus.md — Update directory tree comments for CLAUDE.md and AGENTS.md

**Files:**
- Modify: `future-reference/playbooks/magnum-opus.md` (lines 264–266)

- [ ] **Step 1: Read the current tree block to confirm exact text**

Read `future-reference/playbooks/magnum-opus.md` lines 260–270. Confirm lines 264–266 contain exactly:
```
├── CLAUDE.md           ← project-specific, KB-grounded operational rules
│                           Must include: "Read SOUL.md before anything else"
├── AGENTS.md           ← mission + Sequential protocol ordering (NOT role assignments)
```

- [ ] **Step 2: Edit the tree comments**

Use Edit tool:

old_string:
```
├── CLAUDE.md           ← project-specific, KB-grounded operational rules
│                           Must include: "Read SOUL.md before anything else"
├── AGENTS.md           ← mission + Sequential protocol ordering (NOT role assignments)
```

new_string:
```
├── CLAUDE.md           ← project-specific, KB-grounded operational rules
│                           Must include: Session Start Protocol + Development Workflow + Required Rules
├── AGENTS.md           ← mission + Role Directory (all projects) + Sequential Protocol Ordering (multi-agent only)
```

- [ ] **Step 3: Verify**

Read lines 260–270 and confirm the two updated comment lines are correct. No other lines changed.

---

### Task 2: magnum-opus.md — Replace CLAUDE.md file-by-file rationale

**Files:**
- Modify: `future-reference/playbooks/magnum-opus.md` (line 292)

- [ ] **Step 1: Confirm exact target text**

Read lines 290–295. Confirm line 292 starts with `` `CLAUDE.md` is the project's operating contract `` and ends with ``Self-review happens per artifact, not only at the final gate."``

- [ ] **Step 2: Replace the CLAUDE.md rationale paragraph**

Use Edit tool:

old_string:
```
`CLAUDE.md` is the project's operating contract for Claude — it sets the constraints, the conventions, and the reference to SOUL.md. Without it, Claude starts each session with default behavior. With it, Claude starts each session with project-specific constraints. Required rules in every project CLAUDE.md: (1) "Read SOUL.md before anything else." (2) "At session start, check `.sessions/handoffs/` for the most recent non-superseded handoff and load it before doing anything else." (3) "After completing any meaningful chunk of work — a component, a page, a feature, a spec section — read back what you produced against the acceptance criteria, check for rough edges and missing requirements, and fix any issues before reporting done. Self-review happens per artifact, not only at the final gate."
```

new_string:
```
`CLAUDE.md` is the project's operating contract for Claude — it sets the constraints, the conventions, and the workflow protocol. Without it, Claude starts each session with default behavior. With it, Claude starts each session with project-specific constraints and a complete operational context. Every Cook-generated CLAUDE.md must contain three sections:

**(1) Session Start Protocol** — a numbered, ordered list every session executes before any work. Required steps, in order: (a) Read SOUL.md — load character before anything else. (b) Read AGENTS.md — load operational context and role directory. (c) Check `.sessions/handoffs/` for the most recent non-superseded handoff — read it to load phase state. (d) Glob `.claude/agents/*` — discover the actual agent fleet; the directory is authoritative and overrides any stale documentation. (e) Run `git log --oneline -5` — catch agent/config changes since last handoff (a commit like "add agent definitions" is a signal to read new files). (f) If handoff specifies "Next Session Invocations," invoke those skills via the Skill tool before proceeding; if no handoff exists, consult the Development Workflow section and start from the beginning. (g) Before invoking any skill, invoke it via the Skill tool to read its current content — do not assume.

**(2) Development Workflow section** — the project-specific skill chain written by Cook in Phase 4 from Phase 3 selections. Must distinguish: "First session (implementation plan already exists at docs/plans/implementation.md): skip to Execute" from "Per-feature / new work: Brainstorm → Plan → Execute → Review → Commit → Handoff." Must include: "When executing-plans or subagent-driven-development dispatches work, route tasks using the Role Directory in AGENTS.md. The implementation plan's Agent: annotations are authoritative for per-task routing."

**(3) Required Rules section** — must contain: "After completing any meaningful chunk of work, read back what you produced against the acceptance criteria, check for rough edges and missing requirements, and fix any issues before reporting done. Self-review happens per artifact, not only at the final gate." AND: "Before ending any session — whether complete or interrupted — invoke the `session-handoff` skill. This is not optional."
```

- [ ] **Step 3: Verify**

Read lines 290–310. Confirm the old single paragraph is replaced by the three-section description. Confirm no other lines were altered.

---

### Task 3: magnum-opus.md — Replace AGENTS.md file-by-file rationale

**Files:**
- Modify: `future-reference/playbooks/magnum-opus.md` (line 294)

- [ ] **Step 1: Confirm exact target text**

Read lines 293–296. Confirm line 294 reads:
```
`AGENTS.md` defines the mission in one sentence and the phase ordering for multi-agent work. It does NOT assign specific agents to specific tasks — that is the Sequential protocol's job. AGENTS.md gives agents the context they need to self-select appropriate roles.
```

- [ ] **Step 2: Replace the AGENTS.md rationale paragraph**

Use Edit tool:

old_string:
```
`AGENTS.md` defines the mission in one sentence and the phase ordering for multi-agent work. It does NOT assign specific agents to specific tasks — that is the Sequential protocol's job. AGENTS.md gives agents the context they need to self-select appropriate roles.
```

new_string:
```
`AGENTS.md` defines the mission in one sentence, the Sequential Protocol Ordering for multi-agent work, and a Role Directory for task-level dispatch during execution. These are distinct sections with distinct purposes.

The **Sequential Protocol Ordering** section describes phase sequencing — which agent category goes first, what it produces, what the next category receives. Agents self-select within each phase based on what predecessors produced. This is NOT pre-assignment of specific tasks to specific agents — that is what the Role Directory handles.

The **Role Directory** is a routing table for task-level dispatch. When executing-plans spawns a subagent for a specific task, the Role Directory maps task type to agent. Populated in Phase 4 from Phase 3 selections. Each row: agent filename (without .md), model tier, project-specific trigger condition. The implementation plan's `**Agent:**` annotations take precedence over this table for individual tasks — the Role Directory is the reference and fallback.

Both sections belong in every project with agents in `.claude/agents/`. The Role Directory is not exclusive to multi-agent topologies — a single-session project with a code-reviewer agent still benefits from documenting when to use it. If `.claude/agents/` contains files not in the Role Directory, they must be read and added before execution begins.
```

- [ ] **Step 3: Verify**

Read the updated section. Confirm the distinction between Sequential Ordering and Role Directory is clear and no other lines changed.

---

### Task 4: magnum-opus.md — Add implementation.md annotation instruction

**Files:**
- Modify: `future-reference/playbooks/magnum-opus.md` (after line 300)

- [ ] **Step 1: Confirm exact target text**

Read lines 298–303. Confirm line 300 ends with: ``Without rationale, decisions look arbitrary when revisited.``

- [ ] **Step 2: Add implementation.md rationale paragraph after design.md paragraph**

Use Edit tool:

old_string:
```
`docs/plans/design.md` captures every decision from Phases 2-3 with rationale. It answers: why this model tier, why this topology, why these agents, why these hooks. Without rationale, decisions look arbitrary when revisited.

**Done-gate checklist
```

new_string:
```
`docs/plans/design.md` captures every decision from Phases 2-3 with rationale. It answers: why this model tier, why this topology, why these agents, why these hooks. Without rationale, decisions look arbitrary when revisited.

`docs/plans/implementation.md` must annotate every task with the agent from AGENTS.md Role Directory that should execute it. Format: `**Agent: [agent-name]**` on the line after the task description. Tasks with no matching agent are noted as "inline — no agent delegation." This annotation is what executing-plans reads to dispatch the correct `.claude/agents/` definition. Without it, subagent dispatch operates without the fleet, and the Role Directory exists only as documentation.

**Done-gate checklist
```

- [ ] **Step 3: Verify**

Read the new paragraph and confirm it follows the design.md paragraph and precedes the done-gate header.

---

### Task 5: magnum-opus.md — Add 4 new done-gate items

**Files:**
- Modify: `future-reference/playbooks/magnum-opus.md` (after done-gate line 310)

- [ ] **Step 1: Confirm exact end of done-gate**

Read the done-gate block. Confirm the last two items are:
```
- [ ] Eval criteria defined in `docs/plans/design.md` before any implementation code exists
- [ ] Security threat model started in `docs/plans/design.md`
```

- [ ] **Step 2: Append 4 new items to done-gate**

Use Edit tool:

old_string:
```
- [ ] Eval criteria defined in `docs/plans/design.md` before any implementation code exists
- [ ] Security threat model started in `docs/plans/design.md`

---
```

new_string:
```
- [ ] Eval criteria defined in `docs/plans/design.md` before any implementation code exists
- [ ] Security threat model started in `docs/plans/design.md`
- [ ] `CLAUDE.md` has `## Session Start Protocol` section — the old two individual rules (1) and (2) are replaced by this section, not kept alongside it
- [ ] `CLAUDE.md` has `## Development Workflow` section populated from actual Phase 3 skill selections — not generic template text, specific to this project's confirmed skills
- [ ] `AGENTS.md` has `## Role Directory` section populated with all agents in `.claude/agents/` — trigger conditions are project-specific, not generic catalog descriptions
- [ ] `docs/plans/implementation.md` tasks are annotated with `**Agent:**` from the Role Directory

---
```

- [ ] **Step 3: Verify**

Read the done-gate block. Confirm 12 total items (8 original + 4 new), all using `- [ ]` syntax.

---

### Task 6: magnum-opus.md — Add maintenance contract row + commit

**Files:**
- Modify: `future-reference/playbooks/magnum-opus.md` (maintenance contract table)

- [ ] **Step 1: Confirm exact end of maintenance table**

Read lines 370–382. Confirm last table row is:
```
| A phase needs to route to a new KB section | Update the phase pointer in this document |
```

- [ ] **Step 2: Add new row**

Use Edit tool:

old_string:
```
| A phase needs to route to a new KB section | Update the phase pointer in this document |
```

new_string:
```
| A phase needs to route to a new KB section | Update the phase pointer in this document |
| Agent added to `.claude/agents/` mid-project | AGENTS.md Role Directory + re-annotate affected `docs/plans/implementation.md` tasks |
```

- [ ] **Step 3: Verify**

Read the full maintenance contract table. Confirm the new row is present and table formatting is correct (all pipes aligned).

- [ ] **Step 4: Commit magnum-opus.md**

```bash
git add future-reference/playbooks/magnum-opus.md
git commit -m "feat(magnum-opus): add Session Start Protocol, Role Directory, and session continuity enforcement to Phase 4

- CLAUDE.md template: replace old rules 1+2 with Session Start Protocol (7-step ordered list incl. Glob fleet discovery, git log check, handoff enforcement)
- CLAUDE.md template: add Development Workflow section requirement (project-specific skill chain from Phase 3)
- AGENTS.md template: add Role Directory section (task-level routing, distinct from Sequential protocol ordering)
- implementation.md: require Agent: annotations per task for executing-plans dispatch
- Done-gate: 4 new checklist items
- Maintenance contract: new row for mid-project agent fleet changes

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

Expected: `[main xxxxxxx] feat(magnum-opus): add Session Start Protocol...`

---

### Task 7: cook/SKILL.md — Update file list descriptions and add 3 generation steps

**Files:**
- Modify: `future-reference/skills-catalog/meta/cook/SKILL.md` (lines 106–107, after line 117)

- [ ] **Step 1: Update CLAUDE.md and AGENTS.md file list descriptions**

Use Edit tool:

old_string:
```
- `CLAUDE.md` — project-specific, includes: "Read SOUL.md before anything else"
- `AGENTS.md` — mission + sequential ordering (for multi-agent or agent teams)
```

new_string:
```
- `CLAUDE.md` — project-specific; must include Session Start Protocol (7-step ordered list), Development Workflow (from Phase 3 skill selections), and Required Rules (self-review + session-handoff enforcement)
- `AGENTS.md` — mission + Role Directory (all projects with agents) + Sequential Protocol Ordering (multi-agent only)
```

- [ ] **Step 2: Add 3 generation steps after the file list, before the done-gate**

Use Edit tool:

old_string:
```
**Done-gate — verify every item before reporting scaffold complete:**
```

new_string:
```
**After copying agents to `.claude/agents/` and skills to `.claude/skills/`, execute these three generation steps before writing any other file:**

**Generation Step A — Populate CLAUDE.md Session Start Protocol and Development Workflow:**
Write these two sections using the exact skill names confirmed in Phase 3, in the order they apply to this project. Do not use a generic template — the workflow must reflect actual Phase 3 selections. The Development Workflow section must include the "First session (implementation plan exists): skip to Execute" conditional. The Required Rules section must include the session-handoff enforcement rule ("Before ending any session — whether complete or interrupted — invoke the `session-handoff` skill. This is not optional."). Remove the old rules (1) and (2) — they are replaced by the Session Start Protocol section entirely.

**Generation Step B — Populate AGENTS.md Role Directory:**
Add a `## Role Directory` section to AGENTS.md. One row per agent in `.claude/agents/`. Each row: agent filename without .md extension, model tier (haiku/sonnet/opus), and a project-specific trigger condition written for this project's context — not a generic catalog description. Add this self-healing note below the table: "If `.claude/agents/` contains files not listed here, Glob the directory, read those files, and add them before proceeding."

**Generation Step C — Annotate implementation.md tasks with Agent:**
For every task in `docs/plans/implementation.md`, add `**Agent: [agent-name]**` on the line after the task description, using the Role Directory to assign. Tasks with no matching agent get: `**Agent: inline — no delegation.**` This annotation is what executing-plans reads to dispatch `.claude/agents/` definitions.

**Done-gate — verify every item before reporting scaffold complete:**
```

- [ ] **Step 3: Verify**

Read the updated Phase 4 section. Confirm generation steps A, B, C appear between the file list and the done-gate header. Confirm no existing content was deleted.

---

### Task 8: cook/SKILL.md — Add 4 new done-gate items + commit

**Files:**
- Modify: `future-reference/skills-catalog/meta/cook/SKILL.md` (done-gate)

- [ ] **Step 1: Confirm exact end of Cook's done-gate**

Read the done-gate. Confirm last two items are:
```
- [ ] Eval criteria defined in `docs/plans/design.md`
- [ ] Security threat model started in `docs/plans/design.md`
```

- [ ] **Step 2: Append 4 new items**

Use Edit tool:

old_string:
```
- [ ] Eval criteria defined in `docs/plans/design.md`
- [ ] Security threat model started in `docs/plans/design.md`

### Phase 5
```

new_string:
```
- [ ] Eval criteria defined in `docs/plans/design.md`
- [ ] Security threat model started in `docs/plans/design.md`
- [ ] `CLAUDE.md` Session Start Protocol and Development Workflow sections are populated with project-specific content — not generic template text
- [ ] `CLAUDE.md` Required Rules section includes the session-handoff enforcement rule
- [ ] `AGENTS.md` Role Directory section is populated with all agents in `.claude/agents/` — trigger conditions are project-specific
- [ ] `docs/plans/implementation.md` tasks are annotated with `**Agent:**` from the Role Directory

### Phase 5
```

- [ ] **Step 3: Verify**

Read the done-gate. Confirm 10 total items (6 original + 4 new).

- [ ] **Step 4: Commit cook/SKILL.md**

```bash
git add future-reference/skills-catalog/meta/cook/SKILL.md
git commit -m "feat(cook): add Generation Steps A/B/C to Phase 4 and extend done-gate

Generation Step A: write CLAUDE.md Session Start Protocol + Development Workflow from Phase 3 selections
Generation Step B: write AGENTS.md Role Directory from Phase 3 agent selections
Generation Step C: annotate implementation.md tasks with Agent: from Role Directory
Done-gate: 4 new items verifying all generation steps completed

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

### Task 9: session-handoff/SKILL.md — Add workflow step, Glob note, 3 output sections + commit

**Files:**
- Modify: `future-reference/skills-catalog/workflow/session-handoff/SKILL.md`

- [ ] **Step 1: Add step 5 to the Workflow section**

Use Edit tool:

old_string:
```
5. Generate a resume command for the next session.
```

new_string:
```
5. Use the Glob tool with pattern `.claude/agents/*` to discover the active agent fleet. List every file found in the Active Agent Fleet output section.
6. To fill **Next Session Invocations**: read the `## Development Workflow` section of `CLAUDE.md`, identify the current phase, and list the remaining skills in sequence. Use exact skill names (e.g., `superpowers:executing-plans`, not "execute"). If mid-task, specify the sub-step (e.g., "task 4 of 9").
7. Generate a resume command for the next session.
```

- [ ] **Step 2: Add 3 new required sections to the output template**

Use Edit tool:

old_string:
```
## Key Decisions Made
- [decision 1 and why]
- [decision 2 and why]

## Learnings Captured
```

new_string:
```
## Key Decisions Made
- [decision 1 and why]
- [decision 2 and why]

## Current Phase
- **Workflow phase**: [brainstorm / plan / execute / review / done]
- **Sub-step**: [e.g., "executing-plans — task 4 of 9 complete" or "plan written, not yet executing"]
- **Last verified checkpoint**: [last artifact confirmed correct against acceptance criteria]

## Active Agent Fleet
[Use Glob tool: `.claude/agents/*` — list every file found with one-line purpose]
- `[agent-filename].md` — [what it does / when to use it]
[If new files appeared since last handoff, note them here.]

## Next Session Invocations
[Read CLAUDE.md Development Workflow. Based on current phase, list skills to invoke first, in order:]
1. [exact skill name, e.g., superpowers:executing-plans] — [one-line context, e.g., "resume from task 4, auth module"]
2. [next skill if applicable]
[If session is complete: "No pending invocations — project is at [phase]."]

## Learnings Captured
```

- [ ] **Step 3: Verify**

Read the full updated session-handoff SKILL.md. Confirm:
- Workflow now has 7 steps (was 5)
- Output template has the 3 new sections between Key Decisions Made and Learnings Captured
- No existing sections were deleted or reordered

- [ ] **Step 4: Commit session-handoff/SKILL.md**

```bash
git add future-reference/skills-catalog/workflow/session-handoff/SKILL.md
git commit -m "feat(session-handoff): add Current Phase, Active Agent Fleet, and Next Session Invocations sections

Three new required output sections capture phase state across session boundaries.
Workflow updated: step 5 (Glob fleet discovery) + step 6 (populate Next Session Invocations from CLAUDE.md Development Workflow).
Closes the session continuity loop — next session reads exact invocation sequence, not reconstruction.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

### Task 10: Write global memory file

**Files:**
- Create: `~/.claude/projects/-Users-t-rawww-AI-Knowledgebase/memory/feedback_agent_fleet_discovery.md`

- [ ] **Step 1: Write the memory file**

Use Write tool with this exact content:

```markdown
---
name: Agent fleet discovery during context exploration
description: Always Glob .claude/agents/* at session start; follow git log signals for agent commits; CLAUDE.md Development Workflow + AGENTS.md Role Directory are authoritative references
type: feedback
---

Always Glob `.claude/agents/*` during context exploration for any project. Follow git log signals — a commit message like "add agent definitions" is a direct instruction to read `.claude/agents/`. Never reconstruct the agent fleet from memory or assume what agents exist.

**Why:** Viridian session (2026-04-16) failed to discover six agents despite a direct git log signal ("chore: add agent definitions and transcript implementation plan"). Context was reconstructed from scratch each session. Skills were proposed by name without being invoked to read their actual content.

**How to apply:** Session start sequence for any project with a `.claude/` directory:
1. Glob `.claude/agents/*` — discover actual fleet
2. Cross-reference with AGENTS.md Role Directory (if present)
3. Check `.sessions/handoffs/` for current phase + Next Session Invocations
4. Invoke skills from Next Session Invocations list via Skill tool — read them, don't assume
5. Before invoking ANY skill in any session, invoke it via Skill tool to read current content
```

- [ ] **Step 2: Verify**

Read the created file. Confirm frontmatter has correct type (`feedback`), name, and description. Confirm body has Why and How to apply sections.

- [ ] **Step 3: Update MEMORY.md index**

Read `/Users/t-rawww/.claude/projects/-Users-t-rawww-AI-Knowledgebase/memory/MEMORY.md`. Add one line under `## Agent Best Practices`:

```
- [Agent fleet discovery at session start](feedback_agent_fleet_discovery.md) — Glob `.claude/agents/*` always; follow git log signals; never reconstruct fleet from memory
```

- [ ] **Step 4: Commit memory entry**

```bash
git add -A
git commit -m "feat(memory): add agent fleet discovery feedback rule

Documents Viridian session gap: agents in .claude/agents/ not discovered
despite git log signal. Rule: always Glob .claude/agents/* at session start,
follow commit message signals, invoke skills to read before using.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

### Task 11: Update KB-INDEX.md

**Files:**
- Modify: `KB-INDEX.md`

- [ ] **Step 1: Find current magnum-opus.md entry in KB-INDEX.md**

Read KB-INDEX.md, search for `magnum-opus`. Note the current entry's line range and description.

- [ ] **Step 2: Read updated file to get new line counts**

```bash
wc -l future-reference/playbooks/magnum-opus.md
wc -l future-reference/skills-catalog/meta/cook/SKILL.md
wc -l future-reference/skills-catalog/workflow/session-handoff/SKILL.md
```

- [ ] **Step 3: Update KB-INDEX.md entries**

For each of the three changed files, update the entry with:
- New line count
- Add note about new sections added (Session Start Protocol, Role Directory, session-handoff sections)

Use Edit tool to find and update each entry. The entries will be under the playbooks/skills-catalog sections.

- [ ] **Step 4: Commit KB-INDEX.md**

```bash
git add KB-INDEX.md
git commit -m "docs(KB-INDEX): update line ranges for magnum-opus, cook, session-handoff

All three files expanded with session continuity additions.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

### Task 12: Push and verify

- [ ] **Step 1: Verify all 5 target files are committed**

```bash
git log --oneline -8
```

Expected: 5 commits visible (magnum-opus, cook, session-handoff, memory, KB-INDEX).

- [ ] **Step 2: Push**

```bash
git push origin main
```

- [ ] **Step 3: Final sanity check — read each changed section**

Read these specific sections to confirm correctness:
- `future-reference/playbooks/magnum-opus.md` lines 264–266 (tree comments)
- `future-reference/playbooks/magnum-opus.md` lines 290–320 (CLAUDE.md + AGENTS.md rationale + implementation.md note + done-gate)
- `future-reference/playbooks/magnum-opus.md` — maintenance contract table (last row)
- `future-reference/skills-catalog/meta/cook/SKILL.md` Phase 4 section (generation steps + done-gate)
- `future-reference/skills-catalog/workflow/session-handoff/SKILL.md` (workflow + output template)

If any section looks wrong, fix with Edit tool and amend or create a new commit.

---

## Self-Review

**Spec coverage check:**

| Spec change | Covered by task |
|---|---|
| CLAUDE.md Session Start Protocol (7 steps incl. Glob, git log, invocation) | Task 2 |
| CLAUDE.md Development Workflow section (project-specific, first-session conditional) | Task 2 |
| CLAUDE.md Required Rules (self-review + session-handoff enforcement) | Task 2 |
| AGENTS.md Role Directory (routing table, self-healing note) | Task 3 |
| AGENTS.md rationale updated (Role Directory vs. Sequential distinction) | Task 3 |
| implementation.md annotation requirement | Task 4 |
| Magnum Opus done-gate 4 new items | Task 5 |
| Maintenance contract new row | Task 6 |
| Cook file list descriptions updated | Task 7 |
| Cook Generation Steps A, B, C | Task 7 |
| Cook done-gate 4 new items | Task 8 |
| Session-handoff workflow step 5+6 (Glob + Next Invocations instruction) | Task 9 |
| Session-handoff 3 new output sections | Task 9 |
| Global memory entry | Task 10 |
| KB-INDEX.md updated | Task 11 |

All 15 spec requirements covered. No gaps.

**Placeholder scan:** No TBDs, no "implement later", no vague steps. Every Edit call shows exact old_string and new_string. ✓

**Consistency check:** "Session Start Protocol" used consistently across all tasks. "Role Directory" used consistently. `**Agent:**` annotation format consistent between Task 4 (magnum-opus instruction), Task 7 (Cook Generation Step C), and the spec. ✓
