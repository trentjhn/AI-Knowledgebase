# Presentation Mastery Skill Implementation Plan

> **For Claude:** Use executing-plans or follow this plan task-by-task to build the skill + execute the Instacart case study.

**Goal:** Create a reusable "presentation-mastery" skill that orchestrates 12 presentation prompts in 4 phases, then immediately use it to build the Instacart autonomous delivery case study (5-8 slides in 3 days).

**Architecture:** 
- Skill: 4-phase workflow (foundation → structure → content → polish) with embedded prompts and checklists
- Patrick Winston prompts: 6 new .md files added to KB presentation-design folder
- Instacart execution: Apply skill phases across research (Day 1) + strategy/slides (Days 2-3) + polish (final)

**Tech Stack:** 
- Skill files: Markdown with YAML frontmatter
- Slide creation: Canva (with MCP for AI visuals) + Claude canvas for quick mocks
- Research: `/last30days` on autonomous delivery + last-mile logistics
- Delivery: PDF submission to Greenhouse

---

## KB Resources for Instacart Challenge

**Reference during brainstorming phase (Day 1):**

| Phase | KB File | Why It Matters | Reference Point |
|-------|---------|----------------|-----------------|
| **Foundation (Phase 1)** | `/Users/t-rawww/AI-Knowledgebase/evaluation.md` | How to define metrics rigorously; frameworks like Ragas, LLM-as-judge patterns | Informs pilot success definition |
| **Foundation (Phase 1)** | `/Users/t-rawww/AI-Knowledgebase/agentic-engineering.md` | How autonomous systems make decisions; Twelve Leverage Points, agentic patterns (Plan-Build-Review, Orchestrator, HITL) | Informs strategy on exception handling, decision-making complexity |
| **Structure (Phase 2)** | `/Users/t-rawww/AI-Knowledgebase/ai-security.md` | Privacy, robustness, adversarial risks for autonomous systems; mitigation strategies | Risk/mitigation section (slide 4 or dedicated risk slide) |
| **Content (Phase 3)** | `/Users/t-rawww/AI-Knowledgebase/specification-clarity.md` | How to specify systems precisely, avoid ambiguity | MVP features slide (slide 5) — make specs concrete |
| **Content (Phase 3)** | `/Users/t-rawww/AI-Knowledgebase/context-engineering.md` | How to structure information for autonomous system decisions | Optional: Customer context, order context for routing decisions |
| **Content (Phase 3)** | `/Users/t-rawww/AI-Knowledgebase/reasoning-llms.md` | When/how to use reasoning for complex decisions | Optional: Edge case handling (weather, blocked routes, unavailable customers) |

**How to use:**
- During Phase 1 (Foundation), open evaluation.md + agentic-engineering.md to ground your strategy thinking
- During Phase 2 (Structure), consult ai-security.md for risk framing
- During Phase 3 (Content), reference evaluation.md for metrics, agentic-engineering.md for MVP design
- See `KB-REFERENCES.md` in Instacart directory for quick links

---

## Phase A: Build Skill Infrastructure

### Task 1: Create Patrick Winston prompt files in KB

**Files:**
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/start-any-presentation/prompt.md`
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/start-any-presentation/README.md`
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/structure-persuasive-talk/prompt.md`
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/structure-persuasive-talk/README.md`
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/make-ideas-unforgettable/prompt.md`
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/make-ideas-unforgettable/README.md`
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/eliminate-slide-crimes/prompt.md`
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/eliminate-slide-crimes/README.md`
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/end-powerfully/prompt.md`
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/end-powerfully/README.md`
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/props-stories-teach/prompt.md`
- Create: `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/props-stories-teach/README.md`

**Step 1: Create start-any-presentation folder and files**

```bash
mkdir -p /Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/start-any-presentation
```

**prompt.md** content:
```markdown
# START ANY PRESENTATION RIGHT

Act as a presentation coach applying Patrick Winston's MIT framework — every talk must open with an empowerment promise that tells the audience exactly what they will know by the end that they didn't know at the beginning.

Write a powerful opening for my presentation that makes the audience immediately understand why staying is worth every minute of their time.

## Steps

1. Ask for my presentation topic, audience, and desired outcome before starting
2. Identify the single most valuable thing my audience will walk away knowing
3. Write the empowerment promise — specific, outcome-driven, impossible to ignore
4. Design the first 60 seconds — promise, context, and why this matters now
5. Flag everything that should be cut from the opening — jokes, thank yous, apologies

## Rules

