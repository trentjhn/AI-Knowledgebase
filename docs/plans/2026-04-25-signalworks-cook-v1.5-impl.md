# /cook v1.5 SignalWorks-Mode Implementation Plan

> **For Claude:** Adapt the bite-sized task template for markdown-and-skill-edit work. Verification is grep + manual end-to-end test (no pytest equivalent). Companion design doc: `docs/plans/2026-04-25-signalworks-cook-v1.5-design.md`.

**Goal:** Ship /cook v1.5 SignalWorks-mode. When `/cook` classifies a project as SignalWorks consulting engagement, it runs Phase 0.5 (engagement discovery, 11 Qs), Phase 0.7 (authority + brand, 3 Qs), Phase 0.9 (security pre-flight, 6 yes/no checks), branches Phase 2 by Type A/B, and produces a substantively complete consulting-grade scaffold (full doc spine + audit triad + 7-agent universal fleet + skill fleet + security baseline + project-local takeaways folder + engagement registration in signal-works-internal). Also revises session-handoff extension to dual-write (project-local + canonical).

**Architecture:** Single skill, two modes (Approach 1). Audit triad content lives in `~/AI-Knowledgebase/future-reference/templates/audit-protocol/` as 5 source-of-truth files; `/cook` Phase 4 copies them into new projects. session-handoff extension's Step 4 expanded to dual-write. Existing brett-gove-intell project untouched.

**Tech Stack:** Markdown content + bash skill instructions. No application code. Verification: end-to-end manual test by running `/cook` in a sandbox SignalWorks project.

---

## Phase 1: Audit triad source files (5 files in KB templates/)

### Task 1: Create audit-protocol/ folder with audit-protocol.md

**Files:**
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/templates/audit-protocol/audit-protocol.md`

**Step 1:** Create the folder + write the canonical playbook (~80 lines):

```markdown
# Audit Protocol

**Purpose:** Canonical playbook for multi-agent audit sweeps in SignalWorks engagements. Referenced by every project's CLAUDE.md Session End Protocol.

## When to run
- Session-end (mandatory before invoking session-handoff)
- Pre-tier-ship in multi-tier work (mandatory before declaring tier complete)
- Pre-delivery (mandatory before sharing client-facing artifact)

## How many agents
Default: 4 parallel sub-agents on non-overlapping territories.
Optional 5th territory based on engagement (e.g., "model behavior" for Type A; "performance" for high-throughput).

## Default 4 territories
1. Code correctness + error handling — `docs/prompts/audits/code-correctness.md`
2. Security + secrets + external access — `docs/prompts/audits/security.md`
3. UX + content + delivery — `docs/prompts/audits/ux-delivery.md`
4. Docs + runbook + onboarding — `docs/prompts/audits/docs-operations.md`

## Self-critique mandate
Every audit prompt ends with: "After your initial sweep, spend a second pass looking for what you might have missed." This second pass consistently surfaces findings the initial sweep missed.

## Output format
Each agent returns:
```
## P1 (blocks ship)
- [ID-NNN] description | file:line | fix shape | effort | reversibility

## P2 (fix before client share)
...

## P3 (polish, post-launch)
...
```

## Consolidation step
1. Dedupe across agents.
2. Triage by "does the fix require a costly re-run?" before severity (cohort split).
3. Ship P1 fixes in-session.
4. Log P2/P3 in handoff's "Audit Directions for Next Session" slot.

## Length budget per agent
1500 words for code/security/UX agents. 900 words for structural (docs) agents.

## Provenance
Pattern proven on brett-roberts-la-metro 2026-04 (Tier 3 + Tier 3.5 sweeps). 8+ audit sub-agents, 40+ findings, 0 false positives at P1 tier.
```

**Step 2:** Verify

```bash
wc -l /Users/t-rawww/AI-Knowledgebase/future-reference/templates/audit-protocol/audit-protocol.md
```

Expected: ~50-80 lines.

**Step 3:** Defer commit (batched with Tasks 2-5 in Task 6).

---

### Task 2: Write code-correctness audit prompt template

**Files:**
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/templates/audit-protocol/code-correctness.md`

