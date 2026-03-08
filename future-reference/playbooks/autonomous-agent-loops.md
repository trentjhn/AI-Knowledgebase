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
9. [When to Use Each Pattern](#when-to-use-each-pattern)

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

**Definition:** Agent runs in a REPL-like environment where state persists across calls. Agent can see what it wrote last time.

**Best for:** Exploratory work, long-running agents, agents that learn from their own output history.

**Example: Data Analysis Agent**

```
[Session 1]
Agent writes: data_analysis.py
│
├─ [Session 1, output]
└─ Discovers: "Sales correlate strongly with temperature"

[Session 2]
Agent reads: data_analysis.py (from last session)
Agent reads: output log (from last session)
Agent executes: python data_analysis.py
│
├─ New discovery: "Correlation is stronger on weekends"
├─ Writes: updated_analysis.py
└─ Knows: what was done in Session 1 (via persistent files)

[Session 3]
Agent reads: both previous analysis files
Agent builds on previous work
├─ Test new hypothesis based on Session 2 findings
└─ Avoid re-doing work already done
```

**Implementation:**
```bash
# Nanoclaw pattern: files persist, agent can read them
ls -la ./analysis_session_*.py  # See previous work
cat ./analysis_session_1.py     # Read what was done
python analyze_new.py           # Build on it
```

**Characteristics:**
- State persists in files (git-tracked for audit trail)
- Agent can reference previous work
- No context bloat (agent doesn't have to re-explain history)
- Enables long-running projects

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

If loop is making **no progress** (same error repeating, or oscillating between states):

```
Detect: Same error appears in iterations 1, 2, 3
Action: Break loop, escalate to human with error log

Detect: Oscillating (Iteration 1 fixes A, Iteration 2 breaks A to fix B)
Action: Break loop, escalate (loop is unstable)

Detect: Cost exceeds budget
Action: Immediately break loop, escalate
```

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
