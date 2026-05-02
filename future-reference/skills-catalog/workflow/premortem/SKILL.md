---
name: premortem
description: "Run a premortem on any plan, launch, product, hire, strategy, or decision. Assumes it already failed 6 months from now and works backward to find every reason why. Produces a revised plan with blind spots exposed, routed to spec changes / CLAUDE.md constraints / waivers. MANDATORY TRIGGERS: 'premortem this', 'premortem my', 'run a premortem', 'what could kill this', 'future-proof this', 'stress test this plan', 'what am i missing here', 'find the blind spots'. STRONG TRIGGERS: 'what could go wrong', 'am i missing anything', 'poke holes in this', 'where will this break', 'devil's advocate this'. Do NOT trigger on simple feedback requests or factual questions. DO trigger when someone has a plan or commitment where the cost of being wrong is high. MANDATORY for SignalWorks engagements at Phase 1.6 (after spec confirmation, before harness design)."
---

# Premortem

A premortem is the opposite of a postmortem. Instead of figuring out what went wrong after something fails, you imagine it already failed and figure out why before you start.

The method comes from psychologist Gary Klein, published in Harvard Business Review. Daniel Kahneman called it his single most valuable decision-making technique. Google, Goldman Sachs, and P&G use it before major decisions.

The core insight: when you ask "what could go wrong?" you get cautious, hedged answers. When you say "this already failed, tell me why," the brain switches into narrative mode and generates far more specific, honest reasons — what researchers at Wharton and Cornell call "prospective hindsight."

The reason this matters for AI-assisted work: Claude defaults to agreeable, optimistic responses. If you ask "is this a good plan?" it will find reasons to say yes. The premortem breaks this by forcing the frame into "this is dead, explain how it died." Claude stops looking for reasons the plan will work and starts explaining how it fell apart.

**Estimated wall clock: ~15–20 min + ~5 min per failure agent.**

---

## When to run

**Good targets:**
- A product, feature, or system you're about to build
- A consulting engagement commitment (scope, timeline, fixed price)
- A launch plan with money or reputation on the line
- A strategy, pricing change, or positioning pivot
- Any commitment where the cost of being wrong is high

