#!/usr/bin/env python3
"""
ArXiv Deep Dive — Job 2 of the automated KB integration pipeline.

Reads the latest weekly digest, fetches full paper HTML for each paper,
calls Claude API to analyze and route, outputs structured proposals JSON.
"""

import re
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
ARXIV_HTML_BASE = "https://arxiv.org/html"
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