**Step 1:** Write the audit prompt (~80-100 lines) with `{{PROJECT_CONTEXT}}`, `{{SLICE}}`, `{{KNOWN_PRIORS}}` placeholders. Content lifted from brett-roberts-la-metro Tier 3.5 patterns:
- Project context placeholder
- Slice (which files / which territory)
- Known priors (past findings to avoid rediscovering)
- Hunt categories: zombie tests (anti-pattern A6), data-format change adjacency drift (A9), silent failures (A4), unhandled error paths
- Output format: P1/P2/P3 with `CORR-NNN` tag prefix
- Self-critique meta-questions (4-5 specific to code correctness)
- Length budget: 1500 words

**Step 3:** Defer commit.

---

### Task 3: Write security audit prompt template

**Files:**
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/templates/audit-protocol/security.md`

**Step 1:** Same structure as Task 2 but for security territory:
- Hunt categories: prompt-injection (URL-scheme XSS), token leakage in logs (A13), centralized vs inlined redaction, fork-lineage privacy (A3), GitHub Actions permissions, CF Pages preview bypass, `.env.example` placeholder hygiene, branch-protection rules
- Tag prefix: `SEC-NNN`
- Self-critique meta-questions calibrated to security

**Step 3:** Defer commit.

---

### Task 4: Write UX/delivery audit prompt template

**Files:**
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/templates/audit-protocol/ux-delivery.md`

**Step 1:** Same structure for UX territory:
- Hunt categories: bare-dashboard problem (A10), client-ready vs ship-ready (A16), first-impression failure modes, accessibility (h1 / screen reader), responsive QA, content scannability, mailto/email choreography
- Tag prefix: `UX-N`
- Self-critique meta-questions: "would a fresh viewer call this a product or a placeholder?"

**Step 3:** Defer commit.

---

### Task 5: Write docs/operations audit prompt template

**Files:**
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/templates/audit-protocol/docs-operations.md`

**Step 1:** Same structure for docs territory:
- Hunt categories: doc debt vs code debt rate (A5), README contradicts itself, runbook references stale versions, missing alert-response decision tree, missing operator-commands.md (A8 fallout), missing invariants.md, decision log gaps
- Tag prefix: `DOC-N`
- Length budget: 900 words (structural agent)

**Step 3:** Defer commit.

---

### Task 6: Commit Phase 1 audit triad source files

```bash
cd /Users/t-rawww/AI-Knowledgebase
git add future-reference/templates/audit-protocol/
git commit -m "Add audit-protocol/ source files for /cook v1.5 SignalWorks scaffolding

Five files (audit-protocol.md + 4 audit prompt templates) that /cook
copies into every new SignalWorks project's docs/audit-protocol.md
and docs/prompts/audits/. Lifted from brett-roberts-la-metro Tier 3.5
patterns (proven, not theoretical)."
```

Push deferred to Task 18.

---

## Phase 2: /cook SKILL.md patches

### Task 7: Add Phase 0.5 Engagement Discovery to /cook

**Files:**
- Modify: `/Users/t-rawww/.claude/skills/cook/SKILL.md` (insert between Phase 0.5 Domain Research and Phase 1)

**Step 1:** Read current SKILL.md. Insert new Phase 0.6 (calling it 0.6 to avoid colliding with existing 0.5 Domain Research):

```markdown
### Phase 0.6: SignalWorks Engagement Discovery [SignalWorks engagements only]

If the project is classified as a SignalWorks consulting engagement (Phase 1, Q4), run discovery BEFORE Phase 1.5. Otherwise skip.

Reference: `signalworks-consulting.md` Section 1 (Engagement Discovery).

Ask one question at a time. Capture answers verbatim into the eventual scaffold.

