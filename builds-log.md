# AI Builds Log

> Personal record of AI systems built — architecture, key decisions, what made each solution elegant.
> Updated as I build. Not exhaustive — focused on things worth remembering.

---

## The Pattern Running Through All of This

Before diving into individual systems, there's a meta-pattern worth naming:

```
CLAUDE.md (behavioral contract)
  + context/ (live state as files)
  + scripts/ or templates/ (tools)
  + git (persistence + history)
  = a self-contained AI-native system
```

Every system below uses some version of this. The agent behavior lives in files, not in chat memory. Sessions are stateless by design — the files ARE the memory. This is the context-as-files pattern applied consistently across domains: trading, job search, interview prep, knowledge management.

The second pattern: **dual AI portability**. Three systems now have both CLAUDE.md and GEMINI.md (same behavioral contract, different tool dialects). When one AI hits limits, swap to the other without losing context.

---

## Systems

### 1. edge_lab — Trading Analyst System

**Status:** Live
**Location:** `/Users/t-rawww/edge_lab/`
**Config:** `CLAUDE.md` + `GEMINI.md`

#### What It Is
A session-aware swing trading analyst grounded in a pre-built framework. Not a generic chatbot — it reasons strictly within my macro bias, key levels, portfolio state, and trade journal. It stress-tests my thesis, never generates one from thin air.

#### Architecture

```
edge_lab/
├── CLAUDE.md / GEMINI.md     ← Behavioral contract (dual AI)
├── context/
│   ├── macro-outlook.md      ← Current HTF bias (agent updates in-session)
│   ├── portfolio-state.md    ← Open positions, risk snapshot
│   ├── market-snapshot.md    ← Generated indicator data (make refresh)
│   ├── macro-snapshot.md     ← Macro conditions
│   └── pending-setups.md     ← Watchlist — auto-price-checked at session start
├── levels/
│   ├── macro-levels.md       ← Yearly/quarterly opens per symbol
│   └── watchlist.md          ← Monthly/weekly opens + key levels
├── journal/
│   ├── INDEX.md              ← Built by scripts/build-index.py
│   ├── template.md
│   └── YYYY-MM-DD-[SYM]-[TF].md  ← Trade entries
├── playbook/
│   ├── README.md             ← Index + matching guide (always read first)
│   └── [one file per setup type]
├── framework/                ← Personal trading framework rules
├── reviews/                  ← Weekly/periodic review outputs
├── scripts/
│   ├── position-sizer.py     ← --calc mode: shares, % at risk, buffer impact
│   ├── live-prices.py        ← yfinance multi-ticker fetch
│   ├── build-index.py        ← Rebuilds journal/INDEX.md
│   ├── check_alerts.py       ← Watchlist alert logic
│   ├── fetch_market_state.py ← Market condition fetch
│   ├── weekly-summary.py     ← Weekly review generation
│   └── [full test suite]     ← test_*.py for every script
└── Makefile                  ← `make refresh` etc.
```

#### Key Decisions and Why They're Elegant

**1. Context as files, not conversation memory**
All state lives in structured markdown — macro outlook, portfolio state, watchlist. Agent reads fresh each session. No hallucinated continuity from chat history.

**2. Dual AI portability**
CLAUDE.md and GEMINI.md are the same behavioral contract with different tool dialects. When Claude usage hits limits, Gemini picks up with zero behavior drift. Tool mapping:
```
Read → read_file  |  Write → write_file  |  Edit → replace
Bash → run_shell_command  |  (+) save_memory  |  (+) ask_user
```

**3. Auto-stale detection**
On every chart upload: checks `market-snapshot.md` timestamp. >24h → flags immediately. Macro outlook >7 days → flags. Prevents silent stale-data analysis.

**4. Watchlist price monitoring at session start**
`pending-setups.md` stores symbol + target level + condition. At session start, agent fetches live prices via yfinance and flags any ticker within 3% of its target. Zero manual checking required.

**5. Journal-driven similarity matching**
Before any analysis, reads `journal/INDEX.md` → finds 3 structurally similar past setups → reads full entries. Analysis grounded in personal trade history, not generic TA patterns.

**6. Non-interactive position sizer**
`position-sizer.py --calc` runs inline during trade discussion (not after). Pulls portfolio value/maint req/margin from context. Outputs shares, % at risk, buffer impact, binding constraint.

