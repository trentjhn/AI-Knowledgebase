# ArXiv Automated KB Integration Pipeline — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans (if available) or follow manually to implement this plan task-by-task.

**Goal:** Build a three-job GitHub Actions pipeline that automatically fetches full arXiv paper HTML, deep-dives content, routes to the right KB sections, writes integrations, updates KB-INDEX and playbooks, and produces a human-readable weekly summary — all committing per paper for surgical revertability.

**Architecture:** Job 2 (`arxiv-deep-dive.py`) fans out parallel threads per paper, fetches arXiv HTML, calls Claude API with integration rubric, outputs structured proposals JSON. Job 3 (`arxiv-integrate.py`) reads proposals sequentially, re-reads target KB files between each write to avoid line drift, commits per paper, then writes the weekly summary. GitHub Actions chains: `generate-digest → deep-dive-analysis → kb-integration`.

**Tech Stack:** Python 3.11, `anthropic`, `requests`, `beautifulsoup4`, `subprocess` for git, GitHub Actions `needs:` chaining.

---

## Task 1: Create directory structure + integration-rubric.md

**Files:**
- Create: `raw/arxiv-proposals/.gitkeep`
- Create: `raw/arxiv-weekly-summary/.gitkeep`
- Create: `.scripts/integration-rubric.md`

**Step 1: Create the two new raw directories with gitkeep**

```bash
touch /Users/t-rawww/AI-Knowledgebase/raw/arxiv-proposals/.gitkeep
touch /Users/t-rawww/AI-Knowledgebase/raw/arxiv-weekly-summary/.gitkeep
```

**Step 2: Write integration-rubric.md**

Create `.scripts/integration-rubric.md` with this content:

```markdown
# KB Integration Rubric — CI Version

Used by the automated deep-dive pipeline. Distilled from kb-paper-integration skill.

## Quality Gate (run first — if any fail, confidence ≤ 0.60)

1. **Is this a mechanism, not an application?**
   - MECHANISM: generalizable pattern, insight into why something works/fails
   - APPLICATION: domain-specific deployment, infrastructure tuning, benchmark chasing
   - If application with no extractable mechanism: confidence ≤ 0.50, skip integration

2. **Does it generalize?**
   - Would this pattern apply to other agents/prompts/systems beyond the paper's domain?
   - Yes → proceed. No → confidence ≤ 0.55

3. **Does it fill a gap or contradict existing KB content?**
   - Read KB-INDEX to see what the target section already covers
   - Duplicates existing content without new insight → confidence ≤ 0.55
   - Fills gap or contradicts existing assumption → high value

## KB Section Routing (primary destination)

| Paper focus | Primary KB file |
|---|---|
| Prompting technique, few-shot, output control | LEARNING/FOUNDATIONS/prompt-engineering/prompt-engineering.md |
| RAG, retrieval, context selection, context window | LEARNING/FOUNDATIONS/context-engineering/context-engineering.md |
| Reasoning, CoT, planning, thinking effort | LEARNING/FOUNDATIONS/reasoning-llms/reasoning-llms.md |
| Multimodal, vision-language, audio, video | LEARNING/FOUNDATIONS/multimodal/multimodal.md |
| Emerging architectures, SSM, MoE, tokenization | LEARNING/FOUNDATIONS/emerging-architectures/emerging-architectures.md |
| Agent architecture, tool use, orchestration, HITL | LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md |
| Multi-agent systems, coordination, self-organizing | LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md |
| Claude Agent SDK patterns, Task tool, subagents | LEARNING/AGENTS_AND_SYSTEMS/agent-sdk/agent-sdk.md |
| MCP, external tools, API integration | LEARNING/AGENTS_AND_SYSTEMS/mcp/mcp.md |
| Skills, reusable instruction patterns | LEARNING/AGENTS_AND_SYSTEMS/skills/skills.md |
| Evaluation, benchmarking, LLM-as-judge | LEARNING/PRODUCTION/evaluation/evaluation.md |
| Security, jailbreak, adversarial, prompt injection | LEARNING/PRODUCTION/ai-security/ai-security.md |
| Fine-tuning, LoRA, RLHF, DPO | LEARNING/PRODUCTION/fine-tuning/fine-tuning.md |
| RL alignment, GRPO, reward hacking, RLVR | LEARNING/PRODUCTION/rl-alignment/rl-alignment.md |
| Inference, latency, quantization, serving | LEARNING/PRODUCTION/inference-optimization/inference-optimization.md |
| Specification, requirements, acceptance criteria | LEARNING/PRODUCTION/specification-clarity/specification-clarity.md |

## Secondary Section Rules

Only add a secondary section if:
- The finding is DIRECTLY actionable there (not just "mentioned")
- You can write 2-3 distinct, non-redundant sentences for the secondary
- The two insights are genuinely different angles (not the same point restated)

## Section Anchor Format

The `section_anchor` field must be an EXACT QUOTE of a section heading from the target KB file — the text that appears after `## ` or `### ` in that file. Examples:
- "Special Case: Function-Calling Agents and the Reasoning Paradox"
- "LLM-as-Judge: Using AI to Evaluate AI"
- "Reward Hacking and the Alignment Tax"

Use KB-INDEX section descriptions to identify the right heading. The integration script searches for this heading literally in the file.

## Playbook Routing

Update a playbook ONLY when the paper has PRACTICAL, IMPLEMENTABLE methodology:
- Code patterns, deployment checklists, validation metrics, step-by-step procedures
- NOT: theoretical findings alone (those go in KB docs only)