1. Client name + role + organization?
2. What's the problem? (capture exactly as you say it)
3. What's the deliverable? (URL / dashboard / automation / model / etc.)
4. What's explicitly NOT in scope? (list 3+ items)
5. Type A (AI is the deliverable) or Type B (AI accelerates a non-AI build)? Or hybrid?
6. Timeline + budget envelope? (duration in weeks, hard end-date if any, fixed-price vs hourly)
7. Success criteria? (numeric where possible)
8. Authority block — what can Claude decide autonomously? What requires you to approve?
9. Client-specific brand voice rules beyond SignalWorks defaults?
10. Existing context to ingest? (folder paths, docs, brand guidelines)
11. Operational constraints? (compliance, budget caps, security clearance)

Capture answers into in-memory dialogue state. Do NOT write to files yet — Phase 4 writes them all at once into the proper artifacts.
```

**Step 3:** Defer commit (batched with Tasks 8-13 in Task 14).

---

### Task 8: Add Phase 0.7 Authority + Brand to /cook

**Files:**
- Modify: `/Users/t-rawww/.claude/skills/cook/SKILL.md` (insert after Phase 0.6)

**Step 1:** Insert:

```markdown
### Phase 0.7: Authority + Brand [SignalWorks engagements only]

3 questions, populates CLAUDE.md "Authority Block" section.

12. Decide-autonomously list: which categories of decisions can Claude make without pausing?
   - [ ] Code edits within locked architecture
   - [ ] Test additions / refactors
   - [ ] Doc updates
   - [ ] Sub-agent feedback interpretation
   - [ ] Tie-breaking on reversible options
   - Free-form additions:

13. Pause-for-operator list: which categories require explicit approval?
   - [ ] Physical UI tasks (account creation, token gen, client emails)
   - [ ] Irreversible actions (force push, hard reset, drop tables)
   - [ ] Client-facing product changes
   - [ ] Test suite failing after 2 fix attempts
   - [ ] Crossing a locked decision
   - Free-form additions:

14. Locked decisions at kickoff: any pre-locked architectural / scope decisions Claude should NOT cross?
```

**Step 3:** Defer commit.

---

### Task 9: Add Phase 0.9 Security Pre-flight to /cook

**Files:**
- Modify: `/Users/t-rawww/.claude/skills/cook/SKILL.md` (insert after Phase 0.7, before Phase 1)

**Step 1:** Insert:

```markdown
### Phase 0.9: Security Pre-flight [SignalWorks engagements only]

6 yes/no checks. Failures don't block scaffold but get TODOed in `docs/plans/design.md` "Security Action Items" section. References anti-pattern A3 (fork lineage).

15. Repo privacy: private from day 1? (default yes for client work; mandatory yes if Q11 flagged compliance)
16. Fork lineage: forked from anywhere? (if yes, check public-fork → private feasibility per anti-pattern A3)
17. .env.example placeholders only? (default yes; auto-scaffolded)
18. GitHub Actions workflow permissions = `contents: read` minimum? (default yes; baked into .github/workflows/)
19. Default branch protection rules? (default yes; surfaces as TODO with `gh` command)
20. Sensitive content scan needed at pre-ship? (default yes if Q11 flagged compliance; surfaces as recurring CI check)

Failures and TODOs are captured in dialogue state for Phase 4 to write into design.md.
```

**Step 3:** Defer commit.

---

### Task 10: Add Type A/B branching to Phase 2 Harness Design

**Files:**
- Modify: `/Users/t-rawww/.claude/skills/cook/SKILL.md` (in Phase 2 section)

**Step 1:** After existing Phase 2 introduction, add Type A/B branch:

```markdown
**For SignalWorks engagements (Phase 0.6 Q5 = Type A, Type B, or hybrid):**

If Type A (AI deliverable):
- Eval framework setup: which 3 levels (offline/online/human)? Which judge?
- Hallucination prevention architecture: verbatim-selection? grounding check? NER gate? allow-list?
- Model selection: which model + version + fallback? Cost envelope per request?
- Prompt architecture: versioned in `docs/prompts/`?
- Pre-flight calibration plan: how many real-data outputs before strict-gate ship?
- Reference: `signalworks-consulting.md` §16 (Type A Specifics)

