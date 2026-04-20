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
    assert result == SAMPLE_KB

def test_insert_at_anchor_end_of_file():
    from arxiv_integrate import insert_at_anchor
    content = "# Doc\n\n## Last Section\n\nSome content."
    result, success = insert_at_anchor(content, "Last Section", "## Appended\n\nContent.")
    assert success is True
    assert "## Appended\n\nContent." in result
    assert result.index("## Appended") > result.index("## Last Section")

def test_insert_at_anchor_level4_heading():
    from arxiv_integrate import insert_at_anchor
    content = "# Doc\n\n## Section\n\n#### Deep Heading\n\nDeep content.\n\n## Next\n\nNext content."
    result, success = insert_at_anchor(content, "Deep Heading", "#### Inserted\n\nNew deep content.")
    assert success is True
    assert "Inserted" in result
    deep_pos = result.index("Deep Heading")
    inserted_pos = result.index("Inserted")
    assert inserted_pos > deep_pos

def test_insert_at_anchor_no_triple_newline_at_eof():
    from arxiv_integrate import insert_at_anchor
    content = "# Doc\n\n## Last Section\n\nSome content.\n"
    result, success = insert_at_anchor(content, "Last Section", "## Appended\n\nContent.")
    assert success is True
    assert '\n\n\n' not in result  # No triple newlines

def test_insert_at_anchor_duplicate_heading_uses_first():
    from arxiv_integrate import insert_at_anchor
    content = "# Doc\n\n## Examples\n\nFirst examples.\n\n## Other\n\nMiddle.\n\n## Examples\n\nSecond examples.\n"
    result, success = insert_at_anchor(content, "Examples", "## New\n\nContent.")
    assert success is True
    # Insertion should happen after FIRST "Examples", before "Other"
    first_examples = result.index("First examples")
    new_pos = result.index("New")
    other_pos = result.index("Other")
    assert first_examples < new_pos < other_pos


# ---------------------------------------------------------------------------
# Regression tests for update_kb_index and mark_digest_integrated
# ---------------------------------------------------------------------------

import tempfile, os as _os


def test_update_kb_index_simple_line_count(tmp_path):
    """update_kb_index updates simple line counts like (467 lines)."""
    import arxiv_integrate as _ai
    old_root = _ai.REPO_ROOT
    _ai.REPO_ROOT = tmp_path
    try:
        # Create a fake KB file with 10 lines
        kb_dir = tmp_path / 'LEARNING' / 'FOUNDATIONS' / 'reasoning-llms'
        kb_dir.mkdir(parents=True)
        kb_file = kb_dir / 'reasoning-llms.md'
        kb_file.write_text('\n' * 9 + 'last line')  # 10 lines

        # Create a fake KB-INDEX with simple line count
        kb_index = tmp_path / 'KB-INDEX.md'
        kb_index.write_text(
            '### LEARNING/FOUNDATIONS/reasoning-llms/reasoning-llms.md (467 lines)\n\n'
            '| Lines | Content |\n|---|---|\n| 1-50 | Intro |\n\n---\n'
        )

        result = _ai.update_kb_index(
            'LEARNING/FOUNDATIONS/reasoning-llms/reasoning-llms.md',
            '2603.29957v1',
            'Test finding'
        )
        assert result is True
        updated = kb_index.read_text()
        assert '10 lines' in updated
        assert 'arXiv:2603.29957v1' in updated
    finally:
        _ai.REPO_ROOT = old_root


def test_update_kb_index_comma_line_count(tmp_path):
    """update_kb_index updates comma-formatted line counts like (1,260+ lines)."""
    import arxiv_integrate as _ai
    old_root = _ai.REPO_ROOT
    _ai.REPO_ROOT = tmp_path
    try:
        kb_dir = tmp_path / 'LEARNING' / 'PRODUCTION' / 'ai-security'
        kb_dir.mkdir(parents=True)
        kb_file = kb_dir / 'ai-security.md'
        kb_file.write_text('\n' * 1299 + 'last')  # 1300 lines

        kb_index = tmp_path / 'KB-INDEX.md'
        kb_index.write_text(
            '### LEARNING/PRODUCTION/ai-security/ai-security.md (1,260+ lines)\n\n'
            '| Lines | Content |\n|---|---|\n| 1-50 | Intro |\n\n---\n'
        )

        result = _ai.update_kb_index(
            'LEARNING/PRODUCTION/ai-security/ai-security.md',
            '2604.00001v1',
            'Security finding'
        )
        assert result is True
        updated = kb_index.read_text()
        assert '1300 lines' in updated
    finally:
        _ai.REPO_ROOT = old_root


def test_mark_digest_integrated_appends_marker(tmp_path):
    """mark_digest_integrated appends ✅ marker to the correct Link line."""
    import arxiv_integrate as _ai
    from pathlib import Path

    digest = tmp_path / '2026-04-17.md'
    digest.write_text(
        '1. **Some Paper**\n'
        '   - **Link:** [2604.15224v1](https://arxiv.org/abs/2604.15224v1)\n'
        '   - **ArXiv Topics:** cs.AI\n'
    )
    result = _ai.mark_digest_integrated(
        '2604.15224v1',
        'LEARNING/PRODUCTION/evaluation/evaluation.md',
        digest
    )
    assert result is True
    content = digest.read_text()
    assert '✅' in content
    assert 'evaluation.md' in content


def test_mark_digest_integrated_idempotent(tmp_path):
    """mark_digest_integrated does not double-append if already marked."""
    import arxiv_integrate as _ai

    digest = tmp_path / '2026-04-17.md'
    digest.write_text(
        '1. **Some Paper**\n'
        '   - **Link:** [2604.15224v1](https://arxiv.org/abs/2604.15224v1)  ✅ 2026-04-17 Integrated → evaluation.md\n'
    )
    result = _ai.mark_digest_integrated(
        '2604.15224v1',
        'LEARNING/PRODUCTION/evaluation/evaluation.md',
        digest
    )
    assert result is True
    content = digest.read_text()
    assert content.count('✅') == 1  # Not doubled
