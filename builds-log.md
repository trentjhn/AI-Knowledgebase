# AI Builds Log

> Personal record of AI systems built — architecture, key decisions, what made each solution elegant.
> Updated as I build. Not exhaustive — focused on things worth remembering.

---

## Systems Overview

Quick look at what's been built and why each matters:

| System | Status | Type | Problem Solved |
|--------|--------|------|---|
| **YouTube Summarizer Premium** | Production-deployed | Full-Stack AI | Long videos require watching in full to extract information; chunking-based tools lose narrative coherence |
| **edge_lab** | Live | Trading Automation | Trading frameworks break down under real-time pressure — steps skipped, math approximated, thesis drifted |
| **Zenkai** | Functional | Learning Platform | Good reference material doesn't create retention; needed active recall and spaced repetition for AI content |
| **AI-Knowledgebase** | Continuously growing | Knowledge Library | AI engineering knowledge scattered across 100+ sources with no practitioner-depth synthesis that ages well |
| **interview-prep** | Live | Job Search OS | 10+ concurrent applications across memory-less sessions; needed live-state CRM with company-specific context |
| **mariana-interview** | Complete | Case Study Prep | Generic PM templates fail in industrial domains — wrong personas, wrong success metrics, missing physical constraints |
| **security-var-agent** | Functional | Recommendation Engine | VAR workflows require market-real vendor analysis, ROI modeling, and confidence scoring; manual comparison is error-prone |

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

### 1. YouTube Summarizer Premium — Full-Stack AI Video Intelligence

**Status:** Production-deployed
**Location:** `/Users/t-rawww/Projects/youtube-summarizer-complete/`
**Repo:** `trentjhn/youtube-summarizer-complete` (private)

#### The Problem
Long videos require watching in full to extract information. Most AI summarization tools hit context limits and chunk the video — losing the narrative arc and connection between ideas. The result is bullet points that look comprehensive but miss the through-line.

#### What It Is
Full-stack AI application that transforms YouTube videos into structured intelligence. Dual-mode summarization (Quick: ~30 seconds, Deep: ~60 seconds) with context-aware agentic chat and seamless timestamp navigation back to source material.

#### Stack
- **Frontend:** React + Vite + Tailwind CSS v4 + Framer Motion (Bento Grid layout)
- **Backend:** Flask (Python) + SQLite + Redis + WebSockets (SocketIO)
- **LLM Models:** Google Gemini 2.5 Flash-Lite (primary), OpenAI GPT-4o-mini (chat fallback)
- **Infrastructure:** Vercel (frontend), Render (backend with IaC via render.yaml)

#### Key Decisions and Why They're Elegant

**1. Model migration for economics + context**
Switched from OpenAI GPT-4o-mini → Google Gemini 2.5 Flash-Lite. Economics: 33% cost reduction. Context: 8x larger window (1M vs 128K tokens). Practical impact: eliminates chunking for 99%+ of videos. Documented migration logic in `ai_summarizer.py` shows deliberate model economics optimization beyond just "newer is better."

**2. Dual-mode summarization architecture**
Two completely different prompting strategies with identical core principles but different output depth:
- **Quick Mode:** 5 hyper-focused JSON components (quick takeaway, key points, topics, timestamps, summary)
- **Deep Mode:** Same 5 components but 8-module breakdown with detailed analysis, key quotes, arguments sections
The separation lets users choose summarization depth without branching prompt logic — same prompt engine, two different output targets.

**3. Production-grade prompt engineering**
Sophistication rarely seen in deployed systems. Core principles baked into prompts:
- **Comprehensiveness Principle:** Content dictates output length, not arbitrary constraints. 3-hour video gets deeper analysis than 10-minute video.
- **Faithful Representation:** Preserve tone/intent without sanitizing, intentional for controversial content. Reflects actual speaker message, not watered-down version.
- **Attribution Preservation:** Clear sourcing when speaker quotes others or references studies. Maintains context connection.
- **Tone Matching:** 5 configurable tones (Objective, Academic, Casual, Skeptical, Provocative) applied consistently across all outputs.
- **Few-shot learning embedded:** BAD vs GOOD output examples in prompt itself, teaching the model what to avoid.
Prompt versioning (v5.0) auto-invalidates cache on prompt changes — no stale summaries.

