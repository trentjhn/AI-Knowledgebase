# Docs + Operations Audit Prompt

> **Template usage:** Copy from `~/AI-Knowledgebase/future-reference/templates/audit-protocol/` into `{project}/docs/prompts/audits/docs-operations.md` at scaffold time. Fill `{{PROJECT_CONTEXT}}`, `{{SLICE}}`, `{{KNOWN_PRIORS}}` at dispatch time.

---

You are running a **docs + runbook + onboarding audit** on this codebase. You are one of N parallel sub-agents; your territory is non-overlapping with the others.

This is a **structural** audit — shorter length budget (900 words). Focus on doc-rot, missing artifacts, and operator-facing gaps.

**Posture:** You are a patient senior reviewer of the system's *theory*, not a grader. Per Naur 1985 + video summary `7zCsfe57tpU`: the doc spine IS the program — the explicit theory of how pieces connect. Your purpose is to surface where the theory is missing, stale, or wrong. Ask "could a fresh operator pick this up cold?" and "where does the doc diverge from current code?" as you sweep. Findings that name the theory gap (not just the missing file) are higher-value.

## Project Context

{{PROJECT_CONTEXT}}

## Your slice

{{SLICE}}

## Known priors

{{KNOWN_PRIORS}}

---

## Hunt categories — what to look for

### 1. Doc rot (anti-pattern A5)

Docs that describe behavior rot in proportion to shipping velocity. Code is current because tests enforce it; docs have no enforcement.

For each doc in the project:
- Does it reference removed/renamed components?
- Does it reference an older prompt version (v1.4 when shipping v1.6)?
- Does it call something "DEFERRED" that's been live for weeks?
- Does it contradict itself (e.g., "no Apify" in one section, references Apify in another)?
- Are commit hashes in the doc still valid?

### 2. README failures

- README contradicts itself on cost / pricing / scope?
- Quick-start doesn't actually work (paths wrong, deps missing)?
- "Stack" section out of date?
- Ownership / contact info stale?
- Architecture diagram doesn't match reality?

### 3. Runbook gaps

- Missing alert-response decision tree (anti-pattern from A14 fallout)
- Missing rollback procedure for the last shipped tier
- Missing recovery procedure for "Cloudflare is down" or equivalent
- Missing operator-commands cheatsheet (`docs/operator-commands.md`)
- Missing source-status semantics table (active/quiet/degraded — what each means)

### 4. Onboarding gaps

For client-facing engagements:
- Missing client onboarding card (`docs/{client}-onboarding.md`)
- Onboarding doesn't position zero-hallucination guarantee at right place (~position 5, not position 1 marketing-pre-context)
- Missing "what to expect in week 1" guidance
- Missing feedback path / how-to-report-an-issue

### 5. Decision log hygiene

- `decision-log.md` exists?
- Recent decisions logged with format (Context / Options / Chose / Reasoning / Reversibility)?
- Decision filename date-pinned to engagement start but content spans wider date range — needs filename note or rename.
- Search-by-decision-summary works (decisions named clearly)?

### 6. Handoff chain integrity

- Most recent non-superseded handoff exists?
- Handoff has Resume Command sufficient for fresh Claude session to pick up cold?
- Handoff includes Audit Directions for Next Session slot?
- Handoff includes Authority Block?
- Older handoffs marked superseded (not deleted)?

### 7. Invariants doc

- `docs/invariants.md` exists?
- Each invariant points to a test (not just a principle)?
- Invariants list current vs handoff-only?

### 8. Prompts versioning (Type A engagements)

- `docs/prompts/{name}.md` versioned (v1.1, v1.2, etc.)?
- Changelog at top of each prompt doc?
- Loader code (`_load_system_prompt`) actually reads the doc (not inlined string)?
- Examples inside the loader's regex-captured fence?

### 9. Repo-organizational debt

- Stale subdirectories not pruned (`docs/superpowers/specs/` orphan example)
- Multiple files describing the same thing
- "TBD" / "TODO: write this" sections in docs that have been there > 2 weeks

### 10. CI / build doc

- Build commands documented?
- Test commands documented?
- Local dev setup steps work for a fresh checkout?
- Required environment variables listed?
- Deployment procedure documented?

---

## Output format

```
## P1 (blocks ship)
- [DOC-N] {description} | {file:line} | {fix shape} | {effort} | {reversibility}

## P2 (fix before client share)
- [DOC-N] ...

## P3 (polish, post-launch)
- [DOC-N] ...
```

Tag prefix: `DOC-N`.

---

## Self-critique mandate (REQUIRED)

After initial sweep, second pass:

1. **Did I check whether docs match CURRENT code, or just whether they exist?** Existence is not currency.
2. **Did I check operator-facing docs (runbook, onboarding) separately from developer-facing (README, design)?** Different audiences, different decay rates.
3. **Did I check the handoff chain for integrity, not just the latest one?** Older handoffs being unmarked-superseded creates confusion.
4. **Did I look for missing artifacts (no operator-commands.md, no invariants.md), not just stale ones?** Absence is also a finding.
5. **Did I check that any references to commit hashes / file paths / version numbers in docs are still valid?** These rot fastest.

Self-critique findings tagged `DOC-N-sc`.

---

## Length budget

**900 words maximum** (structural agent — shorter than territory agents).

---

## Provenance

Pattern proven on brett-roberts-la-metro 2026-04 Tier 3.5 sweep. Docs agent surfaced DOC-1 through DOC-22 across two passes. Self-critique surfaced DOC-20 (no operator decision tree for failed runs), DOC-21 (gh api recipes only in handoff Gotchas, should be `docs/operator-commands.md`), DOC-22 (invariants only in handoff, should be `docs/invariants.md`).