**Bad targets — stop here and don't run:**
- Vague ideas with no concrete plan yet (help them plan first, then premortem)
- Questions with one right answer (just answer them)
- Creative feedback on a draft (that's editing, not a premortem)
- Decisions already made AND irreversible (premortem only helps when you can still change course)

---

## Pre-flight: Is there still a decision to make?

Before scanning context, confirm the decision is still open. Ask:

> "Before we run this — is the scope/approach/architecture still changeable? If major decisions are locked (SOUL.md locked decisions, Phase 0.7 constraints, signed client scope), flag them now. I'll mark any failure reason that assumes you can change a locked decision as 'architecture-locked — verify intent' rather than running a full agent on it."

This prevents wasting agent cycles on failures that can't happen given existing constraints. Record locked decisions in memory for the alignment filter in Step 1.

---

## Context gathering

A premortem is only as good as the context it runs on. Before asking the user anything, scan what already exists.

### Step 1: Load structured artifacts first

If running from Phase 1.6 (inside /cook), these files already contain everything needed — read them before asking a single question:

- `docs/plans/design.md` — problem statement, deliverable, scope, success criteria, Three Questions, locked decisions
- `SOUL.md` — engagement character, locked decisions, definition of done, success criteria
- `CLAUDE.md` — authority block, constraints, operator-approved decisions

If these exist, you can likely proceed to the premortem immediately without any follow-up questions. Extract from them:
1. **What is it?** — problem + deliverable in one sentence
2. **Who is it for?** — audience, stakeholders, client
3. **What does success look like?** — numeric where possible

If not running from /cook, scan workspace for equivalent context (project briefs, requirements docs, conversation history).

### Step 2: Fill gaps conversationally (only if needed)

If any of the three required pieces are missing after reading artifacts, ask one targeted question at a time:
- "What specifically are you about to build/decide?" (if no deliverable)
- "Who is this for?" (if no audience)
- "What does a win look like?" (if no success criteria)

Don't ask more than you need. If you can infer from context, do that instead.

---

## How a premortem session works

### Step 1: Locked-decision alignment filter

Before generating failure reasons, cross-reference the plan against locked decisions from SOUL.md and Phase 0.7. For each locked decision found, note: "Failure reasons that assume this can be changed will be flagged as architecture-locked rather than dispatched as full agents."

Example: If SOUL.md says "Static HTML only," a failure reason about "chose wrong framework" gets flagged, not dispatched.

### Step 2: Set the frame

State the premortem premise explicitly:

> "OK — here's the frame: it's 6 months from now. [The plan] has failed. Not 'struggled a bit' — it's done. We're looking back and figuring out why. I'm going to generate every genuine reason this could have died."

This framing matters. It shifts mode from "evaluate this plan" (triggers agreeable responses) to "explain why this died" (triggers honest, specific failure identification).

### Step 3: Generate failure reasons

Run the raw premortem as a single comprehensive analysis:

> "This plan has failed 6 months from now. Generate every genuine reason it could have died. Be comprehensive. Be specific. Ground every reason in the actual details of the plan. Don't pad with weak reasons and don't stop early if there are more."

Each failure reason should be:
- Specific to this plan (not generic advice that applies to anything)
- Grounded in actual details from the spec
- A genuine threat (not a minor inconvenience or extremely unlikely edge case)

**Cap at 8 failure reasons.** If more than 8 genuine reasons emerge, cluster thematically-adjacent ones (e.g., "three scope-related failures" → one clustered failure reason) before proceeding. Unbounded parallel agents are expensive and produce synthesis that's hard to act on.

**Mark any failure reason that assumes a locked decision as `[ARCHITECTURE-LOCKED]`** — do not dispatch a full agent for these. Surface them to the operator with a note: "This failure assumes [X], which is a locked decision. Verify intent before proceeding."

### Step 4: Deep-dive agents (one per failure reason, all in parallel)

Dispatch one sub-agent per non-locked failure reason, all in a single message. Each agent goes deep on its assigned failure independently.

**Sub-agent prompt template:**

```
You are an investigator in a premortem analysis. You've been assigned one specific failure reason to analyze in depth.

THE PLAN:
---
[full context: what it is, who it's for, success criteria, scope, timeline, budget — from design.md/SOUL.md]
---

PREMORTEM FRAME: It is 6 months from now. This plan has failed.

YOUR ASSIGNED FAILURE REASON: [the specific failure reason from Step 3]

Your output must include all five sections:

1. THE FAILURE STORY: A 2-3 paragraph narrative of how this failure played out. Be specific. Use details from the plan. Name the exact moments things went wrong and why. Make it feel like a case study of something that actually happened.

2. THE UNDERLYING ASSUMPTION: The one thing that was taken for granted that made this failure possible. One sentence.

3. EARLY WARNING SIGNS: 1-2 concrete, observable signals that would indicate this failure is starting to play out. Must be measurable or directly observable — not vague feelings.

4. SEVERITY [1-5]: How bad if this happens?
   1 = minor inconvenience, easily recovered
   3 = significant rework or cost, recoverable
   5 = project-ending, client relationship destroyed, or major financial loss

5. LIKELIHOOD [1-5]: How probable given this specific plan?
   1 = unlikely edge case, requires unusual circumstances
   3 = plausible — could see this happening
   5 = this almost certainly happens without intervention

Keep total response under 400 words. Be direct. Don't hedge. Don't sugarcoat.
```

### Step 5: Synthesis

After all agents return, synthesize across ALL findings using the quantified ratings:

**PREMORTEM REPORT**

1. **Most Likely Failure** — Highest likelihood score (or highest combined score if tied). Why this one? Quote the underlying assumption.

2. **Most Dangerous Failure** — Highest severity × likelihood score. This is the one worth insuring against even if less likely.

3. **Hidden Assumption** — Across all failure stories, what's the single biggest thing the plan takes for granted that hasn't been questioned? This is often where the real value lives: the assumption so obvious it was invisible.

4. **Revised Plan** — Specific changes to address the top failure modes. For each item, assign exactly one of three labels:
   - `[SPEC-CHANGE]` — requires a change to the spec before Phase 2
   - `[CLAUDE-CONSTRAINT]` — requires a new constraint block in CLAUDE.md before first build session
   - `[WAIVER: {reason}]` — accepted as known risk; reason documented

   Each item must be something concrete and doable. Not "consider your timeline." Say "reduce fixed-price scope to 5 of the 7 stated deliverables and move the remaining 2 to a Phase 2 option, documented in the signed scope."

5. **Pre-Commitment Checklist** — 3-5 specific things to verify, test, or put in place before executing. Each one maps directly to a specific failure mode identified above.

### Step 6: Route revised-plan items to outcomes

For every `[SPEC-CHANGE]` item: update `docs/plans/design.md` before advancing to Phase 2.
For every `[CLAUDE-CONSTRAINT]` item: add to CLAUDE.md under appropriate constraint section.
For every `[WAIVER]` item: log in `docs/plans/design.md` under a "Premortem Waivers" section with the acceptance reason.

**Gate: Do not advance to Phase 2 until every revised-plan item is labeled and actioned.** An unrouted finding is a finding that won't survive to the build phase.

### Step 7: Save output

Save the full premortem transcript to: `.sessions/premortems/premortem-{YYYY-MM-DD}.md`

The transcript includes: context loaded, locked decisions flagged, failure reasons generated, all agent deep-dives with severity/likelihood, and the full synthesis with routed outcomes.

If operator wants a shareable artifact (client presentation, async review), generate `premortem-report-{YYYY-MM-DD}.html` on request. HTML is optional — markdown is the default and how we actually work.

---

## Output format

Every premortem produces:
```
.sessions/premortems/premortem-{YYYY-MM-DD}.md    # canonical transcript
docs/plans/design.md                              # updated with spec changes + waivers
CLAUDE.md                                         # updated with any new constraints
```

Also provide a concise in-chat summary: most likely failure (one sentence), hidden assumption (one sentence), most important revised-plan action (one sentence). The transcript has the full details.

---

## Example: SignalWorks consulting engagement

**Context:** About to build a government-transparency dashboard for a county supervisor. Fixed price: $18K. 8-week timeline. Deliverable: public-facing agenda tracker with AI summaries of upcoming votes across 3 government sources. SOUL.md locked: "Static HTML + Python scraper only — no database."

**Raw premortem generates 6 failure reasons:**
1. Government data sources are inconsistently maintained — if one source moves its URL or changes its format mid-engagement (LA Metro did this in production), the scraper breaks silently and the dashboard shows stale data
2. Fixed-price underscoping — the PDF-to-structured-data pipeline alone takes 3 weeks; the 8-week timeline assumed clean structured feeds
3. Client approval bottleneck — government stakeholders have 2-week approval cycles; every design decision needs sign-off, and this isn't reflected anywhere in the timeline
4. AI summary accuracy risk — incorrect AI summaries of government documents create reputational and legal exposure for the client; "close enough" is not acceptable for a public official's dashboard
5. Scope creep from success — if the dashboard works, the client asks "can you add the city council? The school board?" in week 6 at no additional cost; no scope-change language in the agreement
6. Data access reality — "publicly available" data is sometimes behind login walls or requires FOIA requests; this wasn't validated before scoping

**Locked decision check:** "Static HTML + Python scraper only" is locked. Any failure reason assuming a database solution gets flagged `[ARCHITECTURE-LOCKED]`.

**6 agents dispatch in parallel.** Failure #2 and #3 both rate Likelihood 4–5. Failure #4 rates Severity 5.

**Synthesis:**
- Most Likely: Failure #3 (client approval bottleneck, Likelihood 5). Underlying assumption: client will respond within 48 hours.
- Most Dangerous: Failure #4 (AI accuracy risk, Severity 5 × Likelihood 3). An incorrect summary on a public official's site triggers media coverage.
- Hidden Assumption: "publicly available" = "programmatically accessible without friction" — this is false and was never validated.
- Revised Plan:
  - `[SPEC-CHANGE]` Validate programmatic access for all 3 sources before signing scope
  - `[SPEC-CHANGE]` Add scope-change clause to agreement: new sources = new SOW
  - `[CLAUDE-CONSTRAINT]` All AI summaries require human review gate before publish — no auto-publish
  - `[WAIVER: client-accepted]` Client approval lag — client agrees to 48-hour SLA; documented in scope

---

## Important notes

- **Always spawn all failure agents in parallel.** Sequential spawning wastes time and lets earlier responses influence later ones.
- **Always set the premortem frame explicitly.** "This has already failed" is the psychological mechanism that makes this work. Without it, analysis defaults to polite risk assessment.
- **Cap at 8 agents.** Cluster thematically-adjacent failure reasons rather than spawning unlimited agents.
- **The synthesis is the product.** Most people will read the synthesis and skim the agent cards. Make it specific and actionable.
- **Don't sugarcoat.** The point is to tell the operator things they don't want to hear before reality does. If a plan has serious problems, say so directly.
- **Revised-plan items must be concrete AND routed.** Not "consider your timeline." Every item labeled `[SPEC-CHANGE]`, `[CLAUDE-CONSTRAINT]`, or `[WAIVER]` and actioned before the gate passes.
- **Locked decisions are not failure candidates.** Don't run agents on failures that assume you can change what's already decided. Flag them and move on.