**4. Context-aware chat with layered context management**
Chat service builds conversation context from three layers: video title → structured summary → transcript (truncated to 5K chars). Conversation history limited to 10 messages to prevent context bloat while maintaining conversational coherence. Context engineering in action: careful composition prevents token waste while preserving relevance.

**5. Real-time processing feedback via WebSocket**
SocketIO integration streams progress during LLM processing. Provides UX feedback for operations taking 30-60 seconds. Progress updates sent in real-time, no artificial polling.

**6. YouTube extraction resilience**
Handles modern YouTube's anti-bot measures: yt-dlp integration + Netscape cookie format parsing + cookie-based auth to bypass datacenter IP blocks. Accumulates extraction errors for debugging without crashing. Solves the "silent 500 error" failure mode.

**7. Token accounting and context strategy**
Conservative max input (900K/1M tokens) leaves explicit buffer for 65K-token output. Detailed token-per-word calculation (1.3 tokens/word English, 150 words/minute of speech). Therefore: ~195 tokens per minute of video, ~11,700 tokens per hour. Strategic math prevents runtime surprises.

**8. Deployment infrastructure-as-code**
Frontend (Vercel): Root `VITE_API_URL` environment variable points to backend. Backend (Render): `render.yaml` IaC blueprint with Web Service provisioning. Critical decision: Web Service instead of serverless, because Lambda/serverless timeouts before LLM processing finishes. Deployment logic reflects real constraints.

**9. Cache invalidation strategy**
SQLite persistence + Redis caching for processed videos. Cache key versioning lets admin clear cache without data loss (`/api/admin/clear-cache` endpoint). Useful for testing prompt changes without incrementing version.

---

### 2. edge_lab — Trading Analyst System

**Status:** Live
**Location:** `/Users/t-rawww/edge_lab/`
**Config:** `CLAUDE.md` + `GEMINI.md`

#### The Problem
Trading frameworks are easy to write and hard to follow under real-time pressure. Without a system that enforces your own rules at every decision, steps get skipped — macro alignment unchecked, position sizing eyeballed, past trade history ignored. The failure mode isn't a bad framework. It's a good framework that doesn't get used.

#### What It Is
A session-aware swing trading analyst grounded in a pre-built framework. Not a generic chatbot — it reasons strictly within my macro bias, key levels, portfolio state, and trade journal. It stress-tests my thesis, never generates one from thin air.

#### Architecture

