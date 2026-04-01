---
name: planning
description: Creates comprehensive implementation plans. Use when you have a spec or requirements for a multi-step task, before touching code.
---

# Planning Implementation

## When to use this skill
- When you have a validated design or spec
- Before writing any code for a multi-step task
- When tasked with creating an implementation plan

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

## Instructions

**Context:** This should be run in a dedicated worktree (created by brainstorming skill) if applicable.

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

### Bite-Sized Task Granularity

**Each step must be one action (2-5 minutes):**
1. "Write the failing test" - step
2. "Run it to make sure it fails" - step
3. "Implement the minimal code to make the test pass" - step
4. "Run the tests and make sure they pass" - step
5. "Commit" - step

### Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans (if available) or follow manually to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

### Task Structure

Use the following template for each task in the plan:

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## Remember
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD, frequent commits

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans (if available), batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- Use subagent-driven-development skill (if available) or iterate manually
- Stay in this session
- Fresh subagent per task + code review

**If Parallel Session chosen:**
- Guide them to open new session in worktree
- Use executing-plans skill (if available)
