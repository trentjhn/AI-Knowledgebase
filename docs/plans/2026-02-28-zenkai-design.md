# Zenkai — Design Document

**Date:** 2026-02-28
**Status:** Approved — design complete, known issues documented below
**Repo:** `trentjhn/zenkai` (separate repository — this doc moves there when the repo is created)

---

## Known Issues — Fix Before Building

These are gaps identified in the Gemini design system output. Every item here must be resolved before or during the first implementation sprint. Do not treat the Gemini code as production-ready as-is.

### Code Fixes (must resolve before touching any component)

**1. Register CSS variables are missing from globals.css**
The JSX files reference `var(--register-study-bg)` and `var(--register-battle-bg)` inline, but these are never declared as CSS custom properties. They're defined in `tailwind.config.js` as `register.study` and `register.battle` but that only creates Tailwind classes, not CSS variables. Add to `:root` in `globals.css`:
```css
--register-study-bg: 235 21% 11%;   /* Cool/contemplative */
--register-battle-bg: 280 25% 14%; /* Warm/dynamic */
```

**2. Wrong module names throughout — must be replaced**
Gemini invented placeholder module names: "Neural Basics I", "Deep Learning I", "Zenkai Dōjō", etc. The actual Zenkai roadmap is:
- Module 0: AI PM Foundations
- Module 1: Prompt Engineering
- Module 2: Context Engineering
- Module 3: Reasoning LLMs
- Module 4: Agentic Engineering
- Module 5: Skills
- Module 6: Evaluation
- Module 7: Fine-tuning
- Module 8: AI Security
- Module 9: Playbooks

Replace all placeholder names in `world-map/page.tsx` module data array and anywhere else they appear.

**3. Body font is wrong**
`tailwind.config.js` sets `fontFamily.body` to `Inter`. The design specifies **Geist or Satoshi** (not Inter). Update before any component is built — changing it after touches every text element.

**4. ConceptCard props don't match content generation output**
The current `ConceptCard` accepts generic `concept` and `depthContent` string props. It needs to accept the structured JSON our generation prompts (1a and 1b) actually produce:
```tsx
interface ConceptCardProps {
  defaultLayer: {
    title: string
    hook: string
    explanation: string[]
    analogy: string | null
  }
  deepLayer: {
    mechanism: string[]
    edge_cases: string[]
    key_number: string
    failure_story: string
  }
}
```
Without this fix the content pipeline has no way to render generated content correctly.

---

### Assets — Blocked Until Created

The following image files are referenced in code but do not exist. Every `<Image>` tag in the Gemini output will render a broken image until these are created. Recommended path: build all screens with colored placeholder `<div>` elements first, swap in real assets when ready.

| Asset | Referenced In | How to Create |
|---|---|---|
| `/assets/map/map-base.png` | world-map/page.tsx | Pixel art world map — Midjourney or Aseprite |
| `/assets/map/fog-overlay.png` | world-map/page.tsx | Semi-transparent mist layer — CSS may suffice |
| `/assets/sprites/ronin_idle_walk.png` | world-map/page.tsx | Form 1 samurai sprite — Midjourney pixel art |
| `/assets/sprites/warrior_battle_idle.png` | quiz/battle/page.tsx | Form 2 combat sprite |
| `/assets/sprites/evolution_forms_strip.png` | character-sheet/page.tsx | All 4 forms side-by-side strip |
| `/assets/ui/segmented_bar_texture.png` | quiz/battle/page.tsx | CSS alternative likely simpler |

**Recommendation:** Replace all `<Image src="...">` tags with `<div className="bg-zen-slate border border-zen-plasma/30 flex items-center justify-center">` placeholders during build. Label each with the asset name as text. Swap real art in once the UI is fully functional.

---

### Components — Concept Only, Not Yet Coded

These components are designed and specced but have no implementation code yet. They need to be built during the implementation sprint:

| Component | Status | Notes |
|---|---|---|
| Prediction question | Spec only | Pre-concept MC question, answer revealed after explanation |
| Confidence rating chips | Spec only | Candle/flame/fire icons, three states, required after every answer |
| Worked annotated example | Spec only | Artifact inspection frame, floating rune tags, speech bubble on click |
| Spec writing exercise | Spec only | Monospace textarea, FORGE SPEC button, submission particle effect, model answer reveal |
| Cheatsheet | Spec only | 3-column mini-scroll grid, hover tooltip, golden seal for mastered concepts |

---

### Design Validation Needed

**Color palette may not match Pinterest images.** Gemini generated the color system from its training data (the palette resembles Tokyo Night, a VS Code theme), not from the actual Pinterest inspiration images uploaded. The `zen-gold`, `zen-plasma`, and `zen-sakura` values should be validated visually once the app is running — they may need to be pulled closer to the muted deep navy, vermillion red, and earthy amber from the samurai reference images. Do not permanently lock in the palette until you've seen it rendered at full scale.

---

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
| 6 | Evaluation | How to measure whether AI systems are working — connects to every module |
| 7 | Fine-tuning | Customizing model behavior — completes the prompting → RAG → fine-tuning picture |
| 8 | AI Security | Understanding risks once you know the power |
| 9 | Playbooks | Capstone — apply everything to real build scenarios |

**Module 0 — AI PM Foundations** is a short prerequisite module that reads from `pm-context/` rather than the AI KB. It covers: what an AI PM actually does, how the role differs from traditional PM, core PM frameworks (discovery, roadmap, prioritization, metrics, PRDs), and why specification is the AI PM's primary technical contribution. This gives context for every PM lens applied in Modules 1–7 — without it, the AI PM application sections would lack grounding.

Modules unlock sequentially. A module unlocks after hitting ≥70% quiz score on the previous module. Spaced repetition resurfaces weak concepts on a schedule.