```
edge_lab/
├── CLAUDE.md / GEMINI.md     ← Behavioral contract (dual AI)
├── context/
│   ├── macro-outlook.md      ← Current HTF bias (agent updates in-session)
│   ├── positions.md          ← Current positions, risk snapshot
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
│   ├── calc.py               ← 12-command calculator — all math offloaded here
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
All state lives in structured markdown — macro outlook, open positions, watchlist. Agent reads fresh each session. No hallucinated continuity from chat history.

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
`position-sizer.py --calc` runs inline during trade discussion (not after). Pulls live position sizing data from context. Outputs shares, % at risk, buffer impact, binding constraint.

**7. Session close = git push**
End-of-session protocol: list changed files → rebuild journal index → `git add -A && git commit && git push`. Framework versioned automatically.

**8. Two types of index files**
edge_lab has two distinct index patterns serving different purposes:

- `journal/INDEX.md` — **dynamically generated** by `scripts/build-index.py` every time a trade entry is added. The agent never manually maintains it. Run the script, it rebuilds from scratch. Always accurate.
- `playbook/README.md` — **mandatory-first-read** index. The CLAUDE.md explicitly enforces: *"ALWAYS read playbook/README.md first — it is the index. Use the Matching Guide to identify the correct setup file, then open only that file. Never open individual playbook files without reading the README index first."*

The distinction matters: the journal index is a catalog (what exists), the playbook index is a router (which one to open). Different jobs, different maintenance models.

**9. `calc.py` — math fully offloaded to Python**
12-command calculator covering every calculation type in swing trading: R:R, R multiple, week R, P&L, exposure, drawdown, avg cost, $ at risk, spot conversion, price vs levels. CLAUDE.md has a hard rule: agent never computes numbers in-context, always calls `calc.py` and shows output directly. Solves a real failure mode — LLM arithmetic compounds errors in long-context sessions; Python doesn't.

**10. Tested scripts**
Every script in `scripts/` has a corresponding `test_*.py`. Production-grade practices applied to a personal trading tool.

**11. Two-mode news system**
Two distinct protocols with different jobs — not one "news" command:

- **Morning Brief** (`/morning-brief` or "morning brief"): Runs last30days on 5 X accounts + Polymarket, filters output to facts only (strips sentiment, predictions, opinions), writes to `context/news-snapshot.md`. Curated, persistent, 4-6 bullets. Feeds the analysis context.
- **Daily Digest** (`/daily-digest` or "daily digest"): Runs last30days 5 times — one targeted call per account with account-matched topic keywords. Synthesizes into thematic narratives + notable events + upcoming items. Session only, never writes to a file. Comprehensive, informational, not tied to any analysis workflow.

The separation matters: morning brief is a context-preparation tool (facts → file → analysis). Daily digest is a reading tool (synthesis → understand what happened today). Same accounts, completely different intent and output.

**12. Global slash command skills**
`/morning-brief` and `/daily-digest` installed at `~/.claude/skills/` — available in any Claude Code session globally, not just edge_lab. Each skill is self-contained with the full protocol so it works standalone. The auto-triggers in CLAUDE.md also remain, so natural language and slash commands both work.

**13. `fetch-digest.py` — parked custom X scraper**
Built a direct X API scraper using `requests` + session cookies (AUTH_TOKEN + ct0) that bypasses last30days entirely. Pulls all original posts from all 5 accounts with recency-boosted engagement scoring and ID caching to avoid rate limits. Parked pending a valid Bearer token (last30days's internal bird-search client handles this; raw requests cannot use a stale public token). Lives at `scripts/fetch-digest.py` — activate by adding `X_BEARER_TOKEN` to `.env`.

---

### 3. Zenkai — Personalized AI Learning App

**Status:** Functional — end-to-end working for Module 2. 8 modules remaining for full content coverage.
**Repo:** `trentjhn/zenkai`
**Design doc:** `/Users/t-rawww/AI-Knowledgebase/docs/plans/2026-02-28-zenkai-design.md`

#### The Problem
Reading well-written reference material doesn't create retention. The AI-Knowledgebase had hundreds of pages of synthesized AI engineering content — but without active recall and spaced repetition, it stayed reference-only: useful to look up, not useful to apply from memory. The vision: something like Duolingo for AI, where learning is interactive, gated by mastery, and actually engaging.

#### What It Is
A local web app that turns this knowledge base into an interactive learning experience. Named after the DBZ Zenkai boost. Spaced repetition, scenario-based quizzes with AI PM framing, module gating (≥70% to unlock next).

#### Stack
- Frontend: React + Tailwind + shadcn/ui + Framer Motion
- Backend: FastAPI (Python)
- DB: SQLite (local)
- AI: Claude claude-sonnet-4-6 via Anthropic API

#### Key Design Decision
**Delta sync via git commit hashes** — compares KB file hash against last-generated hash. Only regenerates quiz content for files that actually changed. Avoids burning API credits on unchanged content every launch. The KB is the source of truth; Zenkai derives from it.

---

### 4. AI-Knowledgebase — Personal Knowledge Library

**Status:** Live (continuously growing)
**Location:** `/Users/t-rawww/AI-Knowledgebase/`
**Repo:** `trentjhn/AI-Knowledgebase` (private)

#### The Problem
AI engineering knowledge is scattered across 100+ papers, documentation sites, and blog posts of wildly varying depth. Most tutorials are either too shallow for practitioners or benchmark-focused — which decays fast as models improve. No single resource synthesized core concepts, frameworks, and operational playbooks at practitioner depth in a form that aged well.

#### What It Is
A personal AI knowledge library built for genuine depth — distilled, practitioner-level reference docs on core AI engineering topics. Built for personal use and as a methodology foundation for future consulting/audit work.

#### Architecture

```
AI-Knowledgebase/
├── CLAUDE.md                ← Behavioral contract + last30days research trigger
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