Relevant playbooks:
- `future-reference/playbooks/building-ai-agents.md` — agent build patterns
- `future-reference/playbooks/building-rag-pipelines.md` — RAG methodology
- `future-reference/playbooks/multi-agent-orchestration.md` — multi-agent deployment
- `future-reference/playbooks/cost-optimized-llm-workflows.md` — cost/efficiency
- `future-reference/playbooks/production-agent-patterns.md` — HITL, stateful agents

## Magnum Opus Flag

Flag for magnum-opus update if the paper introduces a pattern that should inform project-level decisions (not just KB reference). Phrase as: "Phase N ([phase name]) — [one sentence on what should be added/updated]"

## Output Format

Return ONLY valid JSON matching this schema exactly:
{
  "paper_id": "string",
  "title": "string",
  "html_available": boolean,
  "quality_gate": {
    "is_mechanism": boolean,
    "generalizes": boolean,
    "fills_gap": boolean,
    "confidence": float
  },
  "kb_routing": {
    "primary_file": "string (relative path from repo root)",
    "section_anchor": "string (exact section heading text from KB file)",
    "secondary_file": null or "string"
  },
  "playbook_routing": {
    "applies": boolean,
    "playbook_file": null or "string",
    "section_anchor": null or "string"
  },
  "magnum_opus_flag": null or "string",
  "key_findings": "string (2-3 sentences, empirical numbers where available)",
  "draft_kb_text": "string (full prose, KB writing standards: plain English first, define jargon, narrative before bullets, concrete examples)",
  "draft_playbook_text": null or "string",
  "highlights_blurb": "string (2 sentences — what it found and why a practitioner should care)"
}
```

**Step 3: Commit**

```bash
git add raw/arxiv-proposals/.gitkeep raw/arxiv-weekly-summary/.gitkeep .scripts/integration-rubric.md
git commit -m "feat(arxiv): scaffold automation directories and integration rubric"
```

---

## Task 2: Write digest parser with unit test

**Files:**
- Create: `.scripts/arxiv-deep-dive.py` (initial: parse_digest only)
- Create: `.scripts/tests/test_deep_dive.py`

**Step 1: Write failing test**

Create `.scripts/tests/test_deep_dive.py`:

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

SAMPLE_DIGEST = """# ArXiv Digest — April 17, 2026
*Generated: 2026-04-17 09:24 UTC*

**KB-Relevant Papers: 2 (filtered from 50)**

1. **Think Anywhere in Code Generation**
   - **Published:** 2026-03-31
   - **KB Topics:** Reasoning LLMs
   - **Abstract:** The paper introduces Think-Anywhere...
   - **Link:** [2603.29957v1](https://arxiv.org/abs/2603.29957v1)
   - **ArXiv Topics:** cs.SE

2. **Context Over Content**
   - **Published:** 2026-04-16
   - **KB Topics:** Evaluation, AI Security
   - **Abstract:** The LLM-as-a-judge paradigm...
   - **Link:** [2604.15224v1](https://arxiv.org/abs/2604.15224v1)
   - **ArXiv Topics:** Alignment & Safety
"""

def test_parse_digest_count():
    from arxiv_deep_dive import parse_digest
    papers = parse_digest(SAMPLE_DIGEST)
    assert len(papers) == 2

def test_parse_digest_fields():
    from arxiv_deep_dive import parse_digest
    papers = parse_digest(SAMPLE_DIGEST)
    assert papers[0]['id'] == '2603.29957v1'
    assert papers[0]['title'] == 'Think Anywhere in Code Generation'
    assert papers[0]['abstract'] == 'The paper introduces Think-Anywhere...'
    assert papers[0]['kb_topics'] == ['Reasoning LLMs']

def test_parse_digest_second_paper():
    from arxiv_deep_dive import parse_digest
    papers = parse_digest(SAMPLE_DIGEST)
    assert papers[1]['id'] == '2604.15224v1'
    assert 'Evaluation' in papers[1]['kb_topics']
    assert 'AI Security' in papers[1]['kb_topics']
```

**Step 2: Run tests to see them fail**

```bash
cd /Users/t-rawww/AI-Knowledgebase
python -m pytest .scripts/tests/test_deep_dive.py -v
```

Expected: `ModuleNotFoundError: No module named 'arxiv_deep_dive'`

**Step 3: Create arxiv-deep-dive.py with parse_digest**

Create `.scripts/arxiv-deep-dive.py`:

```python
#!/usr/bin/env python3
"""
ArXiv Deep Dive — Job 2 of the automated KB integration pipeline.

Reads the latest weekly digest, fetches full paper HTML for each paper,
calls Claude API to analyze and route, outputs structured proposals JSON.
"""

import re
import json
import os
import sys
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
import anthropic
from bs4 import BeautifulSoup


REPO_ROOT = Path(__file__).parent.parent
ARXIV_HTML_BASE = "https://arxiv.org/html"
MAX_WORKERS = 5
CONFIDENCE_THRESHOLD = 0.80


def parse_digest(content: str) -> list[dict]:
    """Parse digest markdown, return list of paper dicts."""
    papers = []
    # Match numbered paper entries
    entry_pattern = re.compile(
        r'\d+\.\s+\*\*(.+?)\*\*\n'           # title
        r'.*?- \*\*Published:\*\* (.+?)\n'    # published
        r'.*?- \*\*KB Topics:\*\* (.+?)\n'    # kb_topics
        r'.*?- \*\*Abstract:\*\* (.+?)\n'     # abstract
        r'.*?- \*\*Link:\*\* \[(.+?)\]',      # arxiv id
        re.DOTALL
    )
    for m in entry_pattern.finditer(content):
        kb_topics = [t.strip() for t in m.group(3).split(',')]
        papers.append({
            'title': m.group(1).strip(),
            'published': m.group(2).strip(),
            'kb_topics': kb_topics,
            'abstract': m.group(4).strip(),
            'id': m.group(5).strip(),
        })
    return papers


def find_latest_digest() -> Path:
    """Return path to the most recently generated digest."""
    digest_dir = REPO_ROOT / 'raw' / 'arxiv-papers'
    digests = sorted(digest_dir.glob('*.md'), reverse=True)
    if not digests:
        raise FileNotFoundError("No digest files found in raw/arxiv-papers/")
    return digests[0]
```

