# SignalWorks Takeaways Capture & Consulting Playbook — Design

**Date:** 2026-04-24
**Status:** Approved, ready for planning
**Owner:** Trent Johnson
**Brainstorming session:** This file is the validated output of a brainstorming pass on automating workflow-takeaway capture across SignalWorks engagements.

---

## Problem statement

Today, after each work session on a SignalWorks client engagement (e.g., `brett-gove-intell`), Trent manually prompts Claude to extract workflow takeaways and append them to a per-project file (`docs/workflow-notes/session-takeaways.md`). The manual prompting is friction; the per-project location means takeaways go stale once the engagement wraps; and there is no mechanism to flow proven patterns back into `/cook` (the project scaffolder) or into a SignalWorks-specific consulting methodology. The existing `/cook` workflow, driven by `magnum-opus.md`, is generic — it does not know about consulting-specific opinions (authority blocks, decision-log discipline, multi-agent audit, tier-based shipping, brand voice) that have repeatedly proven valuable on Brett-style engagements.

Result: lessons learned in client work do not compound. Each new SignalWorks engagement starts from the same generic baseline as a personal experiment.

## Goals

1. **Auto-capture** workflow takeaways at session end, $0 incremental API cost, no manual prompting required.
2. **Aggregate** takeaways into a durable SignalWorks-internal location so they survive engagement archival.
3. **Specialize** the project-scaffolding workflow for SignalWorks engagements (consulting playbook), more opinionated and more effective than generic Magnum Opus.
4. **Close the loop** via a periodic harvest skill that promotes proven patterns from per-engagement takeaways into the consulting playbook (and, when patterns are universally evergreen, into the personal KB).
5. **Fix the `/cook` skill-deployment gap** observed on `brett-gove-intell` (front-end skills were not deployed into the project's `.claude/skills/` despite the engagement having UI deliverables).

## Non-goals (deliberately out of scope)

- Stop hooks calling the Anthropic API for transcript extraction (rejected: incremental cost; in-session extraction during `session-handoff` is free and higher-quality because context is already loaded).
- Cross-project deduplication on capture (deferred to harvest).
- Real-time aggregation across multiple concurrent sessions on the same engagement (single-session assumption is fine for v1).
- Auto-creating new client folders in `signal-works-internal/clients/` from `/cook` (manual operational step).
- Migrating non-SignalWorks projects (e.g., personal experiments) into this system. Scope is SignalWorks-only.

## Architecture

Five components across three locations:

```
~/signal-works-internal/                    (operational hub, co-owned with Jahleel)
├── takeaways/                              [NEW folder]
│   ├── brett-roberts-la-metro.md           [NEW per-engagement file, auto-appended]
│   └── {future-engagement-slug}.md
├── process/
│   ├── case-study-template.md              [existing]
│   ├── consulting-playbook.md              [NEW — methodology, seeded day 1]
│   └── client-engagement-CLAUDE-template.md  [NEW — snippet for per-project CLAUDE.md]
└── ...

~/.claude/skills/
├── session-handoff/SKILL.md                [EXTENDED — auto-appends takeaways]
└── cook/SKILL.md                           [PATCHED — Phase 1 routing + Phase 2 skill deployment]

{client-engagement-repo}/                   (e.g., brett-gove-intell)
├── CLAUDE.md                               [includes mandate snippet + signalworks_takeaways_target line]
├── docs/workflow-notes/                    [pre-existing on brett-gove-intell, optional going forward]
│   └── session-takeaways.md
└── .sessions/handoffs/                     [unchanged]
```

### Component 1 — `signal-works-internal/takeaways/{slug}.md` (per-engagement raw capture)

Top-level `takeaways/` folder in the SignalWorks operational hub. One file per engagement, named by client slug to align with `clients/{slug}/`. Format mirrors the existing `brett-gove-intell` `session-takeaways.md` exactly (Pattern → Evidence → Transfer rule), so harvest can read both.

**Why top-level not nested in `clients/{slug}/`:** Takeaways are methodology, not client operations. Keeping them separate from `clients/{slug}/contact.md` and `outreach-v2.md` preserves folder semantics and makes harvest a one-folder scan.

**Why durable:** `signal-works-internal` is the operational hub Trent and Jahleel use across all engagements forever. When a per-engagement code repo (`brett-gove-intell`) goes inactive, the takeaways survive in the hub.

### Component 2 — `AI-Knowledgebase/future-reference/playbooks/signalworks-consulting.md` (curated methodology)

The SignalWorks-specific scaffolding playbook. Lives next to `case-study-template.md` (the existing process/methodology home). Read by `/cook` Phase 1 when classification matches "SignalWorks consulting engagement."

**Effectiveness target:** as effective as Magnum Opus, or more, by being more opinionated and more specific to consulting work. Magnum Opus is generic; this playbook can mandate proven patterns ("every SignalWorks engagement uses tier-based shipping with commit checkpoints") without watering them down for non-consulting use cases.

**Day-1 seeded content** (extracted from `brett-gove-intell` handoffs v3-v7 and `session-takeaways.md`):

1. **Engagement Discovery** — client problem framing, scope negotiation, deliverable type classification (Type A vs Type B — see below), success criteria, timeline, budget, authority block negotiation
2. **Type Classification** — Type A (AI deliverable: AI workflow/automation IS the product) vs Type B (AI-accelerated build: AI coding agents help build a non-AI deliverable). Branch the rest of the playbook based on type
3. **Authority Block Setup** — explicit list of what Claude can decide autonomously vs what requires Trent/client approval (covers reversibility, locked decisions, irreversible actions)
4. **Source-of-Truth Doc Spine** — `design.md`, `implementation.md`, `prompts/`, `.sessions/handoffs/`, decision log
5. **CLAUDE.md Mandate** — "invoke session-handoff at session end, not optional" + `signalworks_takeaways_target` path + Session Start Protocol
6. **Tier-Based Shipping** — decompose any ambitious refactor into 3-5 tiers each individually shippable; commit checkpoint per tier; rollback path per tier
7. **Multi-Agent Audit Discipline** — for client-ready sweeps, dispatch N parallel sub-agents on non-overlapping territories, each with mandatory self-critique pass; consolidate findings as P1/P2/P3
8. **Baseline-Before-Change** — first step of any output-changing refactor is `git revert`-proof baseline capture
9. **Live Verification** — at least one live dry-run per tier; unit tests verify the code you wrote, live runs verify the data shapes you didn't anticipate
10. **Decision Log Format** — structured Context / Options Considered / Chose / Reasoning / Live-Verification / Residual Gaps / Reversibility / Trent-review-needed
11. **Handoff Chain Discipline** — versioned handoff files with Resume Command sufficient for fresh Claude session to pick up cold
12. **Invariants Tied to Tests** — convert every principle in SOUL.md into an invariant with a named test; principles rot, invariants don't
13. **Pre-Delivery Sweep ("Brett-Ready" sweep)** — 4 parallel agents sweep code correctness / security / UX / docs territories before client delivery
14. **Brand & Voice Rules** — no em-dashes in customer-facing copy, code comments, aria labels, or site metadata; direct/warm/specific
15. **Engagement Closure** — wrap criteria, archive protocol, case-study trigger via `process/case-study-template.md`

**Type A specifics** (when applicable): eval framework setup, hallucination prevention architecture, model selection rationale, prompt engineering rigor, NER gates / grounding checks if applicable.

**Type B specifics** (when applicable): design/UX rigor, front-end skill deployment (`frontend-design`, `web-design-patterns`, `shadcn-ui`, `frontend-taste`), Lighthouse gates if marketing site, responsive QA.

### Component 3 — `signal-works-internal/process/client-engagement-CLAUDE-template.md` (mandate snippet)

The CLAUDE.md content every new SignalWorks engagement project gets. Baked into new project CLAUDE.md by `/cook` Phase 2. Includes:

- **Session Start Protocol** — load order: SOUL.md, AGENTS.md, latest handoff, agent fleet, recent commits
- **Session-handoff mandate** — "Before ending any session — whether complete or interrupted — invoke the session-handoff skill. This is not optional."
- **Takeaways target line** — `signalworks_takeaways_target: /Users/t-rawww/signal-works-internal/takeaways/{client-slug}.md` — read by extended session-handoff skill to know where to append
- **Authority block template** — placeholder list to be filled at engagement kickoff
- **Reference to consulting-playbook.md** — pointer back to the methodology

Existing `brett-gove-intell/CLAUDE.md` becomes the reference implementation; the template is essentially the generalizable subset of it.

### Component 4 — Extended `~/.claude/skills/session-handoff/SKILL.md`

Edit the existing user-level skill to add a new step in its workflow:

1. **Detect SignalWorks project** — read project CLAUDE.md; look for `signalworks_takeaways_target:` line. If absent, skill behaves exactly as today (no SignalWorks-specific impact on non-SignalWorks projects).
2. **In-session extraction** — when target is present, the skill prompts Claude (in-session, free) to identify transferable workflow patterns from the current session, formatted as Pattern → Evidence → Transfer rule entries.
3. **"Transferable rule" gate** — only entries with a clear transferable rule get appended. If nothing qualifies, write nothing (avoid noise).
4. **Append + auto-commit + auto-push** — append to the target file in `signal-works-internal`. Then:
   - `cd /Users/t-rawww/signal-works-internal && git pull --rebase` (mandatory per signal-works-internal CLAUDE.md collaboration rules)
   - `git add takeaways/{slug}.md && git commit -m "takeaways({slug}): N entries from {date} session"`
   - `git push`
5. **Failure handling** — if any git step fails (network, merge conflict, etc.), the skill writes the takeaway content to a fallback path `signal-works-internal/takeaways/{slug}.md.pending` and surfaces the failure in the handoff doc with a manual-resolution note. Never blocks the handoff itself.

**Behavior on non-SignalWorks projects:** unchanged. The detect step short-circuits if no target line is present.

### Component 5 — Patched `~/.claude/skills/cook/SKILL.md`

Two patches to `/cook`:

**Patch A — Phase 1 routing addition.** Add classification "SignalWorks consulting engagement" to Phase 1. When matched, route to `AI-Knowledgebase/future-reference/playbooks/signalworks-consulting.md` (alongside any other matching playbooks like `building-ai-agents.md`). Same one-line addition pattern as existing routing.

**Patch B — Phase 2 skill deployment + CLAUDE.md mandate baking.** Phase 2 (Harness Design) gains two responsibilities:
- **Skill deployment fix:** consult the project classification → deploy classification-appropriate skills into `{new-project}/.claude/skills/` (e.g., a Type B engagement with UI components gets `frontend-design`, `web-design-patterns`, `shadcn-ui`, `frontend-taste`; a Type A engagement gets `eval-harness`, `cost-aware-llm-pipeline`, etc.). The deployment is a copy from `~/.claude/skills/{skill-name}/` into `{new-project}/.claude/skills/{skill-name}/`.
- **CLAUDE.md mandate baking:** for SignalWorks engagements, copy the `client-engagement-CLAUDE-template.md` content into the new project's CLAUDE.md, with `{client-slug}` substituted into the `signalworks_takeaways_target` line.

### Component 6 (deferred 2-3 weeks) — `/harvest-takeaways` skill

Manual invocation, weekly cadence. Reads `signal-works-internal/takeaways/*.md`, deduplicates entries, ranks by recurrence across engagements. Proposes promotions:

- **Pattern repeats across 2+ engagements** → propose promotion to `consulting-playbook.md`
- **Pattern is universally evergreen (not consulting-specific)** → propose promotion to existing KB doc (`agentic-engineering.md`, `magnum-opus.md`)
- **Pattern is `/cook`-shaped (changes scaffolding behavior)** → propose patch to `/cook` itself

User approves/rejects each proposal; the skill applies approved ones with commits.

**Why deferred:** without a 2-3 week corpus of takeaways across multiple engagements, harvest has nothing to dedupe or rank. Building it sooner means harvesting an empty room.

## Migration plan (existing `brett-gove-intell` content)

**Don't migrate.** Per Trent's preference, the existing `brett-gove-intell/docs/workflow-notes/session-takeaways.md` stays in place because Trent still has things to add there during the project's wind-down.

**Do copy** the existing content into the new `signal-works-internal/takeaways/brett-roberts-la-metro.md` as the day-1 seed. From this point forward, the extended session-handoff skill writes new entries to BOTH files (the existing per-project file remains the project-local copy; the new SignalWorks-internal file is the durable canonical copy that survives project archival).

After Brett engagement wraps, the per-project file becomes a frozen historical artifact; the SignalWorks-internal file remains the live source.

## Critical-review notes

1. **Git collision risk on `signal-works-internal`** — co-owned with Jahleel; concurrent edits possible. Mitigation: extended session-handoff always does `git pull --rebase` immediately before append, then `git push` immediately after. If rebase or push fails, fallback to `.pending` file (Component 4 step 5).

2. **`signalworks_takeaways_target` is project-bound, not session-bound** — the target file is determined by which project repo Claude is running in. If Trent works on two SignalWorks engagements in the same session (rare), only one would receive takeaways. Acceptable trade for v1.

3. **Skill resolution conflict** — `brett-gove-intell/.claude/skills/session-handoff/SKILL.md` exists and overrides user-level. Need to either delete the project copy or update both. Brett project is almost done so this is moot for the canonical project; for new engagements, `/cook` Phase 2 should NOT copy the user-level session-handoff skill into `.claude/skills/` (let the user-level version run).

4. **Day-1 seed content quality** — the patterns extracted from `brett-gove-intell` handoffs are high-signal but represent one engagement's experience. Risk of overfitting the playbook to Brett-style work. Mitigation: explicitly mark each seeded pattern with provenance ("first observed in: brett-roberts-la-metro, 2026-04") so future-Trent can spot patterns that don't generalize.

5. **Type A vs Type B branching adds complexity** — the consulting playbook becomes longer because of the type-specific subsections. Mitigation: structure the playbook with universal sections at top, type-specific sections clearly demarcated below. If a section grows past ~500 lines, split into sub-files.

6. **Harvest deferred but not forgotten** — Component 6 is the actual compounding mechanism. Set a calendar reminder for 2-3 weeks out to evaluate corpus and build harvest skill.

7. **Brand-rule duplication** — voice rules ("no em-dashes") exist in `signal-works-internal/CLAUDE.md` line 39, in `brett-gove-intell/CLAUDE.md` line 60, and would also live in `consulting-playbook.md`. Three copies invite drift. Mitigation: `consulting-playbook.md` references signal-works-internal/CLAUDE.md as canonical; per-project CLAUDE.md inherits the rule by reference.

## Open questions / followups

- **Harvest cadence and triggers:** Weekly cron? Manual `/harvest-takeaways`? On every Nth append? Defer to v1.5 design.
- **Cross-engagement pattern detection:** does harvest do pure dedup, or does it also surface "this engagement re-invented a pattern that exists in another"? Defer.
- **`/cook` Phase 2 skill deployment registry:** which skills correspond to which classifications? Build a small mapping table in `/cook` itself, or extract to a config file? Likely inline table for v1, extract if it grows.
- **What about `signal-works-personal`?** Personal SignalWorks brainstorming workspace. Not in scope for takeaways v1; brainstorms there are pre-engagement, not session-takeaways.

## Implementation order (high-level — detailed plan to come from planning skill)

1. Create `signal-works-internal/takeaways/` folder.
2. Copy `brett-gove-intell/docs/workflow-notes/session-takeaways.md` content into `signal-works-internal/takeaways/brett-roberts-la-metro.md` as day-1 seed.
3. Write `AI-Knowledgebase/future-reference/playbooks/signalworks-consulting.md` with the 15 seeded sections + Type A/B branching.
4. Write `signal-works-internal/process/client-engagement-CLAUDE-template.md` extracted from `brett-gove-intell/CLAUDE.md`.
5. Edit `~/.claude/skills/session-handoff/SKILL.md` to add the SignalWorks detection + extraction + auto-commit logic.
6. Patch `~/.claude/skills/cook/SKILL.md` Phase 1 (routing) and Phase 2 (skill deployment + CLAUDE.md baking).
7. Test end-to-end: simulate session-end on `brett-gove-intell`, verify takeaways append to both files and auto-commit.
8. Update `MEMORY.md` index entries for the new system.
9. Commit all changes.

## Success criteria

- After v1 ships, ending any session in `brett-gove-intell` automatically appends qualifying takeaways to `signal-works-internal/takeaways/brett-roberts-la-metro.md` with auto-commit, no manual prompting required.
- Running `/cook` for a new SignalWorks engagement produces a project scaffold with: (a) CLAUDE.md containing the mandate snippet + correct `signalworks_takeaways_target` path; (b) classification-appropriate skills deployed into `.claude/skills/`; (c) `consulting-playbook.md` consulted during Phase 1.
- The `consulting-playbook.md` exists, is seeded with 15 sections of working methodology, and feels at least as effective as Magnum Opus when applied to a consulting engagement.
- Non-SignalWorks projects are unaffected — extended session-handoff short-circuits when no `signalworks_takeaways_target` line is present.
