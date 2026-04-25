# /cook v1.5 — SignalWorks-Mode Consulting-Grade Scaffolding — Design

**Date:** 2026-04-25
**Status:** Approved, ready for planning
**Owner:** Trent Johnson
**Companion docs:** `2026-04-24-signalworks-takeaways-capture-design.md` (v1) + this doc (v1.5).
**Brainstorming session:** Validated output of brainstorming after v1 ship — surfaced gaps in /cook's operationalization of the consulting-playbook.

---

## Problem statement

Current `/cook` produces a **skeleton** project scaffold: minimum required files (CLAUDE.md, AGENTS.md, SOUL.md, README, .gitignore, basic .claude/agents/ + .claude/skills/, docs/plans/{design,implementation}.md). For SignalWorks consulting engagements this is insufficient — the operator opens the new project and finds 60% of the consulting-playbook's mandated artifacts missing, then has to manually scaffold the audit-protocol, prompt templates, decision log format, handoff stub, security baseline, takeaways folder, and engagement registration entries.

Symptom: `brett-gove-intell` was scaffolded by an earlier `/cook` run and ended up missing the 4-agent audit prompt library, the audit-protocol doc, and front-end skills despite being a UI deliverable. Each gap was fixed manually mid-engagement. That's wasted operator cycles and a real regression risk on the next engagement.

Root cause: `/cook` references the consulting-playbook but doesn't operationalize it. The playbook says "every engagement gets the audit-as-default triad on day 1" — `/cook` doesn't actually scaffold it. The playbook says "deploy classification-appropriate skills" — the registry I added in v1 does this but only for skills, not for subagents, and not for the broader doc spine.

## Goals

1. **Substantively complete consulting-grade scaffold** for any SignalWorks engagement — operator cd's into the new directory and finds every artifact the playbook mandates already in place.
2. **Discovery dialogue captured into artifacts**, not a separate notes file. Answers to /cook's discovery questions populate `SOUL.md`, `CLAUDE.md`, `docs/plans/design.md`, `client-facing-scope.md`-equivalent in design.md, etc.
3. **Security pre-flight as a mandatory phase**, not buried in discovery questions. Anti-pattern A3 (fork lineage) cost cycles on Brett — should be impossible to forget.
4. **Dual-write takeaways extension** — every SignalWorks project has a project-local `docs/workflow-notes/session-takeaways.md` AND the canonical signal-works-internal copy. session-handoff writes to both.
5. **Engagement registration** — adds new engagement to `signal-works-internal/TASKS.md` "In Progress" + creates `signal-works-internal/clients/{slug}/scope.md` + creates empty `signal-works-internal/takeaways/{slug}.md`.
6. **Type A vs Type B branching that actually changes /cook behavior**, not just classification metadata.

## Non-goals (deliberately out of scope)

