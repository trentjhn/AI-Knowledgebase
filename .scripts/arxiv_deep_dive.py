#!/usr/bin/env python3
"""
ArXiv Deep Dive — Job 2 of the automated KB integration pipeline.

Reads the latest weekly digest, fetches full paper HTML for each paper,
calls Gemini 3 Flash via two-call architecture:
  Call 1 (triage): quality gate + routing — all papers
  Call 2 (draft):  KB text generation — only papers passing confidence threshold
Outputs structured proposals JSON.
"""

import re
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
MAX_WORKERS = 5
DRAFT_THRESHOLD = 0.75  # papers above this get a second call for draft text


def parse_digest(content: str) -> list[dict]:
    """Parse digest markdown, return list of paper dicts.

    Splits digest into per-entry chunks first to prevent malformed entries
    from consuming fields of subsequent entries.
    """
    papers = []
    chunks = re.split(r'(?=^\d+\.\s+\*\*)', content, flags=re.MULTILINE)
    field_patterns = {
        'title':     re.compile(r'^\d+\.\s+\*\*(.+?)\*\*', re.MULTILINE),
        'published': re.compile(r'-\s+\*\*Published:\*\*\s+(.+)'),
        'kb_topics': re.compile(r'-\s+\*\*KB Topics:\*\*\s+(.+)'),
        'abstract':  re.compile(r'-\s+\*\*Abstract:\*\*\s+(.+)'),
        'link_id':   re.compile(r'-\s+\*\*Link:\*\*\s+\[(.+?)\]'),
    }
    for chunk in chunks:
        m = {k: p.search(chunk) for k, p in field_patterns.items()}
        if not all(m.values()):
            continue
        kb_topics = [t.strip() for t in m['kb_topics'].group(1).split(',')]
        papers.append({
            'title':     m['title'].group(1).strip(),
            'published': m['published'].group(1).strip(),
            'kb_topics': kb_topics,
            'abstract':  m['abstract'].group(1).strip(),
            'id':        m['link_id'].group(1).strip(),
        })
    return papers


def find_latest_digest() -> Path:
    """Return path to the most recently generated digest."""
    digest_dir = REPO_ROOT / 'raw' / 'arxiv-papers'
    digests = sorted(digest_dir.glob('*.md'), reverse=True)
    if not digests:
        raise FileNotFoundError("No digest files found in raw/arxiv-papers/")
    return digests[0]


TARGET_SECTIONS = {
    'abstract', 'introduction', 'method', 'methodology',
    'approach', 'experiment', 'result', 'ablation',
    'analysis', 'conclusion', 'limitation', 'discussion'
}


def extract_sections(html_content: str) -> str:
    """Extract key sections from arXiv HTML. Returns concatenated text."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    extracted = []
    consumed = set()

    for section in soup.find_all(['section', 'div'], recursive=True):
        if id(section) in consumed:
            continue
        heading = section.find(['h1', 'h2', 'h3'], recursive=False) or \
                  section.find(['h1', 'h2', 'h3'])
        if not heading:
            continue
        heading_text = heading.get_text().lower().strip()
        heading_clean = re.sub(r'^\d+\.?\s*', '', heading_text)
        if any(kw in heading_clean for kw in TARGET_SECTIONS):
            extracted.append(section.get_text(separator=' ', strip=True))
            for descendant in section.find_all(True):
                consumed.add(id(descendant))

    return '\n\n'.join(extracted) if extracted else ''


def fetch_paper_html(arxiv_id: str) -> tuple[str, bool]:
    """
    Fetch full paper HTML from arxiv.org/html/{id}.
    Returns (sections_text, html_available).
    """
    import urllib.request
    import urllib.error
    ARXIV_HTML_BASE = "https://arxiv.org/html"
    base_id = re.sub(r'v\d+$', '', arxiv_id)
    url = f"{ARXIV_HTML_BASE}/{base_id}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'arxiv-kb-bot/1.0'})
        with urllib.request.urlopen(req, timeout=20) as resp:
            if resp.status == 200:
                sections = extract_sections(resp.read().decode('utf-8', errors='replace'))
                if sections:
                    return sections, True
        return '', False
    except (urllib.error.URLError, OSError):
        return '', False


def extract_headings(kb_file_rel: str) -> list[str]:
    """Return all ##–##### heading texts from a KB file."""
    kb_path = REPO_ROOT / kb_file_rel
    if not kb_path.exists():
        return []
    headings = []
    for line in kb_path.read_text().splitlines():
        m = re.match(r'^#{2,5}\s+(.+)', line)
        if m:
            headings.append(m.group(1).strip())
    return headings


