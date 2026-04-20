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
    pattern = re.compile(
        rf'^(#{{2,5}})\s+{re.escape(anchor)}\s*$',
        re.MULTILINE
    )
    match = pattern.search(content)
    if not match:
        return content, False

    all_matches = pattern.findall(content)
    if len(all_matches) > 1:
        import sys
        print(
            f"  Warning: anchor '{anchor}' matches {len(all_matches)} headings — inserting after first match.",
            file=sys.stderr
        )

    heading_level = len(match.group(1))
    after_heading = match.end()

    next_heading_pattern = re.compile(
        rf'^#{{2,{heading_level}}}\s',
        re.MULTILINE
    )
    next_match = next_heading_pattern.search(content, after_heading + 1)

    if next_match:
        insert_pos = next_match.start()
    else:
        insert_pos = len(content)

    prefix = content[:insert_pos].rstrip('\n')
    suffix = content[insert_pos:]
    modified = prefix + '\n\n---\n\n' + new_text.strip() + '\n'
    if suffix:
        modified += suffix
    return modified, True