**Step 4: Add `__init__.py` so tests can import the module**

```bash
touch /Users/t-rawww/AI-Knowledgebase/.scripts/__init__.py
touch /Users/t-rawww/AI-Knowledgebase/.scripts/tests/__init__.py
```

**Step 5: Run tests — expect pass**

```bash
cd /Users/t-rawww/AI-Knowledgebase
python -m pytest .scripts/tests/test_deep_dive.py::test_parse_digest_count .scripts/tests/test_deep_dive.py::test_parse_digest_fields .scripts/tests/test_deep_dive.py::test_parse_digest_second_paper -v
```

Expected: `3 passed`

**Step 6: Commit**

```bash
git add .scripts/arxiv-deep-dive.py .scripts/tests/test_deep_dive.py .scripts/__init__.py .scripts/tests/__init__.py
git commit -m "feat(arxiv): add digest parser with tests"
```

---

## Task 3: HTML fetcher + section extractor

**Files:**
- Modify: `.scripts/arxiv-deep-dive.py` — add `fetch_paper_html()` and `extract_sections()`
- Modify: `.scripts/tests/test_deep_dive.py` — add HTML extraction tests

**Step 1: Write failing tests**

Add to `.scripts/tests/test_deep_dive.py`:

```python
SAMPLE_HTML = """
<html><body>
<section id="S1"><h2>1 Introduction</h2><p>This paper presents a novel approach.</p></section>
<section id="S2"><h2>2 Method</h2><p>We use GRPO with alpha=0.1.</p></section>
<section id="S3"><h2>3 Experiments</h2><p>Results on LeetCode: 69.4%.</p></section>
<section id="S4"><h2>4 Ablation</h2><p>Without cold start: 47.9%.</p></section>
<section id="S5"><h2>5 Conclusion</h2><p>Think-Anywhere achieves SOTA.</p></section>
</body></html>
"""

def test_extract_sections_finds_method():
    from arxiv_deep_dive import extract_sections
    result = extract_sections(SAMPLE_HTML)
    assert 'GRPO' in result

def test_extract_sections_finds_results():
    from arxiv_deep_dive import extract_sections
    result = extract_sections(SAMPLE_HTML)
    assert '69.4%' in result

def test_extract_sections_finds_ablation():
    from arxiv_deep_dive import extract_sections
    result = extract_sections(SAMPLE_HTML)
    assert '47.9%' in result
```

**Step 2: Run to confirm failure**

```bash
python -m pytest .scripts/tests/test_deep_dive.py::test_extract_sections_finds_method -v
```

Expected: `ImportError` or `AttributeError`

**Step 3: Implement in arxiv-deep-dive.py**

Add after `find_latest_digest()`:

```python
TARGET_SECTIONS = {
    'abstract', 'introduction', 'method', 'methodology',
    'approach', 'experiment', 'result', 'ablation',
    'analysis', 'conclusion', 'limitation', 'discussion'
}


def extract_sections(html_content: str) -> str:
    """Extract key sections from arXiv HTML. Returns concatenated text."""
    soup = BeautifulSoup(html_content, 'html.parser')
    extracted = []

    for section in soup.find_all(['section', 'div'], recursive=True):
        heading = section.find(['h1', 'h2', 'h3'])
        if not heading:
            continue
        heading_text = heading.get_text().lower().strip()
        # Strip leading numbers: "3 Experiments" → "experiments"
        heading_clean = re.sub(r'^\d+\.?\s*', '', heading_text)
        if any(kw in heading_clean for kw in TARGET_SECTIONS):
            extracted.append(section.get_text(separator=' ', strip=True))

    return '\n\n'.join(extracted) if extracted else ''


def fetch_paper_html(arxiv_id: str) -> tuple[str, bool]:
    """
    Fetch full paper HTML from arxiv.org/html/{id}.
    Returns (content, html_available).
    Falls back to empty string if unavailable.
    """
    # Strip version for HTML endpoint (arxiv html uses base id)
    base_id = re.sub(r'v\d+$', '', arxiv_id)
    url = f"{ARXIV_HTML_BASE}/{base_id}"
    try:
        resp = requests.get(url, timeout=20)
        if resp.status_code == 200:
            sections = extract_sections(resp.text)
            if sections:
                return sections, True
        return '', False
    except requests.RequestException:
        return '', False
```

**Step 4: Run tests — expect pass**

```bash
python -m pytest .scripts/tests/test_deep_dive.py -v
```

Expected: `6 passed`

**Step 5: Commit**

```bash
git add .scripts/arxiv-deep-dive.py .scripts/tests/test_deep_dive.py
git commit -m "feat(arxiv): add HTML fetcher and section extractor with tests"
```

---

## Task 4: Claude API analysis → proposals JSON

**Files:**
- Modify: `.scripts/arxiv-deep-dive.py` — add `analyze_paper()` and `run_deep_dive()`

**Step 1: Add analyze_paper() to arxiv-deep-dive.py**

Add after `fetch_paper_html()`:

```python
ANALYSIS_SYSTEM_PROMPT = """You are an expert research analyst for a practitioner-depth AI knowledge base.
Your task: analyze a research paper and produce a structured integration proposal.

You will receive:
1. The KB integration rubric (routing rules, quality gate, output format)
2. The current KB-INDEX (what sections exist and what they cover)
3. The paper content (key sections: methods, results, ablation, conclusion)

Follow the rubric exactly. Return ONLY valid JSON — no markdown fences, no explanation.
The draft_kb_text must follow KB writing standards: plain English first, define jargon on first use,
narrative prose before bullets, concrete examples with real numbers, no placeholder text."""


def load_rubric_and_index() -> tuple[str, str]:
    rubric = (REPO_ROOT / '.scripts' / 'integration-rubric.md').read_text()
    kb_index = (REPO_ROOT / 'KB-INDEX.md').read_text()
    return rubric, kb_index


def analyze_paper(paper: dict, rubric: str, kb_index: str) -> dict:
    """
    Fetch paper HTML and call Claude API to produce a structured proposal.
    Returns proposal dict matching the proposals JSON schema.
    """
    paper_content, html_available = fetch_paper_html(paper['id'])

    # Fallback: use abstract if HTML unavailable
    if not html_available:
        paper_content = f"Abstract: {paper['abstract']}"

    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    user_message = f"""INTEGRATION RUBRIC:
{rubric}

KB-INDEX (current KB structure):
{kb_index}

PAPER TO ANALYZE:
Title: {paper['title']}
ArXiv ID: {paper['id']}
Published: {paper['published']}
KB Topics (pre-scored): {', '.join(paper['kb_topics'])}
HTML Available: {html_available}

Paper Content:
{paper_content[:40000]}"""  # Cap at 40K chars to stay within context

    try:
        response = client.messages.create(
            model='claude-sonnet-4-6',
            max_tokens=4000,
            system=ANALYSIS_SYSTEM_PROMPT,
            messages=[{'role': 'user', 'content': user_message}]
        )
        result = json.loads(response.content[0].text.strip())
        result['paper_id'] = paper['id']
        result['title'] = paper['title']
        result['html_available'] = html_available
        # Cap confidence if HTML unavailable
        if not html_available:
            result['quality_gate']['confidence'] = min(
                result['quality_gate']['confidence'], 0.60
            )
        return result
    except (json.JSONDecodeError, KeyError, Exception) as e:
        print(f"  Analysis failed for {paper['id']}: {e}", file=sys.stderr)
        return {
            'paper_id': paper['id'],
            'title': paper['title'],
            'html_available': html_available,
            'quality_gate': {'confidence': 0.0, 'is_mechanism': False,
                             'generalizes': False, 'fills_gap': False},
            'error': str(e)
        }


def run_deep_dive(digest_path: Path) -> Path:
    """Main orchestration: parse digest → parallel analysis → write proposals JSON."""
    content = digest_path.read_text()
    papers = parse_digest(content)

    if not papers:
        print("No papers found in digest.", file=sys.stderr)
        sys.exit(0)

    print(f"Analyzing {len(papers)} papers...", file=sys.stderr)
    rubric, kb_index = load_rubric_and_index()

    proposals = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(analyze_paper, paper, rubric, kb_index): paper
            for paper in papers
        }
        for future in as_completed(futures):
            paper = futures[future]
            try:
                proposal = future.result()
                proposals.append(proposal)
                conf = proposal.get('quality_gate', {}).get('confidence', 0)
                print(f"  ✓ {paper['id']} — confidence: {conf:.2f}", file=sys.stderr)
            except Exception as e:
                print(f"  ✗ {paper['id']} — {e}", file=sys.stderr)
            time.sleep(0.5)  # Gentle rate limiting

    # Write proposals JSON
    date_str = datetime.now().strftime('%Y-%m-%d')
    output_path = REPO_ROOT / 'raw' / 'arxiv-proposals' / f'{date_str}.json'
    output_path.write_text(json.dumps(proposals, indent=2))
    print(f"Proposals written to {output_path}", file=sys.stderr)
    return output_path


if __name__ == '__main__':
    digest = find_latest_digest()
    print(f"Processing digest: {digest.name}", file=sys.stderr)
    run_deep_dive(digest)
```

**Step 2: Verify script runs without import errors**

```bash
cd /Users/t-rawww/AI-Knowledgebase
python -c "from arxiv_deep_dive import analyze_paper, run_deep_dive; print('imports ok')"
```

Expected: `imports ok`

**Step 3: Commit**

```bash
git add .scripts/arxiv-deep-dive.py
git commit -m "feat(arxiv): add Claude API analysis and deep-dive orchestration"
```

---

## Task 5: insert_at_anchor() with unit tests — the critical function

**Files:**
- Create: `.scripts/tests/test_integrate.py`
- Create: `.scripts/arxiv-integrate.py` (initial: insert_at_anchor only)

**Step 1: Write failing tests — test all anchor edge cases**

Create `.scripts/tests/test_integrate.py`:

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

SAMPLE_KB = """# Reasoning LLMs

## What Makes a Reasoning Model Different?

Standard LLMs work like this: immediate response generation.

## Thinking Effort: Controlling How Much They Think

Use budget_tokens to control reasoning depth.

| Tier | Range | When to Use |
|---|---|---|
| Low | 1024-3000 | Simple problems |
| High | 15000-32000 | Complex analysis |

## Special Case: Function-Calling Agents and the Reasoning Paradox

Excessive reasoning degrades tool routing accuracy.

## Limitations and What Goes Wrong

Reasoning models aren't magic.
"""

def test_insert_at_anchor_basic():
    from arxiv_integrate import insert_at_anchor
    new_text = "## New Section\n\nThis is new content."
    result, success = insert_at_anchor(
        SAMPLE_KB,
        "Special Case: Function-Calling Agents and the Reasoning Paradox",
        new_text
    )
    assert success is True
    assert "New Section" in result
    # New section should appear AFTER function-calling section
    fc_pos = result.index("Special Case: Function-Calling")
    new_pos = result.index("New Section")
    assert new_pos > fc_pos