def correct_anchor(suggested: str, kb_file_rel: str) -> tuple[str, bool]:
    """
    Return (best_anchor, was_corrected).
    Exact match → (suggested, False).
    Fuzzy match  → (closest_heading, True).
    No match     → (suggested, False) — will hit anchor_not_found in Job 3.
    """
    import difflib
    headings = extract_headings(kb_file_rel)
    if not headings or suggested in headings:
        return suggested, False
    matches = difflib.get_close_matches(suggested, headings, n=1, cutoff=0.4)
    if matches:
        return matches[0], True
    return suggested, False


def extract_kb_section(kb_file_rel: str, anchor: str) -> str:
    """Extract existing content of the target section for context in draft call."""
    kb_path = REPO_ROOT / kb_file_rel
    if not kb_path.exists():
        return ''
    content = kb_path.read_text()
    pattern = re.compile(rf'^(#{{2,5}})\s+{re.escape(anchor)}\s*$', re.MULTILINE)
    match = pattern.search(content)
    if not match:
        return ''
    heading_level = len(match.group(1))
    after = match.end()
    next_heading = re.compile(rf'^#{{2,{heading_level}}}\s', re.MULTILINE)
    nxt = next_heading.search(content, after + 1)
    end = nxt.start() if nxt else len(content)
    return content[match.start():end].strip()[:3000]


def make_client():
    import os
    import openai as _openai
    return _openai.OpenAI(
        api_key=os.getenv('GOOGLE_API_KEY'),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )


def _parse_json_response(text: str) -> dict:
    import json
    text = text.strip()
    if text.startswith('```'):
        text = re.sub(r'^```(?:json)?\s*\n?|\n?```\s*$', '', text, flags=re.MULTILINE).strip()
    return json.loads(text)


TRIAGE_SYSTEM_PROMPT = """You are an expert research analyst for a practitioner-depth AI knowledge base.

CALL 1 — TRIAGE: Analyze this paper for quality and routing only. Do NOT write KB draft text.

You will receive:
1. The KB integration rubric (quality gate scoring rules)
2. The current KB-INDEX (what sections already exist and what they cover)
3. The paper content (key sections)

Follow the rubric quality gate exactly. Be honest and strict — most papers are confirmatory (≤0.72).
Reserve ≥0.85 only for genuine gaps or contradictions you can specifically name.
Include a reasoning field (1-2 sentences) explaining which gate drove your confidence score.

Return ONLY valid JSON matching the Triage Output Schema in the rubric. No markdown, no explanation."""


DRAFT_SYSTEM_PROMPT = """You are an expert technical writer for a practitioner-depth AI knowledge base.

CALL 2 — DRAFT: Write KB integration text for a paper that passed quality screening.

You will receive:
1. The triage result (routing, key_findings, highlights_blurb)
2. The existing content of the target KB section (what's already there — do not restate this)
3. The paper content

Write draft_kb_text that adds genuinely new insight. KB writing standards:
- Plain English first, define jargon on first use
- Narrative prose before bullets or tables
- Concrete numbers and examples from the paper
- 200–500 words. No hedge phrases. No placeholder text.

Return ONLY valid JSON: {"draft_kb_text": "...", "draft_kb_text_secondary": null or "...", "draft_playbook_text": null or "..."}"""


def triage_paper(paper: dict, paper_content: str, html_available: bool,
                 rubric: str, kb_index: str, client) -> dict:
    """Call 1: quality gate + routing. Returns partial proposal without draft text."""
    import json
    import sys

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
{paper_content[:40000]}"""

    response = client.chat.completions.create(
        model='gemini-3-flash-preview',
        max_tokens=2048,
        messages=[
            {'role': 'system', 'content': TRIAGE_SYSTEM_PROMPT},
            {'role': 'user', 'content': user_message}
        ]
    )
    result = _parse_json_response(response.choices[0].message.content)
    result['paper_id'] = paper['id']
    result['title'] = paper['title']
    result['html_available'] = html_available
    if not html_available:
        qg = result.setdefault('quality_gate', {})
        qg['confidence'] = min(qg.get('confidence', 0.60), 0.60)

    # Correct anchors and persist correction metadata
    routing = result.get('kb_routing', {})
    if routing.get('primary_file') and routing.get('section_anchor'):
        corrected, was_corrected = correct_anchor(routing['section_anchor'], routing['primary_file'])
        if was_corrected:
            routing['anchor_original'] = routing['section_anchor']
            routing['anchor_corrected'] = True
            routing['section_anchor'] = corrected
            print(f"  Anchor corrected: '{routing['anchor_original']}' → '{corrected}'", file=sys.stderr)
        else:
            routing['anchor_corrected'] = False
    if routing.get('secondary_file') and routing.get('secondary_section_anchor'):
        corrected, was_corrected = correct_anchor(routing['secondary_section_anchor'], routing['secondary_file'])
        if was_corrected:
            routing['secondary_anchor_original'] = routing['secondary_section_anchor']
            routing['secondary_anchor_corrected'] = True
            routing['secondary_section_anchor'] = corrected
        else:
            routing['secondary_anchor_corrected'] = False

    return result


def draft_paper(paper: dict, paper_content: str, triage: dict, client) -> dict:
    """Call 2: generate draft KB text for papers that passed triage."""
    routing = triage.get('kb_routing', {})
    existing_section = extract_kb_section(
        routing.get('primary_file', ''),
        routing.get('section_anchor', '')
    )

    user_message = f"""TRIAGE RESULT:
Paper: {triage['title']} [{triage['paper_id']}]
Routes to: {routing.get('primary_file', '')} → section: "{routing.get('section_anchor', '')}"
Key findings: {triage.get('key_findings', '')}
Highlights: {triage.get('highlights_blurb', '')}
Secondary file: {routing.get('secondary_file', 'none')}

EXISTING SECTION CONTENT (do not restate — add new insight only):
{existing_section}

PAPER CONTENT:
{paper_content[:35000]}"""

    response = client.chat.completions.create(
        model='gemini-3-flash-preview',
        max_tokens=6144,
        messages=[
            {'role': 'system', 'content': DRAFT_SYSTEM_PROMPT},
            {'role': 'user', 'content': user_message}
        ]
    )
    return _parse_json_response(response.choices[0].message.content)


def analyze_paper(paper: dict, rubric: str, kb_index: str) -> dict:
    """
    Full analysis: triage → (if confidence ≥ DRAFT_THRESHOLD) draft.
    Returns complete proposal dict.
    """
    import sys
    import openai as _openai

    client = make_client()
    paper_content, html_available = fetch_paper_html(paper['id'])
    if not html_available:
        paper_content = f"Abstract: {paper['abstract']}"

    def _with_retry(fn):
        import time
        try:
            return fn()
        except _openai.AuthenticationError:
            raise
        except _openai.APIError as e:
            print(f"  API error for {paper['id']} (retrying in 5s): {e}", file=sys.stderr)
            time.sleep(5)
            return fn()

    stub = {
        'paper_id': paper['id'],
        'title': paper['title'],
        'html_available': html_available,
        'quality_gate': {'confidence': 0.0, 'is_mechanism': False,
                         'generalizes': False, 'fills_gap': False,
                         'deployment_relevant': False},
    }

    try:
        result = _with_retry(
            lambda: triage_paper(paper, paper_content, html_available, rubric, kb_index, client)
        )
    except _openai.APIError as e:
        return {**stub, 'error': f"triage_api_error: {e}"}
    except Exception as e:
        return {**stub, 'error': f"triage_error: {e}"}

    conf = result.get('quality_gate', {}).get('confidence', 0)
    if conf >= DRAFT_THRESHOLD:
        try:
            draft = _with_retry(lambda: draft_paper(paper, paper_content, result, client))
            result.update(draft)
        except _openai.APIError as e:
            print(f"  Draft API error for {paper['id']} (skipping draft): {e}", file=sys.stderr)
            result['draft_error'] = f"draft_api_error: {e}"
        except Exception as e:
            print(f"  Draft error for {paper['id']} (skipping draft): {e}", file=sys.stderr)
            result['draft_error'] = f"draft_error: {e}"

    return result


def run_deep_dive(digest_path: Path) -> Path:
    """Main orchestration: parse digest → parallel analysis → write proposals JSON."""
    import sys
    import json
    from concurrent.futures import ThreadPoolExecutor, as_completed

    content = digest_path.read_text()
    papers = parse_digest(content)

    if not papers:
        print("No papers found in digest.", file=sys.stderr)
        sys.exit(0)

    print(f"Analyzing {len(papers)} papers (triage + draft for passers)...", file=sys.stderr)
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
                reasoning = proposal.get('quality_gate', {}).get('reasoning', '')
                flag = '✓' if conf >= 0.80 else '~' if conf >= DRAFT_THRESHOLD else '✗'
                print(f"  {flag} {paper['id']} — conf: {conf:.2f} | {reasoning[:80]}", file=sys.stderr)
            except Exception as e:
                print(f"  ✗ {paper['id']} — {e}", file=sys.stderr)

    date_str = digest_path.stem
    output_path = REPO_ROOT / 'raw' / 'arxiv-proposals' / f'{date_str}.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(proposals, indent=2))
    print(f"Proposals written to {output_path}", file=sys.stderr)
    return output_path


def load_rubric_and_index() -> tuple[str, str]:
    rubric = (REPO_ROOT / '.scripts' / 'integration-rubric.md').read_text()
    kb_index = (REPO_ROOT / 'KB-INDEX.md').read_text()
    return rubric, kb_index


if __name__ == '__main__':
    import sys
    digest = find_latest_digest()
    print(f"Processing digest: {digest.name}", file=sys.stderr)
    run_deep_dive(digest)