- Never open with a joke — audience isn't ready
- Never open with "thank you for having me" — weak and forgettable
- Empowerment promise must be specific — not "you'll learn about X" but "by the end you'll be able to do Y"
- First 60 seconds must earn the next 60 minutes
- Cut everything that doesn't serve the promise

## Output Format

Empowerment Promise → First 60 Seconds → What to Cut → Opening Script
```

**README.md** content:
```markdown
# START ANY PRESENTATION RIGHT

## When to Use

Use this prompt as the **opening component** of any presentation (interview case study, pitch, conference talk, product review). Apply it in **Phase 1 (Foundation)** of the presentation-mastery workflow, after you've established your key message and narrative arc.

## Why It Works

Patrick Winston's empowerment promise forces you to define the *single most valuable insight* your audience will gain. Unlike weak openers ("Thank you for having me"), the empowerment promise creates immediate tension: *the audience wants to know what they'll learn.* It's the difference between optional and essential.

## Trade-Offs

**What it does well:**
- Creates urgent, compelling reason to listen
- Forces you to crystallize the core value of your presentation
- Eliminates filler and weak opens
- Takes 10 minutes to craft and pays dividends in attention

**What it sacrifices:**
- Requires honesty about what your presentation actually delivers
- Can't hedge or include multiple competing promises

## Related Techniques

- **Specificity Principle:** "You'll be able to do X" beats "You'll learn about Y"
- **Audience-Centric Framing:** Promise is for them, not about you
- **Tension & Resolution:** Promise creates tension; rest of presentation resolves it

## Example Use Case

**Scenario:** You're presenting an autonomous delivery strategy to Instacart leadership.

**Weak open:** "Today I'm going to talk about autonomous delivery."

**Empowerment promise:** "By the end of this presentation, you'll know exactly which customer segments benefit most from autonomous delivery, when it becomes profitable vs. when it's a money-losing feature, and the first 90 days of a pilot that proves it."

That's specific. That's outcome-driven. Audience knows why they should listen.

## Application in presentation-mastery Skill

This prompt appears in **Phase 1: Foundation**, after:
- Build Blueprint (established objective, audience, key message)
- Turn Into Story (mapped narrative arc)

Use it to finalize the opening 60 seconds, then move to **Phase 2: Structure** where Patrick Winston: STRUCTURE builds the full vision/proof/contributions framework.
```

**Step 2: Create remaining 5 Patrick Winston prompt folders**

Repeat the pattern above for:
- `structure-persuasive-talk/` (from your notes on STRUCTURE ANY TALK THAT PERSUADES)
- `make-ideas-unforgettable/` (from MAKE YOUR IDEAS UNFORGETTABLE using Star framework)
- `eliminate-slide-crimes/` (from ELIMINATE YOUR SLIDE CRIMES)
- `end-powerfully/` (from END ANY PRESENTATION POWERFULLY)
- `props-stories-teach/` (from USE PROPS AND STORIES TO TEACH ANYTHING)

For each, create `/prompt.md` and `/README.md` using the same template structure.

**Step 3: Commit Patrick Winston prompts**

```bash
cd /Users/t-rawww/AI-Knowledgebase
git add future-reference/prompt-catalog/presentation-design/start-any-presentation/
git add future-reference/prompt-catalog/presentation-design/structure-persuasive-talk/
git add future-reference/prompt-catalog/presentation-design/make-ideas-unforgettable/
git add future-reference/prompt-catalog/presentation-design/eliminate-slide-crimes/
git add future-reference/prompt-catalog/presentation-design/end-powerfully/
git add future-reference/prompt-catalog/presentation-design/props-stories-teach/

git commit -m "feat: add Patrick Winston presentation frameworks (6 prompts)

- START ANY PRESENTATION RIGHT: empowerment promise framework
- STRUCTURE ANY TALK THAT PERSUADES: vision/proof/contributions
- MAKE YOUR IDEAS UNFORGETTABLE: Star framework (symbol/slogan/surprise)
- ELIMINATE YOUR SLIDE CRIMES: slide audit checklist
- END ANY PRESENTATION POWERFULLY: contributions close framework
- USE PROPS AND STORIES TO TEACH ANYTHING: demonstration + narrative

These prompts are orchestrated by presentation-mastery skill.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

### Task 2: Create presentation-mastery skill SKILL.md

**Files:**
- Create: `/Users/t-rawww/.claude/skills/presentation-mastery/SKILL.md`

**Step 1: Create skill directory**

```bash
mkdir -p /Users/t-rawww/.claude/skills/presentation-mastery
```