def test_insert_at_anchor_before_next_section():
    from arxiv_integrate import insert_at_anchor
    new_text = "## Inserted Section\n\nInserted content."
    result, success = insert_at_anchor(
        SAMPLE_KB,
        "Special Case: Function-Calling Agents and the Reasoning Paradox",
        new_text
    )
    assert success is True
    # Should be inserted before "## Limitations"
    new_pos = result.index("Inserted Section")
    limits_pos = result.index("Limitations and What Goes Wrong")
    assert new_pos < limits_pos

def test_insert_at_anchor_not_found():
    from arxiv_integrate import insert_at_anchor
    result, success = insert_at_anchor(
        SAMPLE_KB,
        "This Section Does Not Exist",
        "## New\n\nContent."
    )
    assert success is False
    assert result == SAMPLE_KB  # Content unchanged

def test_insert_at_anchor_end_of_file():
    from arxiv_integrate import insert_at_anchor
    content = "# Doc\n\n## Last Section\n\nSome content."
    result, success = insert_at_anchor(content, "Last Section", "## Appended\n\nContent.")
    assert success is True
    assert result.endswith("## Appended\n\nContent.")
```

**Step 2: Run to confirm failure**

```bash
python -m pytest .scripts/tests/test_integrate.py -v
```

Expected: `ModuleNotFoundError: No module named 'arxiv_integrate'`

**Step 3: Create arxiv-integrate.py with insert_at_anchor**

Create `.scripts/arxiv-integrate.py`:

```python
#!/usr/bin/env python3
"""
ArXiv KB Integration — Job 3 of the automated KB integration pipeline.

Reads proposals JSON, sequentially integrates high-confidence papers into
the KB, updates KB-INDEX, checks playbook routing, commits per paper,
and writes the weekly human-readable summary.
"""

import re
import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CONFIDENCE_THRESHOLD = 0.80


class AnchorNotFoundError(Exception):
    pass


def insert_at_anchor(content: str, anchor: str, new_text: str) -> tuple[str, bool]:
    """
    Find section heading matching anchor, insert new_text after that section
    (before the next same-or-higher-level heading, or at end of file).

    anchor: exact text of the section heading (without ## prefix)
    Returns: (modified_content, success)
    """
    # Search for the heading: ## anchor or ### anchor
    pattern = re.compile(
        rf'^(##{{1,3}})\s+{re.escape(anchor)}\s*$',
        re.MULTILINE
    )
    match = pattern.search(content)
    if not match:
        return content, False

    heading_level = len(match.group(1))  # 2 or 3
    section_start = match.start()
    after_heading = match.end()

    # Find end of this section: next heading at same or higher level
    next_heading_pattern = re.compile(
        rf'^#{{1,{heading_level}}}\s',
        re.MULTILINE
    )
    next_match = next_heading_pattern.search(content, after_heading + 1)

    if next_match:
        insert_pos = next_match.start()
    else:
        insert_pos = len(content)

    # Insert with separator
    separator = '\n\n---\n\n'
    modified = content[:insert_pos] + separator + new_text.strip() + '\n' + content[insert_pos:]
    return modified, True
```

**Step 4: Run tests — expect pass**

```bash
python -m pytest .scripts/tests/test_integrate.py -v
```

Expected: `4 passed`

**Step 5: Commit**

```bash
git add .scripts/arxiv-integrate.py .scripts/tests/test_integrate.py
git commit -m "feat(arxiv): add insert_at_anchor with edge case tests"
```

---

## Task 6: KB-INDEX updater + digest marker

**Files:**
- Modify: `.scripts/arxiv-integrate.py` — add `update_kb_index()`, `mark_digest_integrated()`

**Step 1: Add to arxiv-integrate.py**

```python
def update_kb_index(kb_file_rel: str, paper_id: str, key_findings: str):
    """
    Re-read KB-INDEX, find the entry for kb_file_rel, append a new line
    noting the new content. Uses rough line count from actual file.
    """
    kb_index_path = REPO_ROOT / 'KB-INDEX.md'
    kb_file_path = REPO_ROOT / kb_file_rel

    content = kb_index_path.read_text()
    actual_lines = len(kb_file_path.read_text().splitlines())

    # Find file entry in KB-INDEX
    file_short = Path(kb_file_rel).name
    # Update line count in the header line for this file
    content = re.sub(
        rf'({re.escape(file_short)}\s*\()[\d+]+(\s*lines)',
        rf'\g<1>{actual_lines}\2',
        content
    )

    # Append new entry bullet under the file's table
    new_entry = f'| **NEW:** | **{key_findings[:120]}** (arXiv:{paper_id}) |'

    # Find the table for this file and append before the next --- separator
    file_section_pattern = re.compile(
        rf'###\s+{re.escape(kb_file_rel)}.*?\n(.*?)(?=\n---|\Z)',
        re.DOTALL
    )
    m = file_section_pattern.search(content)
    if m:
        insert_pos = m.end(1)
        content = content[:insert_pos] + '\n' + new_entry + content[insert_pos:]

    kb_index_path.write_text(content)


def mark_digest_integrated(paper_id: str, kb_file_rel: str, digest_path: Path):
    """Append ✅ integrated marker to the paper's Link line in the digest."""
    content = digest_path.read_text()
    date_str = datetime.now().strftime('%Y-%m-%d')
    kb_short = Path(kb_file_rel).name

    # Find the Link line for this paper and append marker
    updated = re.sub(
        rf'(\*\*Link:\*\*\s+\[{re.escape(paper_id)}\].*?)$',
        rf'\1  ✅ {date_str} Integrated → {kb_short}',
        content,
        flags=re.MULTILINE
    )
    digest_path.write_text(updated)


