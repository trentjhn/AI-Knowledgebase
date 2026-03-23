# Prompt Engineering

## The 7 Levels of Prompt Maturity

Prompts exist on a spectrum. Understanding where yours falls helps you choose the right complexity and avoid over-engineering.

| Level | Name | Key Characteristic |
|-------|------|-------------------|
| 1 | **Static** | Fixed instructions, no variation |
| 2 | **Parameterized** | Accepts input via variables (`$ARGUMENTS`) |
| 3 | **Conditional** | Branches based on input or state |
| 4 | **Contextual** | Incorporates external files/docs |
| 5 | **Composed** | Invokes other prompts/commands |
| 6 | **Self-Modifying** | Updates itself based on execution |
| 7 | **Meta-Cognitive** | Improves other prompts in the system |

### Level Evolution Paths

```
Level 1 → 2: "I need this to work with different inputs" → add $ARGUMENTS
Level 2 → 3: "I need different behavior for different input types" → add conditionals
Level 3 → 4: "I need this to understand my codebase" → add file references
Level 4 → 5: "I need this to coordinate with other commands" → add sub-command invocation
Level 5 → 6: "I want this to get better over time" → add self-improvement protocol
Level 6 → 7: "I want to improve the whole system" → add cross-prompt analysis
```

**Rule:** Start at the lowest level that meets requirements. Let actual usage drive evolution.

### What Each Level Actually Looks Like

One concrete example per level, using document summarization to show the progression:

**Level 1 — Single-Shot:** One instruction, no context.
```
Summarize this document.
```

**Level 2 — Parameterized (Few-Shot):** Adds examples to establish the expected pattern.
```
Here's an example summary: [example output]. Now summarize this document: {document}
```

**Level 3 — Conditional:** Adds branching based on input properties.
```
Summarize this document: {document}

If the document is technical, include a glossary of key terms.
If it's intended for executives, lead with the key takeaway in one sentence.
```

**Level 4 — Contextual:** Adds dynamic context injection from external sources.
```
User background: {user_background}
Document topic: {topic}

Summarize the document in a way that is relevant to this user's background and expertise level.

Document: {document}
```

**Level 5 — Composed:** Breaks the task into a chain of sub-prompts, each feeding the next.
```
Step 1 → Extract the 5 most important points from the document.
Step 2 → Identify who the intended audience is based on tone and vocabulary.
Step 3 → Using the key points from Step 1, write a summary tailored to the audience identified in Step 2.
```

**Level 6 — Self-Modifying:** The agent rewrites its own prompt based on feedback signals. After receiving a low clarity score, the prompt appends a new instruction to its own template:
```
[auto-added after low clarity score on 2025-03-15]
Ensure transitions between paragraphs are explicit. Use linking phrases ("Building on this...", "As a result...").
```

**Level 7 — Meta-Cognitive:** The orchestrator's prompt produces a specialized prompt for each sub-agent it spawns. The orchestrator doesn't summarize — it generates a tailored summarization prompt for each document type it encounters, then delegates execution to a specialist.

Each level is visibly more sophisticated in what it requires the model to do — but also more expensive to build, test, and maintain. Match complexity to the actual problem.

### Level 6: Self-Modifying (Git History as Learning Signal)

1. Run `git diff` (uncommitted), `git diff --cached` (staged), `git log` (recent commits)
2. Analyze changes to domain-relevant files for new patterns and anti-patterns
3. Update the Expertise section with dated references to the commit that revealed the insight
4. Keep Workflow sections stable — only update Expertise

**Conservative update rules:** PRESERVE existing patterns unless confirmed obsolete. APPEND new learnings with commit references. DATE new entries. REMOVE only patterns contradicted by multiple recent implementations.

---

## Canonical Prompt Structure (7 Sections)

```markdown
---
name: agent-name              # kebab-case
description: When to use this # Action-oriented, triggers delegation
tools: Tool1, Tool2           # Minimal required tools
model: haiku | sonnet | opus  # Match to task complexity
---

# Title

## Purpose
You are a [role]. Your sole focus is [single responsibility].

## Variables
USER_PROMPT: $1
STATIC_CONFIG: value

## Instructions
- IMPORTANT: Critical constraint here
- Positive instruction (do this)
- Negative instruction (never do this)

## Workflow
1. Parse Input
2. Gather Context
3. Execute Task
4. Verify Results
5. Report

## Report
### Summary
- **Status**: [success/failure]
### Details
[Exact markdown structure expected]
```

### Critical: Output Format Requirements

Every actionable prompt should forbid meta-commentary — it breaks downstream parsing:

**FORBIDDEN patterns:**
- "Based on the changes..."
- "I have created..."
- "Here is the..."
- "Let me..."
- "I will..."
- "Looking at..."

**Output-first design:** Before writing any instructions, define exactly what output format is acceptable. Use JSON schemas, markdown templates, or exact examples.

### Output Template Categories

| Category | Use Case | Failure Sentinel |
|----------|----------|------------------|
| Message-Only | Simple answers | `0` |
| Path Resolution | File locations | `0` for not found |
| Action | Operations with side effects | Exit code |
| Structured Data | Machine-parseable results | Empty `{}` or `[]` |

### Expertise vs. Workflow Separation (Level 6+)

For self-improving prompts, **strictly separate**:
- `## Expertise` — domain knowledge that accumulates over time (updated by improve commands)
- `## Workflow` — operational procedures that remain stable (NEVER updated automatically)

---

## Model-Invoked vs. User-Invoked Prompts

### Model-Invoked (Skills)

Activated automatically via semantic matching. The model analyzes the user's request and selects relevant prompts.

**Strengths:** User doesn't need to memorize command names. New capabilities integrate transparently.

**Costs:** Harder to debug. Less predictable.

