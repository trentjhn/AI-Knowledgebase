# AI Knowledgebase

## Purpose
Personal AI knowledge library. Distilled, practitioner-depth reference docs on AI engineering topics.
Built for personal reference and as a methodology foundation for consulting/audit work.

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
- After adding or updating content: commit and push to GitHub
- When adding a new topic: update `KB-INDEX.md` with file path, line count, read time, one-liner
- Playbooks in `future-reference/playbooks/` are updated when new build techniques are learned

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
