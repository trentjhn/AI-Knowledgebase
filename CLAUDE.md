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

## GitHub
Repo: `trentjhn/AI-Knowledgebase` (private)
Branch: `main`
After any session with meaningful changes: `git add -A && git commit -m "..." && git push origin main`
