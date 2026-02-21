# Practices

## Debugging Agents

### Agent Debugging vs. Traditional Debugging

Traditional code debugging traces deterministic execution paths. Agent debugging works backward from observed behavior to infer what the model "thought," since internal reasoning is opaque.

**Diagnostic framework:**

```
Observed failure
       │
       ├─ Wrong output → prompt or context
       ├─ Looping → termination conditions
       ├─ Premature termination → stopping criteria
       ├─ Tool selection errors → tool descriptions
       ├─ Hallucination → context, grounding
       └─ Crashes → tool errors, context overflow
```

### Common Failure Modes

**Context overflow:** Agent behaves erratically near context limits. Solution: proactive compaction, fresh agents.

**Tool errors:** Wrong tool selected, malformed parameters, misinterpreted results. Solution: better tool descriptions, examples, validation.

**Hallucination:** Model generates plausible-sounding false information. Solution: grounding in retrieved context, RAG with citations.

**Instruction drift:** Early instructions lose influence as context fills. Solution: repeat critical instructions near the task, validate outputs programmatically.

**Tool selection confusion:** Multiple tools with overlapping functionality. Solution: clearer differentiation in descriptions, "Do NOT use for" sections.

**Premature termination:** Agent stops before task completion. Solution: explicit stopping criteria, verification steps.

**Multi-agent state confusion:** Agents operate on stale or incorrect shared state. Solution: context isolation, fresh agent instances.

### Debugging Techniques

1. **Structured logging** — capture every tool call with parameters and results
2. **Minimal reproduction** — isolate the failing case with smallest possible input
3. **A/B prompt testing** — compare working vs. failing prompts to identify the delta
4. **Context inspection** — audit what's actually in the agent's context at decision time
5. **Trace replay** — replay the full thought-action-observation chain
6. **Model comparison** — test same prompt on multiple models to isolate model vs. prompt issues

### Anti-Patterns