- Client-facing artifacts (proposals, scope statements signed by clients, pricing). Higher leverage but bigger surface area; deferred until pricing is locked (see TASKS.md "Decisions Needed").
- Sales-pipeline tracking or notes/ → synthesis automation.
- Backporting to existing engagements (brett-gove-intell stays as-is; v1.5 only applies to NEW engagements scaffolded after this ships).
- Auto-creating `signal-works-internal/clients/{slug}/` if it already exists from prior outreach (just append/update; don't overwrite).
- Cross-engagement coordination (e.g., "two SignalWorks engagements running in parallel — pause one for the other").

## Architecture — Approach 1: SignalWorks-mode inside existing /cook

Single skill, two modes. When `/cook` Phase 1 classifies the project as a SignalWorks engagement, the SignalWorks-mode branches activate. Non-SignalWorks projects keep current `/cook` behavior unchanged.

```
/cook flow (with SignalWorks branches marked [SW])
├── Phase 0: Intake (existing)
├── Phase 0.5: Engagement Discovery [SW only — NEW] (11 questions)
├── Phase 0.7: Authority + Brand [SW only — NEW] (3 questions)
├── Phase 0.9: Security Pre-flight [SW only — NEW] (5-6 yes/no checks)
├── Phase 1: Classification (existing) — adds SignalWorks branch + Type A/B
├── Phase 1.5: Specification + Pre-flight (existing)
├── Phase 2: Harness Design (existing) — Type A/B branches NEW
├── Phase 2.5: Build Methodology (existing)
├── Phase 3: Capability Selection (existing) — Skill Deployment Registry expanded NEW
├── Phase 4: Scaffold Output (existing) — substantive expansion for [SW]
└── Phase 5: Eval + Security Baseline (existing) — TASKS.md + clients/ registration NEW
```

---

## Discovery dialogue — 11 questions (Phase 0.5, [SW] only)

Each question one at a time, multiple choice where possible, captured directly into the scaffold output (not a separate notes file).

1. **Client name + role + organization?** → flows into `SOUL.md` "About the End Client" section + `CLAUDE.md` line 1.
2. **What's the problem? (verbatim — captured exactly as you say it)** → flows into `docs/plans/design.md` "Problem Statement" section, in client's own words.
3. **What's the deliverable?** → flows into `docs/plans/design.md` "Deliverable" section.
4. **What's explicitly NOT in scope? (must list 3+ items)** → flows into `docs/plans/design.md` "Out of Scope" section.
5. **Type A (AI is the deliverable) or Type B (AI accelerates a non-AI build)? Or hybrid?** → drives Phase 2 questions, Phase 3 skill registry, agent fleet selection.
6. **Timeline + budget envelope?** (duration in weeks, hard end-date if any, fixed-price vs hourly) → flows into `docs/plans/design.md` "Engagement Envelope" section.
7. **Success criteria? (numeric where possible)** → flows into `docs/plans/design.md` "Success Criteria" section + `SOUL.md` "Definition of Done".
8. **Authority block — what can Claude decide autonomously? What requires you to approve?** → flows into `CLAUDE.md` "Authority Block" section, replaces `[FILL AT ENGAGEMENT KICKOFF]` markers.
9. **Client-specific brand voice rules beyond SignalWorks defaults?** → flows into `SOUL.md` "Voice Rules" + `CLAUDE.md` "Operational Rules". (SignalWorks defaults: no em-dashes, direct/warm/specific. Client adds: e.g., "Brett's exact title is X," "no jargon," "third-person only.")
10. **Existing context to ingest? (folder paths, docs, brand guidelines, prior designs)** → flows into `docs/client-context.md` (NEW file). For Brent's engagement that would be `signal-works-internal/clients/brent-stokes-product-launch/{capabilities-menu,monday-dinner-prep,opportunity-context,product-notes,README}.md` — symlinked or referenced, not copied.
11. **Operational constraints? (compliance, budget caps, security clearance, regulatory notification)** → flows into `docs/plans/design.md` "Constraints" section + Phase 0.9 security pre-flight defaults.

## Authority + Brand (Phase 0.7, [SW] only) — 3 questions

12. **Decide-autonomously list:** What categories of decisions can Claude make without pausing? (multiple choice + free-form additions)
13. **Pause-for-operator list:** What categories require explicit approval? (multiple choice + free-form additions)
14. **Locked decisions at kickoff:** Any pre-locked architectural / scope decisions Claude should NOT cross? (free-form list)

These three populate `CLAUDE.md` "Authority Block" + `docs/plans/design.md` "Locked Decisions" sections.

## Security Pre-flight (Phase 0.9, [SW] only) — 6 yes/no checks

Auto-runs after Phase 0.7. Each gate is a yes/no with documented default. Failures don't block scaffold but get TODOed in `docs/plans/design.md` "Security Action Items" section.

15. **Repo privacy: private from day 1?** Default yes for client work. If yes: `gh repo create --private` after scaffold. If client-sensitive (compliance flagged in Q11): mandatory yes.
16. **Fork lineage: is this forked from anywhere?** If yes: check public-fork → private feasibility (anti-pattern A3). Surface blocker if conflict.
17. **`.env.example` placeholders only?** Default yes; auto-scaffolded.
18. **GitHub Actions workflow permissions = `contents: read` minimum?** Default yes; baked into `.github/workflows/` if `gh` workflows are scaffolded.
19. **Default branch protection rules?** Default yes; surfaces as TODO with `gh` command.
20. **Sensitive content scan needed at pre-ship?** Default yes if Q11 flagged compliance; surfaces as recurring CI check.

---

## Scaffold output — substantive consulting-grade list

For SignalWorks engagements, Phase 4 produces:

### Source-of-truth doc spine (always)
- `SOUL.md` — engagement-specific character (60-80 lines). Filled from Q1 (client) + Q2 (problem) + Q7 (success criteria) + Q9 (voice rules). NOT a template — actual content.
- `CLAUDE.md` — baked from `signal-works-internal/process/client-engagement-CLAUDE-template.md`, all `[FILL AT ENGAGEMENT KICKOFF]` markers replaced from Q1, Q5, Q8, Q9, Q10. Includes mandatory `signalworks_takeaways_target:` line.
- `AGENTS.md` — agent fleet roster + sequential protocol ordering (60 lines). Lists deployed subagents with one-line role descriptions.
- `docs/plans/design.md` — engagement discovery captured (Q2, Q3, Q4, Q6, Q7, Q11) + locked decisions (Q14) + Phase 2 architectural decisions.
- `docs/plans/implementation.md` — initial ordered build plan with `**Agent:**` annotations per task.
- `docs/client-context.md` — symlinks/references to existing context from Q10.
- `docs/invariants.md` — empty stub with format header (one section per invariant: name, enforcement mechanism, test reference).

### Audit-as-Default Triad (always — playbook S11)
- `docs/audit-protocol.md` — canonical playbook for when/how to run multi-agent audits (60 lines). Specifies: when to run (session-end + pre-tier-ship), how many agents (default 4), self-critique mandate, output format (P1/P2/P3 with ID tags), consolidation step.
- `docs/prompts/audits/code-correctness.md`
- `docs/prompts/audits/security.md`
- `docs/prompts/audits/ux-delivery.md`
- `docs/prompts/audits/docs-operations.md`

Each audit prompt is a fill-the-blanks template with `{{PROJECT_CONTEXT}}` / `{{SLICE}}` / `{{KNOWN_PRIORS}}` placeholders — same structure as proven on brett-roberts-la-metro Tier 3.5 sweep. Self-critique mandate baked in.

### Session continuity (always)
- `.sessions/handoffs/handoff-{date}-v1.md` — initial stub with: Status (engagement just scaffolded), What's Done (scaffold complete), What's In Progress (none yet), What's Pending (Step 1 of implementation.md), Resume Command (instructions for fresh Claude session to pick up cold), Audit Directions for Next Session (empty list with format).
- `.sessions/handoffs/decision-log-{date}.md` — header with the 8-field format template (Decision, Date, Context, Options Considered, Chose, Reasoning, Live-Verification, Reversibility, Operator-review-needed). Pre-seeded with one entry: "Decision: Engagement scaffolded with /cook v1.5 on {date}" capturing initial decisions from Q5, Q8, Q14.

### Subagent fleet (`.claude/agents/`)

**Universal SignalWorks fleet (always deployed, copied from `~/AI-Knowledgebase/future-reference/agent-catalog/`):**
- `core/planner.md` → `.claude/agents/planner.md`
- `core/architect.md` → `.claude/agents/architect.md`
- `core/code-reviewer.md` → `.claude/agents/code-reviewer.md`
- `core/doc-updater.md` → `.claude/agents/doc-updater.md`
- `quality/tdd-guide.md` → `.claude/agents/tdd-guide.md`
- `quality/security-reviewer.md` → `.claude/agents/security-reviewer.md`
- `quality/evaluator.md` → `.claude/agents/evaluator.md`

**Type A (AI deliverable) additions:**
- `ai-specialist/prompt-engineer.md`
- `ai-specialist/eval-designer.md`
- `ai-specialist/context-architect.md`
- `ai-specialist/data-analyst.md` (if data-analysis is part of the AI pipeline)

**Type B (AI-accelerated build) additions:**
- `design/product-designer.md`
- `design/ui-designer.md`
- `design/accessibility-reviewer.md`
- `quality/typescript-reviewer.md` (if TS stack)

**Optional based on engagement size (Q6 timeline):**
- `meta/chief-of-staff.md` — for complex multi-week engagements with multiple parallel workstreams
- `product/spec-writer.md` — for engagements with formal spec docs
- `product/technical-writer.md` — for client-facing docs

### Skill fleet (`.claude/skills/`)

Extends the v1 Skill Deployment Registry. Same source: `~/.claude/skills/{name}/`. Copy with `cp -r`, verify with `ls`. Existence check before copy (NEW in v1.5 per gap #2).

**Universal SignalWorks (always):** `brainstorming`, `planning`, `smart-commit`, `deslop`, `pre-ship`, `verification-loop`, `security-review`, `tdd-workflow`

**Type A additions:** `eval-harness`, `cost-aware-llm-pipeline`, `error-handling-patterns`, `context-budget`, `http-client-hygiene`

**Type B additions:** `frontend-design`, `web-design-patterns` (if exists), `shadcn-ui` (if exists), `frontend-taste` (if exists)

**Important: do NOT deploy `session-handoff`** at project level. Let the user-level skill (with the SignalWorks Takeaways Extension) run.

### Security baseline (always — populated from Phase 0.9 answers)
- `.env.example` — placeholder format only
- `.gitignore` — comprehensive (`.env`, `.DS_Store`, `.sessions/`, `__pycache__/`, `node_modules/`, `dry_run_output/`, `*.pyc`, etc.)
- `.claude/settings.json` — deny-list: `Bash(rm -rf*)`, `Bash(git push --force*)`. Permit-list scoped to project's expected commands.
- `src/secret_redactor.py` — stub if Type A (per anti-pattern A13). Pre-implements `redact()` + `safe_err()` skeleton with PAT/key regex placeholders.

### Project-local takeaways folder (NEW in v1.5)
- `docs/workflow-notes/session-takeaways.md` — empty file with provenance header (matches brett-roberts-la-metro pattern). The session-handoff extension dual-writes here AND to canonical signal-works-internal copy.

### Engagement registration in signal-works-internal (NEW in v1.5)
- Append entry to `signal-works-internal/TASKS.md` "In Progress" section: `| {Operator} | {Project name} — Step 1 of implementation.md | {date} | New SignalWorks engagement. See clients/{slug}/scope.md |`
- Create or update `signal-works-internal/clients/{slug}/scope.md` — discovery summary (Q1-Q7, Q11). If file exists, prompt for confirm-overwrite vs append.
- Create empty `signal-works-internal/takeaways/{slug}.md` with provenance header (same format as brett-roberts-la-metro.md).
- All three changes get one commit + push (with pull-rebase first per signal-works-internal CLAUDE.md). Failure handling: surface to operator, fall back to TODO file.

---

## Revised session-handoff extension — dual-write

Current v1 extension (single-write to canonical signal-works-internal target) gets revised to dual-write:

**Step 4 revised:**

```
4a. Write to project-local target (always):
    - Append qualified entries to {project-root}/docs/workflow-notes/session-takeaways.md
      under heading "## Session: {YYYY-MM-DD}"
    - This file is committed with the project (no separate git operations)

4b. Write to canonical target (if signalworks_takeaways_target line exists):
    - Append same entries to canonical path under same heading
    - cd to canonical repo, git pull --rebase, git add + commit + push
    - If git ops fail: write to {canonical}.pending and surface in handoff Gotchas
```

Both files get the **same content**. Project-local serves in-project visibility + travels with project archive. Canonical serves cross-engagement aggregation + survives project archival + harvest scanning.

---

## Type A vs Type B branching in /cook

### Phase 2 (Harness Design) — branch by Type

**Type A questions (AI deliverable):**
- Eval framework setup: which 3 levels (offline/online/human)? Which judge?
- Hallucination prevention architecture: verbatim-selection? grounding check? NER gate? allow-list?
- Model selection: which model + version + fallback? Cost envelope per request?
- Prompt architecture: versioned in `docs/prompts/`?
- Pre-flight calibration plan: how many real-data outputs before strict-gate ship?

**Type B questions (AI-accelerated build):**
- DESIGN.md before code: yes (mandatory)?
- Frontend stack: React/Vue/Astro/Next? shadcn-ui? Tailwind?
- Lighthouse target: ≥90 mobile?
- Performance budgets: LCP < 2.5s, CLS < 0.1, INP < 200ms?
- Browser/device matrix?

### Phase 3 (Capability Selection) — Skill Deployment Registry already extended in v1; agent-catalog deployment NEW in v1.5 (above)

---

## Critical-review pass

1. **Risk: 11 discovery + 3 authority + 6 security = 20 questions = significant friction at scaffold time.** Mitigation: each question is yes/no, multiple choice, or short answer. Estimated total dialogue time: 8-12 minutes for a full SignalWorks scaffold. Faster than manually creating 20+ files post-scaffold.

2. **Risk: TASKS.md auto-update modifies a co-owned doc (Jahleel sees it).** Mitigation: append-only to "In Progress" section, never edit existing rows. Show diff before commit. /cook surfaces the diff for explicit approval before push.

3. **Risk: `signal-works-internal/clients/{slug}/scope.md` creation may collide with existing client folder content** (e.g., Brent already has 5 files). Mitigation: detect existing folder, ask "create new scope.md, overwrite existing, or append to existing?" — let operator choose.

4. **Risk: 7 universal + 3-4 type-specific subagents = 10-11 agent files in `.claude/agents/`.** Could be overwhelming for small engagements. Mitigation: Q6 (timeline + budget) drives a "small engagement" branch — if duration < 2 weeks AND budget < $5K, deploy minimal 4-agent fleet (planner, code-reviewer, security-reviewer, evaluator).

5. **Risk: Some skills referenced in registry may not exist on operator's machine** (e.g., `frontend-taste`, `web-design-patterns` may not be installed). Mitigation: existence check before `cp -r` (per gap #2). Missing skills logged as TODO + surface to operator with install instructions.

6. **Risk: Audit prompt templates are 4 files of substantive content (~50-100 lines each) that I need to actually write, not just outline.** Mitigation: written as part of v1.5 implementation, ~200 lines of audit prompt content total. Lifted from brett-roberts-la-metro Tier 3.5 sub-agent prompts (proven, not theoretical).

7. **Risk: Session-handoff extension change is invasive** (modifies a skill that just shipped a week ago). Need to make sure dual-write logic doesn't break single-write behavior on existing brett-gove-intell sessions. Mitigation: dual-write is additive — project-local write is new, canonical write logic stays identical. Brett project's takeaways file already exists and writes will continue working.

8. **Risk: This is a substantial /cook expansion.** Adding ~400-500 lines to SKILL.md (which is currently 157 lines). Total post-v1.5: ~600-700 lines. Mitigation: structure with clear phase headers; use markdown sections; consider extracting subagent fleet table + skill registry into separate referenced files if SKILL.md grows past 800 lines.

9. **Deliberately NOT in scope for v1.5 (named, not omitted):**
   - Client-facing artifacts (proposal generation, client scope statements for sign-off)
   - Pricing automation
   - Sales-pipeline tracking
   - Notes/ → synthesis automation
   - Backporting to brett-gove-intell or other existing engagements
   - Cross-engagement coordination
   - "Small engagement" path's exact threshold (just propose < 2 weeks + < $5K — refine via dogfood)

---

## Migration

**brett-gove-intell stays as-is.** Already ~92% complete with v1 takeaways system live. Don't backport v1.5 scaffold to it. It will continue to use the existing artifacts (which were built manually). The only v1.5 change that affects brett: the dual-write session-handoff extension will start writing takeaways to BOTH `brett-gove-intell/docs/workflow-notes/session-takeaways.md` (already exists) AND `signal-works-internal/takeaways/brett-roberts-la-metro.md` (already seeded). Net: no breakage; takeaways file will receive entries from both writes; if duplicates appear, harvest dedupes.

**Other engagements (Mary PRAEGIS, Bryan GMG, Brent Stokes):** none are at /cook stage yet. When the next engagement reaches scaffold, it will use v1.5.

**Existing client folders in signal-works-internal/clients/:** untouched until that client's project hits scaffold. Then `scope.md` is added (with overwrite check per critical-review #3).

## Success criteria

1. Run `/cook` for a NEW SignalWorks engagement → resulting project has: substantive `SOUL.md`/`CLAUDE.md`/`AGENTS.md` (not template stubs), full audit-as-default triad, decision log + handoff stubs with format, 7+ subagents in `.claude/agents/`, full skill fleet in `.claude/skills/`, security baseline, project-local takeaways folder, engagement registered in signal-works-internal.
2. The dialogue captures discovery answers verbatim into the artifacts, not into a separate notes file.
3. Phase 0.9 security pre-flight surfaces and resolves anti-pattern A3 (fork lineage) BEFORE any work begins.
4. session-handoff dual-writes correctly: same content lands in project-local AND canonical takeaways files, both auto-commit.
5. Existing brett-gove-intell project continues working without modification.

## Implementation order (high-level — planning skill produces step-by-step)

1. **Inventory existing scaffold output** — read current `/cook` Phase 4 to understand what's already produced.
2. **Verify all referenced agent files exist** in `~/AI-Knowledgebase/future-reference/agent-catalog/` (already done — see brainstorming session).
3. **Verify skill files exist** in `~/.claude/skills/` for the registry — write existence-check helper.
4. **Write the audit prompt templates** (4 files, ~50-100 lines each, ~250-350 lines total) lifted from brett-roberts-la-metro Tier 3.5 patterns.
5. **Write the audit-protocol.md** canonical playbook.
6. **Patch /cook SKILL.md** — add Phase 0.5, 0.7, 0.9 [SW] phases; expand Phase 2 with Type A/B branches; expand Phase 4 scaffold output list; add Phase 5 engagement registration.
7. **Edit ~/.claude/skills/session-handoff/SKILL.md** — Step 4 dual-write logic.
8. **Update MEMORY.md** with v1.5 system index entries.
9. **Update KB-INDEX.md** if any new playbook entries (likely not — audit-protocol.md and audit prompts live in scaffolded projects, not in KB).
10. **Manual test gate** (operator runs `/cook` for a sandbox SignalWorks project; verifies output matches success criteria #1-4).
11. **Commit + push design + impl + edits across signal-works-internal and AI-Knowledgebase.**

---

## v1.5 status

Approved 2026-04-25 in brainstorming session. Companion implementation plan to come from `planning` skill. Autonomous execution authorized per prior session pattern (commit + push as we go on `signal-works-internal`; KB commits batched).
