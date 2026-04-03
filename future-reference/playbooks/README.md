# Playbooks — Scenario-Based Implementation Guides

Playbooks are step-by-step guides for building AI systems. Each is focused on a **primary pattern** (chatbot, RAG, agent, or prompt) and can optionally integrate secondary capabilities via cross-references.

---

## Structure of Every Playbook

Every playbook follows this consistent format:

### 1. Decision Tree (Top of File)

Routes you to the right primary playbook based on your use case.

**Format:** ASCII flowchart with 3–4 branching questions

**Purpose:** Answer "Do I need THIS playbook or a different one?"

**Example:**
```
What's the core pattern?
├─ Real-time conversation → chatbot playbook
├─ Document retrieval → RAG playbook
├─ Multi-step autonomous task → agent playbook (THIS ONE)
└─ Single LLM call → prompting playbook
```

---

### 2. Add Optional Capabilities (After Decision Tree)

If your use case needs secondary patterns, this section tells you which other playbooks to reference and where.

**Format:**
```
Does your [primary pattern] also need [secondary capability]?
→ Yes: See [playbook-name.md](path) lines X–Y, specifically [section]
       Then return here for [phase] to integrate
```

**Purpose:** Keep each playbook focused on its primary pattern; reference others only when needed.

**Example:** "Does your agent need to retrieve documents?" → Jump to RAG playbook Phase 1–2, then return to agent playbook Phase 2.3

---

### 3. Phases

Playbooks are divided into **phases** (typically 3–5 per playbook). Each phase accomplishes a specific goal.

**Phase structure:**
```
### Phase N: [Phase Name]

**Goal:** [What you accomplish]

#### Step N.X: [Action — Verb Form]

[Complete step structure below]
```

---

### 4. Steps (Granular Actions)

Each phase contains **3–5 steps**. Each step takes 10–30 minutes of active work.

**Complete step structure:**

```markdown
#### Step N.X: [Verb + Specific Action]

**What you're doing:** [1 sentence plain English explaining the purpose]

**KB Reference:** [Section Name](path/to/file.md lines X–Y)

**Action:**

1. [First action]
2. [Second action — may include code]
3. [Third action]

```code
# Code example if applicable
def example():
    return result
```

**Validation:**
- [ ] [Specific outcome 1 happened]
- [ ] [Specific outcome 2 happened]
- [ ] [You can point to evidence]
```

**Example:**

```markdown
#### Step 1.1: Write Your Agent Specification

**What you're doing:** Define the agent's purpose, scope, constraints, and success criteria before writing any code.

**KB Reference:** [Seven Properties of Executable Spec](../../LEARNING/PRODUCTION/specification-clarity/specification-clarity.md lines 52–83)

**Action:**

1. Create a file: `AGENT-SPEC.md` in your project root
2. Fill in: Purpose, Scope, What it CAN do, What it CANNOT do, Success Criteria, Constraints, Starting Input, Output Format
3. Read what you wrote. Are there any ambiguities? If yes, clarify.

**Validation:**
- [ ] Spec has all 8 sections filled in
- [ ] Success criteria are measurable
- [ ] At least 2 constraints defined
```

---

## KB Citations — Format & Rules

Every step must reference at least one KB section.

**Format:**
```
[Section Name](path/to/file.md lines X–Y)
```

**Rules:**
1. **Always include file path** — Relative from KB root, e.g., `../../LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md`
2. **Always include line numbers** — Start–End range (e.g., `lines 52–83`)
3. **Always include section name** — Visible in the link text (e.g., "Seven Properties of Executable Spec")
4. **Verify line numbers** — Use `grep -n` to find exact lines in the KB before adding to playbook

**Examples:**
- ✅ `[Prompt Maturity Levels](../../LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md lines 161–192)`
- ✅ `[Tool Use: Design, Selection, Restrictions](../../LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md lines 675–847)`
- ❌ `[See agentic-engineering for tool stuff](agentic-engineering.md)` — Missing lines, vague title

---

## Using Playbooks Effectively

**1. Check the decision tree first**
   - Are you in the right playbook?
   - If not, the tree routes you elsewhere

**2. Check "Add Optional Capabilities"**
   - Do you need secondary patterns (retrieval, interruption handling, etc.)?
   - Jump to other playbooks for those specific sections, then return

**3. Follow phases in order**
   - They build on each other
   - Complete and commit each phase before moving to the next

**4. Do each step as written**
   - Exact commands, exact file paths, exact code
   - Don't skip validation

**5. Validate before proceeding**
   - Use the checklist at the end of each step
   - Confirm it worked before moving on

**6. Commit after each phase**
   - Small commits are easier to debug
   - Include what phase you completed

---

## Playbook Reference

| Playbook | Primary Pattern | When to Use | Phases |
|---|---|---|---|
| **building-ai-agents.md** | Multi-step autonomous task | Research agent, workflow automation, data processing | 5+ |
| **building-rag-pipelines.md** | Document retrieval & ranking | Search internal docs, extract structured info | 4+ |
| **building-chatbots.md** | Real-time conversation | User interaction, multi-turn state | 4+ |
| **writing-production-prompts.md** | Single LLM call | Classification, generation, summarization | 3+ |

---

## Contributing to Playbooks

When writing or updating a playbook:

**Before starting:**
- [ ] Decide on primary pattern (what's this playbook for?)
- [ ] Identify which secondary patterns might apply ("Add Optional Capabilities" section)
- [ ] Map out phases (3–5 per playbook)

**While writing:**
- [ ] Follow the step template exactly
- [ ] Every step must have a KB citation
- [ ] Every step must be 10–30 minutes of actual work
- [ ] Every step must have a validation checklist
- [ ] Each action should include code/commands where relevant

**Before committing:**
- [ ] Verify all KB line numbers (use `grep -n` in the KB)
- [ ] Test that all file paths are correct (relative from KB root)
- [ ] Read through as if you were someone unfamiliar with the codebase
- [ ] Would you be able to follow this and build something real?

**Commit message format:**
```
docs(playbooks): Add [Phase Name] to [Playbook Name]

- Step X.1: [action]
- Step X.2: [action]
- Step X.3: [action]

Each step includes KB reference (file + lines), action, and validation checklist.
```

---

## Quality Checklist for Playbook Updates

Before merging a playbook update:

- [ ] Decision tree (if new playbook) routes clearly to primary pattern
- [ ] "Add Optional Capabilities" section cross-references other playbooks with specific phases/sections
- [ ] All KB citations verified (file path + exact line numbers)
- [ ] Each step is 10–30 minutes of active work
- [ ] Each step has validation checklist
- [ ] No time estimates (redundant with AI assistance)
- [ ] Code examples are complete and runnable
- [ ] Commands are exact (including flags and expected output)
- [ ] Someone unfamiliar with the project could follow this

---

## Future Playbooks

Consider adding:
- **Evaluation Workflows** — Testing agent/RAG/chatbot quality
- **Cost Optimization** — Model routing, batch processing
- **Fine-tuning Workflows** — When and how to fine-tune
- **Security & Guardrails** — Adding safety constraints to agents
