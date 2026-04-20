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


def update_kb_index(kb_file_rel: str, paper_id: str, key_findings: str) -> bool:
    """
    Re-read KB-INDEX, find the entry for kb_file_rel, append a new line
    noting the new content. Uses rough line count from actual file.
    Returns True if the entry was found and updated, False otherwise.
    """
    kb_index_path = REPO_ROOT / 'KB-INDEX.md'
    kb_file_path = REPO_ROOT / kb_file_rel

    content = kb_index_path.read_text()
    actual_lines = len(kb_file_path.read_text().splitlines())

    # Find file entry in KB-INDEX
    file_short = Path(kb_file_rel).name
    # Update line count in the header line for this file
    # Matches both plain digits (467) and comma-formatted (1,260+)
    content = re.sub(
        rf'({re.escape(file_short)}\s*\()[\d,]+\+?(\s*lines)',
        rf'\g<1>{actual_lines}\2',
        content
    )

    # Append new entry bullet under the file's table
    new_entry = f'| **NEW:** | **{key_findings[:120]}** (arXiv:{paper_id}) |'

    # Find the table for this file and append before the next --- separator
    # Use #{2,5} to match all heading depths KB-INDEX uses (##, ###, ####, #####)
    file_section_pattern = re.compile(
        rf'#{{2,5}}\s+{re.escape(kb_file_rel)}.*?\n(.*?)(?=\n---|\Z)',
        re.DOTALL
    )
    m = file_section_pattern.search(content)
    if m:
        insert_pos = m.end(1)
        content = content[:insert_pos] + '\n' + new_entry + content[insert_pos:]
        kb_index_path.write_text(content)
        return True

    print(f"  Warning: KB-INDEX entry not found for {kb_file_rel}", file=sys.stderr)
    return False


def mark_digest_integrated(paper_id: str, kb_file_rel: str, digest_path: Path) -> bool:
    """Append ✅ integrated marker to the paper's Link line in the digest.
    Returns True if the marker was applied (or already present), False if the
    Link line was not found.
    """
    content = digest_path.read_text()
    date_str = datetime.now().strftime('%Y-%m-%d')
    kb_short = Path(kb_file_rel).name

    # Idempotency guard — skip if this paper is already marked
    already_marked = re.search(rf'\[{re.escape(paper_id)}\].*?✅', content)
    if already_marked:
        return True

    # Find the Link line for this paper and append marker
    updated = re.sub(
        rf'(\*\*Link:\*\*\s+\[{re.escape(paper_id)}\].*?)$',
        rf'\1  ✅ {date_str} Integrated → {kb_short}',
        content,
        flags=re.MULTILINE
    )
    if updated == content:
        print(f"  Warning: Link line for {paper_id} not found in digest", file=sys.stderr)
        return False
    digest_path.write_text(updated)
    return True


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
