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

    # Update KB-INDEX (primary)
    update_kb_index(kb_file_rel, proposal['paper_id'], proposal.get('key_findings', ''))
    result['files_modified'].append('KB-INDEX.md')

    # Secondary KB file (non-fatal if it fails)
    secondary_file = proposal.get('kb_routing', {}).get('secondary_file')
    secondary_anchor = proposal.get('kb_routing', {}).get('secondary_section_anchor', '')
    secondary_draft = proposal.get('draft_kb_text_secondary', '')
    if secondary_file and secondary_draft and secondary_anchor:
        sec_path = REPO_ROOT / secondary_file
        if sec_path.exists():
            sec_content = sec_path.read_text()
            sec_modified, sec_success = insert_at_anchor(sec_content, secondary_anchor, secondary_draft)
            if sec_success:
                sec_path.write_text(sec_modified)
                update_kb_index(secondary_file, proposal['paper_id'], proposal.get('key_findings', ''))
                result['files_modified'].append(secondary_file)
            else:
                print(f"  Secondary anchor not found for {proposal['paper_id']}: '{secondary_anchor}'", file=sys.stderr)
        else:
            print(f"  Secondary KB file not found: {secondary_file}", file=sys.stderr)

    # Playbook routing
    playbook_updated = integrate_playbook(proposal, digest_path)
    if playbook_updated:
        result['files_modified'].append(proposal['playbook_routing']['playbook_file'])

    # Mark digest
    mark_digest_integrated(proposal['paper_id'], kb_file_rel, digest_path)
    result['files_modified'].append(str(digest_path.relative_to(REPO_ROOT)))

    # Per-paper commit
    kb_short = Path(kb_file_rel).stem
    commit_msg = (
        f"docs({kb_short}): {proposal.get('key_findings','')[:80]} "
        f"[{proposal['paper_id']}]\n\n"
        f"{proposal.get('highlights_blurb', '')}"
    )
    try:
        git_commit([str(REPO_ROOT / f) for f in result['files_modified']], commit_msg)
    except subprocess.CalledProcessError as e:
        print(f"  Warning: git commit failed for {proposal['paper_id']}: {e}", file=sys.stderr)
        result['status'] = 'error'
        result['reason'] = f'git_commit_failed: {e}'
        return result

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
        elif result['status'] in ('skipped', 'anchor_not_found'):
            proposals_only.append({**proposal, 'reason': result['reason']})
        else:
            errors.append({**proposal, 'error': result['reason']})

    return integrated, proposals_only, filtered, errors


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
        if p.get('kb_routing', {}).get('secondary_file'):
            lines.append(
                f"**Also integrated:** `{p['kb_routing']['secondary_file']}` "
                f"→ after section: \"{p['kb_routing'].get('secondary_section_anchor','')}\""
            )
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
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text('\n'.join(lines))
    print(f"Summary written to {summary_path}", file=sys.stderr)
    return summary_path


if __name__ == '__main__':
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

    # Rebase on latest remote before pushing all per-paper commits
    subprocess.run(['git', 'pull', '--rebase', 'origin', 'main'], cwd=REPO_ROOT, check=True)

    # Push all commits
    subprocess.run(['git', 'push', 'origin', 'main'], cwd=REPO_ROOT, check=True)

    print(f"Done. {len(integrated)} papers integrated.", file=sys.stderr)
