# [Playbook Title] — [What It's For]

> **Purpose:** [One sentence describing what you're building and when to use this playbook]
> 
> **Time Estimate:** X–Y hours  
> **Prerequisites:** [What you need before starting]

---

## Decision Tree: Should You Use This Playbook?

**Use this tree to determine if this is the right guide for your project.**

```
[Root question]
│
├─ [Answer 1]
│  ├─ [Follow-up question]
│  │  ├─ [Answer leads to this playbook]
│  │  └─ [Answer leads to different playbook]
│  │
│  └─ [Answer leads elsewhere → cite playbook name]
│
└─ [Answer 2]
   └─ [Branches...]
```

**Example structure:**
```
Are you building an agent?
│
├─ No → Not an agent problem.
│        Try: RAG pipeline playbook, chatbot playbook, or fine-tuning
│
└─ Yes → Does your agent interact with users in real-time?
         │
         ├─ Yes → Use chatbot playbook
         │
         └─ No → Is it autonomous task execution?
                 │
                 ├─ Yes → Stay here (this playbook)
                 │
                 └─ Unsure → See decision matrix below
```

---

## Overview & Prerequisites

**What you're building:** [2–3 sentences plain English]

**When to use this playbook:**
- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

**When NOT to use:**
- [Anti-pattern 1]
- [Anti-pattern 2]

**Prerequisites:**
- [ ] Git repo initialized with CLAUDE.md (see [template](../../CLAUDE.md))
- [ ] Python/Node.js environment set up (if applicable)
- [ ] [Other prerequisite]

**Estimated time:** X–Y hours total (Y hours for Phase 1, etc.)

---

## Phases

### Phase 1: [Phase Name]

**Goal:** [What you accomplish in this phase]

**Estimated time:** 45–90 minutes

---

#### Step 1.1: [Action — Verb Form]

**What you're doing:** [1 sentence plain English explaining the purpose]

**KB Reference:** [KB-SECTION](file.md lines X–Y — brief description of relevant section)

**Action:**

1. [First action]
2. [Second action]
3. [Third action — may include code block if needed]

```python
# Example code if applicable
def example():
    return result
```

**Validation:**
- [ ] [Specific thing happened]
- [ ] [Specific output is visible]
- [ ] [You can point to evidence]

**Estimated time:** X–Y minutes

---

#### Step 1.2: [Action — Next Step]

**What you're doing:** [1 sentence]

**KB Reference:** [KB-SECTION](file.md lines X–Y — description)

**Action:**

1. [Instruction]
2. [Instruction with command if needed]

```bash
# Run this command
command --flag value
# Expected output:
# Success message here
```

**Validation:**
- [ ] [Verification method]
- [ ] [Second verification]

**Estimated time:** X–Y minutes

---

#### Step 1.3: [Checkpoint]

**What you're doing:** Commit your work for this phase.

**Action:**

```bash
git add [files you modified]
git commit -m "feat: [phase achievement]

[Brief explanation of what was accomplished and why]"
```

**Validation:**
- [ ] `git log` shows your commit
- [ ] All files are tracked

---

### Phase 2: [Next Phase Name]

[Repeat structure: Goal → Steps → Validation → Commit]

---

## Decision Matrix (If Applicable)

If your playbook has multiple valid approaches, include a comparison:

| Approach | Complexity | Time | When to Use |
|---|---|---|---|
| Simple approach | Low | 1–2h | Starting out, prototyping |
| Standard approach | Medium | 3–4h | Most projects |
| Advanced approach | High | 6–8h | High-performance needs |

---

## Common Gotchas & How to Fix Them

**Gotcha 1: [Common mistake]**  
Cause: [Why it happens]  
Solution: See [KB-SECTION](file.md lines X–Y), specifically step [X]  
Test: [How to verify you fixed it]

**Gotcha 2: [Another common mistake]**  
Cause: [Why it happens]  
Solution: [Fix]  
Test: [Verification]

---

## Troubleshooting

**If [error/symptom] occurs:**
- Check: [Diagnostic step]
- Reference: [KB section]
- Fix: [Solution]

---

## Next Steps

After completing this playbook:
- [ ] You have [concrete deliverable]
- [ ] Next step: [Link to next playbook or KB section]
- [ ] Optional improvement: [Advanced topic link]

---

## Citation Format Reference

All KB references in this playbook use this format:

```
[KB-SECTION](file.md lines X–Y — description of what this covers)
```

**Examples:**
- `[Prompt Maturity Levels](agentic-engineering.md lines 147–190 — 7-level maturity model for agent prompts)`
- `[Context Management](context-engineering.md lines 507–670 — context degradation thresholds and management patterns)`
- `[Evaluation Strategy](evaluation.md lines 1775–1779 — 3-scenario test approach: happy path, failure mode, edge case)`

**Rules:**
- Always include KB file path (relative to KB root: e.g., `agentic-engineering.md`, not `LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md`)
- Always include line numbers (start–end)
- Always include 1-line description of what section covers
- Description should match KB-INDEX entry for consistency