If Type B (AI-accelerated build):
- DESIGN.md before code: yes (mandatory)?
- Frontend stack: React/Vue/Astro/Next? shadcn-ui? Tailwind?
- Lighthouse target: ≥90 mobile?
- Performance budgets: LCP < 2.5s, CLS < 0.1, INP < 200ms?
- Browser/device matrix?
- Reference: `signalworks-consulting.md` §17 (Type B Specifics)

If hybrid: apply both.
```

**Step 3:** Defer commit.

---

### Task 11: Expand Phase 3 Capability Selection — subagent fleet for SignalWorks

**Files:**
- Modify: `/Users/t-rawww/.claude/skills/cook/SKILL.md` (in Phase 3 / Skill Deployment Registry section)

**Step 1:** Add Subagent Deployment Registry table next to existing Skill Deployment Registry:

```markdown
#### Subagent Deployment Registry [SignalWorks engagements]

For SignalWorks engagements, deploy these agents from `~/AI-Knowledgebase/future-reference/agent-catalog/` into `{new-project}/.claude/agents/`:

**Universal SignalWorks fleet (always):**
| Agent | Source path |
|---|---|
| planner | `core/planner.md` |
| architect | `core/architect.md` |
| code-reviewer | `core/code-reviewer.md` |
| doc-updater | `core/doc-updater.md` |
| tdd-guide | `quality/tdd-guide.md` |
| security-reviewer | `quality/security-reviewer.md` |
| evaluator | `quality/evaluator.md` |

**Type A additions:**
| Agent | Source path |
|---|---|
| prompt-engineer | `ai-specialist/prompt-engineer.md` |
| eval-designer | `ai-specialist/eval-designer.md` |
| context-architect | `ai-specialist/context-architect.md` |
| data-analyst | `ai-specialist/data-analyst.md` |

**Type B additions:**
| Agent | Source path |
|---|---|
| product-designer | `design/product-designer.md` |
| ui-designer | `design/ui-designer.md` |
| accessibility-reviewer | `design/accessibility-reviewer.md` |
| typescript-reviewer | `quality/typescript-reviewer.md` (if TS stack) |

**Optional (engagement-size based, Q6 timeline):**
| Agent | When to deploy |
|---|---|
| chief-of-staff | Multi-week complex engagements |
| spec-writer | Engagements with formal spec docs |
| technical-writer | Client-facing docs needed |

**Small-engagement override** (Q6 < 2 weeks AND budget < $5K): deploy only minimal 4-agent fleet (planner, code-reviewer, security-reviewer, evaluator).

For each agent: `cp ~/AI-Knowledgebase/future-reference/agent-catalog/{path} {new-project}/.claude/agents/{name}.md`. Verify with `ls {new-project}/.claude/agents/`.
```

**Step 3:** Add skill existence check helper above the existing Skill Deployment Registry:

```markdown
**Skill existence check helper (apply before each cp):**

```bash
deploy_skill() {
  local skill_name="$1"
  local target_project="$2"
  if [ -d "$HOME/.claude/skills/$skill_name" ]; then
    cp -r "$HOME/.claude/skills/$skill_name" "$target_project/.claude/skills/$skill_name"
    echo "✓ Deployed: $skill_name"
  else
    echo "⚠ MISSING: $skill_name — skipped. Install or remove from registry."
  fi
}
```
```

**Step 4:** Defer commit.

---

### Task 12: Expand Phase 4 Scaffold Output — substantive consulting-grade

**Files:**
- Modify: `/Users/t-rawww/.claude/skills/cook/SKILL.md` (Phase 4 section)

**Step 1:** Add new section to Phase 4 BEFORE the existing Required Files list:

```markdown
**SignalWorks engagement additional outputs (Phase 0.6 classified as SignalWorks):**

In addition to the universal Required Files below, SignalWorks engagements scaffold:

### Audit-as-Default Triad
Copy from `~/AI-Knowledgebase/future-reference/templates/audit-protocol/`:
- `~/AI-Knowledgebase/future-reference/templates/audit-protocol/audit-protocol.md` → `{new-project}/docs/audit-protocol.md`
- `~/AI-Knowledgebase/future-reference/templates/audit-protocol/code-correctness.md` → `{new-project}/docs/prompts/audits/code-correctness.md`
- `~/AI-Knowledgebase/future-reference/templates/audit-protocol/security.md` → `{new-project}/docs/prompts/audits/security.md`
- `~/AI-Knowledgebase/future-reference/templates/audit-protocol/ux-delivery.md` → `{new-project}/docs/prompts/audits/ux-delivery.md`
- `~/AI-Knowledgebase/future-reference/templates/audit-protocol/docs-operations.md` → `{new-project}/docs/prompts/audits/docs-operations.md`

### Session continuity stubs
- `{new-project}/.sessions/handoffs/handoff-{YYYY-MM-DD}-v1.md` — initial stub:
  - Status: "Engagement just scaffolded by /cook v1.5 on {date}"
  - What's Done: scaffold complete
  - What's In Progress: none yet
  - What's Pending: Step 1 of `docs/plans/implementation.md`
  - Resume Command: "Continue {project} engagement at {path}. Read SOUL.md → AGENTS.md → CLAUDE.md → this handoff. Start at Step 1 of implementation.md."
  - Audit Directions for Next Session: empty list with format
- `{new-project}/.sessions/handoffs/decision-log-{YYYY-MM-DD}.md` — header with 8-field format template + pre-seeded entry: "Decision: Engagement scaffolded with /cook v1.5" capturing initial decisions from Q5, Q8, Q14.

### Project-local takeaways folder
- `{new-project}/docs/workflow-notes/session-takeaways.md` — empty file with provenance header. Format matches `signal-works-internal/takeaways/brett-roberts-la-metro.md` header. Session-handoff dual-writes here.

### Client context (if Q10 provided paths)
- `{new-project}/docs/client-context.md` — references / symlinks to existing context paths from Q10.

### Invariants stub
- `{new-project}/docs/invariants.md` — empty stub with format header (one section per invariant: name, enforcement mechanism, test reference).

### Security baseline (populated from Phase 0.9 answers)
- `{new-project}/.env.example` — placeholder format only
- `{new-project}/.gitignore` — comprehensive (`.env`, `.DS_Store`, `.sessions/`, `__pycache__/`, `node_modules/`, `dry_run_output/`, `*.pyc`, etc.)
- `{new-project}/.claude/settings.json` — deny-list: `Bash(rm -rf*)`, `Bash(git push --force*)`. Permit-list scoped to project's expected commands.
- If Type A: `{new-project}/src/secret_redactor.py` — stub with `redact()` + `safe_err()` skeleton.

### CLAUDE.md baking
Bake from `signal-works-internal/process/client-engagement-CLAUDE-template.md`. Replace ALL `[FILL AT ENGAGEMENT KICKOFF: ...]` markers from discovery answers (Q1, Q5, Q8, Q9, Q10, Q14). Substitute `{PROJECT_NAME}`, `{CLIENT_SLUG}`, `{CLIENT_NAME_AND_ROLE}`, `{ENGAGEMENT_DESCRIPTION}`, `{OPERATOR_NAME}`. Result is the new project's CLAUDE.md.

### SOUL.md substantive content
Generate substantive SOUL.md (60-80 lines) from Q1 (client) + Q2 (problem verbatim) + Q7 (success criteria) + Q9 (voice rules). NOT a template stub — actual character of THIS engagement.

### design.md substantive content
Write `{new-project}/docs/plans/design.md` with sections populated from discovery:
- Problem Statement (Q2 verbatim)
- Deliverable (Q3)
- Out of Scope (Q4)
- Engagement Envelope (Q6)
- Success Criteria (Q7)
- Constraints (Q11)
- Locked Decisions (Q14)
- Security Action Items (Phase 0.9 failures)
- Phase 2 Architectural Decisions (Type A/B answers)
```

**Step 3:** Defer commit.

---

### Task 13: Add Phase 5 SignalWorks engagement registration

**Files:**
- Modify: `/Users/t-rawww/.claude/skills/cook/SKILL.md` (after Phase 5 Eval + Security Baseline)

**Step 1:** Add new sub-phase:

```markdown
### Phase 5.5: SignalWorks Engagement Registration [SignalWorks engagements only]