---

## Module Structure

Each of the 9 topics (plus Module 0) becomes a module with consistent internal structure:

### 1. Concept Layer

Each concept is a layered card — not a wall of text. Two depths, learner-controlled:

**Default view (what loads first):**
- **Prediction question** — one MC question *before* the explanation loads. Forces a guess, primes the brain. Answer revealed after the full explanation.
- **Hook + plain-English explanation** — why this matters, then what it is. ~200 words. Analogy where one fits naturally.
- **Visual** — Mermaid diagram or Claude-generated SVG. Always present.
- **Quick check** — one MC question immediately after. Locks in the concept before moving on.

**"Go Deeper" tap (learner-initiated):**
- How it actually works mechanically — the real internals, not just the surface description
- Edge cases and nuances
- Research numbers and empirical findings where available (e.g., "Zero-shot CoT pushed MultiArith accuracy from 17.7% to 78.7%")
- One real-world failure mode as a brief story — what happened when someone got this wrong

The quiz questions test material from *both* layers. To hit 70% and unlock the next module, learners will naturally need to engage with the deeper layer on most concepts. Depth is self-directed but structurally incentivized.

**Three enhancements applied across every concept:**

1. **Prediction question (pre-concept)** — Before the explanation loads, one question appears testing what the learner already suspects. Wrong guesses are expected and fine — the act of forming a prediction is the mechanism. After the full explanation is read, the prediction answer is revealed with context.

2. **Worked, annotated examples** — After the explanation (default or deep layer), at least one real artifact showing the concept applied: an actual prompt using the technique, an actual architecture diagram with components labeled, an actual bad-vs-good comparison. Callouts point to where the concept is visible. This bridges "I understand the concept" and "I can recognize it in practice."

3. **Spec writing micro-exercise (per module, not per concept)** — At the end of each module's concept layer, a 2-minute applied exercise. Given a scenario, write: one acceptance criterion, or the one question you'd ask your engineering team, or identify the failure mode in a described system. One or two sentences typed in, then compared to a model answer with explanation. Builds specification literacy directly — the actual PM skill, not just knowledge about it.

**Real failure case (per module):** One short story (3–4 paragraphs) about a real AI system failure, analyzed through the lens of what the module covers. Placed before the module quiz. Makes the stakes real and creates a memorable anchor for abstract concepts. Examples: Air Canada's chatbot promising unauthorized refunds (agentic engineering, authority scoping), Amazon's hiring algorithm (evaluation, metric gaming), Microsoft Tay (alignment, RLHF gone wrong).

**Concept connections:** After each concept, a brief visual thread showing how it connects to concepts learned in previous modules and where it leads in future modules. Builds the web rather than isolated nodes.

### AI PM Application Section (per module, not per concept)
Each module has one lightweight PM application section — not a section on every individual concept. This is intentional. Zenkai's primary goal is AI learning. The PM context is a lens, not the subject.

The PM section appears at the end of each module's concept layer. It covers:
- **What this module means for your role** — how these concepts show up in an AI PM's actual work (2–3 sentences)
- **The key decision** — what call does an AI PM make that requires understanding this module's content
- **One question to ask your team** — a single pointed question that reveals whether the engineering team has thought it through

This section is generated from *both* the KB content (for technical grounding) and `pm-context/ai-pm-applications.md` (for role-specific framing). It's a 150–200 word supplement, not a parallel curriculum. The goal is to anchor the AI learning in practical context — not to teach PM fundamentals inside every module.

Example for RAG (module-level, not per-concept): "As an AI PM on a product using RAG, you own the decision of whether RAG is the right architecture, define the quality bar for retrieval relevance, and write the acceptance criteria that determines whether the system is working. The question to bring to your engineering team: 'What's our evaluation strategy for both retrieval quality and answer faithfulness — and how will we know when they degrade in production?'"

### 2. Quiz Layer

**The goal is interactive and fun — not a typing exercise.** Every question is multiple choice. No short answer, no fill-in-the-blank. The learning happens through choosing between plausible options and understanding why the right answer is right — not through recalling a definition on demand.

**Question formats:**

- **Multiple choice (4 options)** — Always. Distractors are plausible, not obviously wrong. The wrong answers represent common misconceptions or real tradeoffs, so evaluating them teaches something even when you're wrong.
- **Scenario-based MC** — "You're an AI PM and X is happening. What do you do?" Four options, each representing a different judgment call. These are the primary question type — recognition of a named concept is less valuable than knowing what to do when you encounter it.
- **Ordering questions** — "Put these steps in the right sequence." Drag-and-drop. Used for process concepts (RAG pipeline stages, agent loop, spec review checklist).
- **Match the pairs** — Match a pattern to its use case, a failure mode to its symptom, a framework to the problem it solves. Used for taxonomy-heavy concepts.

**All scenario questions are set in AI PM contexts.** Not "what is HyDE?" but "Your team proposes using HyDE for query enhancement in your RAG pipeline. What questions do you ask before approving it?" Four options — each a plausible PM response, only one correct. Not "what is prompt injection?" but "You're reviewing the security posture of your customer-facing AI chatbot before launch. Which of the following is the most critical thing to verify?"

**After every answer:**
1. **Immediate feedback** — correct/incorrect with a 1–2 sentence explanation of why. Not just "correct!" — the explanation is part of the learning.
2. **Confidence rating** — a second tap: Guessed / Somewhat sure / Knew it. This is separate from correctness. Getting it right on a guess still schedules an early review.
3. **Framer Motion spring transition** — smooth animated reveal of feedback, then transition to next question. No jarring cuts.