**7. Session close = git push**
End-of-session protocol: list changed files → rebuild journal index → `git add -A && git commit && git push`. Framework versioned automatically.

**8. Tested scripts**
Every script in `scripts/` has a corresponding `test_*.py`. Production-grade practices applied to a personal trading tool.

---

### 2. interview-prep — Job Search OS

**Status:** Live
**Location:** `/Users/t-rawww/interview-prep/`
**Config:** `CLAUDE.md` + `GEMINI.md`

#### What It Is
A full job search operating system — not a notes folder. Tracks 10+ active/passive opportunities, stores STAR stories, maintains interview schedules, logs every session, and holds all core materials. The CLAUDE.md doubles as a live CRM.

#### Architecture

```
interview-prep/
├── CLAUDE.md / GEMINI.md    ← Behavioral contract + live pipeline state
├── core-materials/
│   ├── paypal-narrative.md  ← PayPal PM story (the origin story)
│   ├── paypal-metrics.md    ← Verified numbers (140M logins, $2.4M margin, 52% lift)
│   ├── behavioral-stories.md ← STAR story beats (4 stories, deploy-ready)
│   ├── master-pitch.md      ← Pitch versions (60s, 2min, modular)
│   ├── pm-playbook.md       ← Reusable frameworks
│   └── pm-frameworks-refresher.md ← RICE, CIRCLES, metrics
├── companies/               ← 27 folders, one per company tracked
│   ├── mariana-minerals/
│   ├── bridgestone/
│   ├── ziff-davis/
│   └── [24 more...]
├── sessions/                ← Date-stamped session logs (YYYY-MM-DD.md)
├── session-recaps/          ← Condensed recaps for review
├── templates/               ← Reusable interview templates
├── docs/                    ← Supporting documents
└── side-hustle/             ← Parallel tracks, consulting exploration
```

#### Key Decisions and Why They're Elegant

**1. CLAUDE.md as live CRM**
The CLAUDE.md holds the full pipeline: 10 ranked opportunities, interview schedules, key contacts with context, STAR stories, what's working/not working. Every session starts with this loaded — no re-explaining. It gets updated in-session as new information comes in.

**2. Company folders as atomic context units**
Each of the 27 companies has its own folder. Company-specific prep, call notes, and research are isolated — never bleeds between opportunities. When prepping for a specific call, load only that company's folder.

**3. Session log as institutional memory**
Daily sessions logged at `sessions/YYYY-MM-DD.md`. Recaps live in `session-recaps/`. Can look back and trace exactly when a belief changed, when an opportunity shifted, what worked in a call.

**4. human-voice skill integration**
All outreach drafts (emails, thank-yous, LinkedIn messages) run through the `human-voice` skill first. Enforces direct, Oakland-rooted voice — not corporate filler. The behavioral rule is in the CLAUDE.md itself: no em dashes, no motivational poster BS.

**5. Dual AI portability**
GEMINI.md exists for the same reason as edge_lab — continuity across AI tool switches mid-job-search.

**6. Communication style baked in as constraints**
The CLAUDE.md has explicit language rules: no em dashes, no filler phrases, don't over-rehearse, simplify when brain fog hits. These override default AI communication tendencies at the system level.

---

### 3. mariana-interview — Case Study Preparation System

**Status:** Complete (used for Round 2 interview)
**Location:** `/Users/t-rawww/mariana-interview/`
**Config:** `CLAUDE.md`

#### What It Is
A purpose-built preparation environment for the Mariana Minerals Round 2 collaborative PRD case study. Not generic interview prep — purpose-built for a specific 60-minute interview with a specific company in a specific domain (industrial mining software).

#### Architecture

```
mariana-interview/
├── CLAUDE.md               ← Behavioral contract + language rules
├── QUICKREF.md             ← Fast reference for session
├── interviewer-PREP-ONLY.md ← Notes on Sam Sperling
├── context/
│   ├── company.md          ← PlantOS, MineOS, CapitalProjectOS: personas, metrics, tensions
│   └── glossary.md         ← Industrial terminology (SX-EW, flotation, RFI, EPCC, P&ID...)
├── ai-reference/
│   └── ai-pm-framing.md    ← Load only when prompt involves AI/ML explicitly
├── templates/
│   └── prd-mariana.md      ← Custom PRD template (NOT generic PM template)
└── output/
    ├── PRD-AutomatedBidEvaluation.md    ← Produced during session
    └── PreMortem-AutomatedBidEvaluation.md
```