After scaffold output (Phase 4) completes, register the engagement in signal-works-internal:

1. **Append to TASKS.md "In Progress"** (signal-works-internal/TASKS.md):
   - Pull-rebase signal-works-internal first.
   - Append row: `| {operator} | {project name} — Step 1 of implementation.md | {YYYY-MM-DD} | New SignalWorks engagement. See clients/{slug}/scope.md |`
   - Show diff to operator before commit.

2. **Create or update `signal-works-internal/clients/{slug}/scope.md`:**
   - If file exists: prompt "create new scope.md, overwrite existing, or append to existing?"
   - Content: discovery summary (Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q11) — narrative, not bullet-only.

3. **Create empty `signal-works-internal/takeaways/{slug}.md`:**
   - With provenance header (same format as brett-roberts-la-metro.md but empty body):
     ```
     # {Client Name} ({Slug}) — Workflow Takeaways

     **Engagement:** {Q1 answer}
     **Project repo:** `{new-project absolute path}`
     **Status as of seed date ({date}):** Just scaffolded.
     **File purpose:** Canonical SignalWorks-internal copy of per-engagement workflow takeaways. Extended `session-handoff` skill auto-appends new entries here at session end.
     **Provenance tag:** First observed in: {slug}, {YYYY-MM}.

     ---

     (Empty — entries will be appended by session-handoff at session end.)
     ```

4. **Commit + push** all three changes in one commit:
   ```bash
   cd /Users/t-rawww/signal-works-internal
   git add TASKS.md clients/{slug}/scope.md takeaways/{slug}.md
   git commit -m "Register {slug} engagement: scope, takeaways stub, TASKS.md entry"
   git push
   ```

5. **Failure handling:** if any git step fails, write changes locally and surface to operator: "⚠ Engagement registration partially failed at git layer. Files written locally; commit manually:" + commands.
```

**Step 3:** Defer commit.

---

### Task 14: Commit /cook SKILL.md edits (Phase 2 batch)

**No git** — `~/.claude/skills/` is not a git repo. Edits persist locally on operator's machine.

Verify with grep:

```bash
grep -c "SignalWorks engagement\|Phase 0.6\|Phase 0.7\|Phase 0.9\|Phase 5.5\|Subagent Deployment Registry\|Audit-as-Default Triad" ~/.claude/skills/cook/SKILL.md
```

Expected: ≥ 7.

---

## Phase 3: session-handoff dual-write

### Task 15: Edit session-handoff SKILL.md Step 4 → dual-write

**Files:**
- Modify: `/Users/t-rawww/.claude/skills/session-handoff/SKILL.md` (Step 4 of SignalWorks Takeaways Extension)

**Step 1:** Replace existing Step 4 with dual-write logic:

```markdown
### Step 4: Dual-write — project-local + canonical

**4a. Write to project-local target (always):**

The project's takeaways folder is at `{project-root}/docs/workflow-notes/session-takeaways.md`. This file should already exist (scaffolded by `/cook` v1.5+) or pre-existed (e.g., brett-gove-intell).

```bash
PROJECT_TAKEAWAYS="$(git rev-parse --show-toplevel)/docs/workflow-notes/session-takeaways.md"
if [ -f "$PROJECT_TAKEAWAYS" ]; then
  # Append entries under "## Session: {YYYY-MM-DD}" heading
  echo "" >> "$PROJECT_TAKEAWAYS"
  echo "## Session: $(date +%Y-%m-%d)" >> "$PROJECT_TAKEAWAYS"
  echo "" >> "$PROJECT_TAKEAWAYS"
  echo "$ENTRIES" >> "$PROJECT_TAKEAWAYS"
fi
```

