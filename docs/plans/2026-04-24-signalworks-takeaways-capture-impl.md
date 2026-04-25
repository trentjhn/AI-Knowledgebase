# SignalWorks Takeaways Capture & Consulting Playbook — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans or subagent-driven-development to implement this plan task-by-task. Companion design doc: `docs/plans/2026-04-24-signalworks-takeaways-capture-design.md`.

**Goal:** Ship v1 of the SignalWorks takeaways capture system. Extended `session-handoff` skill auto-appends workflow takeaways to `signal-works-internal/takeaways/{slug}.md` with auto-commit at session end. `/cook` routes new SignalWorks engagements to a seeded `consulting-playbook.md` and deploys classification-appropriate skills into the new project's `.claude/skills/`. Brett-gove-intell content seeds the system on day 1.

**Architecture:** 5 components across 3 locations. Per-engagement raw files in `signal-works-internal/takeaways/`. Curated `consulting-playbook.md` and `client-engagement-CLAUDE-template.md` in `signal-works-internal/process/`. Extended user-level `~/.claude/skills/session-handoff/SKILL.md`. Patched user-level `~/.claude/skills/cook/SKILL.md`. Component 6 (`/harvest-takeaways`) deferred 2-3 weeks until a corpus accumulates.

**Tech Stack:** Markdown files (per-engagement takeaways, playbook, CLAUDE template). Bash skill instructions in SKILL.md files. No application code; no test framework. Verification is end-to-end: simulate session-end on `brett-gove-intell`, verify takeaways land in both files and auto-commit/push succeeds. `/cook` verification: dry-run on a throwaway sandbox project directory.

**Skill resolution note:** All skill edits are at user level (`~/.claude/skills/`). The project-level `brett-gove-intell/.claude/skills/session-handoff/SKILL.md` is not modified — for the canonical Brett project (~92% complete), the edited user-level skill will not override unless the project-level copy is removed. Per design doc decision #3, do not remove it; future engagements scaffolded by patched `/cook` will not include a project-level session-handoff copy.

---

## Phase 1: Foundation files in signal-works-internal

### Task 1: Create signal-works-internal/takeaways/ folder

**Files:**
- Create: `/Users/t-rawww/signal-works-internal/takeaways/.gitkeep`

**Step 1: Pull latest from co-owned repo**

```bash
cd /Users/t-rawww/signal-works-internal && git pull --rebase
```

Expected: clean pull, or "Already up to date."

**Step 2: Create folder with placeholder**

```bash
mkdir -p /Users/t-rawww/signal-works-internal/takeaways
touch /Users/t-rawww/signal-works-internal/takeaways/.gitkeep
```

**Step 3: Verify**

```bash
ls /Users/t-rawww/signal-works-internal/takeaways/
```

Expected: `.gitkeep`

**Step 4: Commit + push**

```bash
cd /Users/t-rawww/signal-works-internal
git add takeaways/.gitkeep
git commit -m "Add takeaways/ folder for per-engagement workflow takeaways"
git push
```

---

### Task 2: Seed brett-roberts-la-metro.md from project repo

**Files:**
- Source: `/Users/t-rawww/brett-gove-intell/docs/workflow-notes/session-takeaways.md`
- Create: `/Users/t-rawww/signal-works-internal/takeaways/brett-roberts-la-metro.md`

**Step 1: Read the source content** with Read tool (no offset, full file).

**Step 2: Write the destination file** with this header at the top, followed by the source content:

```markdown
# Brett Roberts (LA Metro) — Workflow Takeaways

**Engagement:** Brett C.S. Roberts — Government Relations Manager (LA Metro), Trustee (El Camino College District), Commissioner (Inglewood Traffic).
**Project repo:** `/Users/t-rawww/brett-gove-intell`
**Status as of seed date (2026-04-24):** ~92% Brett-ready; remaining work is external operator actions (repo privacy, CF Pages, key rotation, whitelist) plus P2 quality.
**File purpose:** Canonical SignalWorks-internal copy of per-engagement workflow takeaways. Extended `session-handoff` skill auto-appends new entries here at session end. The original at `brett-gove-intell/docs/workflow-notes/session-takeaways.md` remains active for project-local additions during wind-down (dual-write going forward).
**Provenance tag:** First observed in: brett-roberts-la-metro, 2026-04. Use this tag to track patterns originating here vs. patterns confirmed across multiple engagements.

---

[CONTENT FROM SOURCE FILE GOES HERE — verbatim]
```

**Step 3: Verify**

```bash
wc -l /Users/t-rawww/signal-works-internal/takeaways/brett-roberts-la-metro.md
```

Expected: ≥ source line count + ~10 (header).

**Step 4: Commit + push**

```bash
cd /Users/t-rawww/signal-works-internal
git pull --rebase
git add takeaways/brett-roberts-la-metro.md
git commit -m "Seed brett-roberts-la-metro takeaways from project repo"
git push
```

---

### Task 3: Write client-engagement-CLAUDE-template.md

**Files:**
- Create: `/Users/t-rawww/signal-works-internal/process/client-engagement-CLAUDE-template.md`
- Reference: `/Users/t-rawww/brett-gove-intell/CLAUDE.md` (extract generalizable sections)

**Step 1:** Read `brett-gove-intell/CLAUDE.md` to use as the reference implementation.

**Step 2:** Write the template with these sections (each is generalized from the Brett project):

1. Header: "# {Project Name} — Claude Operating Contract"
2. Mandate to read `SOUL.md` and `AGENTS.md` first
3. Session Start Protocol (load order: SOUL.md → AGENTS.md → latest handoff → agent fleet → recent commits → invoke any "Next Session Invocations" skills)
4. **`signalworks_takeaways_target: /Users/t-rawww/signal-works-internal/takeaways/{client-slug}.md`** — read by extended session-handoff
5. "What This Project Is" (placeholder for engagement description)
6. Source of Truth file list (placeholder)
7. Development Workflow (Brainstorm → Plan → Execute → Review → Commit → Handoff)
8. **Operational Rules** (placeholder for engagement-specific rules)
9. **Required Rules** (always includes: "Before ending any session — whether complete or interrupted — invoke the `session-handoff` skill. This is not optional.")
10. **Authority Block** (placeholder template: "Decide autonomously: ... | Pause for {operator}: ...")
11. When to Ask Before Acting (placeholder list)
12. Reference to `signal-works-internal/process/consulting-playbook.md`

Each placeholder section must include `[FILL AT ENGAGEMENT KICKOFF: ...]` markers so `/cook` Phase 2 knows to fill them.

**Step 3: Verify**

```bash
grep -c "FILL AT ENGAGEMENT KICKOFF" /Users/t-rawww/signal-works-internal/process/client-engagement-CLAUDE-template.md
```

Expected: ≥ 6.

**Step 4: Commit + push**

```bash
cd /Users/t-rawww/signal-works-internal
git pull --rebase
git add process/client-engagement-CLAUDE-template.md
git commit -m "Add CLAUDE.md template for new SignalWorks client engagements"
git push
```

---

### Task 4: Write consulting-playbook.md universal sections (1-12 of 15)

**Files:**
- Create: `/Users/t-rawww/signal-works-internal/process/consulting-playbook.md`
- Source patterns: `signal-works-internal/takeaways/brett-roberts-la-metro.md` (the day-1 seed file from Task 2)

**Step 1:** Write the playbook with this structure (universal sections — apply to both Type A and Type B engagements):