def git_commit(files: list[str], message: str):
    """Stage and commit specific files."""
    subprocess.run(['git', 'add'] + files, cwd=REPO_ROOT, check=True)
    result = subprocess.run(
        ['git', 'diff', '--cached', '--quiet'],
        cwd=REPO_ROOT
    )
    if result.returncode != 0:  # There are staged changes
        subprocess.run(
            ['git', 'commit', '-m', message],
            cwd=REPO_ROOT, check=True
        )
```

**Step 2: Verify imports still clean**

```bash
python -c "import sys; sys.path.insert(0,'.scripts'); from arxiv_integrate import update_kb_index, mark_digest_integrated, git_commit; print('ok')"
```

Expected: `ok`

**Step 3: Commit**

```bash
git add .scripts/arxiv-integrate.py
git commit -m "feat(arxiv): add KB-INDEX updater, digest marker, git commit helper"
```

---

## Task 7: Playbook router + integration orchestrator

**Files:**
- Modify: `.scripts/arxiv-integrate.py` — add `integrate_playbook()`, `integrate_paper()`, `run_integration()`

**Step 1: Add to arxiv-integrate.py**

```python
def integrate_playbook(proposal: dict, digest_path: Path) -> bool:
    """Write playbook update if warranted. Returns success bool."""
    routing = proposal.get('playbook_routing', {})
    if not routing.get('applies') or not routing.get('playbook_file'):
        return False

    playbook_path = REPO_ROOT / routing['playbook_file']
    if not playbook_path.exists():
        print(f"  Playbook not found: {routing['playbook_file']}", file=sys.stderr)
        return False

    content = playbook_path.read_text()
    draft = proposal.get('draft_playbook_text', '')
    if not draft:
        return False

    anchor = routing.get('section_anchor', '')
    modified, success = insert_at_anchor(content, anchor, draft)
    if success:
        playbook_path.write_text(modified)
    return success


def integrate_paper(proposal: dict, digest_path: Path) -> dict:
    """
    Integrate one paper into KB. Returns result dict with status and files_modified.
    Always re-reads KB file from disk before writing.
    """
    result = {
        'paper_id': proposal['paper_id'],
        'title': proposal['title'],
        'status': 'skipped',
        'files_modified': [],
        'reason': ''
    }

    confidence = proposal.get('quality_gate', {}).get('confidence', 0)
    html_available = proposal.get('html_available', False)

    if confidence < CONFIDENCE_THRESHOLD or not html_available:
        result['reason'] = f'confidence {confidence:.2f} or no HTML'
        return result

    kb_file_rel = proposal.get('kb_routing', {}).get('primary_file', '')
    anchor = proposal.get('kb_routing', {}).get('section_anchor', '')
    draft_text = proposal.get('draft_kb_text', '')

    if not (kb_file_rel and anchor and draft_text):
        result['status'] = 'error'
        result['reason'] = 'missing routing fields'
        return result

    kb_path = REPO_ROOT / kb_file_rel
    if not kb_path.exists():
        result['status'] = 'error'
        result['reason'] = f'KB file not found: {kb_file_rel}'
        return result

    # Re-read fresh (critical — previous papers may have modified this file)
    content = kb_path.read_text()
    modified, success = insert_at_anchor(content, anchor, draft_text)

    if not success:
        result['status'] = 'anchor_not_found'
        result['reason'] = f'anchor not found: "{anchor}"'
        return result

    kb_path.write_text(modified)
    result['files_modified'].append(kb_file_rel)

    # Update KB-INDEX
    update_kb_index(kb_file_rel, proposal['paper_id'], proposal.get('key_findings', ''))
    result['files_modified'].append('KB-INDEX.md')

    # Playbook routing
    playbook_updated = integrate_playbook(proposal, digest_path)
    if playbook_updated:
        result['files_modified'].append(proposal['playbook_routing']['playbook_file'])

    # Mark digest
    mark_digest_integrated(proposal['paper_id'], kb_file_rel, digest_path)
    result['files_modified'].append(str(digest_path.relative_to(REPO_ROOT)))

    # Per-paper commit
    short_title = proposal['title'][:60]
    kb_short = Path(kb_file_rel).stem
    commit_msg = (
        f"docs({kb_short}): {proposal.get('key_findings','')[:80]} "
        f"[{proposal['paper_id']}]\n\n"
        f"{proposal.get('highlights_blurb', '')}"
    )
    git_commit([str(REPO_ROOT / f) for f in result['files_modified']], commit_msg)

    result['status'] = 'integrated'
    return result


def run_integration(proposals_path: Path, digest_path: Path):
    """
    Main orchestration: read proposals, group by KB file, integrate sequentially.
    """
    proposals = json.loads(proposals_path.read_text())

    # Sort by primary KB file so same-file edits are sequential
    proposals.sort(key=lambda p: p.get('kb_routing', {}).get('primary_file', ''))

    integrated, proposals_only, filtered, errors = [], [], [], []

    for proposal in proposals:
        conf = proposal.get('quality_gate', {}).get('confidence', 0)
        if conf < 0.60:
            filtered.append(proposal)
            continue

        result = integrate_paper(proposal, digest_path)

        if result['status'] == 'integrated':
            integrated.append({**proposal, **result})
        elif result['status'] == 'skipped':
            proposals_only.append({**proposal, 'reason': result['reason']})
        else:
            errors.append({**proposal, 'error': result['reason']})
            proposals_only.append({**proposal, 'reason': result['reason']})

    return integrated, proposals_only, filtered, errors