**Step 2: Write SKILL.md**

```markdown
---
name: presentation-mastery
description: 4-phase workflow orchestrating 12 presentation prompts (existing KB + Patrick Winston frameworks) for any PM presentation (case studies, pitches, reviews, interviews). Apply in order: Foundation → Structure → Content → Polish.
trigger: When you need to create a high-impact presentation and want a structured, validated workflow. Especially powerful for interview case studies and product pitches where strategic rigor + execution depth differentiate.
---

# Presentation Mastery

**A structured 4-phase workflow that sequences 12 presentation prompts in logical order.**

## When to Use This Skill

- **Interview case study challenges** (Instacart, Airbnb, Amazon, etc.)
- **Product pitches** to stakeholders or investors
- **Product reviews** and PRD walkthroughs
- **Conference talks** and speaking engagements
- **Personal portfolio presentations**

**Do NOT use if:** You're creating a quick 2-slide internal status update or handoff doc. The skill is designed for high-stakes presentations where quality compounds.

---

## The Four Phases

### Phase 1: Foundation (Strategic Thinking)
**Duration:** 30-60 min | **Goal:** Define *what* you're saying and *why*

**Prompts in order:**
1. **Build Blueprint** (existing KB) → Establish objective, audience, key message, logical flow
2. **Turn Into Story** (existing KB) → Map narrative arc (hook/problem/insight/solution/takeaway)
3. **START ANY PRESENTATION** (Patrick Winston) → Craft empowerment promise; what will audience know by the end?

**Output:** Blueprint doc + 60-second opening promise

**Validation before moving to Phase 2:**
- ✓ One key message (not multiple competing ideas)
- ✓ Narrative arc feels natural (not forced)
- ✓ Opening empowerment promise is specific & outcome-driven ("By the end you'll be able to..." not "You'll learn about...")
- ✓ Audience will understand why this matters in first 60 seconds

---

### Phase 2: Structure (Architecture)
**Duration:** 45-90 min | **Goal:** Map slide-by-slide organization and core idea memorability

**Prompts in order:**
1. **STRUCTURE ANY TALK THAT PERSUADES** (Patrick Winston) → Build vision/proof/contributions framework (mirrored open/close)
2. **Design Slides** (existing KB) → Create slide titles, purposes, smooth transitions
3. **MAKE IDEAS UNFORGETTABLE** (Patrick Winston Star framework) → Design symbol/slogan/surprise for your core thesis

**Output:** Slide structure (5-8 slides) + core idea symbol/slogan/story

**Validation before moving to Phase 3:**
- ✓ Every slide has one job; no filler
- ✓ Flow is logical; transitions feel natural
- ✓ Core idea is visually/verbally memorable (symbol + slogan that people could repeat)
- ✓ Opening and closing mirror each other (promise made → promise kept)
- ✓ For PM presentations: Strategy slides (why/when/how) outnumber proof slides (data/examples)

---

### Phase 3: Content (Execution)
**Duration:** 1.5-2 hours | **Goal:** Fill slides with writing and visuals

**Prompts in order:**
1. **Write Slide Content** (existing KB) → Generate text for each slide (50-word constraint for PM slides)
2. **Generate visuals** (Canva MCP or Claude canvas) → Create mocks, charts, flows, user interfaces
3. Integrate visuals and text; ensure every visual supports the key message

**Output:** Completed slide deck (text + visuals)

**Validation before moving to Phase 4:**
- ✓ Every slide text supports the key message
- ✓ Mocks/visuals are specific and credible (not generic placeholder icons)
- ✓ PM presentations include: Strategy (why/when/how) + Proof (data/examples/mockups) + Contributions (what you're proposing)
- ✓ No slide is more than 50 words; font readable at distance

---

### Phase 4: Polish (Delivery)
**Duration:** 1-1.5 hours | **Goal:** Refine design, eliminate weaknesses, perfect the close

**Prompts in order:**
1. **Make Slides Pro** (existing KB) → Visual refinement, design consistency, color harmony
2. **ELIMINATE SLIDE CRIMES** (Patrick Winston) → Audit for: word count, font size, white space, reading slides aloud, final slide weakness
3. **END POWERFULLY** (Patrick Winston) → Design final 60 seconds; ensure contributions slide (not "questions" or "thank you")

**Output:** Polished, submission-ready deck

**Validation before submission:**
- ✓ Font ≥40pt everywhere; no more than 50 words per slide
- ✓ White space is strategic (not cramped); breathing room for audience brain
- ✓ Final slide is contributions/impact/call-to-action, never "Questions?" or "Thank You"
- ✓ Can present coherently without reading slides aloud
- ✓ Opening (promise) and closing (contributions) both reinforce key message
- ✓ Deck is 5-8 slides (not 15)

---

## PM Presentation Special Rules

For case interviews, product reviews, and pitch decks, enforce these constraints:

1. **Strategic Clarity:** Every slide advances either "why" (strategy) or "proof" (execution). Nothing else.
2. **Brevity:** 5-8 slides, period. Force ruthless prioritization.
3. **Opinionated without overconfidence:** Frame as "Here's what I'd do and why" not "Here's the only way."
4. **Credible mocks:** Mocks show you've *thought through* the user experience, not just dreamed it up.
5. **Metrics-driven:** Propose 2-3 specific metrics you'd measure, grounded in your strategy.

**Example:** "I'd measure pilot success on: (1) delivery success rate (target: 97%), (2) unit economics (target: $2.50 net margin per order), (3) customer satisfaction (target: ≥4.5/5). We'd know within 30 days if this works."

---

## How to Use: Step-by-Step

**1. Before you start:** Gather 2-3 resources you'll reference (your KB knowledge, market research, existing frameworks).

**2. Phase 1 (Foundation):** 
   - Run `/presentation-mastery` and request Phase 1
   - Answer prompts: topic, audience, desired outcome
   - Output: Blueprint + empowerment promise

**3. Phase 2 (Structure):**
   - Run `/presentation-mastery` and request Phase 2
   - Input: Blueprint + promise from Phase 1
   - Output: 5-8 slide structure + symbol/slogan for core idea

**4. Phase 3 (Content):**
   - Run `/presentation-mastery` and request Phase 3
   - Use **Canva MCP** or **Claude canvas** to generate visuals
   - Fill in text for each slide (50-word rule)

**5. Phase 4 (Polish):**
   - Run `/presentation-mastery` and request Phase 4
   - Input: Nearly-final deck from Phase 3
   - Output: Polished, submission-ready deck

**6. Submit:** Export as PDF and upload to application portal.

---

## Tools Integrated

- **Existing KB prompts:** `/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/` (6 prompts)
- **Patrick Winston frameworks:** `/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/` (6 new prompts)
- **Canva MCP:** For generating custom charts, user flows, mockups directly in slides
- **Claude canvas:** For quick visual prototypes (UI flows, wireframes)
- **/last30days:** For grounding strategy research in actual market/landscape data

---

## Reusability

This workflow applies to:
- ✓ Interview case study challenges (Instacart, Airbnb, Amazon, etc.)
- ✓ Product pitches to stakeholders or board
- ✓ PRD/project walkthroughs to engineering teams
- ✓ Conference talks and speaking engagements
- ✓ Personal portfolio presentations

Once you've used it once, the 4-phase rhythm becomes automatic and you can execute a full deck in 3-5 hours instead of days.

---

## First Use: Instacart Autonomous Delivery (April 2-4, 2026)

**Day 1 (April 2):** Research landscape + Phase 1 (Foundation)
- Run `/last30days` on autonomous delivery + last-mile logistics
- Phase 1: Build blueprint, narrative arc, empowerment promise
- Output: Opening promise + strategic angle locked

**Day 2 (April 3):** Phase 2 (Structure) + Phase 3 (Content, part 1)
- Phase 2: Build 5-8 slide structure + core idea symbol/slogan
- Phase 3: Write content for slides 1-4 (strategy slides)
- Output: Strategy slides with mocks

**Day 3 (April 4):** Phase 3 (Content, part 2) + Phase 4 (Polish)
- Phase 3: Write content for slides 5-8 (pilot slides) + generate final visuals
- Phase 4: Audit with ELIMINATE SLIDE CRIMES + END POWERFULLY
- Output: Polished 5-8 slide deck, ready to submit as PDF

**Delivery:** Submit as PDF via Greenhouse link by EOD April 4

---

## See Also

- `/AI-Knowledgebase/docs/plans/2026-04-02-presentation-mastery-design.md` — Full design doc
- `/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/` — All 12 prompts
```

