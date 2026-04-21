#!/usr/bin/env python3
"""
ArXiv Deep Dive — Job 2 of the automated KB integration pipeline.

Reads the latest weekly digest, fetches full paper HTML for each paper,
calls Claude API to analyze and route, outputs structured proposals JSON.
"""

import re
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
MAX_WORKERS = 5


def parse_digest(content: str) -> list[dict]:
    """Parse digest markdown, return list of paper dicts.

    Splits digest into per-entry chunks first to prevent malformed entries
    from consuming fields of subsequent entries.
    """
    papers = []
    # Split into per-entry chunks on numbered list boundaries
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
            continue  # skip header/footer chunks and malformed entries
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
    Returns (content, html_available).
    Falls back to empty string if unavailable.
    """
    import requests
    ARXIV_HTML_BASE = "https://arxiv.org/html"
    base_id = re.sub(r'v\d+$', '', arxiv_id)
    url = f"{ARXIV_HTML_BASE}/{base_id}"
    try:
        resp = requests.get(url, timeout=20)
        if resp.status_code == 200:
            sections = extract_sections(resp.text)
            if sections:
                return sections, True
        return '', False
    except requests.exceptions.RequestException:
        return '', False


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
    Fetch paper HTML and call Gemini 3 Flash API to produce a structured proposal.
    Returns proposal dict matching the proposals JSON schema.
    """
    import os
    import json
    import sys
    import openai as _openai

    paper_content, html_available = fetch_paper_html(paper['id'])

    if not html_available:
        paper_content = f"Abstract: {paper['abstract']}"

    client = _openai.OpenAI(
        api_key=os.getenv('GOOGLE_API_KEY'),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

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

    def _call_api():
        response = client.chat.completions.create(
            model='gemini-3-flash-preview',
            max_tokens=4000,
            messages=[
                {'role': 'system', 'content': ANALYSIS_SYSTEM_PROMPT},
                {'role': 'user', 'content': user_message}
            ]
        )
        text = response.choices[0].message.content.strip()
        if text.startswith('```'):
            text = re.sub(r'^```(?:json)?\s*\n?|\n?```\s*$', '', text, flags=re.MULTILINE).strip()
        r = json.loads(text)
        r['paper_id'] = paper['id']
        r['title'] = paper['title']
        r['html_available'] = html_available
        if not html_available:
            qg = r.setdefault('quality_gate', {})
            qg['confidence'] = min(qg.get('confidence', 0.60), 0.60)
        return r

    try:
        return _call_api()
    except _openai.AuthenticationError:
        raise  # Config bug — should fail the whole job
    except _openai.APIError as e:
        import time
        print(f"  API error for {paper['id']} (retrying): {e}", file=sys.stderr)
        time.sleep(5)
        try:
            return _call_api()
        except _openai.APIError as e2:
            print(f"  API error for {paper['id']} (giving up): {e2}", file=sys.stderr)
            return {
                'paper_id': paper['id'],
                'title': paper['title'],
                'html_available': html_available,
                'quality_gate': {'confidence': 0.0, 'is_mechanism': False,
                                 'generalizes': False, 'fills_gap': False},
                'error': f"api_error: {e2}"
            }
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"  Parse error for {paper['id']}: {e}", file=sys.stderr)
        return {
            'paper_id': paper['id'],
            'title': paper['title'],
            'html_available': html_available,
            'quality_gate': {'confidence': 0.0, 'is_mechanism': False,
                             'generalizes': False, 'fills_gap': False},
            'error': f"parse_error: {e}"
        }


def run_deep_dive(digest_path: Path) -> Path:
    """Main orchestration: parse digest → parallel analysis → write proposals JSON."""
    import sys
    import json
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed

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
            time.sleep(0.5)

    date_str = digest_path.stem  # e.g. '2026-04-17' from '2026-04-17.md'
    output_path = REPO_ROOT / 'raw' / 'arxiv-proposals' / f'{date_str}.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(proposals, indent=2))
    print(f"Proposals written to {output_path}", file=sys.stderr)
    return output_path


if __name__ == '__main__':
    import sys
    digest = find_latest_digest()
    print(f"Processing digest: {digest.name}", file=sys.stderr)
    run_deep_dive(digest)
