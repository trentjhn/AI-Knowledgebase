# Models

## Model Selection: Core Principle

**Default to frontier. Downgrade only with evidence.**

For nearly every task, use the state-of-the-art class of models (currently Claude Opus 4.5 for coding). Frontier models consistently outperform smaller alternatives in reasoning depth, tool use, and complex instruction-following.

### The Decision Framework

```
1. Start with frontier model
         │
2. Is the task working reliably?
      │               │
     YES              NO
      │               │
3. Is cost a problem? Debug prompt/context first
      │
     YES
      │
4. Test with smaller model
      │               │
     YES (reliable)   NO (unreliable)
      │               │
  Use smaller      Stay with frontier
```

**Key insight:** Only consider downgrading *after* you have a working solution with a frontier model. Optimizing cost before validating capability is premature optimization.

### Capabilities That Matter Most

1. **Reasoning and tool use** — the capabilities that matter most for agentic work
2. Context length, speed, cost — secondary (important for architecture, not for "can it do the job?")

### When to Downgrade

- **Scouting agents** — Haiku works well for investigative tasks (read and distill). Fast, cheap, sufficient.
- **Simple retrieval or filtering** — When the task is about finding rather than reasoning.

**Small models function as RAG systems.** Keep context minimal (base config, project prompt, tool info, query), let them retrieve and distill, return results to an orchestrator for synthesis.

---

## Three-Tier Spawn Strategy for Multi-Agent Systems

| Model | Cost | Speed | Primary Use Cases | Spawn Count |
|-------|------|-------|-------------------|-------------|
| **Haiku** | Lowest | Fastest | Information gathering, pattern finding, file discovery, grep-style searches | Many (5-10 parallel) |
| **Sonnet** | Medium | Medium | Well-defined implementation, established patterns, standard refactoring | Balanced (2-4 parallel) |
| **Opus** | Highest | Slowest | Architectural decisions, ambiguous problems, creative solutions, security review | Selective (1-2 serial) |

### Pipeline Escalation Pattern

```
Haiku (Research) → Opus (Design) → Sonnet (Implement) → Haiku (Verify)
```

- Research processes large volumes (broad search) → cheap models work
- Design decisions require reasoning about trade-offs → expensive models excel
- Implementation follows established patterns → mid-tier models sufficient
- Verification is pattern matching → cheap models adequate

### Economic Optimization

```
10 Haiku agents (parallel) ≈ 30s, cost $0.10
1 Opus agent              ≈ 30s, cost $1.00
→ Haiku delivers 10× breadth for 1/10 the cost
```

**Orchestrators themselves typically use Sonnet or Opus** — coordination decisions require reasoning, and cost amortizes across many subagent spawns.

---

## Model Behavior

### Variance and Temperature

Models are probabilistic systems, not deterministic functions. At temperature 0, most models approach near-deterministic behavior, but subtle variance remains even at zero.

**Temperature compounds in multi-step workflows:**

| Temperature | Single-Step Success | 10-Step Success |
|-------------|---------------------|-----------------|
| 0.0 | ~99% | ~90% |
| 0.5 | ~97% | ~74% |
| 1.0 | ~95% | ~60% |

**Design guidance:** Default to temperature 0 for multi-agent orchestration or long workflows. Use higher temperature only in isolated creative phases.

### Instruction-Following Reliability

- **Frontier models** (Opus, GPT-4o) follow complex multi-constraint instructions consistently
- **Mid-tier** (Sonnet, GPT-4 Turbo) handle structured instructions well but may skip subtle requirements
- **Smaller models** (Haiku, GPT-3.5) work for simple, well-constrained instructions only

### Family-Level Behavioral Consistency

Models within the same family share instruction-following patterns, tool-use conventions, refusal boundaries, and output formatting tendencies. This is architecturally valuable: orchestrator-specialist systems rely on behavioral consistency so that prompts transfer cleanly across tiers within a family.

### Extended Thinking

Enable when:
- Multi-step reasoning (math, planning, logic)
- Latency is acceptable (batch processing, background jobs)
- Simpler approaches (better prompts, examples) have failed

Skip when:
- Straightforward tasks within model capability
- Latency-critical applications
- Claude already demonstrates correct reasoning

**Note:** Extended thinking requires temperature 0 and has a minimum 1,024 token budget.

### Instruction Fade in Long Contexts

Instructions at the start of long contexts receive less weight than recent messages — recency bias. Most clearly visible when conversations exceed 50% of context window capacity.