#### Key Decisions and Why They're Elegant

**1. Specialized language rules as hard constraints**
The CLAUDE.md bans generic PM vocabulary and forces industrial-specific equivalents:
```
"users"     → plant operators / process engineers / mine planners
DAU/MAU     → recovery rate / cost per ton / schedule variance
"edge case" → failure mode (treat as first-class requirement)
"validate"  → "test this assumption before V2 by [specific method]"
```
This forces the agent to sound like an industrial PM, not a consumer tech PM. The domain framing is enforced at the system level.

**2. 3-phase session workflow mirroring the interview**
The CLAUDE.md maps directly to the interview format:
- **Phase 1 (10 min):** Frame — which product, primary persona, core tension, biggest constraint
- **Phase 2 (35 min):** `/prd` command — reasons first, asks clarifying questions, builds using Mariana template
- **Phase 3 (10 min):** `/premortem` command — Tigers (real risks), Paper Tigers (overblown), Elephants (unspoken)

**3. Conditional context loading**
`ai-pm-framing.md` is loaded **only** when the prompt involves AI/ML explicitly. Domain-specific context on demand — not always loaded. Keeps the context window efficient.

**4. Output folder**
Session outputs saved to `output/`. The PRD and PreMortem are persistent artifacts — can review after the interview and learn from them.

**5. "Fill structure, not words" principle**
The CLAUDE.md frames the agent role explicitly: surface structure and risks, not replace PM judgment. After generating any section, offer 1-2 questions to bring back to the interviewer. Keeps the human's reasoning primary.

**6. Thinking framework baked in**
Every feature analysis forces: systems first (inputs→process→outputs→feedback), costs always (capital/operating/time/risk), three different people (who approves, who uses, who gets fired). Physical constraints named — never ignored.

---

### 4. AI-Knowledgebase — Personal Knowledge Library

**Status:** Live (continuously growing)
**Location:** `/Users/t-rawww/AI-Knowledgebase/`
**Repo:** `trentjhn/AI-Knowledgebase` (private)

#### What It Is
A personal AI knowledge library built for genuine depth — distilled, practitioner-level reference docs on core AI engineering topics. Built for personal use and as a methodology foundation for future consulting/audit work.

#### Architecture

```
AI-Knowledgebase/
├── KB-INDEX.md              ← Navigation layer (line counts, read times, one-liners)
├── builds-log.md            ← This file
├── LEARNING/
│   ├── FOUNDATIONS/
│   │   ├── reasoning-llms/
│   │   ├── multimodal/
│   │   └── emerging-architectures/   ← Frontier monitoring (not how-to)
│   ├── AGENTS_AND_SYSTEMS/
│   │   ├── agentic-engineering/
│   │   ├── context-engineering/
│   │   ├── skills/
│   │   └── mcp/
│   ├── PRODUCTION/
│   │   ├── evaluation/
│   │   ├── fine-tuning/
│   │   ├── inference-optimization/
│   │   └── rl-alignment/
│   ├── SECURITY/
│   │   └── ai-security/
│   └── ai-governance/
├── future-reference/
│   ├── playbooks/           ← How-to protocols (building agents, RAG, websites...)
│   ├── prompt-catalog/
│   └── specs/
└── CAREER/
```

#### What's Elegant Here

**1. Distillation as the primary operation**
Each doc synthesizes 10–20+ primary sources (papers, docs, blog posts) into a single readable reference. Not a bookmark list, not raw notes — a genuine synthesis with narrative explanation before bullets, analogies for abstraction, "why this matters" for every concept. The writing standard was set by explicit feedback: educational first, reference second.

**2. Two-tier structure: LEARNING vs future-reference**
- `LEARNING/` is evergreen conceptual knowledge (what things are, how they work)
- `future-reference/` is operational protocols (how to build things)
These are intentionally separate. Mixing them creates reference docs that are neither good to learn from nor good to execute against.

**3. Frontier monitoring as its own document type**
`emerging-architectures.md` is intentionally not a tutorial. It's a Signal vs. Noise framework for evaluating new research — SSMs/Mamba, MoE, byte-level models, continuous/latent space. Designed to age well. The evaluation framework matters more than specific benchmarks, which decay fast.

**4. KB-INDEX.md as the lightweight navigation layer**
Single file: topic → file path → line count → estimated read time → one-line description. Makes the whole library scannable without opening files. Acts like a table of contents for the entire system.

