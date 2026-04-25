# Audit Protocol

**Purpose:** Canonical playbook for multi-agent audit sweeps in SignalWorks engagements. Referenced by every project's `CLAUDE.md` Session End Protocol. Lives at `docs/audit-protocol.md` in scaffolded projects.

## When to run

- **Session-end** — mandatory before invoking `session-handoff` skill
- **Pre-tier-ship** — mandatory before declaring any tier complete in multi-tier work (see consulting playbook §6)
- **Pre-delivery** — mandatory before sharing any client-facing artifact (URL, dashboard, email, deployable)

## How many agents

Default: **4 parallel sub-agents** on non-overlapping territories. Optional 5th territory based on engagement type:
- Type A: add a "model behavior" agent for AI deliverables
- Type B with high traffic: add a "performance" agent
- Engagements with regulated data: add a "compliance" agent

## Default 4 territories

| Territory | Prompt template | Tag prefix |
|---|---|---|
| Code correctness + error handling | `docs/prompts/audits/code-correctness.md` | `CORR-NNN` |
| Security + secrets + external access | `docs/prompts/audits/security.md` | `SEC-NNN` |
| UX + content + delivery | `docs/prompts/audits/ux-delivery.md` | `UX-N` |
| Docs + runbook + onboarding | `docs/prompts/audits/docs-operations.md` | `DOC-N` |

## Self-critique mandate (non-negotiable)

Every audit prompt ends with:

> "After your initial sweep, spend a second pass looking for what you might have missed. Specifically check: [4-5 meta-questions calibrated to territory]. Don't assume your first pass is complete."

The self-critique pass consistently surfaces findings the initial sweep missed — different cognitive mode (gap-driven vs hypothesis-driven). This is THE highest-leverage discipline in the audit protocol.

**Provenance:** brett-roberts-la-metro 2026-04 — SEC-016 (spacy hash-pinning), CORR-028 (double `reset --hard`), UX-9 (h1 screen-reader) all came from self-critique passes.

## Output format (every agent)

```
## P1 (blocks ship)
- [TAG-NNN] description | file:line | fix shape | effort | reversibility

## P2 (fix before client share)
- [TAG-NNN] ...

## P3 (polish, post-launch)
- [TAG-NNN] ...
```

Each finding includes:
- **Tag**: prefix per territory (CORR/SEC/UX/DOC) + 3-digit number
- **Description**: 1-2 sentences, specific
- **File:line**: exact location
- **Fix shape**: one-line summary of the proposed fix
- **Effort**: rough time estimate (5min / 30min / 2h / 1d)
- **Reversibility**: low / moderate / high

## Length budget per agent

- Code, Security, UX agents: **1500 words**
- Docs/structural agent: **900 words**

Over-budget responses get truncated. Under-budget is fine if territory is genuinely small.

## Consolidation step (operator does this after agents return)

1. **Dedupe** across agents — same finding may appear under multiple tags.
2. **Triage by cohort** before severity (consulting playbook §8):
   - Cohort 1 (no re-run needed): type fixes, redaction, test additions, doc refresh, template cosmetics. Batch into one commit cycle.
   - Cohort 2 (re-run needed): prompt revisions, model migrations, schema changes. Batch into dedicated next-phase cycle.
   - Severity sorts WITHIN each cohort, not across.
3. **Ship P1 fixes in-session** — don't defer.
4. **Log P2/P3 in handoff's "Audit Directions for Next Session" slot** — so the next session's audit starts warm with priors, not cold.

## Audit prompt structure (every territory uses this)

Each `docs/prompts/audits/{territory}.md` follows this structure:

1. **Project context placeholder** — `{{PROJECT_CONTEXT}}` (filled at dispatch with: what this system does, who the end client is, what they care about, current tier/phase)
2. **Slice** — `{{SLICE}}` (which files / which territory boundary; non-overlapping with sibling agents)
3. **Known priors** — `{{KNOWN_PRIORS}}` (past findings to avoid rediscovering; lifted from prior handoff's Audit Directions slot)
4. **Hunt categories** — territory-specific list of failure modes to look for
5. **Output format** — copy of the format above with the territory's tag prefix pre-filled
6. **Self-critique mandate** — 4-5 meta-questions specific to the territory
7. **Length budget** — 1500 or 900 per spec above

## When NOT to run

- Solo refactor with no behavioral change (just lint + tests)
- Doc-only PR
- Single-line bug fix with regression test

When in doubt: run it. The cost of running a 4-agent audit is ~5-10 min wall-clock + sub-agent context cost. The cost of skipping one and shipping a P1 to the client is much higher.

## Reusing prior audit context

Each handoff carries forward an `## Audit Directions for Next Session` slot. The next session's audit dispatch fills `{{KNOWN_PRIORS}}` from that slot — so the next sweep doesn't rediscover what the prior sweep already found.

## Provenance

Pattern proven on brett-roberts-la-metro 2026-04 across two sweeps:
- **Tier 3 audit** — 4 parallel sub-agents on Metro items 1-5 / 6-10 / 11-15 / Inglewood + structural. 16/16 items zero invented specifics.
- **Tier 3.5 Brett-ready sweep** — 4 parallel agents on code correctness / security / UX / docs + self-critique. 40+ findings logged, P1 fixes shipped in-session.

Net effect: the audit becomes the default path. Operator would have to deliberately bypass the CLAUDE.md Session End Protocol to NOT run one.