The project-local file is committed with the project's normal commits (no separate git operations from session-handoff — operator commits as part of regular work).

**4b. Write to canonical target (if signalworks_takeaways_target line exists):**

If the project's CLAUDE.md has a `signalworks_takeaways_target:` line, ALSO append the same entries to that canonical path. This is the existing v1 logic, unchanged:

```bash
TARGET_PATH="<absolute path from step 1>"
TARGET_REPO=$(git -C "$(dirname "$TARGET_PATH")" rev-parse --show-toplevel)
TARGET_RELPATH=$(realpath --relative-to="$TARGET_REPO" "$TARGET_PATH")
SLUG=$(basename "$TARGET_PATH" .md)
TODAY=$(date +%Y-%m-%d)

cd "$TARGET_REPO" && git pull --rebase

# Append same heading + entries
echo "" >> "$TARGET_PATH"
echo "## Session: $TODAY" >> "$TARGET_PATH"
echo "" >> "$TARGET_PATH"
echo "$ENTRIES" >> "$TARGET_PATH"

git add "$TARGET_RELPATH"
git commit -m "takeaways(${SLUG}): N entries from ${TODAY} session"
git push
```

Both files receive identical content. Project-local serves in-project visibility; canonical serves cross-engagement aggregation + survives project archival.