**3. Layered README index hierarchy**
This is the most architecturally deliberate thing in the KB — a 4-level README cascade that lets any reader (or AI agent) orient at any depth:

```
README.md                           ← Root: "what is this repo, what's where"
└── LEARNING/README.md              ← Section: learning path guide (Foundation→Build→Ship)
    ├── FOUNDATIONS/README.md       ← Subsection: what's in FOUNDATIONS, how long, prereqs
    ├── AGENTS_AND_SYSTEMS/README.md
    └── PRODUCTION/README.md
└── future-reference/README.md     ← Section: practical tools vs. study material
└── KB-INDEX.md                    ← Flat catalog: file paths, line counts, read times
```

Each level answers a different question:
- Root README: "Where do I start?"
- Section READMEs: "What's in this section, how long will it take, what should I read first?"
- KB-INDEX.md: "I know what I want — where exactly is it?"

This hierarchy means an AI agent dropped into this repo can navigate without being told anything. It reads README.md, gets oriented, follows the links to the right section README, then hits KB-INDEX.md for the specific file. **Progressive disclosure for navigation.**

**4. Frontier monitoring as its own document type**
`emerging-architectures.md` is intentionally not a tutorial. It's a Signal vs. Noise framework for evaluating new research — SSMs/Mamba, MoE, byte-level models, continuous/latent space. Designed to age well. The evaluation framework matters more than specific benchmarks, which decay fast.

**5. CLAUDE.md with last30days research trigger**
The KB now has a behavioral contract. The key rule: when asked to research or update any topic, automatically run `/last30days [topic] --sources=hackernews,youtube` before synthesizing. HN surfaces what engineers have actually discovered in the field; YouTube pulls transcript content from builders shipping real products. Output is session-only context — it supplements primary sources, never replaces them.

**6. builds-log.md (this file) as the meta-layer**
A record of what was built, why, and what patterns are running across systems. Turns building into deliberate practice — not just shipping and forgetting.

---

### 5. interview-prep — Job Search OS

**Status:** Live
**Location:** `/Users/t-rawww/interview-prep/`
**Config:** `CLAUDE.md` + `GEMINI.md`

#### The Problem
Running 10+ concurrent job applications means managing unique context for every company, hiring manager, interview format, and STAR story alignment — across weeks of sessions that share no memory. Notes apps stay static. Chat history resets. There was no system built for the actual complexity of a multi-track job search campaign.

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

### 6. mariana-interview — Case Study Preparation System

**Status:** Complete (used for Round 2 interview)
**Location:** `/Users/t-rawww/mariana-interview/`
**Config:** `CLAUDE.md`

#### The Problem
Generic PM templates solve the wrong problem in industrial domains. A standard PRD template optimizes for DAU/MAU, but in mining software you measure recovery rate and cost per ton. It assumes users are individual product managers, but plant operators and process engineers have different pain points. It ignores physical constraints (ore composition, flotation chemistry, equipment specs) that drive every technical decision. Using a generic template in a domain-specific case study produces a PRD that *looks* professional but solves the wrong problem at every section.

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

