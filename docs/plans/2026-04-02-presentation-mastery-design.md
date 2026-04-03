# Presentation Mastery Skill Design

**Date:** 2026-04-02  
**Purpose:** Create a reusable presentation workflow skill that sequences existing KB prompts with Patrick Winston frameworks for any PM presentation (case studies, pitches, reviews, interview challenges).

---

## Problem Statement

You have scattered presentation design resources:
- 6 existing prompts (build-blueprint, design-slides, turn-into-story, write-slide-content, make-slides-pro, cut-presentation-down)
- 6 Patrick Winston frameworks (START, STRUCTURE, MAKE UNFORGETTABLE, END POWERFULLY, ELIMINATE CRIMES, PROPS/STORIES)

Without a coherent workflow, you have to manually decide *which* prompt to use *when*, and in what order. This wastes time and creates inconsistent results.

---

## Solution: "presentation-mastery" Skill

A structured, 4-phase workflow that:
1. **Sequences all 12 prompts** in logical order (foundation → structure → content → polish)
2. **Defines when to use each** (what questions trigger which prompt)
3. **Includes checklists** per phase (what to validate before moving forward)
4. **Emphasizes PM presentations** (strategic thinking + execution depth for case interviews)
5. **Reusable for any presentation** (pitches, PRD walkthroughs, conference talks, interview challenges)

---

## Workflow Architecture

### **Phase 1: Foundation (Strategic Thinking)**
**Goal:** Define *what* you're saying and *why*

- **Build Blueprint** prompt → Establish objective, audience, key message, logical flow
- **Turn Into Story** prompt → Map narrative arc (hook/problem/insight/solution/takeaway)
- **Patrick Winston: START** → Craft empowerment promise; what will audience know by the end?
- **Validation Checklist:**
  - ✓ One key message (not multiple competing ideas)
  - ✓ Narrative arc feels natural (not forced)
  - ✓ Opening empowerment promise is specific & outcome-driven
  - ✓ Audience will understand "why this matters in the next 60 seconds"

### **Phase 2: Structure (Architecture)**
**Goal:** Map slide-by-slide organization and core idea memorability

- **Patrick Winston: STRUCTURE** → Build vision/proof/contributions framework (mirrored open/close)
- **Design Slides** prompt → Create slide titles, purposes, transitions
- **Patrick Winston: MAKE IDEAS UNFORGETTABLE** → Design symbol/slogan/surprise for your core thesis
- **Validation Checklist:**
  - ✓ Every slide has one job; no filler
  - ✓ Flow is logical; transitions feel natural
  - ✓ Core idea is visually/verbally memorable (symbol + slogan)
  - ✓ Opening and closing mirror each other (promise made → promise kept)

### **Phase 3: Content (Execution)**
**Goal:** Fill slides with writing and visuals

- **Write Slide Content** prompt → Generate text for each slide (50-word constraint for PM slides)
- **Canva/Claude Canvas** → Generate AI mocks, charts, flows, user interfaces
- **Validation Checklist:**
  - ✓ Every slide text supports the key message
  - ✓ Mocks/visuals are specific, not generic placeholders
  - ✓ PM presentations include: strategy (why/when/how) + proof (data/examples) + contributions (what you're proposing)

### **Phase 4: Polish (Delivery)**
**Goal:** Refine design, eliminate weaknesses, perfect the close

- **Make Slides Pro** prompt → Visual refinement, design consistency
- **Patrick Winston: ELIMINATE SLIDE CRIMES** → Audit for: word count, font size, white space, reading slides aloud, final slide weakness
- **Patrick Winston: END POWERFULLY** → Design final 60 seconds; contributions slide only, no "thank you"
- **Validation Checklist:**
  - ✓ Font ≥40pt; no more than 50 words per slide
  - ✓ White space is strategic; not cluttered
  - ✓ Final slide is contributions/impact, not questions
  - ✓ Can present coherently without reading slides
  - ✓ Opening and closing both reinforce key message

---

## PM Presentation Special Rules

For case interviews, product reviews, and pitch decks, add these constraints:

1. **Strategic Clarity:** Every slide advances either "why" (strategy) or "proof" (execution). Nothing else.
2. **Brevity:** 5-8 slides, not 15. Force prioritization.
3. **Opinionated without overconfidence:** "Here's what I'd do and why" not "Here's the only way."
4. **Credible mocks:** Mocks show you've *thought through* the user experience, not just dreamed it up.
5. **Metrics-driven:** Propose specific metrics you'd measure, grounded in your strategy.

---

## Reusability

This workflow applies to:
- ✓ Interview case study challenges (Instacart, Airbnb, etc.)
- ✓ Product pitches to stakeholders
- ✓ PRD/project walkthroughs to engineering
- ✓ Conference talks and speaking engagements
- ✓ Personal portfolio presentations

---

## First Use: Instacart Autonomous Delivery Case Study

**Timeline:** 3 days (research Day 1, slides Day 2-3)

**Instantiation:**
1. Phase 1 (Foundation): Use blueprint + story + START prompts to lock strategy angle
2. Phase 2 (Structure): STRUCTURE + design-slides to map 5-8 slide flow
3. Phase 3 (Content): Write content + generate Canva mocks for autonomous delivery flows
4. Phase 4 (Polish): Make-slides-pro + eliminate-crimes + end-powerfully for final audit

**Differentiation:** 
- Research grounds strategy in reality (Day 1 `/last30days`)
- KB knowledge (evaluation, agentic patterns) informs pilot design naturally
- Patrick Winston frameworks ensure presentation rigor
- Skill ensures nothing is missed

---

## Skill File Structure

```
presentation-mastery/
├── SKILL.md (frontmatter + 4-phase workflow, PM rules, reusability)
├── phase-1-foundation.md (prompts + checklists)
├── phase-2-structure.md (prompts + checklists)
├── phase-3-content.md (prompts + checklists)
├── phase-4-polish.md (prompts + checklists)
├── pm-presentations.md (special rules + examples)
└── references/
    ├── patrick-winston-frameworks.md (6 prompts + WHEN to use each)
    ├── existing-prompts.md (6 existing KB prompts + WHEN to use each)
    └── case-study-example.md (Instacart walkthrough after completion)
```

---

## Dependencies

- Existing prompts already live in `/AI-Knowledgebase/future-reference/prompt-catalog/presentation-design/`
- Patrick Winston prompts (6) need to be added to same location as .md files with prompts + README
- This skill orchestrates them; doesn't replace them

---

## Success Criteria

- Skill is usable without thinking "which prompt do I use next?"
- PM presentations following this workflow differentiate on strategic rigor + execution depth
- Skill becomes your default for *any* presentation, not just case interviews