**4c. Failure handling for canonical-write:** if git ops fail (network, conflict), write to `${TARGET_PATH}.pending` and surface in handoff Gotchas. Project-local write is unaffected.
```

**Step 2:** Verify

```bash
grep -c "Dual-write\|4a\|4b\|4c\|PROJECT_TAKEAWAYS" ~/.claude/skills/session-handoff/SKILL.md
```

Expected: ≥ 5.

**Step 3:** No git (user-skills not tracked).

---

## Phase 4: Wrap-up

### Task 16: Update MEMORY.md with v1.5 system

**Files:**
- Modify: `/Users/t-rawww/.claude/projects/-Users-t-rawww-AI-Knowledgebase/memory/MEMORY.md`

**Step 1:** Add v1.5 entries under existing "SignalWorks Workflow Capture System" section:

```markdown
## SignalWorks /cook v1.5 (built 2026-04-25)
- /cook now has SignalWorks-mode: Phase 0.6 (engagement discovery, 11 Qs), Phase 0.7 (authority + brand, 3 Qs), Phase 0.9 (security pre-flight, 6 yes/no), Phase 2 Type A/B branching, Phase 4 substantive consulting-grade scaffold output, Phase 5.5 engagement registration in signal-works-internal.
- Audit triad source files: `~/AI-Knowledgebase/future-reference/templates/audit-protocol/{audit-protocol,code-correctness,security,ux-delivery,docs-operations}.md` — copied into every new SignalWorks project's docs/audit-protocol.md + docs/prompts/audits/.
- session-handoff extension v1.5: dual-write (project-local docs/workflow-notes/session-takeaways.md AND canonical signal-works-internal/takeaways/{slug}.md). Same content, project-local committed with project, canonical auto-committed and pushed.
- brett-gove-intell continues working unchanged — dual-write is additive, both files already exist for that project.
- v1.5 only applies to NEW engagements scaffolded after 2026-04-25.
- Design: `docs/plans/2026-04-25-signalworks-cook-v1.5-design.md`
- Plan: `docs/plans/2026-04-25-signalworks-cook-v1.5-impl.md`
- Manual test gate: run `/cook` on a sandbox SignalWorks project; verify all artifact outputs match Success Criteria #1-4 in design doc.
```

**Step 3:** No git (memory file is not committed).

---

### Task 17: Manual test gate (operator runs /cook in sandbox)

**Setup:**

```bash
mkdir -p /tmp/sw-cook-v1.5-test
cd /tmp/sw-cook-v1.5-test
git init
```

**Test:** Operator runs `/cook` (in fresh Claude Code session in `/tmp/sw-cook-v1.5-test`). Answers Q1-Q11 (discovery), Q12-Q14 (authority/brand), Phase 0.9 yes/no checks. Selects classification (e.g., Type A AI/agentic).

**Verify outputs:**
- `/tmp/sw-cook-v1.5-test/CLAUDE.md` exists, contains substituted client name, signalworks_takeaways_target line, filled authority block (no `[FILL AT...]` markers remaining).
- `/tmp/sw-cook-v1.5-test/SOUL.md` exists with substantive content (60+ lines, NOT template).
- `/tmp/sw-cook-v1.5-test/AGENTS.md` exists with subagent roster matching deployed agents.
- `/tmp/sw-cook-v1.5-test/.claude/agents/` contains 7+ agents (universal fleet) + Type-A additions.
- `/tmp/sw-cook-v1.5-test/.claude/skills/` contains universal + Type-A skills (skill existence check ran without copying missing skills).
- `/tmp/sw-cook-v1.5-test/docs/audit-protocol.md` exists.
- `/tmp/sw-cook-v1.5-test/docs/prompts/audits/{code-correctness,security,ux-delivery,docs-operations}.md` all exist.
- `/tmp/sw-cook-v1.5-test/docs/workflow-notes/session-takeaways.md` exists with provenance header.
- `/tmp/sw-cook-v1.5-test/.sessions/handoffs/handoff-{date}-v1.md` exists with Resume Command.
- `/tmp/sw-cook-v1.5-test/.sessions/handoffs/decision-log-{date}.md` exists with format header + pre-seeded first entry.
- `/tmp/sw-cook-v1.5-test/docs/plans/design.md` exists with Q2 problem statement verbatim.
- `/tmp/sw-cook-v1.5-test/.gitignore` includes `.env`, `.sessions/`, `__pycache__/`.
- `signal-works-internal/TASKS.md` has new "In Progress" row.
- `signal-works-internal/clients/{test-slug}/scope.md` created.
- `signal-works-internal/takeaways/{test-slug}.md` created with provenance header.

**Cleanup:** `rm -rf /tmp/sw-cook-v1.5-test` AND remove the test entry from `signal-works-internal/TASKS.md` + the test client folder/takeaways file (if /cook actually committed them — manually revert).

**If any verification failed:** return to relevant Task and fix the SKILL.md edits.

---

### Task 18: Final commit and push (KB)

**Step 1:** Stage all KB changes:

```bash
cd /Users/t-rawww/AI-Knowledgebase
git stash push -m "pre-v1.5-impl-stash" --keep-index 2>/dev/null
git add docs/plans/2026-04-25-signalworks-cook-v1.5-impl.md
git add future-reference/templates/audit-protocol/
```

**Step 2:** Commit:

```bash
git commit -m "Ship /cook v1.5 SignalWorks-mode: audit triad + impl plan

- 5 audit triad source files in future-reference/templates/audit-protocol/
- Implementation plan at docs/plans/2026-04-25-signalworks-cook-v1.5-impl.md
- Companion /cook SKILL.md and session-handoff SKILL.md edits land at user-skill level (not git-tracked)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

**Step 3:** Pull-rebase and push (handle ArXiv-bot auto-pushes):

```bash
git pull --rebase
git push
git stash pop 2>/dev/null
```

---

## Success criteria (gates for "done")

1. Run `/cook` for a new SignalWorks engagement → resulting project has every artifact listed in design doc Section "Scaffold output."
2. Discovery dialogue captures answers verbatim into `SOUL.md`, `CLAUDE.md`, `docs/plans/design.md`, etc.
3. Phase 0.9 security pre-flight surfaces fork-lineage check (anti-pattern A3) BEFORE work begins.
4. session-handoff dual-writes correctly: same content lands in project-local AND canonical takeaways files.
5. Existing brett-gove-intell project continues working unchanged.

---

## Plan complete

**Saved to:** `docs/plans/2026-04-25-signalworks-cook-v1.5-impl.md`

Same execution mode as v1: subagent-driven, this session, autonomous (per prior authorization).
