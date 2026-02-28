# Zenkai — Design Document

**Date:** 2026-02-28
**Status:** Approved
**Repo:** `trentjhn/zenkai` (separate repository — this doc moves there when the repo is created)

---

## What Is Zenkai?

Zenkai is a personalized AI learning system that turns the AI Knowledgebase into a structured, visual, interactive learning experience. Named after the DBZ Zenkai boost — getting dramatically stronger after being pushed to your limits — it's built around the same principle: challenge, recover, come back sharper.

It is not a generic learning app. It is built specifically for one learner (Trenton), around one knowledge base, with one goal: genuine AI expertise for practical application in AI PM and engineering contexts.

---

## Core Design Principles

- **Structured over freeform** — a fixed roadmap, not an open sandbox
- **Practical over theoretical** — every concept framed around real-world AI work
- **Visual over textual** — diagrams and illustrations, not walls of text
- **Active over passive** — quizzes, confidence ratings, spaced repetition
- **Personal** — built for how this specific person learns

---

## Repository Structure

```
AI-Knowledgebase/    ← existing repo, untouched, pure knowledge
zenkai/              ← new repo, the learning app
  ├── frontend/      ← React + Tailwind + shadcn/ui + Framer Motion
  ├── backend/       ← FastAPI (Python)
  ├── database/      ← SQLite schema and migrations
  └── docs/          ← this design doc moves here
```

The learning app reads from the local path of the AI Knowledgebase. No shared repo, no coupling — just a configured path.

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
| 1 | Prompt Engineering | Atomic skill — everything else assumes this |
| 2 | Context Engineering | Natural extension of prompting |
| 3 | Reasoning LLMs | Specialized layer on top of standard models |
| 4 | Agentic Engineering | Where prompts + context + models become systems |
| 5 | Skills | How to package and distribute agentic behaviors |
| 6 | AI Security | Understanding risks once you know the power |
| 7 | Playbooks | Capstone — apply everything to real build scenarios |

Modules unlock sequentially. A module unlocks after hitting ≥70% quiz score on the previous module. Spaced repetition resurfaces weak concepts on a schedule.

---

## Module Structure

Each of the 7 topics becomes a module with consistent internal structure:

### 1. Concept Layer
Claude reads the KB doc and breaks it into 4–8 digestible concepts. Each concept includes:
- Plain-English explanation (2–3 paragraphs max)
- Visual: Mermaid diagram or Claude-generated SVG illustration
- Real-world example framed around AI roles and practical application
- Career callout box: "Why an AI PM needs to understand this"

### 2. Quiz Layer
Three question types per concept:
- **Multiple choice** — recognition and recall
- **Scenario-based** — applied judgment ("You're an AI PM and your RAG pipeline returns irrelevant results — what's your first diagnosis?")
- **Confidence rating** after each answer: Guessed / Somewhat sure / Knew it

Confidence ratings feed the spaced repetition engine. "Guessed" answers get scheduled for early review regardless of correctness.

### 3. Cheatsheet
Auto-generated one-pager per module. Visual summary of key concepts and patterns. Printable/saveable.

### 4. Audio Link
Direct link to the NotebookLM Audio Overview for the topic. User sets these up once by uploading KB docs to NotebookLM. One click opens the podcast version of the module.

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
modules          — module metadata, source file path, last_synced_commit
concepts         — individual concepts within each module
quiz_questions   — questions per concept (multiple choice + scenario)
user_progress    — per-concept performance history
review_schedule  — spaced repetition scheduling (next review date, interval)
sessions         — session history and duration
```

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