```

**Step 2: Verify no import errors**

```bash
python -c "import sys; sys.path.insert(0,'.scripts'); from arxiv_integrate import integrate_paper, run_integration; print('ok')"
```

Expected: `ok`

**Step 3: Commit**

```bash
git add .scripts/arxiv-integrate.py
git commit -m "feat(arxiv): add playbook router and integration orchestrator"
```

---

## Task 8: Weekly summary writer + main entrypoint

**Files:**
- Modify: `.scripts/arxiv-integrate.py` — add `write_weekly_summary()` and `__main__` block

**Step 1: Add to arxiv-integrate.py**

```python
def write_weekly_summary(
    integrated: list,
    proposals_only: list,
    filtered: list,
    errors: list,
    date_str: str
) -> Path:
    """Write human-readable weekly summary markdown."""
    lines = [
        f"# KB Weekly Integration Summary — {date_str}",
        "",
        f"## What was added ({len(integrated)} integrated | "
        f"{len(proposals_only)} proposals only | {len(filtered)} filtered)",
        "",
    ]

    for p in integrated:
        kb_short = Path(p.get('kb_routing', {}).get('primary_file', '')).name
        lines += [
            f"### {p['title']} [{p['paper_id']}] → {kb_short}",
            f"**Why it matters:** {p.get('highlights_blurb', '')}",
            f"**Key findings:** {p.get('key_findings', '')}",
            f"**Where it lives:** `{p.get('kb_routing',{}).get('primary_file','')}` "
            f"→ after section: \"{p.get('kb_routing',{}).get('section_anchor','')}\"",
        ]
        if p.get('playbook_routing', {}).get('applies'):
            lines.append(
                f"**Playbook updated:** `{p['playbook_routing']['playbook_file']}`"
            )
        lines.append("")

    if proposals_only:
        lines += ["---", "", "## Proposals only (your review needed)", ""]
        for p in proposals_only:
            conf = p.get('quality_gate', {}).get('confidence', 0)
            lines.append(
                f"- **[{p['paper_id']}] {p['title']}** — "
                f"confidence {conf:.2f}. {p.get('reason','')}. "
                f"Review: `raw/arxiv-proposals/`"
            )
        lines.append("")

    if filtered:
        lines += ["---", "", "## Filtered post deep-dive", ""]
        for p in filtered:
            conf = p.get('quality_gate', {}).get('confidence', 0)
            lines.append(
                f"- **[{p['paper_id']}] {p['title']}** — "
                f"confidence {conf:.2f} (below 0.60). No KB integration."
            )
        lines.append("")

    magnum_flags = [
        p for p in integrated + proposals_only
        if p.get('magnum_opus_flag')
    ]
    if magnum_flags:
        lines += ["---", "", "## Magnum Opus flags (your action needed)", ""]
        for p in magnum_flags:
            lines.append(f"- **{p['title']}:** {p['magnum_opus_flag']}")
        lines.append("")

    playbook_updates = [p for p in integrated if p.get('playbook_routing', {}).get('applies')]
    if playbook_updates:
        lines += ["---", "", "## Playbook updates made", ""]
        for p in playbook_updates:
            lines.append(
                f"- `{p['playbook_routing']['playbook_file']}`: "
                f"added content from {p['paper_id']}"
            )
        lines.append("")

    if errors:
        lines += ["---", "", "## Errors (check logs)", ""]
        for p in errors:
            lines.append(f"- [{p['paper_id']}] {p['title']}: {p.get('error','unknown')}")

    summary_path = REPO_ROOT / 'raw' / 'arxiv-weekly-summary' / f'{date_str}.md'
    summary_path.write_text('\n'.join(lines))
    print(f"Summary written to {summary_path}", file=sys.stderr)
    return summary_path


if __name__ == '__main__':
    from pathlib import Path

    # Find latest proposals JSON
    proposals_dir = REPO_ROOT / 'raw' / 'arxiv-proposals'
    proposal_files = sorted(proposals_dir.glob('*.json'), reverse=True)
    if not proposal_files:
        print("No proposals JSON found. Run arxiv-deep-dive.py first.", file=sys.stderr)
        sys.exit(1)
    proposals_path = proposal_files[0]

    # Find matching digest (same date or latest)
    date_str = proposals_path.stem  # YYYY-MM-DD
    digest_path = REPO_ROOT / 'raw' / 'arxiv-papers' / f'{date_str}.md'
    if not digest_path.exists():
        digests = sorted((REPO_ROOT / 'raw' / 'arxiv-papers').glob('*.md'), reverse=True)
        digest_path = digests[0] if digests else None
    if not digest_path:
        print("No digest file found.", file=sys.stderr)
        sys.exit(1)

    print(f"Integrating from: {proposals_path.name}", file=sys.stderr)
    print(f"Using digest: {digest_path.name}", file=sys.stderr)

    # Configure git identity for CI
    subprocess.run(['git', 'config', 'user.email', 'arxiv-bot@github.com'], cwd=REPO_ROOT)
    subprocess.run(['git', 'config', 'user.name', 'ArXiv Bot'], cwd=REPO_ROOT)

    integrated, proposals_only, filtered, errors = run_integration(proposals_path, digest_path)

    summary_path = write_weekly_summary(integrated, proposals_only, filtered, errors, date_str)

    # Final commit: summary
    git_commit(
        [str(summary_path)],
        f"docs(arxiv): weekly integration summary {date_str} "
        f"({len(integrated)} integrated, {len(proposals_only)} proposals)"
    )

    # Push all commits
    subprocess.run(['git', 'push', 'origin', 'main'], cwd=REPO_ROOT, check=True)

    print(f"Done. {len(integrated)} papers integrated.", file=sys.stderr)
