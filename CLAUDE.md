# AI Knowledgebase

## Purpose

Personal AI knowledge library. Distilled, practitioner-depth reference docs on AI engineering topics.

**Primary Use Case:** Decision rubric for all new projects. When proposing any idea—building an agent, designing a system, evaluating tech, writing specs, optimizing infrastructure—Claude retrieves relevant KB sections and grounds recommendations in captured best practices. The KB is the operational foundation for sound judgment, not just a reference library.

**Secondary Uses:**
- Personal reference and continuous learning
- Methodology foundation for consulting/audit work
- Rubric for decision-making across projects

## Pattern Recognition — Active Decision Rubric

When any project idea, system design, or problem is described: scan these signals and surface matching pattern(s) *before* implementation. Multiple signals can fire simultaneously — surface all matches and frame the decision explicitly. Never pick one silently.

**Navigation:** Patterns below identify the right *doc*. For section-level routing within large docs (especially `agentic-engineering.md`, `evaluation.md`, `ai-security.md`), consult `KB-INDEX.md` first — it has exact line ranges and section descriptions for every file. Read the targeted section, not the full doc.

**Reference format below:** Full path from KB root for direct Read access.

### Multi-Agent Architecture
**AGENT TEAMS** — peer sessions with shared task list + direct messaging
Signals: "multiple perspectives," "parallel investigation," "different angles," "competing hypotheses," "multi-layer build (frontend/backend/tests)," "parallel reviewers," "agents debate each other," "independent workstreams"
→ `LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agent-teams.md`
→ `future-reference/playbooks/multi-agent-orchestration.md → Claude Code Agent Teams section`

**SUBAGENTS** — disposable workers; only the result returns to the main session
Signals: "just need the result," "side task flooding context," "research in background," "delegate and summarize," "parallel but results come back to me"
→ `LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md → Section 7`

**SELF-ORGANIZING AGENTS** — emergent role discovery; agents decide what's needed
Signals: "don't know what the roles should be," "task structure varies widely," "agents should figure it out," "N > 8 agents," "emergent specialization"
→ `future-reference/playbooks/multi-agent-orchestration.md → Self-Organizing section`

### Retrieval & Context
**RAG PIPELINE** — document search, semantic retrieval, Q&A over a corpus
Signals: "search my documents," "answer questions about [corpus]," "retrieve relevant context," "knowledge base search," "company docs," "find information in"
→ `future-reference/playbooks/building-rag-pipelines.md`

**CONTEXT ENGINEERING** — what goes in the context window and how
Signals: "losing track of earlier context," "context too long," "forgetting instructions," "what to put in system prompt," "noise in context," "context window filling up"
→ `LEARNING/FOUNDATIONS/context-engineering/context-engineering.md`

### Model Selection
**REASONING MODELS** — extended thinking, o3-class, complex multi-step problems
Signals: "complex multi-step reasoning," "needs to plan before acting," "math or logic heavy," "architectural decisions with many constraints," "think hard before answering"
→ `LEARNING/FOUNDATIONS/reasoning-llms/reasoning-llms.md`

**FINE-TUNING** — behavior that prompting can't reliably produce
Signals: "always responds a certain way," "style prompting can't capture," "thousands of labeled examples," "domain-specific behavior," "too expensive at inference time," "behavior that prompting doesn't fix"
→ `LEARNING/PRODUCTION/fine-tuning/fine-tuning.md`

### Quality & Production
**EVALUATION** — measuring whether the AI system actually works
Signals: "does it actually work," "measure quality," "catch regressions," "A/B test prompts," "how do I know it's improving," "benchmark," "production monitoring"
→ `LEARNING/PRODUCTION/evaluation/evaluation.md`

**AI SECURITY** — threat modeling, attack vectors, production safety
Signals: "security review," "prompt injection," "what could go wrong adversarially," "data exposure," "trust boundaries," "production safety," "compliance," "audit"
→ `LEARNING/PRODUCTION/ai-security/ai-security.md`

**SPECIFICATION** — writing unambiguous requirements for AI systems
Signals: "requirements aren't clear," "keeps getting the wrong output," "scope creep," "how to write the spec," "ambiguous instructions," "acceptance criteria"
→ `LEARNING/PRODUCTION/specification-clarity/specification-clarity.md`

**INFERENCE OPTIMIZATION** — latency, throughput, cost at production scale
Signals: "too slow at inference," "serving costs too high," "self-hosting," "latency matters," "high throughput," "10M+ tokens/day," "quantization"
→ `LEARNING/PRODUCTION/inference-optimization/inference-optimization.md`

### Tooling
**MCP** — connecting AI to external systems, tools, APIs
Signals: "connect to [external tool]," "give the agent access to," "tool integrations," "Claude needs to call [API]," "build an MCP server," "external system access"
→ `LEARNING/AGENTS_AND_SYSTEMS/mcp/mcp.md`

### Common Multi-Pattern Scenarios
- RAG + Evaluation → any retrieval system needs eval from day one
- Agent Teams + Security → multi-agent systems need trust boundary analysis
- Fine-tuning + Evaluation → fine-tuning without evals is guessing
- Reasoning Models + Cost → extended thinking is expensive; always check if prompting suffices first

## Structure
- `LEARNING/` — evergreen conceptual knowledge (what things are, how they work)
  - `FOUNDATIONS/` → `AGENTS_AND_SYSTEMS/` → `PRODUCTION/` learning path