**5. builds-log.md (this file) as the meta-layer**
A record of what was built, why, and what patterns are running across systems. Turns building into deliberate practice — not just shipping and forgetting.

---

### 5. Zenkai — Personalized AI Learning App

**Status:** Planned (not yet built)
**Repo:** `trentjhn/zenkai` (not yet created)
**Design doc:** `/Users/t-rawww/AI-Knowledgebase/docs/plans/2026-02-28-zenkai-design.md`

#### What It Will Be
A local web app that turns this knowledge base into an interactive learning experience. Named after the DBZ Zenkai boost. Spaced repetition, scenario-based quizzes with AI PM framing, module gating (≥70% to unlock next).

#### Planned Stack
- Frontend: React + Tailwind + shadcn/ui + Framer Motion
- Backend: FastAPI (Python)
- DB: SQLite (local)
- AI: Claude claude-sonnet-4-6 via Anthropic API

#### Key Design Decision
**Delta sync via git commit hashes** — compares KB file hash against last-generated hash. Only regenerates quiz content for files that actually changed. Avoids burning API credits on unchanged content every launch. The KB is the source of truth; Zenkai derives from it.

---

## Protocols and Playbooks

### Website Build Protocol

**Location:** `/Users/t-rawww/AI-Knowledgebase/future-reference/playbooks/building-professional-websites.md`

A comprehensive protocol for building professional, non-AI-slop websites. Synthesized from: Impeccable (7-domain design skill), interface-design, ui-skills, spec-kit (Spec-Driven Development), DESIGN.md (Google Stitch), Emil Kowalski, Paper.design, Pencil.dev, FontofWeb.

**Phase structure:**
```
Phase 0    → PROJECT.md — what you're building, constraints, aesthetic direction
Phase 0.5  → CLAUDE.md for the web project — persistent rules for the build
Phase 1    → DESIGN.md — typography, color, spacing, motion, component rules
Phase 2    → Tech stack decision (Astro/Next.js/Vite + animation/3D choices)
Phase 3    → spec-kit scaffolding (specify init → specify feature → /speckit.tasks → /speckit.implement)
Phase 4    → Build order: tokens → typography → nav → layout → hero → body → footer → micro-animations → scroll
Phase 4.5  → Copy strategy (copy brief, fingerprint test, section-specific rules)
Phase 4.6  → Image protocol (decision tree, optimization, AI image prompts)
Phase 5    → Quality gates (Impeccable commands, baseline-ui, accessibility, AI fingerprint checklist)
Phase 6    → Metadata + SEO
```

**What's elegant:** DESIGN.md is treated like AGENTS.md or CLAUDE.md — a plain-text contract that tells AI tools what the design intent is. The entire build is spec-driven before a single component is written.

---

## Cross-System Patterns

These patterns appear across multiple systems. Worth recognizing as a personal methodology.

| Pattern | Systems | What It Solves |
|---|---|---|
| **Context as files** | edge_lab, interview-prep, mariana-interview, KB | Session continuity without chat memory dependency |
| **Behavioral contract (CLAUDE.md)** | All 5 systems | Consistent agent behavior across sessions, no re-explaining |
| **Dual AI portability** | edge_lab, interview-prep | Claude↔Gemini handoff with zero behavior drift |
| **Conditional context loading** | mariana-interview, edge_lab | Load domain context on-demand — keep context window efficient |
| **Custom language constraints** | mariana-interview, interview-prep | Force domain-appropriate vocabulary at the system level |
| **Structured output folders** | mariana-interview, edge_lab (journal/) | Persistent artifacts from sessions, not lost to chat history |
| **Non-interactive scripts** | edge_lab | Inline calculation during workflow, not as a separate step |
| **Git as persistence layer** | edge_lab, interview-prep, KB | Version-controlled state — history is automatic |
| **Distillation over aggregation** | KB | Reference-able depth vs. bookmark pile |
| **Frontier monitoring layer** | KB (emerging-architectures) | Evaluate new research without chasing benchmarks |
| **DESIGN.md as design contract** | Website builds | AI tools know design intent before writing code |
| **Delta sync** | Zenkai (planned) | Cost-efficient content regeneration |
| **Session close = commit** | edge_lab | Automatic versioning without manual git discipline |
| **Phase-based workflows** | mariana-interview, website builds | Structured execution that mirrors real-world constraints |