**Quiz UX — full focus mode:**
- Sidebar collapses completely when quiz starts
- Question card centered, large type, breathing room
- Four answer options as tappable cards — not a radio button list
- Selected answer highlights before reveal
- Correct answer glows teal on reveal; incorrect answer dims and correct answer illuminates
- Progress bar at top showing position in quiz set
- Streak counter visible — consecutive correct answers build a visible streak

**Source material for scenario questions:**
- `pm-context/interview-scenarios.md` — 4 categories of realistic AI PM scenarios (system design, evaluating tradeoffs, production failures, risk communication). Used as generation source for scenario-based MC questions.
- KB concept sections — used to generate recognition and application questions per concept.

Confidence ratings feed the spaced repetition engine. "Guessed" answers get scheduled for early review regardless of correctness. A correct answer with "Guessed" confidence is not trusted — it gets resurfaces on the same schedule as a wrong answer.

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

## Design System — From Gemini Session

The full design system was generated via Gemini with Pinterest pixel art / Japanese samurai / JRPG inspiration images. Source files live in the Zenkai repo. Key decisions captured here:

### Tech Foundation
- `tailwind.config.js` — all color tokens, dual-font system, `ma` spacing, `clipped-corners` clip-path utility
- `globals.css` — CSS custom properties for all registers and color tokens
- All components use `clipped-corners` — no border-radius anywhere
- All interactive elements use `ma` (24px) padding rule
- Study/contemplative components: `bg-zen-slate` + `zen-plasma` accents
- Battle/active components: `bg-zen-void` + `zen-sakura` or `zen-gold` accents

### Color Tokens
```
zen-gold:   #F4D03F  — primary, headers, active states
zen-void:   #1A1B26  — deepest background
zen-slate:  #24283B  — card surfaces
zen-sakura: #FF4D6D  — battle/danger/wrong answer
zen-plasma: #7AA2F7  — spirit/correct/deeper layer accent
register-study-bg:  235 21% 11%  — cool, contemplative
register-battle-bg: 280 25% 14% — warm, dynamic
```

### AI Integration Prompt (use to maintain consistency)
> "Use the provided tailwind.config.js and globals.css. Every component must use the clipped-corners utility. All interactive elements must use the 'Ma' padding rule (24px). For Study/Contemplative components, use bg-zen-slate and zen-plasma accents. For Battle/Active components, use bg-zen-void and zen-sakura or zen-gold accents."

---

## Three Main Screens

### World Map (Dashboard)
The overworld — not a card grid. A pixel art map with 10 module regions connected by a winding path. Each region has its own atmospheric identity. Locked regions obscured by fog-of-war mist overlay. Active region visually alive. Completed regions marked with a golden Z seal. User's samurai avatar traverses the map, animating to each selected region. Module status panel below the map with "Enter Dōjō" / "Revisit Dōjō" CTA.

### Module View (Contemplative Register — cool tones)
Split layout: left sidebar (quest log style, concept list with checkmarks) + right main area (concept card). Sidebar functions like a Pokédex or inventory panel. Top right: NotebookLM audio link. Reading experience is the priority — nothing competing for attention.

### Quiz Screen (Battle Register — warm tones)
Full Pokémon battle layout. Challenge/question at top. User's samurai avatar idle in corner. Four move cards at bottom. Segmented streak bar replacing HP bar — fills from crimson (low streak) to plasma blue (high streak). Correct answer: flash + green glow. Wrong answer: screen shake + red dim. After reveal: confidence chips (see below). Framer Motion step transitions — game-feel, not SaaS-fade.

### Character Sheet
Warm/dynamic register. Current samurai form displayed large. Evolution timeline showing all four forms with current form highlighted. Equipment list (Skyrim-style accumulation per module). Stat bars per knowledge domain. XP progress bar to next form evolution.

---

## Component Decisions

### Confidence Rating Chips — Candle / Flame / Fire
Three chips shown after every quiz answer. Visual metaphor: confidence as heat.
- **Guessed** → single candle icon, muted grey border, neutral register
- **Somewhat sure** → flame icon, warm yellow glow, warming register
- **Knew it** → roaring fire icon, plasma blue aura, intense register

This is the design. Do not reduce to text labels.

### ConceptCard — Dual Layer
```
Props: { defaultLayer: { title, hook, explanation[], analogy }, deepLayer: { mechanism[], edge_cases[], key_number, failure_story } }
```
Default view: hook + explanation + analogy. "Go Deeper" button reveals deep layer via AnimatePresence height animation — feels like a scroll unfurling. Button copy: "Go Deeper" → "Close Scroll". Left border accent in `zen-plasma`.

### Worked Annotated Example — Artifact Inspection
Framed as examining a discovered artifact. Shadowbox container with paper-texture CSS overlay. Floating rune/tag markers (+ icons) positioned over key parts of the example. Clicking a marker reveals a pixel speech bubble explaining why that part demonstrates the concept. Copy: examining, not reading.

### Spec Writing Exercise — Forge the Vision
Large multi-line textarea, monospace font. CTA button: **FORGE SPEC** (not "Submit"). On submission: brief sparks/fire particle effect triggers (not during typing — submission only). Reveals model answer + "What makes it strong" explanation after submission.

### Cheatsheet — The Inventory
3-column grid of "Mini-Scrolls." Hover reveals Quick Reference tooltip. Concepts with SRS interval > 30 days show a small golden seal (mastered). Layout functions like an item compendium or Pokédex completion screen.

### Samurai Character Evolution
Four forms, same character, progressively more powerful:
- **Form 1 — Ronin:** Simple gi, straw hat, one katana, meditating idle. No armor.
- **Form 2 — Warrior** (after Module 3): Light leather armor, blue scarf, second blade, combat stance.
- **Form 3 — Samurai** (after Module 6): Full dark plate, elaborate kabuto, golden crest, nodachi.
- **Form 4 — The Ghost/Zenkai** (after Module 9): Semi-translucent, plasma-blue aura, sakura petals drifting. Ghost of Tsushima reference made visual.