**Step 3: Commit SKILL.md**

```bash
cd /Users/t-rawww
git add .claude/skills/presentation-mastery/SKILL.md
git commit -m "feat: create presentation-mastery skill

Skill: 4-phase workflow orchestrating 12 presentation prompts
- Phase 1 (Foundation): Blueprint → Story → START promise
- Phase 2 (Structure): STRUCTURE → Design Slides → Make Unforgettable
- Phase 3 (Content): Write Content → Generate Visuals
- Phase 4 (Polish): Make Pro → Eliminate Crimes → End Powerfully

Includes PM presentation special rules and full timeline for Instacart case study.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Phase B: Day 1 - Research + Foundation

### Task 3: Run landscape research with /last30days

**Files:**
- Create: `/Users/t-rawww/AI-Knowledgebase/docs/instacart-case-study/research-notes.md` (save findings here)

**Step 1: Run /last30days on autonomous delivery**

```bash
# Command (run in Claude Code)
/last30days autonomous delivery drones last-mile logistics --sources=hackernews,youtube --days=30
```

**Expected output:** 
- Hacker News discussions on autonomous delivery, drone regulation, last-mile cost analysis
- YouTube videos on drone delivery technology, pilot programs, market analysis
- Recent discussions on feasibility, challenges, economics

**Step 2: Synthesize key findings into research-notes.md**

Create `/Users/t-rawww/AI-Knowledgebase/docs/instacart-case-study/research-notes.md`:

```markdown
# Autonomous Delivery Research Notes (April 2, 2026)