- Debugging without logs (impossible to diagnose)
- Changing multiple variables simultaneously (can't identify cause)
- Assuming model capability is always the culprit (usually prompt or context)

---

## Cost and Latency

### Frame Cost as Investment

The question isn't "is this expensive?" but "what's the cost of NOT using it?"

**Real-world ROI example (3-person team):**
- ~$12,000/month in API costs (~$4,000 per engineer)
- Week's worth of work shipped **daily** per engineer
- 10× productivity multiplier on feature delivery
- 35,000 lines of code generated and integrated in a single session

For a team with loaded costs of ~$150K/year per engineer ($12.5K/month), spending $4K/month to 10× their output means effective cost per unit of work drops by 90%.

### When Cost Actually Matters

**Cost becomes the constraint when:**
- Batch processing at massive scale (millions of documents)
- Building consumer products with thin margins

**Cost is rarely the constraint when:**
- Building internal tooling (developer time >> API costs)
- Shipping customer features (revenue impact >> API costs)
- Prototyping and validation (speed to learning >> API costs)

### Better Metrics

| Poor Metrics | Better Metrics |
|--------------|----------------|
| Total API spend | Cost per feature shipped |
| Cost per token | API cost as % of engineer loaded cost |
| Agent invocation count | Time-to-delivery improvement vs. baseline |

### Multi-Agent Token Economics

Multi-agent architectures trade tokens for deterministic quality:
- ~15× more tokens than single-agent
- 80× improvement in action specificity
- 100% actionable recommendation rate (vs. 1.7% single-agent)
- Zero quality variance across trials

**The surprising finding:** Architectural value lies in deterministic quality, not speed. Both single and multi-agent achieve similar latency (~40s for complex tasks).

### Token Cost by Feature Type

| Feature Type | Tokens/Invocation | Use When |
|--------------|-------------------|----------|
| Tools | ~100 | One-time actions, simple retrieval |
| Skills | ~1,500+ | Weekly+ repeatable workflows, autonomous activation |
| Subagents | Full conversation history | Parallel work streams, context isolation |
| MCP Servers | 10,000+ | Continuous data access, rich integrations |

---

## Production Concerns

### Lifecycle Hooks for Control

Wire hooks at critical transitions:

| Hook | Use For |
|------|---------|
| `PreToolUse` | Validate commands before execution (catch dangerous operations) |
| `PostToolUse` | Log actions, update metrics, track costs |
| `SubagentStop` | Record outputs, promote artifacts |
| `ErrorEscalation` | Notify human overseers when agents fail |

**The Orchestrator Observes Itself:** Hooks enable real-time visibility into agent behavior. PreToolUse and PostToolUse capture every action, creating:
- Cost tracking (token consumption per tool/subagent/task)
- Audit trails (who did what, when, why)
- Real-time monitoring (detect anomalies or runaway agents)

### Hook-Based Enforcement

Hooks enforce constraints beyond prompt instructions:

**Time-budgeted execution:** Hooks run synchronously and block agent execution.

| Hook | Budget | Graceful Degradation |
|------|--------|----------------------|
| SessionStart | 3-5s | Proceed with defaults |
| PreEdit | 10-15s | Skip optional context injection |
| PreToolUse | 5-10s | Log warning, proceed |

**Pre-edit dependency injection:** Before file modifications, inject dynamic context (current imports, type definitions, available exports from TypeScript language server). Prevents missing imports and type mismatches.

**Scope enforcement:** Validate file modifications against agent's declared contract before write operations.

**Philosophy:** Permissive tools + strict prompts + hook enforcement. Agents have broad access; prompts guide behavior; hooks enforce hard limits.

### Production Lessons from Large Codebases

**Context switching kills productivity:** Boot a new agent rather than salvage a degraded one. Cost of context confusion > cost of restarting.

**CLAUDE.md as convention encoding:** Document project conventions. Agents can't infer all conventions from code alone. Investing in clear specs saves 10× in agent iterations.

**Test-first discipline:** Dedicate a test-writing subagent to create failing tests first. Implementer makes them pass. Reviewer validates without sunk-cost bias.

**Dedicated review gate:** Enforce linting, complexity bounds, security checks. The reviewing agent didn't write the code and has no sunk-cost bias.

**Opus 4.5 for orchestration:** Practitioner consensus — Opus is particularly effective at managing teams of subagents and producing coherent multi-agent workflows.

### Google Cloud Deployment Gotchas

- Enable Cloud Run Admin API before deployment — missing permissions fail with cryptic errors
- Use prefixed environment variable names: `MYAPP_MODEL_NAME` not `MODEL` (conflicts with system variables)
- MCP connections are stateful → load balancers need session affinity at scale
- Default to `async def` for everything in ADK/MCP Python code

---

## Evaluation

### Start Immediately with 3-5 Test Cases

Don't wait for comprehensive test suites. Three to five carefully chosen test cases reveal more than zero:
- Happy path (most common use case)
- Most likely failure mode
- Full end-to-end workflow

### Evaluation Progression

1. **Manual tracing** — run test cases by hand, read logs and outputs
2. **Online user feedback** — deploy to limited users with feedback mechanisms
3. **Offline automated datasets** — build regression test suites from production failures

### Build Regression Tests from Production Failures

Every production failure should become a test case:
1. Capture exact input, context, and expected output
2. Add to regression test suite
3. Verify the fix prevents recurrence
4. Run the test on every subsequent change

### The Compound Error Reality

| Per-Step Accuracy | 10-Step Task Success |
|-------------------|---------------------|
| 99% | 90.4% |
| 95% | 59.9% |
| 90% | 34.9% |

**Key implication:** Increasing per-step accuracy from 95% to 99% more than doubles the 50-step success rate. Optimize per-step reliability above all else.

### Anti-Patterns in Evaluation

- **Waiting for large eval suites before starting** — requirements change; start immediately
- **Testing only final outputs** — check intermediate reasoning, tool calls, decision logic
- **Relying solely on LLM judges** — they have systematic biases; always calibrate against human evaluation
- **Ignoring cost and latency** — a 95%-accurate agent that takes 45 seconds and costs $2/success may not be production-viable