**Description field is critical:** Must include trigger terms, scope boundaries, and differentiation from similar capabilities.

```yaml
---
name: security-reviewer
description: >
  Security-focused code review specialist. Use when analyzing code for
  vulnerabilities, authentication/authorization issues, injection attacks.
  NOT for general code quality or style review.
---
```

### User-Invoked (Slash Commands)

Require explicit triggering by name (e.g., `/review:security`).

**Strengths:** Predictable, explicit, easy to debug.

**Costs:** User must know what's available. Doesn't scale past ~20 commands.

**Naming matters:** `/capture` beats `/knowledge:add-new-entry`. Short, action-oriented, namespaced with prefixes.

### Decision: Which to Use?

| Use Model-Invoked for... | Use User-Invoked for... |
|--------------------------|-------------------------|
| Recurring, semantic workflows | Rare or one-off tasks |
| The trigger can be described semantically | User should consciously choose |
| User benefits from not having to remember | Multiple valid approaches exist |

---

## Language Patterns

### Verb Semantics: Declarative vs. Imperative

**Research finding (SatLM, Ye et al., NeurIPS 2023):** Declarative prompts outperformed imperatives by ~23% on a challenging GSM arithmetic subset — not broadly across all complex reasoning tasks. Imperative style remains competitive on the full GSM8K dataset.

| Task Type | Preferred Mood | Rationale |
|-----------|---------------|-----------|
| Reasoning | Declarative | Encourages state-based thinking |
| Sequential workflow | Imperative | Clear procedural steps |
| Tool-calling | Imperative | Direct action invocation |
| Creative | Declarative | Establishes constraints without rigidity |

**Pattern for multi-phase workflows:** Declarative framing for high-level goals, imperative for operational steps.

### Specificity Calibration

**Modern frontier models (Claude 3.5+, GPT-4.1) follow instructions with high literal fidelity.** This means:
- Be explicit about required output format, constraints, success criteria, and external dependencies
- Remain flexible on implementation approach, intermediate reasoning, and stylistic choices

**Goldilocks:** Specificity helps when tasks have objective correctness criteria. Over-specification harms tasks requiring creative flexibility.

### Constraint Framing: The Pink Elephant Problem

**Negative constraints backfire in long conversations.** "Never use global variables" causes the model to think about global variables. Performance degrades as conversation length increases.

**Convert negative constraints to positive requirements:**

| Negative (Backfires) | Positive (Effective) |
|---------------------|---------------------|
| Never use global state | Use dependency injection |
| Don't expose internal errors | Return user-friendly error messages |
| Never modify files without reading | Read file contents before editing |

### Constraint Ordering

Critical/blocking constraints should appear **first** — the model weights earlier content more heavily.

```markdown
# CRITICAL CONSTRAINTS - NEVER VIOLATE
- Zero data loss
- Pass all existing tests

# IMPORTANT GUIDELINES
- Follow existing code patterns
- Add tests for new functionality

# STYLE PREFERENCES
- Keep functions under 50 lines
```

### Model-Specific Delimiter Preferences

**Claude:** XML-style tags (`<instructions>`, `<context>`, `<constraints>`)

**GPT:** Markdown headers (`###`), horizontal rules (`---`), code fences

**Gemini:** Precision over persuasion; context-last ordering (key info at the end of prompt)

**Format variance impact:** Up to 40% accuracy variance in smaller models based solely on delimiter choice.

### Testing XML vs. JSON Format for Your Use Case

Format choice is not a matter of taste — it has measurable effects on parse reliability and output consistency. Test it:

1. Take 20-30 representative inputs from your actual task distribution (not toy examples)
2. Run each through both formats with otherwise identical instructions
3. Measure three things: **parse success rate**, **output completeness** (does the model include all required fields?), and **answer quality** (human eval or automated metric)
4. Parse error rate is the most important signal — if JSON produces parse errors on more than 5% of outputs, XML is likely better for your use case
5. If both parse reliably, answer quality and completeness break the tie

**Why XML often wins on reliability:** XML tags provide unambiguous boundaries that don't require balanced delimiters to be valid. A partially truncated XML response can still be partially parsed; a partially truncated JSON response is typically unparseable. This matters most for long outputs near the context limit.

**When JSON is still the right choice:** When the downstream consumer is a standard JSON API, when structured nesting is deep, or when you control truncation and can guarantee complete outputs.

### Chain-of-Thought (2025 Status)

Modern reasoning-optimized models (Claude 3.5+, o1) perform internal reasoning by default. Explicit CoT prompting shows **diminishing returns** — it increases response time 20-80% with minimal accuracy gain on tasks within model capability. Use it primarily for debugging reasoning failures or when transparency is required.

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Approach |
|--------------|--------------|-----------------|
| "Be smart about this" | Vague, unactionable | Specify what "smart" means |
| "Do whatever's best" | No criteria provided | Define success criteria |
| Walls of unstructured text | Information overload | Structure with headers |
| Implicit assumptions | Model may not share them | State assumptions explicitly |
| Over-constraining process | Blocks valid solutions | Constrain output, not process |
| Elaborate persona descriptions | Zero informational value | State domain focus instead |
| "The Everything Prompt" (2000+ lines) | Cognitive overload, contradictions hidden in the mass | Delegate to focused specialists |

---

## Measuring Prompt Quality

| Dimension | What It Measures |
|-----------|------------------|
| **Structure** | Is it well-organized and parseable? |
| **Reusability** | Can it be adapted for similar tasks? |
| **Templating** | Are the variable parts clearly delineated? |
| **Breadth** | Does it handle the full scope of expected inputs? |
| **Depth** | Does it handle edge cases and nuances? |
| **Maintainability** | Can someone else understand and modify it? |