```

**Step 2: Run all tests to confirm nothing regressed**

```bash
python -m pytest .scripts/tests/ -v
```

Expected: `7 passed`

**Step 3: Commit**

```bash
git add .scripts/arxiv-integrate.py
git commit -m "feat(arxiv): add weekly summary writer and main entrypoint"
```

---

## Task 9: Extend GitHub Actions workflow

**Files:**
- Modify: `.github/workflows/arxiv-digest.yml`

**Step 1: Read current workflow**

```bash
cat .github/workflows/arxiv-digest.yml
```

**Step 2: Replace workflow file with extended version**

The new `.github/workflows/arxiv-digest.yml`:

```yaml
name: ArXiv Weekly Digest + KB Integration

on:
  schedule:
    - cron: '0 8 * * 5'   # Friday 8:00am UTC — scraper
  workflow_dispatch:

jobs:
  generate-digest:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests anthropic

      - name: Run ArXiv scraper
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python .scripts/arxiv-scraper.py

      - name: Configure Git
        run: |
          git config user.email "arxiv-bot@github.com"
          git config user.name "ArXiv Digest Bot"

      - name: Commit and push digest
        run: |
          git add raw/arxiv-papers/
          git diff --cached --quiet || (git commit -m "docs: add ArXiv weekly digest (Claude-scored KB relevance)" && git push origin main)

  deep-dive-analysis:
    needs: generate-digest
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests anthropic beautifulsoup4

      - name: Run deep-dive analysis
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python .scripts/arxiv-deep-dive.py

      - name: Configure Git
        run: |
          git config user.email "arxiv-bot@github.com"
          git config user.name "ArXiv Bot"

      - name: Commit proposals JSON
        run: |
          git add raw/arxiv-proposals/
          git diff --cached --quiet || (git commit -m "docs(arxiv): add deep-dive proposals $(date +%Y-%m-%d)" && git push origin main)

  kb-integration:
    needs: deep-dive-analysis
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests anthropic

      - name: Run KB integration
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python .scripts/arxiv-integrate.py
        # Per-paper commits + push happen inside the script
```

**Step 3: Verify YAML is valid**

```bash
python -c "import yaml; yaml.safe_load(open('.github/workflows/arxiv-digest.yml')); print('valid YAML')"
```

Expected: `valid YAML`

**Step 4: Commit**

```bash
git add .github/workflows/arxiv-digest.yml
git commit -m "feat(ci): extend arxiv workflow with deep-dive and KB integration jobs"
```

---

## Task 10: Smoke test against latest digest (dry run)

**Files:** No changes — read-only test

**Step 1: Run deep-dive against the April 17 digest (dry run — does not commit)**

```bash
cd /Users/t-rawww/AI-Knowledgebase
ANTHROPIC_API_KEY=$(echo $ANTHROPIC_API_KEY) python -c "
import sys
sys.path.insert(0, '.scripts')
from pathlib import Path
from arxiv_deep_dive import parse_digest, find_latest_digest

digest = find_latest_digest()
content = digest.read_text()
papers = parse_digest(content)
print(f'Found {len(papers)} papers:')
for p in papers:
    print(f'  - {p[\"id\"]}: {p[\"title\"][:60]}')
"
```

Expected: list of 11 papers from April 17 digest with correct IDs

**Step 2: Run HTML fetch test on one paper**

```bash
python -c "
import sys; sys.path.insert(0, '.scripts')
from arxiv_deep_dive import fetch_paper_html
content, available = fetch_paper_html('2604.15224v1')
print(f'HTML available: {available}')
print(f'Content length: {len(content)} chars')
print(f'Preview: {content[:200]}')
"
```

Expected: `HTML available: True`, content length > 1000 chars, readable text preview

**Step 3: Test insert_at_anchor against a real KB file**

```bash
python -c "
import sys; sys.path.insert(0, '.scripts')
from arxiv_integrate import insert_at_anchor
content = open('LEARNING/PRODUCTION/evaluation/evaluation.md').read()
result, success = insert_at_anchor(content, 'LLM-as-Judge: Using AI to Evaluate AI', '## TEST SECTION\n\nTest content.')
print(f'Success: {success}')
if success:
    pos = result.index('TEST SECTION')
    print(f'Inserted at char {pos} of {len(result)}')
    print(f'Context: ...{result[pos-100:pos+50]}...')
"
```

Expected: `Success: True`, shows insertion point in context around LLM-as-judge section

**Step 4: Final test run**

```bash
python -m pytest .scripts/tests/ -v
```

Expected: `7 passed, 0 failed`

**Step 5: Push everything**

```bash
git push origin main
```

---

## Summary: Files Created/Modified

| File | Status | Purpose |
|---|---|---|
| `.scripts/integration-rubric.md` | New | KB routing rubric for CI Claude API calls |
| `.scripts/arxiv-deep-dive.py` | New | Job 2: parallel HTML fetch + Claude analysis → proposals JSON |
| `.scripts/arxiv-integrate.py` | New | Job 3: sequential KB writes + summary |
| `.scripts/tests/test_deep_dive.py` | New | Unit tests for digest parser + HTML extractor |
| `.scripts/tests/test_integrate.py` | New | Unit tests for insert_at_anchor (all edge cases) |
| `.scripts/__init__.py` | New | Makes .scripts importable for tests |
| `.scripts/tests/__init__.py` | New | Makes tests importable |
| `raw/arxiv-proposals/.gitkeep` | New | Tracks new directory in git |
| `raw/arxiv-weekly-summary/.gitkeep` | New | Tracks new directory in git |
| `.github/workflows/arxiv-digest.yml` | Modified | Adds 2 new jobs chained after generate-digest |
