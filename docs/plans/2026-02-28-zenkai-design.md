# Zenkai — Design Document

**Date:** 2026-02-28
**Status:** Approved
**Repo:** `trentjhn/zenkai` (separate repository — this doc moves there when the repo is created)

---

## What Is Zenkai?

Zenkai is a personalized AI learning system that turns the AI Knowledgebase into a structured, visual, interactive learning experience. Named after the DBZ Zenkai boost — getting dramatically stronger after being pushed to your limits — it's built around the same principle: challenge, recover, come back sharper.

It is not a generic learning app. It is built specifically for one learner (Trenton), around one knowledge base, with one goal: genuine AI expertise for practical application in AI PM and engineering contexts.

### Why This Exists — The Context

Trenton is a Yale CS grad with 1.5 years of Technical PM experience at PayPal, currently navigating a difficult job market after a layoff. The traditional PM career path is increasingly saturated and being disrupted — entry-level roles are shrinking, credentials are decoupling from actual skill, and the gap between those who understand AI deeply and those who merely use it is widening fast.

The strategic bet: AI PM is an undersupplied role. The people who will fill it need a combination that's currently rare — enough technical depth to reason about AI systems, enough product thinking to connect those systems to outcomes, and the specification literacy to direct AI with precision. Generic PM experience is a commodity. AI fluency built on genuine understanding is not.

Zenkai exists to build that combination deliberately, in the gap between jobs, so that when the opportunity arrives the foundation is already there — not assembled in a panic but built through structured, spaced, applied learning.

---

## Core Design Principles

- **Structured over freeform** — a fixed roadmap, not an open sandbox
- **Practical over theoretical** — every concept framed around real-world AI work
- **Visual over textual** — diagrams and illustrations, not walls of text
- **Active over passive** — quizzes, confidence ratings, spaced repetition
- **Personal** — built for how this specific person learns
- **AI through a PM lens** — every AI concept learned in the context of what an AI PM would actually do with it

---

## Repository Structure

```
AI-Knowledgebase/    ← existing repo, untouched, pure general-purpose knowledge
zenkai/              ← new repo, the learning app
  ├── frontend/      ← React + Tailwind + shadcn/ui + Framer Motion
  ├── backend/       ← FastAPI (Python)
  ├── database/      ← SQLite schema and migrations
  ├── pm-context/    ← AI PM knowledge source (lives here, NOT in the KB)
  │   ├── ai-pm-role.md         ← what the AI PM role actually is
  │   ├── pm-fundamentals.md    ← core PM frameworks (discovery, roadmap, metrics, PRDs)
  │   ├── ai-pm-applications.md ← how each AI concept maps to PM decisions/responsibilities
  │   └── interview-scenarios.md ← AI PM interview questions and case studies
  └── docs/          ← this design doc moves here
```

**Three-layer architecture — this is intentional:**

1. **AI Knowledgebase** — general, clean, reusable by any project. No PM specificity. Never polluted with role-specific framing.
2. **PM Context** (`zenkai/pm-context/`) — AI PM-specific knowledge. Lives inside Zenkai, not the KB. Contains the role framing, PM fundamentals, and application mappings.
3. **Zenkai** — the learning layer. Reads from both sources and weaves them together. Every AI concept gets the technical explanation from the KB *and* the PM application from the PM context.

The learning app reads from the local path of the AI Knowledgebase and from its own PM context directory. No shared repo, no coupling — just configured paths.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Tailwind CSS + shadcn/ui (heavily customized) |
| Animations | Framer Motion (spring physics) |
| Backend | FastAPI (Python) |
| Database | SQLite (local, persistent) |
| AI | Claude claude-sonnet-4-6 via Anthropic API |
| Diagrams | Mermaid.js + Claude-generated SVGs |
| Audio | NotebookLM Audio Overviews (manual setup, linked per module) |
| Design system | Generated via ui-ux-pro-max skill before build |

---

## Visual Design

**Mode:** Dark mode primary

**Color palette:**
- Background: `#09090b` (Zinc-950, near-black — never pure black)
- Surface/cards: `#18181b` (Zinc-900)
- Primary accent: `#9B8EC4` (Trunks purple — muted, cool, desaturated violet)
- Secondary accent: `#00D4C8` (Electric teal — progress, action, active states)
- Text primary: `#fafafa` (near-white)
- Text muted: `#a1a1aa` (Zinc-400)

**Typography:** Geist or Satoshi (not Inter)

**Design language (from frontend-taste skill):**
- DESIGN_VARIANCE: 8 — asymmetric layouts, not centered grids
- MOTION_INTENSITY: 6 — fluid CSS + Framer Motion spring physics
- VISUAL_DENSITY: 4 — daily app mode, generous but not sparse

**Anti-patterns to avoid:** generic card grids, neon glows, purple gradients, Inter font, centered hero layouts

---

## Learning Roadmap

Fixed sequence — each topic builds on the previous:

| # | Topic | Why This Order |
|---|---|---|
| 0 | AI PM Foundations | Establishes the PM mental model before AI concepts begin |
| 1 | Prompt Engineering | Atomic skill — everything else assumes this |
| 2 | Context Engineering | Natural extension of prompting |
| 3 | Reasoning LLMs | Specialized layer on top of standard models |
| 4 | Agentic Engineering | Where prompts + context + models become systems |
| 5 | Skills | How to package and distribute agentic behaviors |
| 6 | AI Security | Understanding risks once you know the power |
| 7 | Playbooks | Capstone — apply everything to real build scenarios |

**Module 0 — AI PM Foundations** is a short prerequisite module that reads from `pm-context/` rather than the AI KB. It covers: what an AI PM actually does, how the role differs from traditional PM, core PM frameworks (discovery, roadmap, prioritization, metrics, PRDs), and why specification is the AI PM's primary technical contribution. This gives context for every PM lens applied in Modules 1–7 — without it, the AI PM application sections would lack grounding.

Modules unlock sequentially. A module unlocks after hitting ≥70% quiz score on the previous module. Spaced repetition resurfaces weak concepts on a schedule.

---

## Module Structure

Each of the 7 topics becomes a module with consistent internal structure:

### 1. Concept Layer
Claude reads from *both* the KB doc and the PM context source simultaneously, then generates each concept with:
- Plain-English explanation (2–3 paragraphs max)
- Visual: Mermaid diagram or Claude-generated SVG illustration
- Real-world example framed around AI roles and practical application
- **AI PM Application section** (see below — this is the core PM integration layer)

### AI PM Application Section (per concept)
This is not a brief callout. It is a full section on every concept covering:
- **What this means for your role** — how this concept shows up in an AI PM's day-to-day work
- **Decisions you'd own** — what calls an AI PM makes that require understanding this concept
- **Questions to ask your engineering team** — how to engage technically without writing the code
- **How to evaluate it** — what good looks like vs. what red flags look like
- **Specification angle** — how you'd write a clear spec for a system that uses this concept

Example for RAG: "As an AI PM, you don't build the RAG pipeline — but you own the decision of whether RAG is the right architecture for your feature, you define the quality bar for what 'relevant' means, you write the acceptance criteria that determines whether retrieval is working, and you're the one who has to explain to stakeholders why the chatbot said something wrong."

The PM application section is generated by Claude using *both* the KB content (technical depth) and the PM context source (role framing and responsibility mapping). This is what makes Zenkai different from any general AI learning tool — the PM lens is structural, not cosmetic.

### 2. Quiz Layer
Three question types per concept:
- **Multiple choice** — recognition and recall
- **Scenario-based** — applied judgment, always framed in AI PM contexts
- **Confidence rating** after each answer: Guessed / Somewhat sure / Knew it

**All scenario questions are set in AI PM contexts.** Not "what is HyDE?" but "Your team proposes using HyDE for query enhancement in your RAG pipeline. What questions do you ask before approving it? What tradeoffs are you evaluating?" Not "what is prompt injection?" but "You're reviewing the security posture of your company's customer-facing AI chatbot. What attack vectors do you prioritize and how do you communicate the risk to your non-technical stakeholders?"

This is where the specification literacy muscle gets built. The scenario questions are testing whether you understand a concept well enough to *direct* a system built on it — which is the AI PM's core function.

Confidence ratings feed the spaced repetition engine. "Guessed" answers get scheduled for early review regardless of correctness.

### 3. Cheatsheet
Auto-generated one-pager per module. Visual summary of key concepts and patterns. Printable/saveable.

### 4. Audio Link
Direct link to the NotebookLM Audio Overview for the topic. User sets these up once by uploading KB docs to NotebookLM. One click opens the podcast version of the module.

---

## AI PM Integration Architecture

### Why This Isn't Just a "Career Callout"

The original design had a small career callout box per concept. That's not sufficient. The goal isn't to remind yourself that AI is relevant to PM work — the goal is to build the specific judgment an AI PM needs: understanding AI systems deeply enough to specify them, evaluate them, diagnose them when they fail, and communicate about them to non-technical stakeholders.

That requires the PM lens to be structural — woven into how every concept is explained, what every quiz question tests, and what every cheatsheet summarizes. It's a lens, not a module.

### The Two-Source Generation Pattern

When Zenkai generates content for any AI concept, the backend provides Claude with:

1. **The KB content** — the technical explanation from the AI Knowledgebase (e.g., the RAG section from `building-rag-pipelines.md`)
2. **The PM context** — the relevant section from `pm-context/ai-pm-applications.md` that maps this concept to AI PM responsibilities

Claude's generation prompt instructs it to synthesize both: explain the concept with technical accuracy, then explicitly connect it to the PM decision space. The output isn't "here's RAG, and by the way it's relevant to PM" — it's "here's RAG as understood by someone whose job is to own the decision of whether and how to use it."

