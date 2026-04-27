# SignalWorks Consulting Playbook

**Purpose:** Methodology for running a SignalWorks AI consulting engagement end-to-end. More opinionated than `magnum-opus.md` (its sibling in this playbooks folder) — assumes you are doing client work, not personal experiments.

**Location:** `/Users/t-rawww/AI-Knowledgebase/future-reference/playbooks/signalworks-consulting.md` — lives alongside other KB playbooks (`building-ai-agents.md`, `building-rag-pipelines.md`, `magnum-opus.md`, etc.) so `/cook` reads it from the same path conventions.

**Read by:** `/cook` Phase 1 when classification matches "SignalWorks consulting engagement." Read by Trent Johnson and Jahleel Heath at engagement kickoff. Referenced by every SignalWorks project's `CLAUDE.md`.

**Updates:** Patterns flow into this playbook from two sources:
1. Manual integration during engagement post-mortems.
2. The `/harvest-takeaways` skill (deferred 2-3 weeks after takeaways system ships) — promotes patterns from `signal-works-internal/takeaways/*.md` when patterns repeat across 2+ engagements.

**Provenance discipline:** Each section seeded from an existing engagement carries a provenance tag (e.g., `Provenance: brett-roberts-la-metro, 2026-04`). Patterns confirmed across 2+ engagements upgrade to "Confirmed: {engagement-A}, {engagement-B}". Patterns never confirmed beyond their origin should be re-evaluated for SignalWorks-wide applicability vs. one-engagement-only.

**Version:** v1 (2026-04-24) — initial seed from brett-roberts-la-metro engagement.

---

# Part 1 — Universal Sections (apply to all SignalWorks engagements)

---

## Section 1: Engagement Discovery

The first hour with a new client determines whether the rest of the engagement is well-scoped or chaotic. Discovery is not about closing — it's about producing a written, mutually-agreed scope before any code or content gets written.

**Required outputs of discovery:**

1. **Problem statement** — one paragraph in the client's own words, captured verbatim during the call. Re-read it back to them; iterate until they say "yes, that's it." This statement becomes the success-criterion anchor.
2. **Deliverable description** — what they will see and use at end-of-engagement. Be concrete: a URL? An email? A dashboard? An automation that runs daily? A set of trained models?
3. **Out-of-scope list** — at least 3 things explicitly excluded. Vague scope at start = scope creep mid-engagement. Examples: "no email delivery," "no client-side analytics," "v1 is single-user only," "no third-party scraping."
4. **Timeline + budget envelope** — duration in weeks, hard end-date if any, fixed-price vs hourly, payment milestones.
5. **Success criteria** — how does the client decide it worked? Numeric where possible: "Brett opens the dashboard 3+ days/week for 2+ months." "False positive rate under 5%." "Page load under 2s mobile."
6. **Authority negotiation** — see Section 3.
7. **Type classification** — Type A (AI deliverable) or Type B (AI-accelerated build). See Section 2.

**Anti-pattern: under-specifying out-of-scope.** Clients expand scope through micro-asks ("could it also..."). If out-of-scope wasn't named at kickoff, every micro-ask becomes a small yes. Cumulative cost: 30% over budget. Solution: name 3+ things explicitly out at kickoff. Add to `docs/plans/design.md` as "## Out of Scope" section.

**Discovery output lives at:** `docs/plans/design.md` (Engagement Discovery section). Updated only via decision-log entries — never silently rewritten.

---

## Section 1.5: Three Questions That Must Be Answerable Without Running Code

Per Peter Naur's 1985 paper "Programming as Theory Building" (revisited in modern systems-thinking discourse): the *program* is the mental model in the operator's head; the *code* is its shadow. AI generates the shadow on demand, but the theory must be deliberately built. These three questions surface the theory before code is written:

1. **Where does state live?** (Who owns the truth in the system? Database / files / external service / in-memory cache / multiple distributed locations?)
2. **Where does feedback live?** (How do we know the system is working? Logs / metrics / alerts / dashboards / user feedback / silent until broken?)
3. **What breaks if I delete this?** (For every non-trivial component: blast radius. Everything fails / one feature degrades / silent wrong-answer / data corruption?)

**When to ask these questions:**
- **At engagement kickoff** (Phase 0.6 discovery in `/cook`) — forces architectural answers BEFORE code.
- **At every tier-ship gate** (Section 6 below) — re-asked for each tier's surface area.
- **In every code-correctness audit sweep** — agents flag if the answers can't be derived from current docs/code.
- **Before deleting or refactoring any component** — operator can answer "what breaks?" without running tests.

**Why this matters for SignalWorks engagements specifically:** client work has higher reversibility cost than personal experiments. A wrong-answer-at-scale is expensive in client trust. These three questions surface the architectural facts that make blast radius bounded and recovery possible.

**Provenance:** Naur 1985 + video summary `7zCsfe57tpU` on systems thinking, integrated 2026-04-25.

---

## Section 2: Type Classification — Type A vs Type B

Before any architecture work, classify the engagement. The classification routes which sub-sections apply (Part 2 vs Part 3 of this playbook).

**Type A: AI Deliverable.** The AI workflow/automation IS the product the client is paying for. The AI's behavior and quality is the value. Examples:
- AI-summarized governance digest (brett-roberts-la-metro)
- LLM-powered customer support automation
- Document intelligence pipeline (intake → classify → route → respond)
- Lead-generation agent that researches prospects autonomously

If Type A → apply **Part 2: Type A Specifics** (eval framework, hallucination prevention, model selection, prompt rigor, AI security).

**Type B: AI-Accelerated Build.** AI coding agents help you build a deliverable that is not itself an AI product. The AI is the toolkit, not the product. Examples:
- Marketing site for a non-AI company built with Claude Code
- Operational dashboard with no LLM in the data path
- Custom internal tool for a non-AI workflow
- Automation that uses AI for reasoning during development but ships as deterministic code

If Type B → apply **Part 3: Type B Specifics** (design/UX rigor, front-end skill deployment, responsive QA, performance, verification loop).