```markdown
# SignalWorks Consulting Playbook

**Purpose:** Methodology for running a SignalWorks AI consulting engagement end-to-end. More opinionated than `magnum-opus.md` — assumes you are doing client work, not personal experiments.
**Read by:** `/cook` Phase 1 when classification matches "SignalWorks consulting engagement."
**Updates:** `/harvest-takeaways` skill (deferred 2-3 weeks) will promote patterns from `signal-works-internal/takeaways/*.md` into this file when patterns repeat across 2+ engagements.

---

## Section 1: Engagement Discovery
[Client problem framing, scope negotiation, success criteria, timeline, budget, deliverable type classification]

## Section 2: Type Classification — Type A vs Type B

**Type A: AI deliverable.** The AI workflow/automation IS the product (e.g., brett-gove-intell summarization pipeline). Apply Type A specifics in Section 16.

**Type B: AI-accelerated build.** AI coding agents help build a deliverable that is not itself an AI product (e.g., a marketing site built with Claude Code as the dev agent). Apply Type B specifics in Section 17.

[Decision flowchart + branching guidance]

## Section 3: Authority Block Setup
[Explicit decide-autonomously vs pause-for-{operator} list. Reversibility test. Locked decisions list. Reference Brett-gove-intell line 204-208 as canonical example.]

## Section 4: Source-of-Truth Doc Spine
[design.md, implementation.md, prompts/, .sessions/handoffs/, decision log format]

## Section 5: CLAUDE.md Mandate
[Reference client-engagement-CLAUDE-template.md. Required: session-handoff at session-end mandate, signalworks_takeaways_target line]

## Section 6: Tier-Based Shipping
[Decompose ambitious refactors into 3-5 tiers each individually shippable. Commit checkpoint per tier. Rollback path per tier. Provenance: brett-roberts-la-metro, 2026-04.]

## Section 7: Multi-Agent Audit Discipline
[For pre-delivery audits, dispatch N parallel sub-agents on non-overlapping territories. Mandatory self-critique pass per agent. Consolidate as P1/P2/P3. Provenance: brett-roberts-la-metro, 2026-04.]

## Section 8: Baseline-Before-Change
[First step of any output-changing refactor: capture pre-state baseline. Provenance: brett-roberts-la-metro, 2026-04.]

## Section 9: Live Verification
[At least one live dry-run per tier. Unit tests verify code; live runs verify data shapes. Provenance: brett-roberts-la-metro, 2026-04.]

## Section 10: Decision Log Format
[Structured: Context / Options Considered / Chose / Reasoning / Live-Verification / Residual Gaps / Reversibility / Operator-review-needed]

## Section 11: Handoff Chain Discipline
[Versioned handoff files. Resume Command sufficient for fresh Claude session. Reference brett-gove-intell handoffs v3-v7 as canonical example.]

## Section 12: Invariants Tied to Tests
[Convert principles in SOUL.md into invariants with named tests. Principles rot, invariants don't. Provenance: brett-roberts-la-metro, 2026-04.]

## Section 13: Pre-Delivery Sweep ("Client-Ready Sweep")
[Multi-agent sweep: code correctness / security / UX / docs. Self-critique pass each. Provenance: brett-roberts-la-metro, 2026-04 (called "Brett-Ready sweep" there).]

## Section 14: Brand & Voice Rules
[Reference signal-works-internal/CLAUDE.md as canonical for brand rules (no em-dashes; direct/warm/specific). Do NOT restate here — single source of truth.]

## Section 15: Engagement Closure
[Wrap criteria. Archive protocol. Case-study trigger via process/case-study-template.md.]
```

**Step 2: Verify**

```bash
grep -c "^## Section" /Users/t-rawww/signal-works-internal/process/consulting-playbook.md
```

Expected: 15.

**Step 3: Commit + push**

```bash
cd /Users/t-rawww/signal-works-internal
git pull --rebase
git add process/consulting-playbook.md
git commit -m "Add consulting-playbook.md sections 1-15 (universal methodology)"
git push
```

---

### Task 5: Add Type A specifics to consulting-playbook.md

**Files:**
- Modify: `/Users/t-rawww/signal-works-internal/process/consulting-playbook.md` (append after Section 15)

**Step 1:** Append Section 16:

```markdown
---

## Section 16: Type A Specifics — AI Deliverable Engagements

When the AI workflow/automation IS the product, apply these in addition to universal sections:

### 16.1 Eval Framework Setup
[Reference AI-Knowledgebase/LEARNING/PRODUCTION/evaluation/evaluation.md. Required: 3-level eval stack (offline/online/human). LLM-as-judge with bias mitigation if applicable.]

### 16.2 Hallucination Prevention Architecture
[Verbatim-display contracts (display_text), grounding checks, NER gates, allow-lists. Provenance: brett-roberts-la-metro, 2026-04. Tier 1+2+3 zero-hallucination architecture is the canonical example.]

### 16.3 Model Selection Rationale
[Reference AI-Knowledgebase/LEARNING/FOUNDATIONS/reasoning-llms/reasoning-llms.md. Document the why per project — cost vs latency vs reasoning quality.]

### 16.4 Prompt Engineering Rigor
[Reference AI-Knowledgebase/LEARNING/FOUNDATIONS/prompt-engineering/prompt-engineering.md. Versioned prompts in docs/prompts/. Examples inside fence (Tier 1 Brett gotcha).]

### 16.5 AI Security Pre-flight
[Reference AI-Knowledgebase/LEARNING/PRODUCTION/ai-security/ai-security.md. Prompt injection vectors, URL-scheme XSS gates, PAT redaction.]
```

**Step 2: Verify**

```bash
grep -c "^### 16\." /Users/t-rawww/signal-works-internal/process/consulting-playbook.md
```

Expected: 5.

**Step 3: Commit + push**

```bash
cd /Users/t-rawww/signal-works-internal
git pull --rebase
git add process/consulting-playbook.md
git commit -m "Add Type A (AI deliverable) specifics to consulting-playbook"
git push
```

---

### Task 6: Add Type B specifics to consulting-playbook.md

**Files:**
- Modify: `/Users/t-rawww/signal-works-internal/process/consulting-playbook.md` (append after Section 16)

**Step 1:** Append Section 17:

```markdown
---

## Section 17: Type B Specifics — AI-Accelerated Build Engagements

When AI coding agents help build a non-AI deliverable (marketing site, data pipeline without LLM, automation tool):

### 17.1 Design/UX Rigor
[Reference frontend-design / web-design-patterns / shadcn-ui skills. DESIGN.md before code. Lighthouse gates for marketing sites.]

### 17.2 Front-End Skill Deployment
[Mandatory: deploy frontend-design, web-design-patterns, shadcn-ui, frontend-taste skills into project's .claude/skills/ at scaffold time. /cook Phase 2 enforces this — see consulting-playbook Section 5 + /cook patches.]

### 17.3 Responsive QA
[Mobile-first verification, browser matrix (Safari/Chrome/Firefox at minimum).]

### 17.4 Performance & Core Web Vitals
[Reference future-reference/playbooks/building-professional-websites.md (KB). Lighthouse ≥90 mobile target.]

### 17.5 Verification Loop
[Build / lint / type-check on every change. Use verification-loop skill if available.]
```

**Step 2: Verify**

```bash
grep -c "^### 17\." /Users/t-rawww/signal-works-internal/process/consulting-playbook.md
```

Expected: 5.

**Step 3: Commit + push**

```bash
cd /Users/t-rawww/signal-works-internal
git pull --rebase
git add process/consulting-playbook.md
git commit -m "Add Type B (AI-accelerated build) specifics to consulting-playbook"
git push
```

---

## Phase 2: Skill edits

### Task 7: Extend session-handoff SKILL.md — detection step

**Files:**
- Modify: `/Users/t-rawww/.claude/skills/session-handoff/SKILL.md`

**Step 1:** Read current `~/.claude/skills/session-handoff/SKILL.md` (97 lines per earlier inspection).

**Step 2:** Add new section after the existing "## Workflow" section, titled "## SignalWorks Takeaways Extension":

```markdown
## SignalWorks Takeaways Extension

After producing the handoff doc, run this extension step:

1. **Detect.** Read the project's CLAUDE.md (path: `<project-root>/CLAUDE.md`). Look for a line matching `signalworks_takeaways_target: <absolute-path>`. If absent, skip the rest of this section (non-SignalWorks project).

2. **Extract.** Identify transferable workflow patterns from the current session. Format each as:

```
### Pattern: {one-line summary}

**Evidence (this session):** {what happened that surfaced the pattern}

**Transfer rule:** {generalized statement applicable to future engagements}

**Provenance:** {project-slug}, {YYYY-MM-DD}
```

3. **Apply gate.** Only emit entries with a clear, generalized transfer rule. If no entries qualify, write nothing — no noise.

4. **Append + commit + push.** If at least one entry qualifies:
   - Run `cd $(dirname <target-path>) && cd .. && git pull --rebase` (handles co-owner concurrent edits)
   - Append the entries to the target file under a new heading: `## Session: {YYYY-MM-DD}`
   - Run `git add <relative-target-path> && git commit -m "takeaways({slug}): {N} entries from {date} session"`
   - Run `git push`

5. **Failure fallback.** If pull-rebase, commit, or push fails:
   - Write the same content to `<target-path>.pending`
   - Do NOT block the handoff
   - Surface the failure in the handoff's "Gotchas" section: "⚠️ Takeaways write to {target} failed at git layer. Pending content at {target}.pending — resolve manually."
```

**Step 3: Verify**

```bash
grep -c "SignalWorks Takeaways Extension" /Users/t-rawww/.claude/skills/session-handoff/SKILL.md
```

Expected: 1.

**Step 4: Commit (this is the AI-Knowledgebase commit, since user-level skill changes are tracked there if at all — actually skills live at ~/.claude/, so this is a system-level edit. No commit at user-skill level; just save.)**

Note: If `~/.claude/` is a git repo (check with `git -C ~/.claude/skills/session-handoff status`), commit there. Otherwise, this edit is purely local to the user's machine.

```bash
git -C ~/.claude/skills/session-handoff status 2>&1 | head -3
```

If it says "not a git repository," skip commit; the file edit persists.

---

### Task 8: Test session-handoff extension on brett-gove-intell

**Files:**
- Verify: `/Users/t-rawww/brett-gove-intell/CLAUDE.md` (does it have `signalworks_takeaways_target:` line?)

**Step 1:** Check if Brett's CLAUDE.md has the target line:

```bash
grep "signalworks_takeaways_target" /Users/t-rawww/brett-gove-intell/CLAUDE.md
```

If absent (expected on first run of this plan), proceed to Step 2.

**Step 2:** Add the line to brett-gove-intell CLAUDE.md, between the "## What This Project Is" section and the "## Source of Truth" section. Use the Edit tool (read first):

Insert this after the project-description block:

```markdown
---

**Takeaways target:** `signalworks_takeaways_target: /Users/t-rawww/signal-works-internal/takeaways/brett-roberts-la-metro.md`

---
```

**Step 3:** Commit to brett-gove-intell:

```bash
cd /Users/t-rawww/brett-gove-intell
git add CLAUDE.md
git commit -m "Add signalworks_takeaways_target line for session-handoff extension"
git push
```

**Step 4:** Manually invoke session-handoff (in a brett-gove-intell session, type "create a session handoff" or invoke `Skill(session-handoff)`). Verify:
- Handoff doc is created in `.sessions/handoffs/`
- New entries appear in BOTH `brett-gove-intell/docs/workflow-notes/session-takeaways.md` AND `signal-works-internal/takeaways/brett-roberts-la-metro.md`
- Auto-commit/push to signal-works-internal succeeds (check `git log signal-works-internal -1`)

**Note:** This task is a manual end-to-end test gate. If the test fails, fix Task 7's SKILL.md before proceeding to Phase 3.

---

## Phase 3: /cook patches

### Task 9: Patch /cook Phase 1 — add SignalWorks classification + routing

**Files:**
- Modify: `/Users/t-rawww/.claude/skills/cook/SKILL.md`

**Step 1:** Read current `~/.claude/skills/cook/SKILL.md` (find Phase 1 section, lines ~46-62 per earlier inspection).

**Step 2:** Add a new classification option after the existing classification questions:

```markdown
4. "Is this a SignalWorks consulting engagement (paid client work for an external client)? yes/no"
   If yes: route to `/Users/t-rawww/signal-works-internal/process/consulting-playbook.md` IN ADDITION to any other matching playbooks.
```

Update the routing list to include:

```markdown
- SignalWorks client engagement → `/Users/t-rawww/signal-works-internal/process/consulting-playbook.md` (read first, applies on top of type-specific playbooks)
```

Update the report line:

```markdown
Report: "Classification: [type]. SignalWorks engagement: [yes/no]. Playbook(s): [list]. Topology: [single/hierarchical/team]."
```

**Step 3: Verify**

```bash
grep "consulting-playbook.md" /Users/t-rawww/.claude/skills/cook/SKILL.md
```

Expected: ≥ 2 lines.

**Step 4:** Save edit (no separate commit — same file as Task 10).

---

### Task 10: Patch /cook Phase 2 — skill deployment registry + CLAUDE.md baking

**Files:**
- Modify: `/Users/t-rawww/.claude/skills/cook/SKILL.md` (Phase 2: Harness Design section)

**Step 1:** Find Phase 2 section in `cook/SKILL.md`.

**Step 2:** Add a new sub-step in Phase 2 titled "Skill Deployment":

```markdown
### Phase 2.5: Skill Deployment

Based on classification, deploy the matching skills into `{new-project}/.claude/skills/` by copying from `~/.claude/skills/{skill-name}/`:

**Mapping table:**

| Classification | Skills to deploy |
|---|---|
| AI/agentic (Type A) | brainstorming, planning, smart-commit, deslop, eval-harness, cost-aware-llm-pipeline, error-handling-patterns, context-budget, verification-loop, pre-ship, security-review, tdd-workflow |
| Marketing site / static frontend (Type B) | brainstorming, planning, smart-commit, deslop, frontend-design, web-design-patterns, shadcn-ui, frontend-taste, verification-loop, pre-ship |
| Conversational product | brainstorming, planning, smart-commit, deslop, eval-harness, frontend-design (if UI), verification-loop, pre-ship, security-review |
| Single LLM call pipeline | brainstorming, planning, smart-commit, deslop, eval-harness, prompt-engineering (if exists), verification-loop, pre-ship |
| Engineering infrastructure | brainstorming, planning, smart-commit, deslop, deployment-patterns, error-handling-patterns, http-client-hygiene, verification-loop, pre-ship, tdd-workflow |
| SignalWorks engagement (always include) | session-handoff (DO NOT deploy at project level — let user-level run; see design doc note 3) |

For each matching skill: `cp -r ~/.claude/skills/{skill-name}/ {new-project}/.claude/skills/{skill-name}/`

Verify: `ls {new-project}/.claude/skills/` should show the deployed skills.
```

**Step 3:** Add a new sub-step in Phase 2 titled "CLAUDE.md Baking (SignalWorks engagements only)":

```markdown
### Phase 2.6: CLAUDE.md Baking (SignalWorks engagements only)

If this is a SignalWorks engagement (Phase 1 classification):

1. Read `/Users/t-rawww/signal-works-internal/process/client-engagement-CLAUDE-template.md`.
2. Substitute `{client-slug}` everywhere with the client's slug (ask user if not derivable from project name).
3. Substitute `{Project Name}` with the project's name.
4. Write the result to `{new-project}/CLAUDE.md`.
5. Prompt user to fill in `[FILL AT ENGAGEMENT KICKOFF: ...]` markers before first work session.
```

**Step 4: Verify**

```bash
grep -c "Phase 2\\.[56]" /Users/t-rawww/.claude/skills/cook/SKILL.md
```

Expected: 2.

**Step 5: Commit if applicable** (same git status check as Task 7).

---

### Task 11: Test /cook patches on a sandbox project

**Files:**
- Create temporarily: `/tmp/sw-cook-test-project/`

**Step 1:** Create sandbox directory:

```bash
mkdir -p /tmp/sw-cook-test-project
cd /tmp/sw-cook-test-project
git init
```

**Step 2:** Run `/cook` (in a fresh Claude Code session in `/tmp/sw-cook-test-project`). Answer Phase 1 questions:
- Project description: "Test SignalWorks engagement for client X"
- AI/agentic Type A
- Greenfield
- Single agent
- SignalWorks engagement: yes

**Step 3:** Verify outputs:
- `/tmp/sw-cook-test-project/CLAUDE.md` exists, contains the mandate snippet, contains `signalworks_takeaways_target:` line
- `/tmp/sw-cook-test-project/.claude/skills/` contains expected skills (brainstorming, planning, smart-commit, deslop, eval-harness, etc.)
- Phase 1 report mentioned `consulting-playbook.md` as a routed playbook

**Step 4:** Cleanup:

```bash
rm -rf /tmp/sw-cook-test-project
```

**Step 5:** If any verification failed, return to Task 9 or 10 and fix the SKILL.md edits.

---

## Phase 4: Wrap-up

### Task 12: Update AI-Knowledgebase MEMORY.md

**Files:**
- Modify: `/Users/t-rawww/.claude/projects/-Users-t-rawww-AI-Knowledgebase/memory/MEMORY.md`

**Step 1:** Read current MEMORY.md.

**Step 2:** Add a new index entry under an appropriate section (likely "## /cook + Magnum Opus System" or new "## SignalWorks Workflow"):

```markdown
## SignalWorks Workflow Capture System (built 2026-04-24)
- `/Users/t-rawww/signal-works-internal/takeaways/{slug}.md` — per-engagement raw takeaways auto-appended by extended session-handoff
- `/Users/t-rawww/signal-works-internal/process/consulting-playbook.md` — 17 sections (universal + Type A + Type B), seeded from brett-roberts-la-metro
- `/Users/t-rawww/signal-works-internal/process/client-engagement-CLAUDE-template.md` — baked into new SignalWorks projects by /cook
- `~/.claude/skills/session-handoff/SKILL.md` — extended with SignalWorks Takeaways Extension section
- `~/.claude/skills/cook/SKILL.md` — Phase 1 routing + Phase 2.5 skill deployment + Phase 2.6 CLAUDE.md baking
- Component 6 `/harvest-takeaways` deferred to ~2026-05-15
- Design: `docs/plans/2026-04-24-signalworks-takeaways-capture-design.md`
- Plan: `docs/plans/2026-04-24-signalworks-takeaways-capture-impl.md`
```

**Step 3:** Save (memory file is read by Claude on session start; no commit needed).

---

### Task 13: Update KB-INDEX.md if applicable

**Files:**
- Inspect: `/Users/t-rawww/AI-Knowledgebase/KB-INDEX.md`
- Modify (if needed): same file

**Step 1:** Read KB-INDEX.md to determine if it tracks `signal-works-internal` files. (Likely no — KB-INDEX is for AI-Knowledgebase content. Skip if unrelated.)

**Step 2:** If KB-INDEX has a section for design docs, add an entry pointing to:
- `docs/plans/2026-04-24-signalworks-takeaways-capture-design.md`
- `docs/plans/2026-04-24-signalworks-takeaways-capture-impl.md`

**Step 3:** Otherwise, skip.

---

### Task 14: Schedule harvest-takeaways follow-up

**Files:**
- None (uses `schedule` skill or manual calendar reminder)

**Step 1:** Calculate ship-date + ~3 weeks ≈ 2026-05-15.

**Step 2:** Use the `schedule` skill (if available) to create a one-time agent for 2026-05-15 with task: "Build /harvest-takeaways skill per design doc Component 6. Read all signal-works-internal/takeaways/*.md, propose promotions to consulting-playbook.md."

If `schedule` skill not used: add a calendar reminder manually.

---

### Task 15: Final commit and push

**Step 1:** Verify all repos are in clean state:

```bash
git -C /Users/t-rawww/signal-works-internal status
git -C /Users/t-rawww/AI-Knowledgebase status
git -C /Users/t-rawww/brett-gove-intell status
```

Expected: each shows "working tree clean" or only the expected uncommitted edits.

**Step 2:** If AI-Knowledgebase has the design + impl docs uncommitted (Task 12 didn't add them via commit):

```bash
cd /Users/t-rawww/AI-Knowledgebase
git add docs/plans/2026-04-24-signalworks-takeaways-capture-impl.md
git commit -m "docs(plans): SignalWorks takeaways capture implementation plan"
git push
```

**Step 3:** Confirm in user-facing summary:
- ✅ Phase 1: 6 files in signal-works-internal (folder, seed file, CLAUDE template, playbook sections 1-15, Type A, Type B)
- ✅ Phase 2: session-handoff skill extended; tested on brett-gove-intell
- ✅ Phase 3: /cook patched (Phase 1 + Phase 2.5 + Phase 2.6); tested on sandbox
- ✅ Phase 4: MEMORY.md updated; harvest follow-up scheduled

---

## Success criteria (gates for "done")

1. End a session in `brett-gove-intell` (manually or via `session-handoff` skill invocation) → takeaways auto-appear in BOTH `brett-gove-intell/docs/workflow-notes/session-takeaways.md` AND `signal-works-internal/takeaways/brett-roberts-la-metro.md` → auto-commit + push succeeds.
2. Run `/cook` in a new sandbox directory, classify as SignalWorks engagement → resulting project has CLAUDE.md with mandate + target line, and `.claude/skills/` with classification-appropriate skills.
3. `signal-works-internal/process/consulting-playbook.md` exists with 17 sections (15 universal + Type A + Type B); each seeded section has a provenance tag.
4. Non-SignalWorks projects (e.g., personal experiments) are unaffected by extended session-handoff (detection step short-circuits cleanly).

## Risks & mitigations during execution

- **Git collision on signal-works-internal during Tasks 1-6:** mitigation = `git pull --rebase` at start of each task.
- **Skill SKILL.md edits don't take effect:** verify `~/.claude/skills/{skill}/SKILL.md` is what gets loaded (not a cached version). Restart Claude session if behavior is stale.
- **Phase 2.5 skill copy fails (permission, missing source skill):** test command `cp -r ~/.claude/skills/brainstorming/ /tmp/test/.claude/skills/brainstorming/` in isolation before Task 11.
- **brett-gove-intell session-handoff override:** verify project-level `.claude/skills/session-handoff/SKILL.md` is OUTDATED relative to user-level. If it overrides and lacks the SignalWorks Extension, either delete it or copy the user-level edit into it. Decided in design: do not auto-delete; flag in Task 8 verification.

---

## Plan complete

**Plan saved to:** `docs/plans/2026-04-24-signalworks-takeaways-capture-impl.md`

**Two execution options:**

1. **Subagent-Driven (this session)** — I dispatch a fresh subagent per task, review between tasks, fast iteration. Best if you want to ship today and stay in this conversation.

2. **Parallel Session (separate)** — Open a new session, use executing-plans skill, batch execution with checkpoints. Best if you want to step away and come back to results.

**Which approach?**
