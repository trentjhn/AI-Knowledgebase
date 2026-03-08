# Mental Models

## Pit of Success

> Design systems where the easiest path is also the correct path.

From Rico Mariani's work on .NET Framework design: instead of guardrails that prevent mistakes, design the system so the natural path leads to the right outcome.

```
Traditional approach:        Pit of Success:

    ┌─────────┐                 ╲         ╱
    │ SUCCESS │                  ╲       ╱
    └────▲────┘                   ╲     ╱
         │ effort                  ╲   ╱
         │                          ╲ ╱
    ─────┴─────                   SUCCESS

    (climb to success)         (fall into success)
```

### The Context Window as Pit of Success

**The holy grail of agentic engineering:** Shape the input tokens so the most probable output tokens are the correct ones.

Transformers are next-token prediction machines. Every input token influences the probability distribution over output tokens. The context window isn't just "information for the model" — it's the gravitational field that pulls outputs toward certain regions of possibility space.

```
Good context:                     Bad context:
┌─────────────────────┐           ┌─────────────────────┐
│ System prompt       │           │ Vague instruction   │
│ Examples            │  ──►  │   │ Irrelevant context  │  ──►  │
│ Relevant context    │  HIGH │   │ No examples         │  LOW  │
│ Clear instruction   │  P    │   │ Contradictions      │  P    │
└─────────────────────┘  correct  └─────────────────────┘  correct
```

### What Makes Context a Pit of Success

**1. Attention flows to what matters:** Recency bias means information near the end of context gets more attention. Structural clarity helps attention patterns form correctly. Related information grouped together creates coherent attention clusters.

**2. Examples set the distribution:** Few-shot examples don't just "show the model what to do" — they shift the entire probability distribution. Each example is training data at inference time.

**3. Context primes token sequences:** "Let me think step by step" primes chain-of-thought. A code block primes code. Technical vocabulary primes technical output. You're setting up token sequences that make desired continuations statistically dominant.

### Designing for It

**Make the correct output the obvious continuation:**

```
# Weak
"Handle this user request appropriately."

# Strong — correct output is the only sensible continuation
"Respond to this user request with a JSON object containing:
- 'action': one of ['approve', 'deny', 'escalate']
- 'reason': a single sentence explanation

User request: {request}

Response:"
```

**Eliminate competing attractors:** Don't include examples of things you don't want. Don't hedge instructions. Don't include irrelevant context that could prime wrong directions.

**Position information by importance:**
1. System-level identity and constraints → beginning (establishes frame)
2. Task-specific context and data → middle (working memory)
3. Specific instruction and format → end (highest attention, immediate priming)

---

## Specs as Source Code

> Throwing away prompts after generating code is like checking in compiled binaries while discarding source.

Articulated by Sean Grove. In agentic programming, **specs are the truth** and generated code is secondary (can be regenerated).

```
Traditional:                    Agentic:

┌──────────────┐               ┌──────────────┐
│ Source Code  │               │ Specification│
└──────┬───────┘               └──────┬───────┘
       │ compile                      │ agent reads
       ▼                              ▼
┌──────────────┐               ┌──────────────┐
│   Binary     │               │ Generated    │
│ (throwaway)  │               │ Code         │
└──────────────┘               │ (throwaway)  │
                               └──────────────┘
```

### What This Changes

**Version control:** Check in specs, research docs, and planning artifacts — they're the source code. The diff to a spec file is more important than the diff to code it produces.

**Code review:** Review the spec for correctness, completeness, and testability. If the spec is right, the code can always be regenerated.

**Tests:** Write tests that validate the spec was followed, not just that the code runs.

**Project structure:**
```
specs/                   ← Primary (version controlled, reviewed)
  architecture.md
  requirements.md
  plan.md
src/                     ← Derivative (can be regenerated from specs)
  main.py
```

### Living Artifacts: BMAD Pattern

**Code is merely a downstream derivative of specifications.** Four-phase artifact methodology:

1. **Analysis Phase** → Product Brief, Research Summary
2. **Planning Phase** → PRD (Product Requirements Document), UX Design
3. **Solutioning Phase** → Architecture Document, Epics/Stories
4. **Implementation Phase** → Working Code (from the above specs)

Phases 1-3 produce documents. Phase 4 produces code *from* those documents.

**Compliance value:** For regulated industries, this transforms compliance from post-hoc documentation to inherent process. Every decision is captured, versioned, and traceable.

**Adversarial review gates between phases:** An orchestrator critically examines each artifact before allowing progression. Prevents: incomplete PRD → flawed architecture → thousands of lines of wrong code.

### When to Apply

**Good fit:**
- Multi-agent systems (specs become shared interface between agents)
- Long-lived projects (future agents understand the system by reading specs)
- Generated code (the spec is what you maintain; code is disposable)
- Complex domains where "why" is as important as "what"

**Poor fit (overkill):**
- One-off scripts and throwaway automation
- Exploratory prototypes where you're still figuring out what to build
- Stable, finished systems that won't change

### Common Pitfalls

**Spec drift:** Specs and implementation diverge. Solution: test that implementation matches specs; make spec updates part of your change workflow.

**Over-specification:** Specs become harder to maintain than code. Solution: capture intent and constraints, not line-by-line implementation.

**Vague specs:** Too high-level to be executable. Solution: think "testable" — if you can't test whether the spec was followed, it's too vague.

---

## Execution Topologies

Five topologies shape how agentic systems execute work.

### The Five Core Topologies

| Topology | Structure | Best For |
|----------|-----------|----------|
| **Parallel** | Fan-out → concurrent execution → gather | Independent tasks, maximum throughput |
| **Sequential** | A → B → C (output feeds next) | Dependent phases, ordered transformations |
| **Synthesis** | Multiple inputs → single comprehensive output | Research aggregation, multi-perspective review |
| **Nested** | Agents spawning sub-agents | Complex hierarchical decomposition |
| **Persistent** | Long-running agent with evolving state | Continuous workflows, growing knowledge |

### Four Improvement Vectors

To measure whether an agentic system actually improves over time:

1. **Wider** — Handles more diverse task types
2. **Deeper** — Goes further in complex multi-step tasks
3. **Thicker** — Produces higher-quality outputs
4. **Less Friction** — Requires less human intervention

### Autonomy Spectrum (5 Levels)

| Level | Name | Human Role |
|-------|------|------------|
| 1 | **Augmentation** | Human does the work, AI assists |
| 2 | **Copilot** | Human leads, AI suggests |
| 3 | **Supervised Autonomy** | AI acts, human reviews |
| 4 | **Delegated Autonomy** | AI acts, human approves at gates |
| 5 | **Full Autonomy** | AI acts end-to-end |

### Trust Gradients

Match topology to trust level:
- Low trust → Sequential with human checkpoints
- Medium trust → Parallel with review synthesis
- High trust → Persistent with minimal oversight

### Zero-Touch Aspiration

The horizon of fully autonomous execution: agents that understand intent, decompose tasks, execute in appropriate topologies, recover from failures, and deliver results — without human intervention.

Currently achievable for: well-scoped coding tasks, document processing, data transformation.

Not yet reliable for: novel problem-solving requiring judgment, tasks with unclear success criteria, high-stakes irreversible operations.

---

## Context as Code

Context is not just "background information" — it's an executable specification for agent behavior. Structured context that defines:
- Agent identity and constraints
- Domain knowledge and patterns
- Success criteria and evaluation rubrics
- Tool availability and usage patterns

...is functionally a program. The agent executes against the context just as a traditional program executes against instructions.

**Implication:** Context deserves the same engineering rigor as code: version control, review, testing, iteration.