**Hybrid engagements** (rare but real) — when a project has both an AI deliverable AND a substantial non-AI surface (e.g., the brett-roberts-la-metro engagement is Type A for the summarization pipeline AND Type B for the dashboard UX). Apply both parts. Type A's eval rigor on the pipeline; Type B's design rigor on the dashboard. Don't conflate them.

**Decision flowchart:**

```
Will the AI's behavior at runtime be visible to the end user?
├── YES → at least partially Type A. Apply Part 2.
└── NO  → apply Part 3.

Is there a non-trivial human-facing UI surface?
├── YES → at least partially Type B. Apply Part 3.
└── NO  → Type A only.
```

**Classify out loud at kickoff.** Document the classification in `docs/plans/design.md` so future operators don't have to re-derive it.

---

## Section 3: Authority Block Setup

The authority block converts fuzzy "use good judgment" into an explicit checklist. Without it, Claude either stops-and-asks every 3 decisions (slow, frustrating to operator) or moves too fast and crosses a locked constraint (bad, expensive to undo). Define it AT KICKOFF, with the client.

**Decide autonomously: section** — items where Claude can execute without pause:
- Scraper/integration selector updates within an existing target
- Sub-agent feedback interpretation
- Edge cases not covered by locked decisions
- Prompt/test tweaks within locked architectural envelope
- Error-message wording, log-line wording
- Tie-breaking when two reversible options exist (pick more reversible, log reason)
- Uncovering deferred items mid-build (defer to handoff, don't expand scope mid-session)

**Pause for {operator}: section** — items requiring explicit human approval:
- Physical UI tasks (account creation, token generation, sending client emails)
- Irreversible actions (`git push --force`, deleting state, dropping tables, rotating live credentials, archiving repos)
- Client-specific preferences not yet documented (voice, naming, content choices)
- Client-facing product changes not covered by locked decisions
- Test suite failing after 2 fix attempts (root cause > brute force)
- Crossing a locked decision

**Reversibility test for autonomous decisions:**
> "Is this reversible? Is it crossing a locked decision? If no + no → proceed."

### Jagged Frontier — what NOT to delegate (even within autonomous authority)

Per the "jagged frontier" concept from Harvard researchers (re-surfaced in systems-thinking discourse): AI is sharp in some areas and surprisingly dull in others, often within the same session. Authority to decide ≠ capability to decide well. Some decisions belong with the operator regardless of authority block, because the LLM lacks the holistic reasoning to make them safely:

- **Novel-domain architectural decisions** — when there are no priors in training data to draw from, LLM extrapolation is brittle.
- **Security-critical algorithm choices** — probabilistic output is unsafe when a single wrong choice opens an attack surface (crypto primitives, auth flows, access control logic).
- **State machine design** — correctness requires holistic invariant reasoning across all transitions; LLMs reason locally and miss invariants.
- **Irreversible operations on production systems** — financial transactions, deletions, schema migrations, public-facing announcements. Probabilistic acceptable elsewhere; not here.
- **Cross-system contracts where the LLM hasn't seen the full picture** — API design, data format definitions, versioning schemes. The contract has to fit a system the LLM doesn't fully see.
- **Anything where probabilistic behavior could compound into wrong-answer-at-scale** — financial calcs, medical recommendations, legal interpretations.

**Treatment:** these don't go in the autonomous authority list. They go in the pause-for-operator list with explicit reasoning ("Claude lacks holistic invariant reasoning for state machine correctness"). Operator may still consult Claude for input — just doesn't delegate the decision.

**Provenance:** Naur framing + jagged frontier (Harvard) + video summary `7zCsfe57tpU`, integrated 2026-04-25.

**Refinement during engagement.** When Claude encounters an edge case, the answer might be:
- (a) Add it to "decide autonomously" with rationale → log to decision log
- (b) Add it to "pause for {operator}" → log + edit CLAUDE.md
- (c) The category itself is wrong → re-negotiate with operator

Authority block is a living document. Edit it when reality demands. Never drift silently.

**Provenance:** brett-roberts-la-metro, 2026-04 — proven across 8+ handoffs (v3-v7-final).

---

## Section 4: Source-of-Truth Doc Spine

**These docs are not bureaucracy. They are the *theory of the system*** — the program in the operator's head, made explicit and shareable. Per Peter Naur's 1985 paper "Programming as Theory Building," the program is the mental model of how pieces connect; the code is merely its shadow. AI-era engagements require the theory to be explicit and shared, not implicit and trapped in one person's memory. When the theory lives in the doc spine, any operator (or fresh Claude session) can pick up cold. When it lives only in someone's head, the engagement dies if that person leaves.

Every SignalWorks engagement maintains the same six-doc spine. Do not deviate. New operators expect this layout.

1. **`SOUL.md`** — character, voice, values. Non-negotiable rules ("cite sources," "no em dashes," "zero hallucinated items"). ~60 lines. Loaded at session start.
2. **`CLAUDE.md`** — operating contract, generalized from `signal-works-internal/process/client-engagement-CLAUDE-template.md`. ~80-100 lines.
3. **`AGENTS.md`** — agent fleet + role directory. Which agent owns which phase. ~60 lines.
4. **`docs/plans/design.md`** — architectural decisions with rationale (ADRs inline). Updated via decision-log entries.
5. **`docs/plans/implementation.md`** — ordered build plan with `**Agent:**` annotations per step.
6. **`.sessions/handoffs/`** — versioned session continuity. Format: `handoff-YYYY-MM-DD-vN.md`. Most recent non-superseded file is authoritative.
7. **`.sessions/handoffs/decision-log-YYYY-MM-DD.md`** — flat chronology of autonomous + required decisions.

**Optional, by engagement type:**
- `docs/prompts/{name}.md` — versioned system prompts (Type A only)
- `docs/audit-protocol.md` + `docs/prompts/audits/` — reusable audit templates (see Section 7)
- `docs/runbook.md` — operator runbook for production systems
- `docs/{client}-onboarding.md` — first-week orientation card for end client

**Discipline rule:** No critical-path knowledge lives in conversation history alone. Anything load-bearing gets a doc in the spine or a decision-log entry.

---

## Section 5: CLAUDE.md Mandate

Every SignalWorks engagement's `CLAUDE.md` includes these mandates verbatim (or via reference to the template):

1. **Session Start Protocol** — load order: SOUL.md → AGENTS.md → latest handoff → agent fleet → recent commits. If handoff specifies "Next Session Invocations," honor those.
2. **`signalworks_takeaways_target:` line** with absolute path to the takeaways file — read by extended `session-handoff` skill.
3. **Mandate:** "Before ending any session — whether complete or interrupted — invoke the `session-handoff` skill. This is not optional." This is the trigger that activates auto-append-takeaways without manual prompting.
4. **Authority block** (Section 3 of this playbook).
5. **Reference back to this playbook** (this file).

The template at `signal-works-internal/process/client-engagement-CLAUDE-template.md` encodes all of this with `[FILL AT ENGAGEMENT KICKOFF: ...]` markers for the project-specific bits. `/cook` Phase 2.6 bakes the template into new project CLAUDE.md.

---

## Section 6: Tier-Based Shipping

Any ambitious-enough-to-scare-you refactor gets decomposed into 3-5 tiers where each tier individually could ship to production without the rest. If a tier can't ship alone, the decomposition is wrong — split further.

**Tier properties:**
- **Independent shippability** — Tier N must work in production without Tier N+1.
- **Distinct blast radius** — what Tier N can break is bounded.
- **Own commit checkpoint** — one commit (or commit chain) per tier.
- **Own rollback path** — `git revert <sha>` returns to Tier N-1 state.
- **Own test checkpoint** — pytest baseline must pass after Tier N before Tier N+1 starts.

**Example decomposition (brett-roberts-la-metro zero-hallucination architecture):**
- Tier 1: Lowest-risk structural change (verbatim `display_text`). Ship, test, baseline.
- Tier 2: Layer the next concern on top (NER gate). Ship, test, run live.
- Tier 3: Verify only, no new feature (4-agent audit).
- Tier 3.5: Unplanned — comprehensive sweep for everything else that would block the end client.

**When the Tier 3 audit surfaced that the "allow-list is why_relevant only" decision over-dropped 40/45 Metro items, reversing JUST that decision via a Tier 3 refinement was cheap — we didn't have to unpick Tier 1.** That's the test of correct decomposition: can you reverse a single tier's decisions without unraveling everything?

**Naming convention:** Tier 1, Tier 2, ... and Tier N.5 for unplanned mid-engagement work that emerges (Tier 3.5 was the "Brett-ready sweep" that wasn't in the original plan).

**Provenance:** brett-roberts-la-metro, 2026-04.

**Phase-numbered plans become commit-message scaffolding.** When implementation plans number phases (Phase 0, 1, ...), commits naturally adopt the numbering and `git log --oneline` becomes a phase-progression view. Default to numbered phases for all SignalWorks implementation plans, not bullet lists. Without numbering, commits either describe the change (good) but lose plan-trace, or reference the plan in prose (verbose) and bloat the log. Provenance: brett-roberts-la-metro v13→v14, 2026-04-25/26.

---

## Section 7: Multi-Agent Audit Discipline

For pre-delivery audits (and any major mid-engagement check), dispatch N parallel sub-agents on non-overlapping territories. Mandatory self-critique pass per agent. This is the highest-leverage practice in the SignalWorks toolkit.

**Default 4-agent audit:**
1. **Code correctness + error handling**
2. **Security + secrets + external access**
3. **UX + content + delivery**
4. **Docs + runbook + onboarding**

Optional 5th territory based on engagement (e.g., "model behavior" for Type A, "performance" for high-throughput systems).

**Self-critique mandate.** Every audit prompt ends with:

> "After your initial sweep, spend a second pass looking for what you might have missed. Specifically check: [4-5 meta-questions calibrated to territory]. Don't assume your first pass is complete."

The self-critique pass consistently surfaces findings the initial sweep missed (in brett-roberts-la-metro: SEC-016 spacy hash-pinning, CORR-028 double `reset --hard`, UX-9 h1 screen-reader issue all came from self-critique). Why: initial sweep is hypothesis-driven; self-critique is gap-driven. Two different cognitive modes.

**Output format (every agent):**

```
## P1 (blocks ship)
- [FINDING-ID] description | file:line | fix shape | effort | reversibility

## P2 (fix before client share)
- ...

## P3 (polish, post-launch)
- ...
```

**Consolidation step:**
1. Dedupe across agents.
2. Triage by "does the fix require a costly re-run?" before severity (Section 8).
3. Ship P1 fixes in-session.
4. Log P2/P3 in handoff's "Audit directions for next session" slot.

**Reusable prompt library** at `docs/prompts/audits/{code,security,ux,docs}.md`. Each is a fill-the-blanks template with `{{PROJECT_CONTEXT}}` / `{{SLICE}}` / `{{KNOWN_PRIORS}}` placeholders. Copy from the scaffolding repo on day 1.

**Trust-but-verify subagent factual claims with cheap independent checks before acting.** When a subagent makes a specific factual claim about production state, code state, or live data ("X is broken", "Y is missing", "Z is rendering wrong"), run a one-liner verification (`grep` / `curl` / `jq`) before changing anything in response. The cost is seconds; the cost of acting on a wrong claim is hours. Especially important with role-specialized agents that have only the slice of context their brief provided. Verification is cheap; rework is not. Provenance: brett-roberts-la-metro 2026-04-26 (5-agent post-launch sweep — one agent's confident claim about stale renderer output was disproven by a 2-line grep against the live HTML).

**Provenance:** brett-roberts-la-metro, 2026-04 — pattern run twice (Tier 3 + Tier 3.5), surfaced 40+ findings.

---

## Section 8: Triage Cohort Rule — "Re-run Required" vs "No Re-run"

When a multi-agent audit returns 15-20 findings, the first sort is NOT severity. It's:

> "Will verifying this fix require re-running the expensive pipeline (Gemini calls, CI deploy, state reset, model retraining)?"

**Cohort 1: No re-run needed.** Type fixes, security redaction, test additions, doc refresh, template cosmetics, sidebar math, lint. Batch into one commit cycle with a single live verification at the end.

**Cohort 2: Re-run needed.** Prompt revisions, banlist changes, grounding-rule changes, model migrations, schema changes. Batch into a dedicated next-phase cycle where each re-run is budgeted (10-15 min CI turnaround typical).

Severity sorts WITHIN each cohort. The cohort split is the primary axis.

**Why the cohort split matters:** mixing them means you either (a) ship a security fix gated behind an unverified prompt change, or (b) iterate prompts mid-sweep and lose the thread on both. Pre-Phase-3 hardening on brett-roberts-la-metro: 4-agent audit returned ~12 findings; 7 hit "no re-run needed" cohort and shipped in one commit with 18 new tests + one verification; 4 hit "re-run needed" cohort and became Phase 3 punch list. Two clean ship cycles instead of one muddled one.

**Provenance:** brett-roberts-la-metro, 2026-04.

---

## Section 9: Baseline-Before-Change

First step of any output-changing refactor: capture the pre-state baseline. If you can't snapshot the current output, you can't verify improvement.

**What to baseline:**
- Rendered HTML / production output → `dry_run_output/baseline_{date}_{version}.html`
- API response shapes → JSON dump
- Status / metadata → `status.json` snapshot
- Test suite output → `pytest -v` log
- Schema state → DDL dump

**Why critical:** without baseline, every before/after analysis becomes subjective. With one, the conversation moves from "does this feel worse?" to "is this delta accounted for?"

**Concrete:** brett-roberts-la-metro Tier 1 pulled v1.5 rendered HTML + status.json before shipping the verbatim-display-text change. Tier 3 agents referenced the baseline to answer "is this drop rate expected?" — 40→16 items went from alarming to justified once compared.

**Discipline:** baseline is `git revert`-proof. Don't store baselines in the same paths code overwrites. Use `dry_run_output/`, `baselines/`, or `.snapshots/` and gitignore as needed.

**Provenance:** brett-roberts-la-metro, 2026-04.

---

## Section 10: Decision Log Format

Every project gets a decision log. Every non-trivial decision (architecture, library, contract, prompt, scope change) gets an entry. Format:

```
## Decision: {one-line summary}
**Date:** YYYY-MM-DD
**Context:** What problem were we solving? What constraints?
**Options considered:** 1. {option A} 2. {option B} 3. {option C}
**Chose:** option N. Commit: {sha or "pending"}.
**Reasoning:** Why this option, why not the others?
**Live-verification:** Did we verify in production? How?
**Residual gaps:** What's still uncovered or risky?
**Reversibility:** low / moderate / high
**{Operator} review needed?** yes / no
```

**Cost:** ~10 min per decision.
**Payoff:** three months later, "why did we pick ±1% tolerance, not 5%?" has a canonical answer, not a Slack archaeology expedition.

**Meta-payoff:** the FORMAT itself forces sharper thinking. "Options considered" field means you stopped to generate more than one path before committing. "Reversibility" forces explicit risk acknowledgment.

**File path:** `.sessions/handoffs/decision-log-{date-engagement-started}.md`. One file per engagement, append-only, flat chronology.

**Provenance:** brett-roberts-la-metro, 2026-04 — proven across 14+ logged decisions.

---

## Section 11: Handoff Chain Discipline

Handoffs are state-of-the-world artifacts, not session diaries. Each version supersedes the previous; older versions are kept for audit trail.

**Required sections per handoff:**
- **Status** — what shipped this session, branch state, test count
- **What's Done** — completed items
- **What's In Progress** — current task with `file:line` of where you stopped
- **What's Pending** — next tasks with priority
- **Key Decisions Made** — links to decision log entries
- **Files Touched** — `path` — `what changed`
- **Verification Evidence** — test output, live-run links, audit results
- **Gotchas for Next Session** — non-obvious behavior discovered
- **Authority Block** (link to current version)
- **Invariants** (numbered, test-tied — see Section 12)
- **Audit Directions for Next Session** — priors for the next session's audit so it doesn't start cold
- **Resume Command** — self-contained prompt a fresh Claude session can paste to pick up cold

**The Resume Command is the litmus test.** If a fresh Claude session can't pick up from "read handoff-vN.md then continue," the handoff is incomplete.

**Naming:** `handoff-YYYY-MM-DD-vN.md`. Increment `v` per session even if same date. `v3-final.md` is acceptable for last-of-day.

**Triggers for new handoff:** session end (always), major tier ship (always), context window approaching limit, before/after risky operations.

**Provenance:** brett-roberts-la-metro, 2026-04 — proven across 8+ handoffs (v3 → v7-final).

---

## Section 12: Invariants Tied to Tests

Principles in `SOUL.md` rot. Invariants tied to tests don't.

**Wrong (principle):**
> "Silent failures are banned."

That principle didn't prevent Phase 3.2 from being broken for 3+ sessions on brett-roberts-la-metro.

**Right (invariant):**
> **Invariant 14:** Scraper failures render as `degraded`, not `quiet`. Enforced by `_ner_gate_item` + `_classify_source`. Tests: `TestClassifySource::test_degraded_when_scrape_failed`, `TestSummarizeAllPhase32`.

**Convert principles to invariants:** for each principle in `SOUL.md`, ask:
- Is this enforced by code or tests?
- If yes → write the invariant entry pointing to the enforcement.
- If no → either (a) write the test, or (b) downgrade the principle to "we aspire to this."

**Invariants list lives at:** `docs/invariants.md` or in the latest handoff. The list is the human-readable index into the test suite.

**Discipline:** after every major ship, audit `SOUL.md` principles. New principles added without enforcement are debt.

**Provenance:** brett-roberts-la-metro, 2026-04 — 15 invariants by engagement end.

---

## Section 13: Pre-Delivery Sweep ("Client-Ready Sweep")

Before sharing any client-facing artifact (URL, dashboard, email, deployable), run a pre-delivery sweep. This is the multi-agent audit (Section 7) applied with a specific lens: "ready to put in front of the paying client?"

**Two bars to test, separately:**
- **Ship-ready** — necessary condition: nothing is broken, secrets are safe, system runs, data is correct. Implementer's mental model.
- **Client-ready** — sufficient condition: a fresh viewer calls this *a product*, recommends it, trusts it, returns to it. Fresh-eyes review.

**Most pre-ship checklists optimize for ship-ready and miss client-ready.** brett-roberts-la-metro shipped, all tests passed, four-agent QA passed — then the operator opened the URL and said "it's bare." Bare meant: structurally empty on first view, despite being technically correct. Failure of client-ready bar.

**Required for client-ready bar:**
- Dispatch a sub-agent with explicit instructions: *"You are seeing this URL/email/artifact for the first time. You are the end user. Score the experience on first-impression-trust. List everything that reads as broken, generic, low-value, or empty."*
- Apply the **first-share architectural test** (provenance: A10): if the artifact's content depends on event-rate × N-sources × time-window, calculate the base rate. If `P(activity) × N_sources < ~3` per typical day, the rendering window is too narrow. Pivot architecture or extend window.
- Ideally: actual end-client previews in advance (not just operator's review).

**Provenance:** brett-roberts-la-metro, 2026-04 (Tier 3.5 sweep + post-ship "bare dashboard" lesson A10 + A16).

**Iterative ship-then-sweep cycles between "verifier passed" and "delivery sent".** Pre-launch evaluation (verifier scores, test passes, a11y review) gates structural correctness but consistently misses surface-level production bugs that only emerge against real data on a real deployed surface. Build the iteration cycle into the launch plan: ship to staging URL → manual screenshot review → round-1 fixes + redeploy → multi-agent automated sweep → round-2 fixes + redeploy → deliver. Each post-launch sweep takes a fraction of original build cost and prevents embarrassing-on-day-one bugs that erode trust. **Budget for at least 2 sweep cycles between "verifier passed" and "delivery email sent."** Provenance: brett-roberts-la-metro 2026-04-26 (Phase 9 verifier scored 100/100; subsequent manual + 5-agent + 4-agent sweeps surfaced 10 more bugs across 7 commits before actual delivery).

**Manual eyes-on AND automated sweep are both required (they catch different bug classes).** Manual surfaces UX-felt and credibility-sensitive content issues (broken links going to 404, headlines not clickable, source-skew suggesting routing). Automated surfaces structural and edge-case issues (pin-id collisions, mobile-touch invisibility, viewport-unit Safari quirks). Skipping either leaves a class of bugs in the ship. For SignalWorks delivery, always budget BOTH between "verifier passed" and "delivery email sent." Provenance: brett-roberts-la-metro 2026-04-26 (manual walkthrough caught 4 bugs no automation flagged; automated sweeps then caught 6 more no manual walkthrough caught).

---

## Section 13.5: Wait One Natural-Cadence Run Before Client Share

After a heavy-deploy session (multiple force-runs, backfills, manual cycles), **never share the live URL with the client immediately, even if it "looks ready."** Live state reflects dev churn — quota burns, off-cadence timestamps, manual-trigger artifacts in the last-update field, partial state from interrupted runs. Wait for at least one natural scheduled run (daily cron, hourly job, whatever the production cadence is). The 12-24 hour delay is always worth it because the client's first impression should be natural-cadence steady-state, not dev-churn snapshot.

**The cost of waiting is one day. The cost of sharing a dev-churn URL is permanent first-impression damage** — the stakeholder forms their mental model of the system from what they see in the first 30 seconds, and "this looks broken" can't be fully un-formed even after the next clean cron run.

**Provenance:** brett-roberts-la-metro, 2026-04-26 — at v13 close the live dashboard reflected 4 force-runs and 2 backfills that day; recommended deferring the share email to Brett. Trent followed; v14 shipped, ran clean morning cron, then shared. Brett's first impression was natural-cadence, not dev-churn.

---

## Section 14: Brand & Voice Rules

SignalWorks brand voice rules (no em-dashes; direct, warm, specific; not corporate, not startup hype) are canonical in:

> `/Users/t-rawww/signal-works-internal/CLAUDE.md` (sections "Voice rules" and "Commit message style")

**Do not restate brand rules in this playbook or in per-project CLAUDE.md.** Reference the canonical location. Single source of truth prevents drift across three copies.

Per-project CLAUDE.md inherits the rule by reference: "See `signal-works-internal/CLAUDE.md` for SignalWorks voice rules. Apply to all customer-facing copy, code comments, aria labels, site metadata."

### Delivery email rules (proven on brett delivery, 2026-04-26)

**Default to 75-100 word delivery emails for time-constrained stakeholders.** Cut anything the recipient could discover by looking at the artifact itself. Keep: URL, access mechanism, refresh cadence, known scope gaps, invitation for input, reply path. Drop: layout descriptions, feature lists they will see, motivational copy, "we're excited" register. If the longer version feels load-bearing, it usually isn't — it's anxiety about whether the work will be received well. Provenance: brett delivery email — first draft 350 words; rewritten at 80 words after operator feedback "make the email way shorter, it is a lot of ramble." Stakeholder response was positive; nothing in the dropped 270 words was missed.

**Establish the from-address before drafting outbound copy because it shapes voice register.** Ask first: which inbox is this sending from, who signs it, who replies route to. The answer determines first-person singular vs plural, formality, the implied response team, and whether the recipient should expect personal vs team handling. Drafting copy first and then "translating" to a different voice is brittle; getting the from-address right up front saves a redraft. Provenance: brett delivery email — drafted in first-person singular ("I'm working on..."), required full rewrite to plural + dual sign-off + brand mailbox once operator clarified send-from address.

**Pre-empt known scope gaps in delivery comms; don't sandbag.** Name your known scope gaps explicitly and frame them with status ("working on it" / "deferred to v15" / "not in current build"). Stakeholders who would notice the gap unprompted give credibility credit for being told upfront. Stakeholders who would not notice it lose nothing from the disclosure. Sandbagging — shipping a delivery email that implies completeness while known gaps exist — is a credibility trap that triggers when the user finds the gap unprompted. The single sentence of pre-emptive disclosure costs nothing and earns trust durably. Provenance: brett delivery email preserved both ECC schedule-only-degradation and CA Legislature quota-limit gaps in every revision; framed as "known and being worked on" rather than letting the recipient discover them.

---

## Section 14.5: AI Decision Points + Verification Mechanisms

**The deterministic-vs-probabilistic distinction matters.** Compilers are deterministic — same input → same output. LLMs are probabilistic translators — same input may produce different outputs, may introduce subtle vulnerabilities, may hallucinate facts. This is an architectural fact about the system, not a curiosity.

**Mandate:** every place AI output drives runtime behavior in a SignalWorks engagement gets documented in `docs/plans/design.md` under a section "AI Decision Points + Verification Mechanisms." Format per entry:

- **Decision point:** what AI is deciding (e.g., "summarize source documents into display_text", "classify support ticket urgency", "generate code suggestion")
- **Verification mechanism:** how we know the output is acceptable
  - eval framework with regression gate
  - grounding check (substring match against source)
  - human approval before action
  - deterministic post-process (e.g., regex extract from AI output)
  - automated regression test against labeled set
  - none — accepted as best-effort (rare; document why)
- **Failure mode:** what happens if AI is wrong
  - silent wrong-answer
  - degraded UX
  - hard error
  - data corruption
  - irreversible client-facing damage
- **Reversibility:** can we undo the AI's decision after the fact? (low / moderate / high)

**Why this matters:** without explicit documentation, AI decision points become invisible — operators forget which behaviors depend on AI output and where the verification gates are. When something breaks in production, "where does AI touch this?" should be answerable from a single document, not by archaeology across the codebase.

**Provenance:** video summary `7zCsfe57tpU` on systems thinking — "LLMs are probabilistic translators, not deterministic compilers" — integrated 2026-04-25.

---

## Section 15: Engagement Closure

When the engagement is shipping-complete and the client has accepted delivery:

1. **Final handoff** — last handoff in `.sessions/handoffs/` titled `handoff-YYYY-MM-DD-final.md`. Status = "Engagement complete." Resume Command = "Engagement archived; resume only if client requests v1.1 work."
2. **Post-mortem session** — schedule a 30-60 min session to consolidate the takeaways file. Lift novel patterns into this playbook (or queue for `/harvest-takeaways`).
3. **Case study trigger** — if engagement permits, use `signal-works-internal/process/case-study-template.md` to write a public case study.
4. **Repo archive** — set archive flag in GitHub. Move local repo from active path to `~/archived-engagements/` if desired.
5. **Update `signal-works-internal/clients/{client-slug}/`** — final status note in client folder.

---

# Part 2 — Type A Specifics: AI Deliverable Engagements

When the AI's behavior at runtime is the value (Type A per Section 2), apply these in addition to Part 1.

---

## Section 16.1: Eval Framework Setup

Reference: `~/AI-Knowledgebase/LEARNING/PRODUCTION/evaluation/evaluation.md`.

**Required from day 1:**
- 3-level eval stack: offline (regression on labeled set), online (canary on production), human (sample audit).
- LLM-as-judge with bias mitigation if applicable (position bias, verbosity bias, self-enhancement bias).
- Per-metric definitions: faithfulness, relevance, coherence, hallucination rate.

**Anti-pattern:** "we'll add evals later." Type A engagements without evals from day 1 ship on vibes; quality regressions go undetected; client trust erodes after launch.

**Concrete:** brett-roberts-la-metro v1.6 → v1.7 prompt revision included a tightening of `why_relevant` boilerplate. Without an eval gate, the regression risk would have been "we shipped and hope it's fine." With evals: regression gate runs against labeled set; LLM-as-judge confirms tightened output is at least as relevant as v1.6.

---

## Section 16.2: Hallucination Prevention Architecture

Hallucinations are an architecture problem, not a prompting problem. Once "we keep adding rules and they keep slipping" becomes the pattern, the answer is to remove the model's authority to author the hallucinated content.

**Patterns proven on brett-roberts-la-metro:**
1. **Verbatim source selection.** Replace "summarize this" with "select a verbatim span from this." The model can't hallucinate what it isn't allowed to author.
2. **Grounding checks.** Substring match every fact-shaped output against the source. Drop ungrounded items. Tests: `TestGroundingCheck`, `TestApplyGroundingCheck`.
3. **NER gates.** Extract entities (PERSON, ORG, GPE, FAC, LOC, LAW, DATE, EVENT) from output; verify each appears in source OR on an allow-list.
4. **Brett-profile allow-list.** Domain-specific allow-list of expected entity names so allowed mentions don't false-trigger the NER gate.
5. **MONEY tolerance.** Numeric facts compared with ±1% tolerance to handle minor formatting variance.

**Decision flowchart:**
```
Is the model authoring fact-shaped content?
├── YES → can the model select rather than generate?
│   ├── YES → switch to verbatim-selection architecture
│   └── NO → require grounding check + NER gate + per-domain allow-list
└── NO  → standard prompt rigor (Section 16.4)
```

**Transfer rule:** Stop prompt-engineering when the failure pattern is "rules keep slipping." Switch to architecture.

**Provenance:** brett-roberts-la-metro, 2026-04 — Tier 1+2+3 zero-hallucination architecture.

---

## Section 16.3: Model Selection Rationale

Reference: `~/AI-Knowledgebase/LEARNING/FOUNDATIONS/reasoning-llms/reasoning-llms.md`.

Document **why** per project. Cost vs latency vs reasoning quality vs context vs grounding capability.

**Required documentation:**
- Model name + version (and fallback)
- Token budget per inference (input + output)
- Latency budget per inference
- Cost per inference (envelope; track over engagement)
- Why not the obvious alternatives (e.g., "not Claude Opus because cost; not Gemini Pro because rate limits")

**Anti-pattern:** picking a model because it's the latest or familiar. Each engagement justifies its choice in the design log.

**Concrete:** brett-roberts-la-metro chose Gemini Flash 2.5 because (a) cost — free tier covers expected volume, (b) latency — sub-3s per call acceptable, (c) Anthropic SDK not desired (avoid client-perceived dependency on a specific vendor's stack). Fallback: `gemini-1.5-flash`.

---

## Section 16.4: Prompt Engineering Rigor

Reference: `~/AI-Knowledgebase/LEARNING/FOUNDATIONS/prompt-engineering/prompt-engineering.md`.

**Discipline:**
1. **Versioned prompts.** Each prompt is a doc at `docs/prompts/{name}-vN.md` with a changelog. Diff is reviewable in PR.
2. **Loader in code.** `_load_system_prompt()` reads from the doc, not inlined string. Add a debug log that prints what was loaded; verify it matches the file at startup.
3. **Examples inside fence.** If your loader regex-extracts a fenced block, examples must be INSIDE the fence. brett-roberts-la-metro Tier 1 caught a project-life-spanning bug where examples were outside the fence and the model never saw them.
4. **Prompt-engineering as sub-agent task.** Prompt rewrites are produced by a sub-agent with a clear input file (current prompt + audit findings) and reviewed by the operator before commit.
5. **No CoT manual injection** for reasoning models — reasoning happens internally. For non-reasoning models, structured CoT is acceptable but versioned.

**Anti-pattern A2 (provenance):** Strict content gates designed without empirical validation on real model output. Solution: pre-ship calibration run on ≥20 representative outputs before shipping the gate.

**Anti-pattern (load-at-runtime asymmetry):** any config file the code regex-loads gets a "does the loader actually see this?" audit at least once per project.

---

## Section 16.5: AI Security Pre-flight

Reference: `~/AI-Knowledgebase/LEARNING/PRODUCTION/ai-security/ai-security.md`.

**Required pre-flight at engagement kickoff:**
- Repo privacy + fork lineage (anti-pattern A3 — public-fork-of-public can't go private)
- `.env.example` placeholder-only; live `.env` never committed
- GitHub Actions workflow permissions = `contents: read` minimum
- Default branch protection rules
- Cloudflare or equivalent ingress preview-deployment policy (off for sensitive)

**Required at each tier ship:**
- URL-scheme XSS gate on any user-facing href that comes from model output
- Token redaction in error logs (centralized helper, not per-site — provenance A13)
- Pre-flight checks that distinguish auth from availability (provenance A11)
- Centralized log-safety module: `src/secret_redactor.py` with `redact()` + `safe_err()` (provenance A13)

**Provenance for security patterns:** brett-roberts-la-metro, 2026-04 — SEC-001 through SEC-018 covered in Tier 3.5 sweep.

---

# Part 3 — Type B Specifics: AI-Accelerated Build Engagements

When AI coding agents help build a non-AI deliverable (Type B per Section 2), apply these in addition to Part 1.

---

## Section 17.1: Design/UX Rigor

For client-facing UI deliverables, design is first-class. Do not skip.

**Required from day 1:**
- `DESIGN.md` authored before code. Color system, typography, spacing scale, component library, motion principles.
- Reference skills (deployed by `/cook` Phase 2.5):
  - `frontend-design` — distinctive, production-grade interfaces avoiding generic AI aesthetics
  - `web-design-patterns` — DESIGN.md-driven approach
  - `shadcn-ui` — component integration if shadcn is in stack
  - `frontend-taste` — design-language tuning (DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY parameters)
- Lighthouse gates for marketing sites (≥90 mobile target).

**Anti-pattern:** scaffolding a Type B project without front-end skills deployed at scaffold time. The brett-roberts-la-metro dashboard hit this exact failure — UI deliverable existed but the project's `.claude/skills/` had only AI-engineering skills, no design skills. Result: UI iteration was bland and generic until manually fixed.

**`/cook` Phase 2.5 enforces this** — for Type B classification, deploy front-end skills mandatorily.

---

## Section 17.2: Front-End Skill Deployment

Required deployment list for any project with UI surface (deployed by `/cook` Phase 2.5):

| Skill | Source | Purpose |
|---|---|---|
| `frontend-design` | `~/.claude/skills/frontend-design/` | Distinctive frontend aesthetics |
| `web-design-patterns` | `~/.claude/skills/web-design-patterns/` (if exists) or KB ref | DESIGN.md before code |
| `shadcn-ui` | `~/.claude/skills/shadcn-ui/` (if exists) | Component library integration |
| `frontend-taste` | `~/.claude/skills/frontend-taste/` (if exists) | Design parameter tuning |

**Verify after scaffold:** `ls {project}/.claude/skills/` should include the deployed skills.

---

## Section 17.3: Responsive QA

Mobile-first verification is non-negotiable for any client-facing UI. Most users on most projects are on mobile.

**Required browser/device matrix:**
- Mobile: Safari (iOS), Chrome (Android)
- Desktop: Chrome, Firefox, Safari (macOS)
- Tablet: at least one in middle resolution

**Per-tier gate:** rendered output verified on at least mobile + desktop before tier ships.

---

## Section 17.4: Performance & Core Web Vitals

Reference: `~/AI-Knowledgebase/future-reference/playbooks/building-professional-websites.md`.

**Required gates for Type B marketing sites or dashboards:**
- Lighthouse mobile ≥90 (performance + accessibility + best practices + SEO)
- LCP under 2.5s on 3G simulated
- CLS under 0.1
- INP under 200ms
- OG metadata + favicon set per page
- Sitemap + robots.txt for marketing sites

---

## Section 17.5: Verification Loop

Build / lint / type-check on every change. Use `verification-loop` skill if deployed.

**Anti-pattern:** "we'll run the build before commit" — without a verification loop, build breakage lands in commits and slows down review velocity. Make the verification automatic per change.

---

# Appendix — Anti-Patterns Library

The following anti-patterns are confirmed across SignalWorks engagements. Each has a code (A1, A2, ...) for cross-referencing in handoffs and decision logs.

| Code | Pattern | Fix |
|---|---|---|
| A1 | Stale lockfile silently shadowing new deps | Regenerate or delete; never leave stale |
| A2 | Strict contracts without empirical validation on real model output | Pre-ship calibration run on ≥20 real outputs |
| A3 | Fork lineage constrains repo privacy | Pre-flight check at kickoff |
| A4 | Silent failures mask as legitimate empty states | `{items, ok, error}` envelope; raise + classify |
| A5 | Doc debt compounds faster than code debt | Doc refresh sub-step per tier |
| A6 | "Doesn't crash" ≠ "behaves correctly" — zombie tests | Positive assertions; grep for `if X:` test guards |
| A7 | Don't batch risky tool calls with agent dispatches | Risky calls get own message |
| A8 | Two Claude sessions on same branch | `.claude/lock` file; serial handoff only |
| A9 | Fixing one layer of data-format change while adjacent layers stay stale | Grep all sites; lockstep test update |
| A10 | "Bare dashboard" — first-share architectural test failure | Calculate base rate × window; pivot if < ~3/day |
| A11 | Pre-flight checks that don't distinguish auth from availability | Pass on 4xx/5xx that prove reachability; fail only on 401/403/timeout/DNS |
| A12 | CI script-form imports break with package paths | Use module entry points (`python -m`) or sys.path shim |
| A13 | Inlined per-site redaction drifts | Centralized log-safety module |
| A14 | Two-session collision can't be fixed by docs alone | Runtime lock file |
| A15 | Iterative force-run sequence as debugging mode | Budget 3-4 force-runs; every failed run ships fix or test |
| A16 | "Ship-ready" and "client-ready" are different bars | Build two checklists; run both |
| A17 | System incoherence — multiple unrelated concerns inhabit a single boundary | Decompose along single-responsibility lines; signal is sentence-summary, not line count |
| A18 | Recovery handlers narrowed to wrong exception class | Catch broadest applicable `Exception` in recovery paths; use `isinstance()` at re-raise to preserve type-specific context |
| A19 | Parallel template/code branches drift over multiple sessions | Refactor to shared macro/component for structural parity; or audit for behavioral parity periodically |
| A20 | Redesigning presentation while data layer is unstable | Gate redesigns behind data-layer stability — would the new UI render correctly across empty/partial/degraded data states? |

Full narrative descriptions: see `signal-works-internal/takeaways/brett-roberts-la-metro.md`.

### A17 — System Incoherence (full description)

**Symptom:** a file, module, or service contains multiple unrelated concerns — there is no single sentence that summarizes its purpose. The 7,000-line single-file failure mode (from video summary `7zCsfe57tpU`) is one extreme; subtler versions exist at all scales (a "utils" module that does 12 unrelated things; a service that owns auth + rate-limiting + metrics; a "main" function that handles input parsing + business logic + output formatting + error logging).

**The signal is NOT line count.** Big files with single coherent purpose are fine; small files straddling multiple responsibilities are bad. The diagnostic is: can a reader summarize this boundary's responsibility in ONE sentence? If the summary requires "and" or "also" multiple times, the boundary is wrong.

**Why this is a SignalWorks-specific concern:** AI-generated code often defaults to "everything in one place" because LLMs reason locally and don't see decomposition opportunities until prompted. Without operator vigilance, AI-built systems drift into incoherent monoliths that are hard to test, hard to delete from, and hard to understand.

**Fix:**
- Decompose along single-responsibility lines.
- Extract distinct concerns to separate boundaries (modules, files, services).
- Update tests to exercise each in isolation.
- Update adjacent docs to reflect new boundaries (anti-pattern A9 — adjacent layers must be updated in lockstep).

**General rule:** every module, file, service has a single sentence that describes its responsibility. If the sentence requires "and" or "also", the boundary is wrong. The Three Questions (Section 1.5) help here: each boundary should have a single state-owner answer, a single feedback-channel answer, and a bounded blast-radius answer.

**Audit hunt category** (added to `docs/prompts/audits/code-correctness.md`): "System Coherence — for each non-trivial module, can a reader summarize its responsibility in ONE sentence? If 'and' or 'also' is required, flag P2 with A17 reference."

---

# Appendix — Engagement Kickoff Checklist

For every new SignalWorks engagement, check before first work session:

- [ ] Engagement Discovery doc complete (Section 1)
- [ ] Type classified (Section 2)
- [ ] Authority block negotiated and documented in CLAUDE.md (Section 3)
- [ ] Source-of-truth doc spine scaffolded (Section 4) — SOUL.md, CLAUDE.md, AGENTS.md, design.md, implementation.md, handoff template, decision log stub
- [ ] CLAUDE.md mandates baked from template (Section 5)
- [ ] `signalworks_takeaways_target:` line set in CLAUDE.md
- [ ] `signal-works-internal/takeaways/{client-slug}.md` file created (empty or with header)
- [ ] `signal-works-internal/clients/{client-slug}/` folder exists with contact + outreach
- [ ] Repo privacy + fork lineage audited (anti-pattern A3)
- [ ] `.env.example` placeholders only, no live keys
- [ ] GitHub Actions permissions = `contents: read` minimum
- [ ] Default branch protection rules set
- [ ] CF Pages or equivalent preview-deployment policy decided (off for sensitive)
- [ ] Authority block reviewed with operator
- [ ] If Type A: model selected + documented (Section 16.3); eval framework stubbed (Section 16.1)
- [ ] If Type B: front-end skills deployed (Section 17.2); DESIGN.md authored before code (Section 17.1)
- [ ] First handoff stubbed at `.sessions/handoffs/handoff-{date}-v1.md` with Resume Command + Audit Directions slot

---

**Author:** Trent Johnson + Claude Opus 4.7 (1M context), 2026-04-24.
**Status:** v1 seed. Will evolve via manual integration + `/harvest-takeaways` skill (deferred).
**Last harvest run:** none yet.
