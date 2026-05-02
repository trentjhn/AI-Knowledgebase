---
name: decision-log
description: Append a structured entry to the project's decision log when making a substantive trade-off, irreversible-ish action, or constraint that future work shouldn't re-litigate. Captures WHY-this-not-others over time, separate from handoffs (which capture state at a moment) and git history (which captures what changed).
---

# Decision Log

## Why this exists

Three artifacts capture different layers of project memory:

| Artifact | Captures | Granularity |
|---|---|---|
| Git history | What code changed | Per commit |
| Handoff | State at a phase boundary | Per phase |
| **Decision log** | **Why this option, not the others** | **Per decision** |

Code shows the *current* state. Git history shows *what* changed. Neither captures *the reasoning trail*. Six months from now, when someone (you or a future Claude session) asks "why didn't we fork aeo-radar?" or "why N=5 not N=10?" — the answer should be a 1-line decision log entry, not a re-derivation.

## When to invoke

Append a decision log entry when:

- A substantive trade-off is made between two or more real options
- An irreversible-ish action is taken (schema migration, dependency lock-in, vendor commitment)
- A pivot or correction happens mid-build ("Path B over A or C")
- A constraint is locked in that future work shouldn't reopen
- An autonomous decision is made under the project's authority block (per consulting playbook §10)

**Skip for trivial / reversible choices** — variable names, file organization within established patterns, formatting. The decision log should stay readable; logging every micro-choice creates noise.

## Format

Append to the decision log file using this structure:

```markdown
## YYYY-MM-DD HH:MM — [Short title, ≤8 words]

**Context:** [what triggered the decision — 1-2 sentences]
**Options considered:** [list each, briefly]
**Chose:** [the option taken]
**Reasoning:** [why this, not the others — the load-bearing insight or constraint]
**Reversibility:** [reversible / hard-to-reverse / irreversible]
**Operator review needed:** [yes / no]
```

## Where it lives

| Project type | Path |
|---|---|
| Personal builds | `.sessions/decision-log.md` (gitignored — operator-side) |
| SignalWorks engagements | `.sessions/handoffs/decision-log-{YYYY-MM-DD}.md` per consulting playbook §10 |

For SignalWorks engagements, a fresh decision-log file per session is the established norm. For personal builds, a single append-only file works fine.

## Workflow

1. **Trigger fires** — you're about to make a substantive decision.
2. **Write the entry first, code second.** This forces explicit articulation of the trade-off before commitment.
3. **Append-only.** Never edit prior entries. If a decision is reversed later, write a new entry referencing the old one.
4. **Search before deciding.** When about to make a similar choice, grep prior log entries for related decisions. Coherence across the project depends on it.
5. **Surface in handoffs.** The handoff's "Key Decisions" section pulls from the most recent N decision log entries. The handoff cites; the decision log is durable.

## Output checklist

Each entry must answer five questions; if any are weak, rewrite:

- [ ] **What was decided?** (Title + Chose lines)
- [ ] **Why was a decision needed?** (Context line)
- [ ] **What were the alternatives?** (Options considered)
- [ ] **Why this option, not the others?** (Reasoning — the load-bearing why)
- [ ] **What does it commit us to?** (Reversibility)

If the entry doesn't make these answerable in 30 seconds of reading, it failed its purpose.

## Examples

```markdown
## 2026-05-02 11:30 — Greenfield over fork

**Context:** Spec said fork hellowalt/aeo-radar. Live inventory of the repo showed it uses SQLite + Playwright stealth scraping + CLI structure — not the Postgres + Next.js + API-direct stack the spec specifies.
**Options considered:**
  A. Fork-and-strip-rebuild (3+ hours of demolition before any new code)
  B. Greenfield with selective port (zero demolition, port specific patterns)
  C. Fork-as-reference, build-fresh in same repo (squash + rebuild)
**Chose:** B
**Reasoning:** aeo-radar's stack contradicts spec on every major axis (DB, frontend, engine approach). Code-level transferability is <20%, not 60%. Greenfield avoids demolition; MIT attribution via THIRD-PARTY-NOTICES.md handles licensing without git lineage.
**Reversibility:** Reversible (can fork later if pattern transfer becomes valuable)
**Operator review needed:** No (locked at scaffold, captured in design.md)
```

```markdown
## 2026-05-02 14:15 — v1 ships 3 engines, not 5

**Context:** Path A required ~$135 upfront across 5 engines. Path B (3 engines) is $10 upfront with no recurring cost.
**Options considered:**
  A. All 5 engines ($135 upfront + $75/mo SerpAPI subscription)
  B. 3 engines (ChatGPT, Claude, Gemini — $10 upfront, $0 recurring)
  C. 4 engines (skip SerpAPI only — $60 upfront, $0 recurring)
**Chose:** B
**Reasoning:** Operator wants to validate the methodology and one Casamate baseline before committing to recurring spend. v2 roadmap path is open: re-enable Perplexity + AI Overview by editing `lib/engines/index.ts ALL_ENGINES`. Methodology page honestly says "3 engines in v1; Perplexity + AI Overview in v2."
**Reversibility:** Reversible (one-line edit to ALL_ENGINES + add API key)
**Operator review needed:** No (within authority block; captured in design.md Locked Decisions #2)
```

## Anti-patterns

- **One-line entries.** "Decided to use Postgres" is not a decision log entry; it's a tweet. Use the 6-field format every time.
- **Decisions without alternatives.** If you can't name two real options, you weren't really deciding.
- **Backdated entries.** Decision log is append-only and timestamped at the moment of decision. Backdating breaks the trail's integrity.
- **Logging non-decisions.** "Used the standard naming convention" isn't a decision; it's just doing the default. Log only when there was a real choice.
