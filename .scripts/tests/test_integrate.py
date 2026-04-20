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