## Key Findings from /last30days

### Market Landscape
- [Synthesize top 3-5 insights from HN]
- [Synthesize top 3-5 insights from YouTube]

### Constraints & Opportunities
- [What's actually blocking autonomous delivery at scale?]
- [Where is it working today?]
- [What's the regulatory landscape?]

### Economics
- [What are the cost savings projections?]
- [What's the payback period?]
- [When does it become profitable?]

### Gaps & Unknowns
- [What's NOT being discussed that you think matters?]
- [Where could you differentiate your strategy?]

## Personal Take (First Principles)
- [Your gut reaction to the landscape]
- [What angle feels underexplored?]
- [How does this connect to Instacart's specific challenge?]
```

**Step 3: Commit research notes**

```bash
cd /Users/t-rawww/AI-Knowledgebase
mkdir -p docs/instacart-case-study
git add docs/instacart-case-study/research-notes.md
git commit -m "research: autonomous delivery landscape analysis

Findings from /last30days research:
- Market constraints and regulatory landscape
- Cost economics and payback period analysis
- Existing pilot programs and lessons learned
- Gaps in current thinking

These notes inform strategy for Instacart case study.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

### Task 4: Execute Phase 1 (Foundation) - Build Blueprint

**Step 1: Run BUILD BLUEPRINT prompt**

Using the existing prompt at `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/build-blueprint/prompt.md`:

**Inputs:**
- Topic: Autonomous delivery strategy for Instacart
- Audience: Instacart leadership (VP Product, Head of Strategy)
- Goal: Present a differentiated autonomous delivery strategy + pilot plan

**Output:** Blueprint doc with:
- Objective (1 sentence)
- Audience analysis (2-3 sentences)
- Key message (1 sentence)
- Logical flow (5-7 slide topics)
- Recommended slide count (target: 6-8)

**Step 2: Save blueprint to**

`/Users/t-rawww/Instacart-APM-Challenge/01-blueprint.md`

---

### Task 5: Execute Phase 1 - Turn Into Story

**Step 1: Run TURN INTO STORY prompt**

Using existing prompt at `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/turn-into-story/prompt.md`:

**Inputs:**
- Topic: Autonomous delivery strategy
- Audience: Instacart leadership
- Desired outcome: Convince them this is a viable, differentiated approach

**Output:** Narrative arc with:
- Hook (establish tension)
- Problem (last-mile fulfillment challenge)
- Insight (where autonomous delivery wins)
- Solution (your strategy + pilot)
- Takeaway (key decision they should make)

**Step 2: Save narrative to**

`/Users/t-rawww/Instacart-APM-Challenge/02-narrative-arc.md`

---

### Task 6: Execute Phase 1 - START ANY PRESENTATION

**Step 1: Run START ANY PRESENTATION prompt**

Using new prompt at `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/start-any-presentation/prompt.md`:

**Inputs:**
- Topic: Autonomous delivery strategy for Instacart
- Audience: Product leadership
- Outcome: They know when/where autonomous delivery makes sense, what to test, how to measure success

**Output:**
- Empowerment promise (60 words max, specific)
- First 60 seconds script
- List of weak opens to cut

**Example empowerment promise:**
"By the end of this presentation, you'll understand exactly which customer segments benefit most from autonomous delivery, the specific economics that make it profitable, and a 90-day pilot that de-risks the bet before we scale."

**Step 2: Save opening to**

`/Users/t-rawww/Instacart-APM-Challenge/03-opening-promise.md`

---

### Task 7: Commit Phase 1 work

```bash
mkdir -p /Users/t-rawww/Instacart-APM-Challenge
cd /Users/t-rawww/Instacart-APM-Challenge

# Files already created in tasks 4, 5, 6
git add 01-blueprint.md 02-narrative-arc.md 03-opening-promise.md

git commit -m "feat: Phase 1 Foundation - Blueprint, Narrative, Opening Promise

- 01-blueprint.md: Strategic objective, audience, key message, slide flow
- 02-narrative-arc.md: Hook/problem/insight/solution/takeaway story structure
- 03-opening-promise.md: Empowerment promise + first 60 seconds script

Foundation locked. Ready for Phase 2 (Structure).

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Phase C: Day 2-3 - Strategy Slides + Pilot Slides

### Task 8: Execute Phase 2 (Structure) - STRUCTURE ANY TALK THAT PERSUADES

**Step 1: Run STRUCTURE ANY TALK THAT PERSUADES prompt**

Using new prompt at `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/structure-persuasive-talk/prompt.md`:

**Inputs:**
- Goal: Persuade Instacart leadership to pilot autonomous delivery
- Audience: Product leadership, CFO-level stakeholders
- What you want them to do: Approve a 90-day pilot in [specific geography]

**Output:**
- Vision statement (5-7 sentences: problem, new approach, why now)
- Proof of work (specific steps you'd take in pilot)
- 5-minute opening that establishes both vision and credibility
- Contributions close (final slide that mirrors opening promise)

**Step 2: Save structure to**

`/Users/t-rawww/Instacart-APM-Challenge/04-structure-vision-proof.md`

---

### Task 9: Execute Phase 2 - Design Slides

**Step 1: Run DESIGN EVERY SLIDE BEFORE YOU WRITE prompt**

Using existing prompt at `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/design-slides/prompt.md`:

**Inputs:**
- Topic: Autonomous delivery strategy + pilot
- Total slides: 7 (strategy 1-4, pilot 5-7)
- Blueprint: From Task 4

**Output:** Slide-by-slide structure:
- Slide 1: Title + empowerment promise
- Slide 2: The opportunity (why autonomous matters)
- Slide 3: When/where it works (market segmentation)
- Slide 4: The pilot (what we'll test, how we'll measure)
- Slide 5: MVP features (what we build)
- Slide 6: Learnings + metrics (how we'll know it works)
- Slide 7: Contributions (what this means for Instacart)

**Step 2: Save slide structure to**

`/Users/t-rawww/Instacart-APM-Challenge/05-slide-structure.md`

---

### Task 10: Execute Phase 2 - MAKE IDEAS UNFORGETTABLE

**Step 1: Run MAKE IDEAS UNFORGETTABLE prompt (Star framework)**

Using new prompt at `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/make-ideas-unforgettable/prompt.md`:

**Inputs:**
- Core idea: [Your thesis on autonomous delivery]
- Audience: Product leadership
- What you want them to remember: [One specific thing about your approach]

**Output:** Star framework:
- Symbol: A visual or object that represents your idea (e.g., "precision mapping")
- Slogan: A short, repeatable phrase (e.g., "Autonomous only where it works")
- Surprise: The counterintuitive insight (e.g., "Autonomous delivery succeeds by being selective, not universal")
- Salient idea: The one idea that sticks above everything else
- Story: How it all connects

**Step 2: Save Star framework to**

`/Users/t-rawww/Instacart-APM-Challenge/06-core-idea-star.md`

---

### Task 11: Write Phase 3 Content (Slides 1-4: Strategy)

**Step 1: Run WRITE SLIDE CONTENT prompt for slides 1-4**

Using existing prompt at `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/write-slide-content/prompt.md`:

**Inputs:**
- Slide titles: From Task 9 (slides 1-4)
- Key message: From Task 4 (blueprint)
- Constraint: 50 words per slide max, 40pt+ font

**Output:** Polished text for:
- Slide 1: Title + empowerment promise
- Slide 2: Why autonomous delivery (opportunity)
- Slide 3: When/where it makes sense (segmentation)
- Slide 4: The thesis (what we're proposing to test)

**Step 2: Save to Canva**

Create a Canva doc (or PDF template) and paste content:
- File: `/Users/t-rawww/Instacart-APM-Challenge/deck.canva` (or import to Canva web)

**Step 3: Generate visuals using Canva MCP**

For each of slides 1-4, use **Canva MCP** to generate:
- Slide 2: Chart showing last-mile fulfillment costs + opportunity sizing
- Slide 3: Map or table showing customer segments where autonomous works
- Slide 4: Flowchart showing autonomous delivery workflow (store → drone/robot → customer)

**Canva MCP prompts:**
```
"Create a chart showing the Instacart last-mile fulfillment cost breakdown (labor 60%, vehicle 25%, other 15%) and the opportunity to reduce costs by 30% with autonomous."

"Create a segmentation matrix showing which Instacart customer segments are best suited for autonomous delivery (high-density urban, frequent orders, shorter distances, no alcohol)."

"Create a flowchart showing the autonomous delivery workflow: customer order → store pickup → load robot/drone → autonomous delivery → customer delivery → return to hub."
```

**Step 4: Commit Phase 3 (part 1)**

```bash
cd /Users/t-rawww/Instacart-APM-Challenge
git add 04-structure-vision-proof.md 05-slide-structure.md 06-core-idea-star.md
git commit -m "feat: Phase 2 Structure - Vision/Proof, Slide Flow, Core Idea

- 04-structure-vision-proof.md: Vision statement, proof of work, 5-min opening, contributions close
- 05-slide-structure.md: 7-slide structure with titles and purposes
- 06-core-idea-star.md: Symbol/Slogan/Surprise/Salient/Story for core thesis

Structure locked. Ready for Phase 3 content.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

### Task 12: Write Phase 3 Content (Slides 5-8: Pilot)

**Step 1: Run WRITE SLIDE CONTENT prompt for slides 5-8**

Using existing prompt at `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/write-slide-content/prompt.md`:

**Inputs:**
- Slide titles: From Task 9 (slides 5-8: pilot slides)
- Key message: From Task 4
- Constraint: 50 words per slide max, 40pt+ font

**Output:** Polished text for:
- Slide 5: MVP features (what we build in 90 days)
- Slide 6: Pilot location + learnings framework
- Slide 7: Success metrics (3-4 specific metrics we'll measure)
- Slide 8: Contributions (what this means for Instacart's future)

**Step 2: Generate visuals for slides 5-8 using Canva MCP**

**Canva MCP prompts:**
```
"Create a 2x2 matrix showing MVP features vs. nice-to-have features for an autonomous delivery pilot (MVP: order qualification, delivery routing, exception handling; nice-to-have: autonomous return, bad-weather fallback)."

"Create a timeline showing the 90-day pilot phases: Week 1-2 (setup), Week 3-8 (operational), Week 9-12 (analysis/decide). Include key milestones."

"Create a dashboard mockup showing the 3 success metrics for autonomous delivery: (1) Delivery success rate (target 97%), (2) Unit economics (target $2.50 net margin), (3) Customer satisfaction (target 4.5/5)."

"Create a visual showing the future impact of autonomous delivery: Cost reduction trajectory, order volume expansion, customer experience improvement."
```

**Step 3: Assemble full deck in Canva**

- Import all 7 slides with text + visuals
- Ensure consistent branding, font size, color scheme
- Add slide transitions if desired

**Step 4: Commit Phase 3 (part 2)**

```bash
cd /Users/t-rawww/Instacart-APM-Challenge
git add deck.canva README.md  # Deck + notes

git commit -m "feat: Phase 3 Content - Full deck with text and mocks

- Slides 1-4: Strategy (why/when/where/what)
- Slides 5-7: Pilot (MVP/timeline/metrics)
- Slide 8: Contributions (future impact)
- All visuals: cost charts, segmentation, workflows, timelines, dashboards

Ready for Phase 4 polish.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Phase D: Final Polish

### Task 13: Execute Phase 4 - MAKE SLIDES PRO

**Step 1: Run MAKE SLIDES PRO prompt**

Using existing prompt at `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/make-slides-pro/prompt.md`:

**Inputs:**
- Current deck: From Task 12 (7 slides with text + visuals)
- Brand colors: Instacart green + neutral palette
- Design constraints: 40pt+ font, 50-word max per slide

**Output:** Refined visual design recommendations:
- Color harmony and consistency
- Typography polish (consistent font, hierarchy)
- Visual balance (white space, visual weight)
- Professional polish

**Step 2: Apply recommendations in Canva**

- Finalize typography (consistent font family, sizes, colors)
- Ensure white space is strategic (breathing room)
- Verify all visuals are high-quality (not pixelated, consistent style)

---

### Task 14: Execute Phase 4 - ELIMINATE SLIDE CRIMES

**Step 1: Run ELIMINATE SLIDE CRIMES prompt**

Using new prompt at `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/eliminate-slide-crimes/prompt.md`:

**Inputs:**
- Current deck: From Task 13 (7 polished slides)

**Output:** Audit against 10 slide crimes:
1. Too many slides (target: 5-8) ✓
2. Too many words (target: 50/slide max) ✓
3. Font under 40pt? → Fix if found
4. Reading slides aloud? → Flag if yes
5. Laser pointer usage? → Not relevant for PDF
6. Speaker standing far from slides? → Not relevant
7. No white space or air? → Flag if cramped
8. Background clutter/logos? → Ensure clean
9. Collaborators list as final slide? → Remove if present
10. "Thank you" or "Questions?" as final slide? → Remove if present

**Step 2: Apply fixes**

Address any crimes found. Ensure:
- Slide 7 is NOT "Questions?" or "Thank You"
- All fonts are 40pt minimum
- All slides have breathing room (white space)
- No more than 50 words per slide

---

### Task 15: Execute Phase 4 - END POWERFULLY

**Step 1: Run END POWERFULLY prompt**

Using new prompt at `/Users/t-rawww/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/end-powerfully/prompt.md`:

**Inputs:**
- Topic: Autonomous delivery strategy
- Key takeaway: What you want leadership to remember and do

**Output:**
- Contributions slide (final slide redesign if needed)
- Closing words (audience salute, benediction, or call to action)
- Final 60 seconds script

**Example final slide:**
```
CONTRIBUTIONS: Why This Matters

✓ Autonomous delivery reduces last-mile costs by 30%
✓ Pilot de-risks the bet in 90 days with clear metrics
✓ Path to $[X]M annual savings by 2027

Next step: Approve pilot in [City] by [Date]
```

**Step 2: Update slide 7 in Canva**

Replace final slide with contributions slide (not questions, not thank you).

---

### Task 16: Export and submit

**Step 1: Export deck as PDF**

```bash
# In Canva, export as PDF
# File: /Users/t-rawww/Instacart-APM-Challenge/Instacart_APM_Challenge_[YourName]_April2026.pdf
```

**Step 2: Final checklist**

- ✓ 5-8 slides (target: 7)
- ✓ Covers strategy (why/when/where) + pilot (what/how/metrics)
- ✓ Includes mocks/visuals (cost chart, segmentation, workflow, timeline, dashboard)
- ✓ Font ≥40pt throughout
- ✓ ≤50 words per slide
- ✓ Opening promise establishes key message
- ✓ Closing slide is contributions (not questions/thank you)
- ✓ Narrative arc flows naturally
- ✓ Can present without reading slides

**Step 3: Commit final deck**

```bash
cd /Users/t-rawww/Instacart-APM-Challenge
git add Instacart_APM_Challenge_[YourName]_April2026.pdf

git commit -m "feat: Final Instacart APM Challenge submission

- 7-slide deck: Strategy (slides 1-4) + Pilot (slides 5-7)
- Covers: Why/When/Where autonomy works, MVP features, metrics, future impact
- Visuals: Cost analysis, customer segmentation, delivery workflow, timeline, success dashboard
- Audited: Font ≥40pt, ≤50 words/slide, white space optimized
- Opening: Empowerment promise about knowing when/where/how to test
- Closing: Contributions slide (specific impact for Instacart)

Ready to submit via Greenhouse.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

**Step 4: Upload to Greenhouse**

Submit PDF via link provided in Instacart challenge.

---

## Success Criteria

✓ Skill is complete and usable  
✓ Patrick Winston prompts are integrated into KB  
✓ Instacart deck is 5-8 slides, coherent narrative  
✓ Deck includes strategy (research-grounded) + pilot (credible, metrics-driven)  
✓ Visuals are specific and professional (not generic)  
✓ Opening promise + closing contributions mirror each other  
✓ Deck differentiates on strategic rigor + execution depth (not just AI tool use)  
✓ Submitted by April 4, 2026 EOD  

---

## Notes

- **Research day (April 2):** Day 1 focused on grounding your strategy in actual landscape data
- **Build day (April 3):** Day 2 focused on structure, slide architecture, visual mocks
- **Polish day (April 4):** Day 3 focused on refinement and audit
- **Time-to-completion:** Each phase takes 1-2 hours if you're decisive and don't over-iterate
- **AI fluency differentiation:** Your AI tool use should be invisible (great mocks, not "look, AI!") and support your strategy, not replace it