Evolution animations are full-screen moments — flash sequence, silhouette transform, form name reveal. The most emotionally significant events in the app.

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

## Save State Architecture

### Core Principle: Auto-Save Everything, Immediately

No save button. No session flush. Every meaningful action — answer submitted, confidence rated, concept read, module unlocked, XP earned — persists to SQLite the moment it happens. Continuous auto-save, like a modern game. A crash or closed tab never loses progress.

### Designed for Single User Now, Multi-User Later

`user_id` is a column in every progress table, even for personal use where it's always `1`. This costs nothing now and means the migration to public deployment is adding auth middleware — not rewriting the data model. Do not skip this.

**Personal (V1):** SQLite, no auth, `user_id = 1` everywhere.
**Public (V2):** SQLAlchemy ORM connection string changes from SQLite → PostgreSQL. Auth middleware added. User registration/login added. Data model unchanged.

---

## SQLite Schema — Full Column Definitions

### `users`
```sql
id              INTEGER PRIMARY KEY
username        TEXT UNIQUE NOT NULL DEFAULT 'default'
character_form  INTEGER NOT NULL DEFAULT 1          -- 1=Ronin, 2=Warrior, 3=Samurai, 4=Ghost
total_xp        INTEGER NOT NULL DEFAULT 0
current_streak  INTEGER NOT NULL DEFAULT 0
longest_streak  INTEGER NOT NULL DEFAULT 0
last_study_date DATE
created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
```
Single row for personal use. Expands to multi-row when auth is added for public deployment.

### `modules`
```sql
id                  INTEGER PRIMARY KEY
order_index         INTEGER NOT NULL UNIQUE         -- 0-9
title               TEXT NOT NULL
kb_source_path      TEXT                            -- NULL for Module 0 (PM only)
pm_context_path     TEXT                            -- NULL for Modules 1-9 (KB only)
last_synced_commit  TEXT                            -- git hash of last generation
is_unlocked         BOOLEAN NOT NULL DEFAULT 0
quiz_score_achieved REAL                            -- 0.0-1.0, NULL until attempted
unlocked_at         TIMESTAMP
created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
```

### `concepts`
```sql
id                  INTEGER PRIMARY KEY
module_id           INTEGER NOT NULL REFERENCES modules(id)
order_index         INTEGER NOT NULL
title               TEXT NOT NULL
default_layer       JSON NOT NULL                   -- Prompt 1a output
deep_layer          JSON NOT NULL                   -- Prompt 1b output
prediction_question JSON NOT NULL                   -- Prompt 1c output
worked_example      JSON NOT NULL                   -- Prompt 1d output
content_hash        TEXT NOT NULL                   -- hash of source KB section, for delta detection
generated_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
```

### `concept_reads`
```sql
id              INTEGER PRIMARY KEY
user_id         INTEGER NOT NULL REFERENCES users(id)
concept_id      INTEGER NOT NULL REFERENCES concepts(id)
read_default    BOOLEAN NOT NULL DEFAULT 0          -- default layer read
read_deep       BOOLEAN NOT NULL DEFAULT 0          -- go deeper layer read
first_read_at   TIMESTAMP
deep_read_at    TIMESTAMP
UNIQUE(user_id, concept_id)
```

### `quiz_questions`
```sql
id              INTEGER PRIMARY KEY
concept_id      INTEGER NOT NULL REFERENCES concepts(id)
question_type   TEXT NOT NULL                       -- 'mc', 'scenario', 'prediction', 'ordering', 'match'
scenario_type   TEXT                                -- 'system_design', 'production_failure', 'risk_communication'
content         JSON NOT NULL                       -- full question object from generation prompts
generated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
```

### `user_progress`
```sql
id                  INTEGER PRIMARY KEY
user_id             INTEGER NOT NULL REFERENCES users(id)
quiz_question_id    INTEGER NOT NULL REFERENCES quiz_questions(id)
answered_correctly  BOOLEAN NOT NULL
confidence          TEXT NOT NULL                   -- 'guessed', 'somewhat_sure', 'knew_it'
answered_at         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
time_spent_ms       INTEGER                         -- milliseconds on this question
```

### `review_schedule`
```sql
id              INTEGER PRIMARY KEY
user_id         INTEGER NOT NULL REFERENCES users(id)
concept_id      INTEGER NOT NULL REFERENCES concepts(id)
next_review_at  TIMESTAMP NOT NULL
interval_days   REAL NOT NULL DEFAULT 1.0           -- current SRS interval
ease_factor     REAL NOT NULL DEFAULT 2.5           -- SM-2 ease factor
repetitions     INTEGER NOT NULL DEFAULT 0          -- successful review count
last_reviewed_at TIMESTAMP
UNIQUE(user_id, concept_id)
```

### `sessions`
```sql
id                  INTEGER PRIMARY KEY
user_id             INTEGER NOT NULL REFERENCES users(id)
started_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
ended_at            TIMESTAMP
questions_answered  INTEGER NOT NULL DEFAULT 0
correct_answers     INTEGER NOT NULL DEFAULT 0
concepts_read       INTEGER NOT NULL DEFAULT 0
xp_earned           INTEGER NOT NULL DEFAULT 0
```

### `character_equipment`
```sql
id              INTEGER PRIMARY KEY
user_id         INTEGER NOT NULL REFERENCES users(id)
module_id       INTEGER NOT NULL REFERENCES modules(id)   -- which module unlock triggered this
equipment_name  TEXT NOT NULL
equipped_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
```