- `future-reference/` — operational protocols and playbooks (how to build things)
- `CAREER/` — PM context, interview materials
- `KB-INDEX.md` — flat navigation catalog (line counts, read times, descriptions)
- `builds-log.md` — running record of AI systems built
- `raw/` — sourced raw materials (papers, digests, datasets)
  - `raw/arxiv-papers/` — auto-generated weekly ArXiv research digests (see Automated Systems below)
- `.sessions/` — **local only, not in GitHub** — session workspace for in-progress investigations, design explorations, and working notes that don't yet warrant formal KB structure
- `.scripts/` — **hidden from public view** — automation scripts (ArXiv scraper, etc.)

## Automated Systems

### ArXiv Weekly Research Digest

**What it does:** Every Friday at 8am UTC, GitHub Actions automatically queries ArXiv for AI research papers matching your KB topics from the past 1-4 weeks, filters by citation count (1+), and deposits results in `raw/arxiv-papers/YYYY-MM-DD.md`.

**How it works:**
1. `.scripts/arxiv-scraper.py` — Queries ArXiv API for 9 KB topics (Prompt Engineering, Context Engineering, Reasoning LLMs, etc.)
2. Fetches ~10 papers per topic from 1-4 weeks prior
3. Queries Semantic Scholar for citation counts (keeps papers with 1+ citations)
4. Deduplicates papers that match multiple topics
5. Formats as markdown with abstracts, links, and topic tags
6. Writes to `raw/arxiv-papers/{YYYY-MM-DD}.md`
7. Auto-commits and pushes to GitHub

**Output:** ~4-6 quality papers per week in `raw/arxiv-papers/`

**Integration:** Review digest when available, manually integrate interesting papers into KB docs by adding them to the sources list and synthesizing findings into the appropriate topic doc.

**Configuration:** Adjustable thresholds in `.scripts/arxiv-scraper.py`:
- `CITATION_THRESHOLD = 1` (line 57) — minimum citations to include
- Date window in `get_date_range()` (lines 59-63)
- `max_results=10` (line 90) — papers per query

## Research Protocol — last30days
When asked to research, update, or distill a topic (e.g. "let's update the agentic engineering doc",
"research MCP patterns", "what's new in inference optimization", "gather context on X"):

→ Before synthesizing, automatically run the last30days skill for HN + YouTube on that topic:
  `/last30days [topic] --sources=hackernews,youtube --days=30`
  Use `--days=7` for rapidly evolving topics (new model releases, breaking tooling changes).

→ Use output as supplementary context only — community discoveries and recent discussions.
  It does not replace primary sources (papers, official docs). It surfaces what practitioners
  have found in the field that papers haven't captured yet.

→ Do not save last30days output to a file. Session context only.
  If something warrants permanent capture, synthesize it into the relevant KB doc.

## Writing Standards (critical — learned from explicit feedback)
Every KB doc must be educational first, reference second:

1. **Open every concept with plain English** before any technical detail
2. **Define jargon on first use** — never assume familiarity (RAG, CoT, LoRA, etc.)
3. **Use analogies** to ground abstract concepts in familiar experience
4. **Prose before bullets/tables** — build understanding first, then summarize
5. **"Why this matters"** for every concept — motivation, not just definition
6. **Narrative failure modes** — explain what goes wrong as a story, not a bullet list
7. **Concrete examples** with realistic data, not placeholders
8. **Tables only for genuine comparison** — not as a substitute for explanation

## Workflow
- Primary doc per folder — one comprehensive synthesized file, not a collection of fragments
- Distill from sources — synthesize, never copy verbatim
- **After any KB content change (adding/updating sections):**
  - Commit changes to the KB file itself
  - Update `KB-INDEX.md` with new line ranges, sections, and brief descriptions
  - Update any folder-level README if the doc structure changed
  - Commit all index updates together with KB edits
- When adding a new topic: update `KB-INDEX.md` with file path, line count, read time, one-liner
- Playbooks in `future-reference/playbooks/` are updated when new build techniques are learned
- **Catalog-first convention:** When adding any agent to `agent-catalog/`, skill to `skills-catalog/`, or prompt to `prompt-catalog/`: write the `CATALOG.md` entry first, then create the file. Never create a catalog file without a corresponding index entry.
- **After any KB content change that introduces new patterns, capabilities, or architectural guidance:** Review `future-reference/playbooks/magnum-opus.md` and update the relevant phase pointer if the new content should inform project decisions. The magnum opus is only as good as its KB references.

## Session Management — `.sessions/` Workspace

When working on investigations, design explorations, or problems that don't yet have a clear KB home:

- Store working notes, drafts, decision logs in `.sessions/[topic]/` (e.g., `.sessions/arxiv-filtering/`)
- **Never commit `.sessions/` to GitHub** — it's local-only workspace for continuity between sessions
- Files here are read by Claude each session to pick up mid-investigation without losing context
- Once work solidifies into a KB doc or decision, move insights to the formal structure and clean up `.sessions/`

This allows:
- Mid-session context preservation ("we were exploring X, here's where we left off")
- Design explorations that might not make the KB but inform future work
- Investigation logs that help trace how decisions were made

## GitHub
Repo: `trentjhn/AI-Knowledgebase` (private)
Branch: `main`
After any session with meaningful changes: `git add -A && git commit -m "..." && git push origin main`
Note: `.sessions/` is git-ignored and never pushed.
