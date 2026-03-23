# Autonomous Agent Loops

**Adapted from [everything-claude-code](https://github.com/affaan-m/everything-claude-code) by Affaan Madooei**

> Running agents unsupervised: from simple sequential pipelines to infinite improvement loops to RFC-driven DAG orchestration. When to use each pattern and how to design quality gates.

---

## Table of Contents

1. [The Loop Spectrum](#the-loop-spectrum)
2. [Pattern 1: Sequential Pipeline](#pattern-1-sequential-pipeline)
3. [Pattern 2: Iterative Improvement Loop](#pattern-2-iterative-improvement-loop)
4. [Pattern 3: Infinite Refinement](#pattern-3-infinite-refinement)
5. [Pattern 4: RFC-Driven DAG](#pattern-4-rfc-driven-dag)
6. [Pattern 5: Nanoclaw REPL Persistence](#pattern-5-nanoclaw-repl-persistence)
7. [Pattern 6: De-Sloppify Cleanup Pass](#pattern-6-de-sloppify-cleanup-pass)
8. [Quality Gates & Escalation](#quality-gates--escalation)
9. [Designing Success Criteria for New Task Types](#designing-success-criteria-for-new-task-types)
10. [When to Use Each Pattern](#when-to-use-each-pattern)

---

## The Loop Spectrum

Autonomous loops range from simple (one-shot pipeline) to complex (infinite refinement with feedback). Each serves different needs:

```
Complexity / Autonomy
         ↑
         │
    ∞    │  Pattern 6: Infinite Refinement
         │  └─ Never stops, always improving
         │
   RFC   │  Pattern 5: RFC-Driven DAG
         │  └─ Formal review cycle, orchestrated
         │
  Loop   │  Pattern 4: Iterative Improvement Loop
         │  └─ Build → test → fix → repeat until done
         │
   Seq   │  Pattern 3: Sequential Pipeline
         │  └─ Step A → Step B → Step C (deterministic order)
         │
         │
    Gen  └─→ Pattern 1: One-Shot Generation
              └─ Prompt → Output (fire and forget)

         Cost / Reliability
```

---

## Pattern 1: Sequential Pipeline

**Definition:** Input flows through deterministic steps in fixed order. No feedback, no retries.

**Best for:** Data transformation, document processing, structured formatting where success is deterministic.

**Example: PDF to Markdown Pipeline**

```bash
#!/bin/bash
set -e  # Exit on any error

INPUT="$1"
TEMP_DIR="/tmp/pdf_process_$$"
mkdir -p "$TEMP_DIR"

# Step 1: Extract text from PDF
pdftotext "$INPUT" "$TEMP_DIR/extracted.txt"

# Step 2: Have Claude clean up and structure
claude --no-cache < "$TEMP_DIR/extracted.txt" > "$TEMP_DIR/structured.md"

# Step 3: Validate markdown
python3 -m markdownlint "$TEMP_DIR/structured.md" || {
  echo "Markdown validation failed"
  exit 1
}

# Step 4: Copy to output
cp "$TEMP_DIR/structured.md" "${INPUT%.pdf}.md"

# Cleanup
rm -rf "$TEMP_DIR"
echo "Success: ${INPUT%.pdf}.md"
```

**Characteristics:**
- `set -e` ensures pipeline stops on any error
- No loops, no retries
- Fast (linear time complexity)
- Predictable cost
- Works when steps are independent

**Gotchas:**
- One step fails = entire pipeline fails
- No recovery from transient errors
- No way to refine based on quality
- Not suitable for iterative work

---

## Pattern 2: Iterative Improvement Loop

**Definition:** Build → test → evaluate → fix → repeat until success criteria met.

**Best for:** Code implementation, content generation, any task where success is measurable but multiple attempts may be needed.

**Example: Feature Implementation Loop**

```
[Iteration 0]
Generate code
├─ Run tests
├─ Tests pass? → DONE
└─ Tests fail? → continue

[Iteration 1]
Analyze failures
├─ Identify root cause
└─ Fix code

Generate revised code
├─ Run tests
├─ Tests pass? → DONE
└─ Tests fail? → continue

[Iteration 2]
Escalate if no progress detected
├─ If same failure repeats → alert human
├─ If different failure → try again (iteration 3)
└─ If > 3 iterations → escalate
```

**Pseudocode:**

```python
MAX_ITERATIONS = 3
iteration = 0

while iteration < MAX_ITERATIONS:
    code = generate_code(spec)
    test_result = run_tests(code)

    if test_result.passed:
        return code  # SUCCESS

    if iteration > 0 and test_result.failure == last_failure:
        raise EscalationException("Same failure recurring; need human")

    last_failure = test_result.failure
    iteration += 1

raise EscalationException("Max iterations without success")
```

**Characteristics:**
- Clear success criteria (tests pass, evals pass, output meets rubric)
- Bounded iterations (usually 2-3)
- Automatic escalation when stuck
- Can use different models per iteration (cheap first, upgrade if needed)

**Cost Optimization:**
```
Iteration 1: Haiku ($0.001)    ← Try cheap first
├─ Success rate: 85%
└─ Cost if fail: $0.001

Iteration 2: Sonnet ($0.005)   ← Upgrade if Haiku fails
├─ Success rate: 99% given Iteration 1 failed
└─ Cost if fail: $0.006 cumulative

Iteration 3: Opus ($0.015)     ← Last resort
├─ Success rate: 100% (should never reach)
└─ Cost if fail: $0.021 cumulative
```

---

## Pattern 3: Infinite Refinement

**Definition:** No maximum iterations; loop continues until no further improvements detected.

**Best for:** Complex analysis, writing with editorial feedback, machine learning model tuning where "good enough" isn't defined upfront.

**Example: Article Improvement Loop**

```
[Generation 0]
Claude writes article
│
├─ Evaluate: readability, accuracy, tone
├─ Score: 0.72/1.0
└─ Improvements needed: 4 (clarity, examples, citations, flow)

[Generation 1]
Claude revises based on: ["add examples", "improve flow", "add citations"]
│
├─ Evaluate: readability, accuracy, tone
├─ Score: 0.85/1.0 (↑ 0.13)
└─ Improvements needed: 2 (add more citations, tighten conclusion)

[Generation 2]
Claude revises again
│
├─ Evaluate
├─ Score: 0.87/1.0 (↑ 0.02, diminishing returns)
└─ Improvements needed: 1 (very minor)

[Generation 3]
Claude makes final tweak
│
├─ Evaluate
├─ Score: 0.87/1.0 (no change)
└─ STOP: No improvement detected → output current version
```

**Termination Condition:** Stop when score doesn't improve by at least ε (e.g., 0.02) OR max iterations reached.

**Gotchas:**
- Can spiral into infinite loop if success metric is too strict
- Cost grows unbounded
- Hard to predict when loop will end
- Requires **explicit termination logic**

---

## Pattern 4: RFC-Driven DAG

**Definition:** Agents propose changes via RFC (Request for Comments), specialists review in parallel, approved changes merge into main, loop repeats.

**Best for:** Large teams, critical systems, changes with many stakeholders, continuous improvement systems.

**Example: Code Improvement RFC Loop**

```
[RFC Generation]
Analyzer Agent:
├─ Review codebase for improvement opportunities
├─ Score: "This function has 8 cyclomatic complexity (bad)"
└─ Propose RFC: "Refactor function X for readability"

[Parallel Review]
├─ Code Quality Reviewer reads RFC
│  ├─ Approves or requests changes
│  └─ Stamp: ✓ Code-reviewed
│
├─ Performance Reviewer reads RFC
│  ├─ Evaluates: "Will refactoring slow this down?"
│  └─ Stamp: ✓ Performance-safe
│
└─ Security Reviewer reads RFC
   ├─ Checks: "Any new attack surface?"
   └─ Stamp: ✓ Security-approved

[Approval Gate]
All stamps collected?
├─ Yes → Implement RFC → Merge to main
└─ No → Request clarification → New RFC

[Next Iteration]
Loop: find next improvement opportunity
```

**Characteristics:**
- Formal review cycle (proposals must pass review)
- Parallel specialist input
- Explicit approval gate
- Reproducible decision log (all RFCs documented)
- Suitable for governance/compliance

---

## Pattern 5: Nanoclaw REPL Persistence

**Definition:** Agent runs in a REPL-like environment where state persists across calls via files on the filesystem. The agent writes its own state between invocations and reads it back at startup — the "memory" lives on disk, not in the context window.

**Best for:** Long-running code migrations, multi-file refactors, research tasks spanning hours, automated testing campaigns that must survive restarts.

### The Core Insight

A REPL-based agent (running in a terminal or code execution environment) hits context window limits on complex, multi-step work. The fix: externalize memory to files. On each new invocation, the agent reads its state file and picks up exactly where it left off. This bypasses context window limits entirely — completed work doesn't need to be re-summarized or re-explained to fit in context. The filesystem is the memory.

```
[Session 1 — cold start]
Agent reads: state.json → {"status": "new"}
Agent plans: 5 steps to complete
Agent executes: Step 1
Agent writes: state.json → {"status": "in_progress", "completed_steps": ["step 1"], "current_step": "step 2"}
Session ends (user closes terminal, crash, timeout)

[Session 2 — warm start]
Agent reads: state.json → {"status": "in_progress", "current_step": "step 2"}
Agent skips step 1 (already done per state file)
Agent executes: Step 2 → Step 3 → ...
```

### State File Structure

Keep state files human-readable (JSON or Markdown). If the state file is opaque, you cannot debug what the agent decided. Readable state also lets you manually correct it when the agent goes wrong.

```json
{
  "task": "refactor auth module to JWT",
  "status": "in_progress",
  "completed_steps": [
    "analyzed existing code",
    "identified 3 files to change"
  ],
  "current_step": "modify auth.py",
  "findings": {
    "files_to_change": ["auth.py", "middleware.py", "tests/test_auth.py"],
    "approach": "replace session tokens with signed JWTs, keep existing middleware interface"
  },
  "errors": [],
  "last_updated": "2025-03-21T14:30:00Z"
}
```

Fields the agent should always write:
- `completed_steps` — exact list of what's done; agent checks this before running any step
- `current_step` — where to resume on next invocation
- `findings` — accumulated discoveries the agent will need later (don't store these in the prompt, store them here)
- `errors` — failed approaches with reason; prevents the agent from retrying known-dead-ends
- `last_updated` — useful for debugging stale state

### Idempotency Requirement

Every step the agent runs must be idempotent: running it twice produces the same result as running it once. This is non-negotiable. The agent may crash mid-step and re-run that step from the previous checkpoint. If the step is not idempotent (e.g., it appends to a file rather than writing it), partial execution creates corrupted state.

```python
# BAD: Not idempotent — appends a duplicate entry if run twice
def add_import(filepath, import_line):
    with open(filepath, 'a') as f:
        f.write(import_line + '\n')

# GOOD: Idempotent — checks before writing
def add_import(filepath, import_line):
    with open(filepath, 'r') as f:
        content = f.read()
    if import_line not in content:
        with open(filepath, 'a') as f:
            f.write(import_line + '\n')
```

### Handling State Corruption

If the state file is malformed or missing, the agent must **fail loudly**, not silently restart. Silent restart means re-running already-completed work — at best wasteful, at worst destructive (e.g., re-applying a database migration).

```python
import json, hashlib, sys

def load_state(state_path):
    if not os.path.exists(state_path):
        # First run — initialize clean state
        return {"status": "new", "completed_steps": [], "errors": []}

    try:
        with open(state_path) as f:
            state = json.load(f)
        # Validate required fields exist
        required = {"task", "status", "completed_steps", "current_step"}
        if not required.issubset(state.keys()):
            raise ValueError(f"State missing required fields: {required - state.keys()}")
        return state
    except (json.JSONDecodeError, ValueError) as e:
        print(f"FATAL: State file is corrupted: {e}")
        print(f"State file at: {state_path}")
        print("Fix manually or delete to restart from scratch.")
        sys.exit(1)  # Do NOT silently continue
```

### Preventing State Bloat

State files grow unbounded on long tasks. Set a maximum (e.g., 50KB). When approaching the limit, compress findings into summaries and clear the detailed step array.

The agent's rule: "If my state file exceeds 50KB, summarize `completed_steps` into a single paragraph in `findings.summary` and clear the array."

```python
import os, json

def write_state(state_path, state):
    raw = json.dumps(state, indent=2)
    if len(raw.encode()) > 50_000:  # 50KB limit
        # Compress: summarize completed steps, clear the array
        summary = f"Completed {len(state['completed_steps'])} steps: " + \
                  "; ".join(state['completed_steps'][:3]) + \
                  f" ... and {len(state['completed_steps']) - 3} more."
        state['findings']['completed_summary'] = summary
        state['completed_steps'] = []  # Reset — summary is in findings now
    with open(state_path, 'w') as f:
        json.dump(state, f, indent=2)
```

### Full Startup Sequence

```python
def agent_main():
    state = load_state("./task_state.json")

    if state["status"] == "done":
        print("Task already complete. Nothing to do.")
        return

    # Skip any steps already completed
    all_steps = define_steps()
    remaining = [s for s in all_steps if s.name not in state["completed_steps"]]

    for step in remaining:
        print(f"Executing: {step.name}")
        result = step.run(state)

        state["completed_steps"].append(step.name)
        state["current_step"] = next_step_name(all_steps, step)
        state["findings"].update(result.findings)
        write_state("./task_state.json", state)  # Write after every step

    state["status"] = "done"
    write_state("./task_state.json", state)
```

**Characteristics:**
- State persists in files (git-track the state file for a full audit trail)
- Agent resumes exactly from last checkpoint — no wasted work on restart
- Context window carries only current-step context, not the entire history
- Human-readable state enables manual inspection and correction mid-task
- Enables multi-hour and multi-day autonomous tasks without supervision

---

## Pattern 6: De-Sloppify Cleanup Pass

**Definition:** After generation, a "cleanup agent" removes AI-generated slop (over-explanation, unnecessary comments, redundant code) while preserving functionality.

**Best for:** Ensuring production quality, removing "AI-ness" from generated code, final polish before deployment.

**Example: Code Cleanup Pass**

```
[Initial Output from Implementation Agent]
```python
def process_data(items):
    # This function processes a list of items and returns them
    # We iterate through each item
    # Then we filter out None values

    result = []  # Initialize an empty result list
    for item in items:  # For each item
        if item is not None:  # If item is not None
            result.append(item)  # Add it to result

    return result  # Return the processed items
```

[Cleanup Agent Removes]
```
- Obvious comments ("# Initialize an empty result list")
- Over-explanations of simple logic
- Redundant variable names
- Extra blank lines that add no meaning
```

[Final Output]
```python
def process_data(items):
    return [item for item in items if item is not None]
```

**Cleanup Rules:**
```
REMOVE:
├─ Comments that state the obvious
├─ Overly verbose variable names for simple operations
├─ Unnecessary blank lines
└─ "I will now do X" style explanations

KEEP:
├─ Comments explaining WHY (not what)
├─ Comments on non-obvious algorithms
├─ Comments on critical performance/security
└─ Docstrings for public APIs
```

**Characteristics:**
- Final quality gate before production
- Removes "AI flavor" from output
- Keeps code concise without sacrificing readability
- Can be applied to code, docs, configs

---

## Quality Gates & Escalation

### Gate 1: Success Criteria

Every loop must have explicit success criteria that can be evaluated automatically:

```
Feature Implementation Loop:
├─ Success: All tests pass AND code coverage > 80% AND no security flags
├─ Evaluation: Automated (test runner + coverage tool + security scanner)
└─ Escalation: If any gate fails after 3 iterations → human review

Content Generation Loop:
├─ Success: Readability score > 0.8 AND factual accuracy > 0.9 AND length 500-1000 words
├─ Evaluation: Automated (readability tool + fact-checker LLM + word count)
└─ Escalation: If score plateaus for 2 iterations → human review
```

### Gate 2: Iteration Limits

```
Pattern 2 (Iterative): Max 3 iterations
Pattern 3 (Infinite): Max 10 iterations OR no improvement for 3 consecutive
Pattern 4 (RFC-DAG): Explicit human approval required after each cycle
Pattern 5 (Persistence): Max 5 sessions before requiring human intervention
```

### Gate 3: Cost Limits

```
Feature: Can cost max $0.50
├─ Iteration 1: $0.005 (Haiku)
├─ Iteration 2: $0.015 (Sonnet)
├─ Iteration 3: $0.040 (Opus)
└─ If all 3 fail: Escalate to human (cost constraint prevents retry)
```

### Gate 4: Divergence Detection

If the loop is making **no progress** (same error repeating, oscillating between states, or generating nearly identical output), detect it programmatically rather than waiting for a human to notice.

**Three signals to instrument:**

**Signal 1 — Cycle Detection**

Track the last N actions. If the current action matches an action taken 3–5 steps ago, the agent is looping. Maintain a rolling hash of recent actions and check for repeats.

```python
from collections import deque
import hashlib

class CycleDetector:
    def __init__(self, window=5):
        self.recent = deque(maxlen=window)

    def record(self, action: str) -> bool:
        """Returns True if a cycle is detected."""
        action_hash = hashlib.md5(action.encode()).hexdigest()
        if action_hash in self.recent:
            return True  # Cycle detected
        self.recent.append(action_hash)
        return False
```

**Signal 2 — Progress Rate Degradation**

Track measurable work completed per iteration (files changed, tests passing, tasks checked off). If 3 consecutive iterations produce zero progress, trigger a divergence alert.

```python
def check_progress_stall(progress_log: list[int], stall_threshold=3) -> bool:
    """Returns True if the last N iterations all produced zero progress."""
    if len(progress_log) < stall_threshold:
        return False
    return all(p == 0 for p in progress_log[-stall_threshold:])
```

**Signal 3 — Semantic Drift (for language generation tasks)**

Track whether each iteration's output is meaningfully different from the previous. Compute cosine similarity between consecutive outputs — if similarity > 0.95 for 3+ consecutive iterations, the agent is generating variations of the same content rather than improving.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def is_semantically_stalled(outputs: list[str], threshold=0.95, window=3) -> bool:
    if len(outputs) < window + 1:
        return False
    recent = outputs[-(window + 1):]
    vec = TfidfVectorizer().fit_transform(recent)
    sims = [cosine_similarity(vec[i], vec[i+1])[0][0] for i in range(len(recent)-1)]
    return all(s > threshold for s in sims)
```

**Combining signals into a divergence score:**

Don't treat any single signal as definitive — use a composite score. An agent exploring a genuinely new approach may repeat some steps or produce similar intermediate outputs. Only escalate when multiple signals fire together.

```python
def divergence_score(cycle: bool, stalled: bool, semantic_drift: bool) -> float:
    """Returns a score 0.0–1.0. Escalate above 0.6."""
    return (0.4 * cycle) + (0.35 * stalled) + (0.25 * semantic_drift)
```

**Response to detected divergence:**

Don't just stop the loop. Before escalating to a human, inject a structured self-diagnosis prompt and give the agent one recovery attempt:

```
You appear to be in a loop. Your last 3 iterations produced:
- [summary of iteration N-2 output]
- [summary of iteration N-1 output]
- [summary of iteration N output]

Describe:
1. What you are trying to accomplish
2. Why your current approach isn't working
3. A different approach you haven't tried yet

If you cannot identify a different approach, respond with: ESCALATE
```

If the agent responds with `ESCALATE` or the divergence score remains above threshold after this recovery step, break the loop and hand off to a human with the full divergence log.

```
Old signals (still valid):
Detect: Cost exceeds budget → Immediately break loop, escalate
Detect: Oscillating (Iteration 1 fixes A, Iteration 2 breaks A to fix B) → Break loop, escalate (loop is unstable)
```

---

## Designing Success Criteria for New Task Types

Every loop pattern depends on success criteria, but the quality gates section only shows examples. Here's how to *design* them from scratch when you're building something new.

### Two Types of Success Criteria

**Objective criteria** — measurable, automatable, no human judgment required:
- "All 47 tests pass"
- "Output file exists and is > 0 bytes"
- "API returns HTTP 200 with a response body"
- "No `TODO` strings remain in the generated code"
- "Readability score (Flesch-Kincaid) > 60"

**Subjective criteria** — require human judgment:
- "The code is clean"
- "The explanation is clear enough for a junior engineer"
- "The tone matches our brand voice"

Prefer objective criteria wherever possible. When you can't avoid subjective criteria, convert them to LLM-as-judge evaluations with a rubric — this makes them automatable even if they're not objectively computable.

### The Minimum Viable Success Criterion

For any task, define the single criterion that **must** be true for the task to be considered done. Everything else is a quality criterion that informs further iteration, not a gate that blocks completion.

Having one clear "done" criterion prevents scope creep and endless iteration:

```
Task: Generate a product description for our new keyboard

DONE when: Description is 150–300 words AND mentions all 3 key features
           (wireless, backlit, mechanical switches)

Quality criteria (improve if time allows, don't block on):
├─ Reading level appropriate for general consumer audience
├─ No marketing clichés ("game-changing", "revolutionary")
└─ Matches tone of existing product descriptions
```

If you set quality criteria as required gates, the agent loops forever trying to optimize "tone match" against a fuzzy standard.

### How to Discover Your Criteria: Work Backward From Failure

Ask: **"What would I notice first if this went wrong?"** The inverse of your failure signal is your success criterion.

```
Task: Migrate authentication to JWT

What would I notice if it went wrong?
├─ Users can't log in → criterion: test_login() passes
├─ Sessions expire immediately → criterion: token TTL > 0 and matches config
├─ Logout doesn't clear tokens → criterion: blacklist endpoint returns 200 + test_logout() passes
└─ Existing tests break → criterion: full test suite passes

Success criteria:
1. test_login() passes           ← minimum viable
2. test_logout() passes          ← minimum viable
3. token TTL == configured value ← minimum viable
4. Full test suite passes        ← quality criterion (no regressions)
```

### Testing Your Criteria Before Running the Agent

Before launching the loop, manually verify that your criteria correctly classify a known-good and a known-bad output. This takes 5 minutes and prevents wasted agent runs.

```
Criterion: "Output file contains valid JSON"

Known-good test: Run criterion against a file with valid JSON → must PASS
Known-bad test: Run criterion against an empty file → must FAIL
Known-bad test: Run criterion against a file with truncated JSON → must FAIL

If criterion passes an empty file: it's too weak (os.path.exists() isn't enough — add json.loads() check)
If criterion fails a file with a comment at the top: it's too strict (adjust for JSONC if needed)
```

This is the equivalent of writing a test for your test. Skip it and you'll discover mid-run that your gate was never catching real failures.

### Quick Reference: Criteria by Pattern

| Pattern | Minimum Viable Criterion | Common Quality Criteria |
|---|---|---|
| **Sequential** | Output file exists and passes schema validation | Output format matches expected template exactly |
| **Iterative** | All tests pass | Coverage > threshold, no security flags |
| **Infinite** | Score improvement < ε for N consecutive rounds | Absolute score above quality floor |
| **RFC-DAG** | All reviewers have stamped approval | No open comment threads |
| **Persistence** | `state.json` shows `"status": "done"` | All steps completed with no errors logged |
| **Cleanup** | No lint errors; original tests still pass | Line count reduced; no obvious comments remain |

---

## When to Use Each Pattern

| Pattern | Task Type | Success Rate | Cost | Autonomy | When to Use |
|---|---|---|---|---|---|
| **Sequential** | Deterministic transformation | High | Low | Full | Data pipeline, document formatting |
| **Iterative** | Implementation with tests | High | Medium | Full | Feature code, bug fix |
| **Infinite** | Complex analysis, writing | Medium | High | Full | Research, article writing |
| **RFC-DAG** | Large changes, governance | Very High | Very High | Partial (needs review) | Architecture changes, critical systems |
| **Persistence** | Long-running exploration | Medium | Medium | Full | Month-long projects |
| **Cleanup** | Post-generation polish | High | Low | Full | Before final deployment |

---

## Implementation Checklist

- [ ] Choose loop pattern based on task type
- [ ] Define success criteria (automated if possible)
- [ ] Set iteration limits
- [ ] Set cost limits per attempt/phase
- [ ] Implement divergence detection
- [ ] Design escalation path (who/what when loop fails)
- [ ] Test with low-stakes task first
- [ ] Document expected cost per pattern
- [ ] Monitor actual cost vs. expected
- [ ] Collect failure logs for learning

---

## Sources & Notes on Illustrative Examples

**Core Loop Patterns & Frameworks:**
- everything-claude-code: All 6 loop patterns (sequential, iterative, infinite, RFC-DAG, nanoclaw persistence, de-sloppify), quality gates, iteration limits, divergence detection, escalation strategies

**Illustrative Metrics & Examples:**
- Cost figures and success rates (e.g., "Iteration 1: Haiku ($0.001)," "Success rate: 85%") in the cost-optimization section are illustrative examples from everything-claude-code's pattern library. Real-world costs and success rates depend on your models, task complexity, and prompt quality.
- The article improvement loop (generation scores, improvement tracking) demonstrates the infinite refinement pattern using illustrative quality metrics; your actual scores will depend on your evaluation rubric.

**Additional Sources:**
- Production AI teams: Quality gates implementation, iteration limits, divergence detection algorithms
- Stripe: RFC-driven deployment patterns adapted for agent orchestration