### `spec_exercises`
```sql
id              INTEGER PRIMARY KEY
user_id         INTEGER NOT NULL REFERENCES users(id)
module_id       INTEGER NOT NULL REFERENCES modules(id)
user_response   TEXT NOT NULL
submitted_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
```

---

## Spaced Repetition Algorithm (SM-2 Simplified)

After each reviewed concept, update `review_schedule` immediately:

```
IF answered_correctly:
    IF confidence == 'knew_it':
        interval = interval * ease_factor
        ease_factor = min(3.0, ease_factor + 0.1)
    IF confidence == 'somewhat_sure':
        interval = interval * ease_factor
        (ease_factor unchanged)
    IF confidence == 'guessed':
        interval = max(1.0, interval * 0.8)    -- trust a correct guess less
        (ease_factor unchanged)
    repetitions += 1
ELSE:
    interval = 1.0                              -- reset to tomorrow
    ease_factor = max(1.3, ease_factor - 0.2)  -- gets harder to raise interval
    repetitions = 0

next_review_at = NOW + interval (days)
```

Starting values: `interval_days = 1.0`, `ease_factor = 2.5`, `repetitions = 0`

A correct "Guessed" answer is treated with suspicion — the interval grows slowly until confidence improves. This is intentional: lucky guesses don't fool the scheduler.

---

## Session Lifecycle

Every study session is tracked end-to-end:

1. **Session start:** Insert row into `sessions` with `started_at`, `user_id`
2. **During session:** Increment `questions_answered`, `correct_answers`, `concepts_read`, `xp_earned` via PATCH to current session — auto-save after every action
3. **Session end:** Set `ended_at` — triggered when user navigates away, closes app, or explicitly ends
4. **Streak update:** On session end, check `last_study_date`. If yesterday or earlier today: increment `current_streak`. If more than 1 day gap: reset to 1. Update `longest_streak` if current > longest.

---

## Public Deployment Migration Path (V2)

When ready to go public, the changes are additive — nothing in V1 schema gets dropped:

1. **Add auth fields to `users`:** `email`, `password_hash`, `email_verified`, `auth_provider`
2. **Add JWT middleware** to FastAPI — all routes require valid token except `/auth/*`
3. **Swap database:** change SQLAlchemy connection string from `sqlite:///zenkai.db` to `postgresql://...`
4. **Run one-time migration script** to move SQLite data to PostgreSQL
5. **Add user registration/login endpoints** — `/auth/register`, `/auth/login`, `/auth/refresh`
6. **KB path becomes per-user config** — each user syncs their own KB fork or uploads docs

The data model is identical. The business logic is identical. Only the infrastructure layer changes. This is why `user_id` in every table from day one is non-negotiable.

`pm_context_path` on the modules table points to the relevant PM context file used during content generation. Module 0 has no KB source — only a PM context path. Modules 1–9 have both.

---

## Learning Science Implementation

| Principle | Implementation |
|---|---|
| Spaced repetition (Ebbinghaus) | Review intervals double on success, reset on failure |
| Active recall (Roediger & Karpicke) | Quiz before re-reading, not after. Prediction question before each concept. |
| Pre-testing effect | Prediction question before each concept — wrong guesses prime retention |
| Metacognitive monitoring | Confidence rating after every answer |
| Scaffolded learning (Vygotsky ZPD) | Module gating — unlock only when ready |
| Cognitive load theory (Sweller) | Layered depth — default view is brief, "go deeper" is learner-initiated |
| Dual coding (Paivio) | Every concept has both text explanation and visual |
| Elaborative interrogation | Worked annotated examples — seeing the concept applied, not just described |
| Generation effect | Spec writing micro-exercise per module — producing an artifact, not just recognizing one |
| Narrative learning (story anchoring) | Real failure case per module — abstract concepts anchored to real stakes |

---

## Implementation Notes

- Run `ui-ux-pro-max` skill first to generate `DESIGN.md` before touching code
- Use `frontend-taste` skill as the active design skill during frontend build
- Use `web-design-patterns` skill for component architecture
- shadcn/ui components used but heavily customized — never default state
- NotebookLM setup is manual (user uploads KB docs once) — not automated
- Backend reads KB from configured local path, not bundled content

---

## Token & Cost Optimization — Best Practices for Zenkai

This is a first-principles build. Every API call costs money. Zenkai's backend makes real calls to the Claude API for content generation and quiz creation — these costs compound as the KB grows. Design for efficiency from day one.

### The Core Principle: Zenkai's Content Generation IS RAG

Zenkai's backend is a RAG system where the KB is the document store. When generating a concept explanation, the pipeline is: query (what concept?) → retrieve (find the relevant KB sections) → generate (produce explanation + PM application). Apply the RAG best practices from the KB's own `playbooks/building-rag-pipelines.md` directly to Zenkai's own content generation pipeline.

### Rule 1: Cache Everything Permanently

Generated content is expensive to produce and cheap to store. Once a concept explanation, PM application section, or quiz question set is generated, it lives in SQLite permanently. It is never regenerated unless:
- The source KB content changed (detected via git diff on `last_synced_commit`)
- The PM context source changed
- The user explicitly triggers a regeneration

This is not an optimization — it's an architectural requirement. A module with 6 concepts and 3 questions each = 18 API calls. Regenerating on every load would make the app unusable and expensive.

### Rule 2: Model Tiering — Use Haiku for Cheap Tasks

Not all generation tasks require Sonnet. Use the right model for the job:

| Task | Prompt | Model | Reason |
|---|---|---|---|
| Concept explanation — default layer | 1a | claude-sonnet-4-6 | Core learning content — quality matters |
| Concept deep layer | 1b | claude-sonnet-4-6 | Mechanism + failure story require reasoning |
| Prediction question | 1c | claude-haiku-4-5 | Formulaic MC before explanation; cheap |
| Worked annotated example | 1d | claude-sonnet-4-6 | Specific artifacts + callout reasoning |
| Spec writing micro-exercise | 1e | claude-sonnet-4-6 | PM artifact + model answer need quality |
| AI PM Application section | 2 | claude-sonnet-4-6 | Nuanced role framing |
| Multiple choice quiz questions | 3 | claude-haiku-4-5 | Formulaic structure; ~20x cheaper |
| Scenario-based quiz questions | 4 | claude-sonnet-4-6 | Applied judgment needs quality |
| Module cheatsheet | 5 | claude-haiku-4-5 | Summarization from cached content |
| Delta sync detection summary | — | claude-haiku-4-5 | Classification only |

### Rule 3: Chunk Generation — One Concept at a Time

Never send a full 700-line KB doc to Claude and ask for all 6 concepts at once. Instead:
1. Pre-index the KB at build time (section headers → line ranges → stored in SQLite)
2. For each concept, send only the relevant KB section (typically 30–80 lines)
3. Generate one concept at a time, cache immediately, continue
4. Send the PM context section alongside — not the entire pm-context file

This keeps individual prompt sizes small, output is predictable per concept, and partial failures don't waste work already done.

### Rule 4: Pre-Index the KB at Build Time

On first launch (and on KB updates), Zenkai builds a section index:
- Parse markdown headers from each KB file
- Store: file path, section heading, start line, end line, section hash
- On content generation, retrieve only the matching section by line range

This mirrors `KB-INDEX.md` in the KB root — that file exists for Claude Code session efficiency. Zenkai's SQLite-stored version serves the same purpose for the backend. Never grep the KB live during generation — use the pre-built index.

### Rule 5: Inject Context Surgically

When generating a concept explanation, the prompt contains:
1. System prompt (role + instructions) — ~200 tokens
2. The specific KB section — ~500–1,500 tokens depending on section length
3. The specific PM context mapping for this concept — ~300–500 tokens
4. The generation instruction — ~100 tokens

Total per concept call: ~1,000–2,500 tokens input. At Sonnet pricing this is cents per concept. 7 modules × 6 concepts = 42 concept calls. Initial generation of the entire KB costs under $2 at current pricing. The delta sync system means you almost never pay that again.

### Rule 6: Delta Sync Is the Cost Governor

The delta sync system (git commit hash tracking) is not just a UX feature — it's the primary cost control mechanism. When KB content changes:
- Only sections whose hash changed trigger regeneration
- A single paragraph edit regenerates one concept, not the whole module
- Quiz questions regenerate only for concepts whose explanations changed

This means ongoing costs are nearly zero for sessions where the KB didn't change.

### Rule 7: Session-Level Efficiency for Claude Code (Development)

During the Zenkai build phase, apply these rules to Claude Code sessions:
- Use `KB-INDEX.md` (in KB root) to navigate — read section ranges, not full files
- One focused session per feature/task — don't mix design discussions with coding
- Use Grep over Read for search — 20 lines vs. 700 lines for the same answer
- Use subagents for research tasks — they protect the main context window
- Start fresh sessions for new topics rather than extending long ones

---

## Content Generation System Prompts

These are the system prompts sent to Claude API for each generation task. Each prompt is paired with a user message (see structure note below). Outputs are cached permanently in SQLite — these prompts run once per concept/module, not on every user session.

**Input structure for all generation calls:**
- System prompt (below)
- User message: contains the actual KB section text and/or PM context, structured as: `<kb_content>...</kb_content>` and `<pm_context>...</pm_context>` XML tags
- Temperature: 0.3 for factual explanation, 0.7 for quiz generation (more varied distractors)

---

### Prompt 1a — Concept Explanation (Default Layer)

Used for: the default concept card — hook, plain-English explanation, analogy. What loads first.
Model: `claude-sonnet-4-6`
Input: KB section text for this specific concept (30–80 lines, not the full doc)

```
You are an AI learning content writer for Zenkai, a personal AI learning system built for one learner: a Yale CS grad with 1.5 years of Technical PM experience who is building deep AI fluency for AI PM roles.

Your job is to explain one AI concept clearly and engagingly. The learner has a CS background but is approaching most of these topics fresh. They learn best through concrete analogies and specific examples — not abstract definitions.

Produce the default concept card with this exact structure:

1. **Opening hook** (2–3 sentences): Start with why this concept matters before explaining what it is. Ground it in a real-world scenario where getting this wrong causes a real problem.

2. **Plain-English explanation** (2–3 paragraphs): Explain what this concept is. Define every technical term on first use — never assume the reader knows jargon. Build understanding progressively from familiar to unfamiliar.

3. **Analogy** (1 paragraph): One strong analogy grounding the concept in a non-AI experience. If no clean analogy exists, skip it rather than forcing one.

Formatting rules:
- Prose paragraphs only — no bullet lists
- Max 250 words total — this is the hook, not the full explanation
- Specific examples only — no placeholders
- Tone: clear and direct, like an expert talking to a smart colleague who is new to this topic

Output as JSON: { "title": string, "hook": string, "explanation": string[], "analogy": string | null }
```

---

### Prompt 1b — Concept Deep Layer

Used for: the "Go Deeper" section revealed on tap. The real mechanism, edge cases, research numbers, failure story.
Model: `claude-sonnet-4-6`
Input: same KB section as 1a — extract the deeper content