**Solutions:**
- Repeat critical instructions in system prompts closer to the task
- Spawn fresh agents for new tasks (avoid long context accumulation)
- Validate outputs programmatically and regenerate on failures

---

## Model Limitations

### Math → Delegate to external tools
Models lack arithmetic precision. Always delegate numeric computation to tools; models handle interpretation and formatting.

### Hallucination → RAG with mandatory citations
Models generate plausible-sounding false information confidently. Retrieval-Augmented Generation with mandatory citations reduces hallucination rates by 60-80%.

### Context Window → Proactive management
Despite advertised capacity, models degrade when context exceeds ~60% utilization. Compact proactively at 40-60%, not reactively at 95%.

### Instruction Drift → Checkpoint and anchor
Early instructions lose attention weight as context fills. Periodic reinforcement in system prompts preserves critical constraints.

### Tool Use Errors → Provide examples
Concrete usage examples improve accuracy from 72% → 90%. Validate outputs to prevent cascading errors.

### Version Instability → Pin versions
Model upgrades alter probability distributions unpredictably. Pin versions and use staged regression testing for transitions.

---

## Multi-Model Architectures

### When Single Model Suffices

Start with a single frontier model. Multi-model adds complexity that only pays off at scale.

**Use single model when:**
- Task volume is low
- Task complexity is homogeneous
- Total API spend is below ~$500-1000/month

### Orchestrator-Specialist Pattern

Strong reasoning model decomposes tasks and coordinates execution by weaker, cheaper models in parallel.

**NVIDIA ToolOrchestra (arXiv 2511.21689):** Nemotron-Orchestrator-8B routing to domain-specialist models outperformed larger monolithic models on benchmark tasks (FRAMES: 76.3%, tau2-Bench: 80.2%). The finding: routing intelligence in a small orchestrator beats raw scale in a single model.

**Token overhead:** ~15× more tokens than single-agent. Worth it when: complex research requiring parallel domain expertise, quality-critical tasks where deterministic outcomes justify cost, tasks with high parallelization potential.

### Model Cascades

Route to fast/cheap model first. Escalate to expensive model only when quality gate fails.

**Cost structure (70% cheap / 30% expensive):**
- All expensive: 100 × $0.010 = $1.00
- Cascade: (70 × $0.001) + (30 × $0.010) = $0.37 → **62% cost reduction**

**Quality gate strategies:**
- Confidence thresholds
- Semantic validation (schema, required fields)
- Classifier-based routing (trained on historical data)

### Planning-Execution Separation

Planning model (expensive) → structured intermediate representation → Execution model (cheap)

The quality lift comes from plan quality — a structured plan converts an ambiguous goal into unambiguous steps a cheaper model can follow. Measure gains against your own tasks; specific accuracy numbers vary significantly by workload.

---

## Model Evaluation

### The Compound Error Problem

Per-step accuracy `p` compounds over `n` steps: success rate = `p^n`

| Per-Step Accuracy | 10 Steps | 50 Steps | 100 Steps |
|-------------------|----------|----------|-----------|
| 99% | 90.4% | 60.5% | 36.6% |
| 95% | 59.9% | 7.7% | 0.6% |
| 90% | 34.9% | 0.5% | 0.003% |

**Implications:** Optimize per-step reliability above everything else. Minimize workflow length. Implement recovery mechanisms (retries catch 80% of errors → behaves like a much shorter workflow).

### Key Metrics

1. **Task Completion Rate** — percentage of tasks where the agent achieves the defined goal
2. **Tool Calling Accuracy** — correct tool selection + correctly formatted parameters
3. **Error Recovery Rate** — successful recovery from failed steps without human intervention
4. **Cost Per Successful Task** — total cost ÷ successful completions (not cost per attempt)
5. **Latency Distribution** — p50, p95, p99 (average hides catastrophic tail behavior)

### Evaluation Progression

1. **Start immediately with 3-5 test cases** (happy path + most likely failure + full end-to-end)
2. **Phase 2:** Deploy to limited users, track reported failures
3. **Phase 3:** Build regression test suite from production failures
4. Every production failure should become a test case

### LLM-as-Judge

Works when:
- Calibrated against human-annotated dataset
- Using pairwise comparison (not absolute ratings)
- Given explicit evaluation rubrics

Known biases: length bias, position bias in pairwise comparisons, writing style preferences. Always validate with human evaluation on a representative sample.
