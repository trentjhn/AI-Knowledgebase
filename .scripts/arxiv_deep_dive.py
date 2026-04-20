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

    for section in soup.find_all(['section', 'div'], recursive=True):
        heading = section.find(['h1', 'h2', 'h3'])
        if not heading:
            continue
        heading_text = heading.get_text().lower().strip()
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
    except Exception:
        return '', False