```
You are writing the "Go Deeper" layer for an AI learning concept card. The learner has already read the plain-English explanation. This layer is for those who want genuine understanding — the internals, the nuance, the numbers.

Produce four components:

1. **How it actually works** (2–3 paragraphs): The real mechanism — not just what it does, but why it works that way. Go one level deeper than the plain-English explanation. Include enough technical specificity that someone who reads this understands the concept at an implementation-adjacent level.

2. **Edge cases and nuances** (1–2 paragraphs): Where the concept breaks down or behaves unexpectedly. What's often misunderstood or oversimplified. The things that only come up when you've actually built with this.

3. **The number that makes it real** (1–2 sentences): One empirical finding or concrete data point from the KB source. Actual research results, performance differences, cost ratios — something that makes the concept tangible. If no number exists naturally in the source, use a concrete comparison instead.

4. **The failure story** (2–3 paragraphs): One real or realistic scenario where this concept was misunderstood or misapplied and something went wrong. Specific, narrative, with a clear lesson. Real-world examples preferred (Air Canada chatbot, Amazon hiring algorithm, etc.) — if none fits, construct a realistic scenario.

Formatting rules:
- Prose paragraphs — no bullet lists
- Max 400 words total across all four components
- The failure story should read like a brief case study, not a bullet point

Output as JSON: { "mechanism": string[], "edge_cases": string[], "key_number": string, "failure_story": string }
```

---

### Prompt 1c — Prediction Question (pre-concept)

Used for: the question shown *before* the concept explanation loads. Forces a guess to prime retention.
Model: `claude-haiku-4-5`
Input: concept title + one-sentence description only (not the full explanation)

```
You are creating a single pre-concept prediction question for a learning app.

This question appears BEFORE the concept is explained. The learner hasn't seen the explanation yet. The goal is to make them form a hypothesis — not to test knowledge they don't have.

Rules:
- Ask "what do you think X does?" or "why do you think Y is hard?" or "which of these would you guess is the problem?" — not "what is the definition of X?"
- 4 options — all should be reasonable guesses from someone with general CS knowledge but no specific AI expertise
- There is no penalty for being wrong — the question exists to prime thinking, not to assess knowledge
- After the explanation is read, this question's answer is revealed with a 1-sentence explanation of why

Output as JSON: { "question": string, "options": [string, string, string, string], "correct_index": number, "reveal_explanation": string }
```

---

### Prompt 1d — Worked Annotated Example

Used for: the annotated artifact shown after the concept explanation. A real example of the concept in action.
Model: `claude-sonnet-4-6`
Input: concept explanation (1a output) + KB section

```
You are creating a worked, annotated example for an AI learning concept card.

The learner just read the concept explanation. Your job is to show the concept in action — a real artifact (prompt, architecture description, system behavior, before/after comparison) with the key parts explicitly called out.

Produce:
1. **The artifact** — a concrete example: an actual prompt using the technique, an architecture diagram described in text, a before/after output comparison, or a realistic system scenario. Real and specific — no placeholders.
2. **Annotations** — 3–5 callout points, each referencing a specific part of the artifact and explaining what makes it an example of this concept. Format: [Part of artifact] → [Why this demonstrates the concept].

This is the bridge between "I understand the concept" and "I can recognize it in practice."

Output as JSON: { "artifact_type": "prompt" | "architecture" | "before_after" | "scenario", "artifact": string, "annotations": [{ "reference": string, "explanation": string }] }
```

---

### Prompt 1e — Spec Writing Micro-Exercise (per module)

Used for: the applied exercise at the end of each module's concept layer. One short task that produces a PM artifact.
Model: `claude-sonnet-4-6`
Input: list of all concept titles in this module + module topic

```
You are creating a specification writing micro-exercise for an AI learning module. This is a 2-minute applied task — not a quiz question. The learner produces a short PM artifact, then compares it to a model answer.

The learner is a Technical PM building AI fluency. The exercise should require them to apply something from this module in a concrete PM context: writing acceptance criteria, drafting a team question, identifying a failure mode in a described system, or choosing between two architectural options with justification.

Produce:
1. **Scenario** (2–3 sentences): A realistic AI PM situation requiring knowledge from this module. Specific enough that a good answer requires module knowledge — vague enough that there's room to reason.
2. **Task** (1 sentence): What the learner writes. Exactly one of: one acceptance criterion, one question for the engineering team, one identified failure mode with explanation, or one architectural recommendation with one-sentence justification.
3. **Model answer** (2–3 sentences): A strong response to the task. Shows what good looks like — not the only right answer, but a clearly strong one.
4. **What makes it strong** (1–2 sentences): The specific reasoning or knowledge that makes the model answer better than a generic response.

Output as JSON: { "scenario": string, "task": string, "model_answer": string, "strength_explanation": string }
```

---

### Prompt 2 — AI PM Application Section (per module)

Used for: generating the PM application section that appears once per module, at the end of the concept layer.
Model: `claude-sonnet-4-6`
Input: summary of all concept titles + KB section + relevant section from `pm-context/ai-pm-applications.md`

```
You are an AI PM coach writing a brief practical section for a technical PM who is learning AI concepts.

This section appears once per learning module — not on every concept. It is a lightweight supplement, not a parallel curriculum. The learner already understands the AI concepts from the module. Your job is to anchor that understanding in the specific decisions and responsibilities of an AI PM role.

Be specific and practical. Skip motivation — the reader knows why AI matters. Get to the concrete.

Produce exactly three components:

1. **What this means for your role** (2–3 sentences): How do the concepts in this module show up in an AI PM's actual day-to-day work? Be specific — name the artifact, the decision, or the meeting where this shows up.

2. **The key decision you'd own** (1–2 sentences): Describe one concrete decision an AI PM makes that requires genuine understanding of this module's content. Frame it as a choice with real stakes.

3. **One question to ask your engineering team** (1 sentence): A single pointed technical question that an AI PM should ask about a system using these concepts. The question should reveal whether the team has thought through the hard parts — it should be specific enough that a vague answer is a red flag.

Hard constraints:
- Total length: 150–200 words maximum
- No "as an AI PM..." sentence starters — get to the point directly
- No generic PM advice (no "prioritize ruthlessly", "align with stakeholders", etc.)
- Every sentence must be specific to the AI concepts in this module

Output as JSON: { "role_impact": string, "key_decision": string, "team_question": string }
```