### 7. security-var-agent — Value-Added Reseller Recommendation Engine

**Status:** Functional (reached solid state, business case closed)
**Location:** `/Users/t-rawww/AI-Agent-Project/`
**Repo:** `trentjhn/security-var-agent` (GitHub public)

#### The Problem
VAR workflows require evaluating dozens of vendors across multiple dimensions (market position, technical fit, ROI, implementation complexity). Manual comparison is error-prone and time-consuming. Spreadsheet-based scoring misses market context and ROI implications. The result: recommendations based on incomplete analysis or vendor familiarity rather than systematic evaluation.

#### What It Is
A modular service-oriented architecture for comprehensive software solution recommendations. Analyzes client requirements, market conditions, and technical constraints to produce evidence-based vendor recommendations with ROI projections, implementation timelines, and confidence scoring.

#### Stack
- **Frontend:** React + TypeScript (AI Advisor chat interface, side-by-side recommendation comparison)
- **Backend:** Node.js + TypeScript (modular service architecture)
- **Services:** Context Understanding, Analysis, Recommendation Engine, ROI Calculator, Implementation Planning
- **Data:** Market Data Cache Service (99.9% hit rate), Confidence Scoring System
- **Infrastructure:** Supabase (data persistence), Jest (comprehensive test coverage)

#### Key Decisions and Why They're Elegant

**1. Modular service-oriented architecture**
Six independent services (Context, Analysis, Recommendation, ROI, Implementation, Data Freshness) composed by a central orchestrator. Each service is independently testable and replaceable. Changes to vendor scoring logic don't affect ROI calculation or confidence scoring.

**2. Market data cache with 99.9% hit rate**
Market data freshness is critical — recommendations should reflect current vendor positions and pricing. Caching strategy avoids redundant API calls while maintaining real-time context. Cache invalidation rules ensure stale data is caught before reaching recommendations.

**3. Confidence scoring system**
Not all recommendations are equally strong. The system quantifies confidence across four dimensions: market validation (vendor track record), technical fit (architecture compatibility), financial viability (ROI > threshold), and implementation feasibility (timeline realistic). Scoring is transparent to users — they see which recommendations are high-confidence vs. cautious.

**4. ROI calculator with detailed financial modeling**
Beyond "this vendor is cheaper" — the system models total cost of ownership (licensing + implementation + training + maintenance), payback period, and break-even timelines. Financial output is evidence-based and defensible.

**5. Implementation timeline visualization**
Recommendations include detailed phased timelines — pre-implementation (discovery, vendor selection), implementation (deployment, integration, testing), and post-implementation (training, optimization). Timelines account for parallel vs. sequential work, vendor constraints, and client readiness.

**6. TypeScript for type safety across service boundaries**
Services communicate via strict interfaces — a change to the Recommendation output format is caught at compile time across all consumers. Prevents silent failures where one service produces data another service doesn't expect.

**7. Comprehensive test suite**
Jest coverage for service logic, recommendation scoring, ROI calculations, and confidence algorithms. Ensures scoring logic stays consistent as vendor datasets and market conditions change.

**Project Status:** Built to specification for a VAR workflow automation opportunity. Reached functional state with core services operational. Client opportunity closed, but the system demonstrates patterns (modular scoring, financial modeling, confidence transparency) applicable to other recommendation engines (cloud provider selection, SaaS stack optimization, etc.).

---

## What These Systems Demonstrate

Collectively, these seven systems show depth across the full AI engineering stack:

Collectively, these six systems show depth across the full AI engineering stack:

**Full-Stack Capability**: From production deployment (YouTube Summarizer), full-stack architecture (Zenkai), to real-time automation (edge_lab). Not just backend or frontend — end-to-end product thinking.

**Sophisticated Prompt Engineering**: Production-grade techniques (dual-mode prompting, comprehensiveness principle, tone matching, few-shot learning embedded in prompts). Not generic "do better" instructions.