### PM Context Source — What It Contains

`zenkai/pm-context/` is a lean, focused knowledge source — not a comprehensive PM textbook. It contains exactly what's needed to make the AI concepts land in a PM context:

**ai-pm-role.md**
What the AI PM role actually is. How it differs from traditional PM. The specific responsibilities: owning AI feature specs, defining quality bars for model behavior, writing acceptance criteria for AI systems, managing the model lifecycle, communicating AI capabilities and limitations to stakeholders and executives. Why specification is the AI PM's primary technical contribution.

**pm-fundamentals.md**
Core PM frameworks as they apply to AI products: product discovery (but for AI features), roadmap prioritization when the technology is probabilistic, success metrics for AI systems (where standard conversion metrics often fail), PRD structure for AI features, how to write a brief that an engineering team can actually build from.

**ai-pm-applications.md**
The concept-by-concept mapping. For each major AI concept in the KB (prompt engineering, context management, RAG, agent architectures, security), this document answers: what decisions does an AI PM make that require understanding this? What does owning this look like in practice? What are the failure modes an AI PM needs to catch?

**interview-scenarios.md**
AI PM interview questions and case studies. Real scenarios drawn from the types of questions that surface in AI PM interviews: system design from a product perspective, evaluating AI tradeoffs, handling model failures in production, communicating risk. Used to generate practice questions in the quiz layer.

### The Specification Literacy Loop

Every concept, the cycle is:
1. Understand the concept technically (from KB content)
2. Understand what it means to own it as a PM (from PM context)
3. Practice specifying for it through scenario quiz questions
4. Confidence rating surfaces whether you actually know it or are guessing

The scenario questions are the mechanism. "Your team proposes using HyDE for query enhancement. What questions do you ask? What tradeoffs are you evaluating?" tests whether you understand HyDE well enough to direct a team building with it. That's specification literacy applied directly to the AI PM function.

---

## Three Main Screens

### Dashboard / Roadmap
Bento-style grid of 7 topic cards. Each card shows: topic name, completion %, progress ring, locked/unlocked state, new content indicator. Teal accent for progress rings and unlock animations. Purple accent for active/selected module. Clean, high-end SaaS feel.

### Module View
Split layout:
- **Left sidebar:** concept list with checkmarks and current concept highlighted
- **Right main area:** concept title → explanation → visual → career callout
- **Top right:** Audio Overview button (opens NotebookLM)
- Clean reading experience, nothing competing for attention

### Quiz Screen
Full focus mode — sidebar collapses, question and answers centered. Progress bar at top. After each answer: immediate feedback with explanation, then confidence rating prompt. Framer Motion spring transitions between questions. No jarring jumps.

---

## Content Sync — Delta Update System

The KB is git-tracked. The learning system stores the git commit hash it last generated each module from (`last_synced_commit` in SQLite).

**On new KB content:**
1. System detects changed files via git diff against stored commit hash
2. Only the new/changed sections are processed — not the full doc
3. New concepts are generated and appended to the existing module
4. Existing quiz scores and spaced repetition schedule are untouched
5. User sees notification: "N new concepts added to [Module] since you last studied it"

**On new KB folder/topic:**
System detects new markdown file, generates full module, suggests roadmap placement.

This means the learning system evolves alongside the knowledge base without resetting progress.

---

## SQLite Schema (Core Tables)

```
modules          — module metadata, source file path, last_synced_commit, pm_context_path
concepts         — individual concepts within each module
quiz_questions   — questions per concept (multiple choice + scenario, tagged by type)
user_progress    — per-concept performance history
review_schedule  — spaced repetition scheduling (next review date, interval)
sessions         — session history and duration
```

`pm_context_path` on the modules table points to the relevant PM context file used during content generation. Module 0 has no KB source — only a PM context path. Modules 1–7 have both.

---

## Learning Science Implementation

| Principle | Implementation |
|---|---|
| Spaced repetition (Ebbinghaus) | Review intervals double on success, reset on failure |
| Active recall (Roediger & Karpicke) | Quiz before re-reading, not after |
| Metacognitive monitoring | Confidence rating after every answer |
| Scaffolded learning (Vygotsky ZPD) | Module gating — unlock only when ready |
| Cognitive load theory (Sweller) | Max 4–8 concepts per module, one concept per screen |
| Dual coding (Paivio) | Every concept has both text explanation and visual |

---

## Implementation Notes

- Run `ui-ux-pro-max` skill first to generate `DESIGN.md` before touching code
- Use `frontend-taste` skill as the active design skill during frontend build
- Use `web-design-patterns` skill for component architecture
- shadcn/ui components used but heavily customized — never default state
- NotebookLM setup is manual (user uploads KB docs once) — not automated
- Backend reads KB from configured local path, not bundled content

---

## Out of Scope (V1)

- Mobile app (potential V2 after local version works)
- Multi-user / sharing
- Public deployment
- Video generation
- Automated NotebookLM integration