---

### Prompt 3 — Multiple Choice Quiz Questions

Used for: generating comprehension and application questions testing AI concept understanding.
Model: `claude-haiku-4-5`
Input: concept title + generated concept explanation (from Prompt 1)

```
You are a quiz designer creating multiple choice questions for an AI learning system. Your goal is to test genuine understanding, not memorization or recall of definitions.

A learner who understood the concept should get these right through reasoning. A learner who only skimmed should struggle.

Rules for every question:
- 4 options always
- All distractors must be plausible — no obviously wrong answers. Wrong options represent common misconceptions, reasonable-sounding mistakes, or real tradeoffs
- Never ask "what is X" or "what does X stand for" — always ask about application, behavior, or tradeoffs
- Phrasing: "Which of the following..." or "In which situation would you..." or "What happens when..."
- The correct answer explanation must teach something beyond just confirming correctness — address the most tempting wrong answer

Generate exactly 3 questions per concept:
- Question 1: Comprehension — tests understanding of what the concept does or how it works
- Question 2: Application — tests whether the learner can recognize when/how to use it
- Question 3: Tradeoff — tests understanding of the limitations or failure modes

Output as JSON array:
[{
  "type": "comprehension" | "application" | "tradeoff",
  "question": string,
  "options": [string, string, string, string],
  "correct_index": 0 | 1 | 2 | 3,
  "explanation": string  // 1–2 sentences, addresses why correct is right + why main distractor is wrong
}]
```

---

### Prompt 4 — Scenario-Based Quiz Questions (AI PM Context)

Used for: generating applied judgment questions set in AI PM scenarios. These are the primary question type.
Model: `claude-sonnet-4-6`
Input: concept title + concept explanation + relevant section from `pm-context/interview-scenarios.md`

```
You are an AI PM quiz designer creating scenario-based multiple choice questions for a technical PM learning AI concepts.

These questions test applied judgment — not recall. The learner is a Technical PM who needs to understand AI systems well enough to specify them, evaluate them, and make decisions about them. Every question is a realistic situation an AI PM would actually face.

Rules:
- Every question opens with a concrete scenario: "You're reviewing the architecture for..." or "Your team's RAG pipeline is showing..." or "Before approving the launch of..."
- 4 options: each represents a different judgment call a reasonable PM might make. The wrong options are not obviously bad — they're what a PM without deep AI knowledge might choose
- The correct option demonstrates the specific AI understanding this concept provides. Without knowing this concept, you'd likely pick one of the wrong options
- Explanation: focus on why the correct answer shows deeper AI understanding than the alternatives

Scenario types — generate one of each:
- "system_design": PM evaluating an architectural choice or tradeoff
- "production_failure": PM diagnosing or responding to an AI system problem
- "risk_communication": PM deciding how to communicate AI limitations or risks

Output as JSON array:
[{
  "type": "system_design" | "production_failure" | "risk_communication",
  "scenario": string,  // 2–3 sentence setup
  "question": string,  // "What do you do?" or "What is most likely happening?" or "How do you explain this?"
  "options": [string, string, string, string],
  "correct_index": 0 | 1 | 2 | 3,
  "explanation": string  // why this answer requires the AI knowledge from this concept
}]
```

---

### Prompt 5 — Module Cheatsheet

Used for: generating the one-page visual reference for each completed module.
Model: `claude-haiku-4-5`
Input: all generated concept titles + explanations for the module

```
You are creating a module cheatsheet — a compact visual reference card summarizing everything in this learning module.

The learner uses this during spaced repetition review and as a quick reference after completing the module. It must fit on a single screen. If content doesn't fit, cut the least important items.

Produce exactly these sections:

1. **Module summary**: One sentence — what this module is about and why it matters.

2. **Key concepts**: For each concept in the module — name + one-sentence definition. Maximum 8 concepts. If the module has more, include only the most foundational ones.

3. **Core rules**: The most important "if X, then Y" principles from this module. Maximum 4 rules. These are the things a practitioner always keeps in mind.

4. **Watch out for**: The 2–3 most important anti-patterns or failure modes from this module. What goes wrong when people misunderstand or misapply these concepts.

5. **Key number**: One empirical finding or concrete data point from this module that makes the concepts real. If none exists naturally, omit this section.

Output as JSON: {
  "module_summary": string,
  "concepts": [{ "name": string, "definition": string }],
  "core_rules": [string],
  "antipatterns": [string],
  "key_number": string | null
}
```

---

### Prompt 6 — Module 0 (AI PM Foundations)

Module 0 reads only from `pm-context/` — no KB source. It is the prerequisite PM mental model module. Use `claude-sonnet-4-6` for all generation. Concept explanations follow the same structure as Prompt 1 but without KB content input — input is `pm-context/ai-pm-role.md` and `pm-context/pm-fundamentals.md` only. No PM Application section is generated for Module 0 (the whole module is PM context). Quiz questions for Module 0 use Prompt 3 format (not scenario-based) since the learner hasn't covered AI concepts yet.

---

## Out of Scope (V1)

- Mobile app (potential V2 after local version works)
- Multi-user / sharing
- Public deployment
- Video generation
- Automated NotebookLM integration