**Context Engineering at Scale**: Systems that manage complex context strategically — layered composition, conditional loading, token accounting, persistent state as files instead of chat memory.

**Economic Optimization**: Model selection driven by cost/context tradeoffs (33% cheaper, 8x larger window). Strategic math (token-per-word, cache invalidation) to prevent runtime surprises.

**State Management**: Systems that maintain real-world state (trading positions, job opportunities, KB content) and make decisions grounded in that state, not hallucinated context.

**Behavioral Contracts (CLAUDE.md/GEMINI.md)**: Explicit, persistent system instructions that enforce domain-specific vocabulary, constraints, and workflows. AI agents that respect boundaries.

**Dual AI Portability**: Same behavioral contract across different AI tools (Claude↔Gemini), proving that agent behavior can be decoupled from implementation.

These patterns are replicable and applicable to other AI systems beyond these six examples.

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
| **Behavioral contract (CLAUDE.md)** | 6 of 7 systems (all except VAR Agent) | Consistent agent behavior across sessions, no re-explaining |
| **Dual AI portability** | edge_lab, interview-prep | Claude↔Gemini handoff with zero behavior drift |
| **Conditional context loading** | YouTube Summarizer, mariana-interview, edge_lab | Load domain context on-demand — keep context window efficient |
| **Custom language constraints** | mariana-interview, interview-prep | Force domain-appropriate vocabulary at the system level |
| **Structured output folders** | mariana-interview, edge_lab (journal/), YouTube Summarizer | Persistent artifacts from sessions, not lost to chat history |
| **Non-interactive scripts** | edge_lab, YouTube Summarizer | Inline calculation/processing during workflow, not as a separate step |
| **Git as persistence layer** | edge_lab, interview-prep, KB, Zenkai | Version-controlled state — history is automatic |
| **Distillation over aggregation** | KB | Reference-able depth vs. bookmark pile |
| **Frontier monitoring layer** | KB (emerging-architectures) | Evaluate new research without chasing benchmarks |
| **DESIGN.md as design contract** | Website builds, Zenkai | AI tools know design intent before writing code |
| **Delta sync** | Zenkai, YouTube Summarizer (cache versioning) | Cost-efficient content/cache regeneration |
| **Session close = commit** | edge_lab | Automatic versioning without manual git discipline |
| **Phase-based workflows** | mariana-interview, website builds | Structured execution that mirrors real-world constraints |
| **Layered README index hierarchy** | AI-Knowledgebase | Agent (or human) orients at any depth without being told what to read |
| **Dynamic index generation** | edge_lab (journal/INDEX.md) | Index always accurate — rebuilt from source, never manually maintained |
| **Mandatory-first-read index** | edge_lab (playbook/README.md) | Enforced routing — never open sub-files without reading the index first |
| **Math offloading to scripts** | edge_lab (calc.py, position-sizer.py) | Eliminates LLM arithmetic errors entirely — deterministic by design |
| **Token accounting strategy** | YouTube Summarizer | Conservative limits, explicit buffer math, prevent runtime surprises |
| **Production-grade prompt engineering** | YouTube Summarizer | Comprehensiveness principle, faithful representation, tone matching, few-shot examples embedded |
| **Trusted sources constraint** | edge_lab (6 X accounts in CLAUDE.md) | Agent only pulls from named, curated accounts — not the open web |
| **Middle layer / news filter** | edge_lab (news-snapshot.md) | Raw news filtered to facts before reaching analysis layer; thesis ownership stays with human |
| **Modular service architecture** | security-var-agent | Services independently testable/replaceable; changes in one domain don't cascade |
| **Confidence scoring transparency** | security-var-agent | Quantified confidence across multiple dimensions; recommendations include explicit strength assessment |
| **Financial modeling + ROI clarity** | security-var-agent | Detailed cost modeling prevents false economies; breaks down total cost of ownership |
