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


REPO_ROOT = Path(__file__).parent.parent
ARXIV_HTML_BASE = "https://arxiv.org/html"
MAX_WORKERS = 5
CONFIDENCE_THRESHOLD = 0.80


def parse_digest(content: str) -> list[dict]:
    """Parse digest markdown, return list of paper dicts."""
    papers = []
    entry_pattern = re.compile(
        r'\d+\.\s+\*\*(.+?)\*\*\n'
        r'.*?- \*\*Published:\*\* (.+?)\n'
        r'.*?- \*\*KB Topics:\*\* (.+?)\n'
        r'.*?- \*\*Abstract:\*\* (.+?)\n'
        r'.*?- \*\*Link:\*\* \[(.+?)\]',
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
