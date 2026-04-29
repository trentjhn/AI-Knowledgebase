# Reasoning LLMs

**Sources:** Prompting Guide — Reasoning LLMs *(2025)*, Brief Is Better: Non-Monotonic Chain-of-Thought Budget Effects in Function-Calling Language Agents *(2026)*, Think Anywhere in Code Generation — Jiang et al. *(2026, arXiv:2603.29957)*

---

## Table of Contents

1. [What Makes a Reasoning Model Different?](#what-makes-a-reasoning-model-different)
2. [When Should You Use One?](#when-should-you-use-one)
3. [How to Use Them in AI Systems](#how-to-use-them-in-ai-systems)
4. [System Architecture Patterns](#system-architecture-patterns)
5. [How to Prompt Them — Key Differences](#how-to-prompt-them--key-differences)
6. [Thinking Effort: Controlling How Much They Think](#thinking-effort-controlling-how-much-they-think)
7. [Limitations and What Goes Wrong](#limitations-and-what-goes-wrong)
8. [Step-by-Step: Deciding Whether to Use One](#step-by-step-deciding-whether-to-use-one)

---

## What Makes a Reasoning Model Different?

Most AI language models work roughly like this: you send them a message, they immediately start generating a response token by token. They're fast, but they're not "stopping to think." The response they generate is effectively their first attempt.

**Reasoning models** are fundamentally different. They're trained to *work through a problem internally* before producing their final answer. They generate a hidden "chain of thought" — essentially a scratchpad where they reason step by step — and only then write their response.

> **Analogy:** Imagine two students taking the same math exam. Student A reads the problem and immediately writes whatever answer comes to mind. Student B reads the problem, works through it carefully on scratch paper, checks the work, and then writes the final answer. Both students might know the same math — but Student B's process consistently leads to higher accuracy on complex problems.

Standard LLMs are Student A. Reasoning LLMs are Student B.

**Current examples of reasoning models (as of 2025):**
- **OpenAI o3** — OpenAI's reasoning model series
- **Claude 3.7 Sonnet** — Anthropic's extended thinking model
- **Gemini 2.5 Pro** — Google's reasoning-capable model

**The core trade-off:** Reasoning takes time and uses more tokens (which cost money). A standard model might respond in 2 seconds. A reasoning model working through the same problem might take 15-60 seconds and generate 5-10× more tokens internally before responding. For simple tasks, this overhead is wasteful. For genuinely complex problems, it's often worth it.

---

## When Should You Use One?

The critical mistake people make is assuming that reasoning models are always better. They're not — they're *specifically better* at certain types of problems. Using them indiscriminately wastes money and adds latency without improving results.

### Use Reasoning Models For:

**Multi-step problems with long chains of logic.** If solving the problem correctly requires keeping many pieces of information in mind simultaneously and reasoning through their implications in sequence, reasoning models excel. Examples: complex algorithm design, multi-constraint optimization, legal analysis, research synthesis.

**Ambiguous situations without a clear "right answer."** When there are competing considerations that need to be weighed against each other — not just facts to retrieve — reasoning models are better at navigating the tradeoffs.

**High-stakes tasks where mistakes are expensive.** Scientific research, complex debugging, financial modeling, medical analysis — situations where the cost of error is high enough to justify slower, more careful reasoning.

**Large codebase work.** Reviewing and debugging complex code requires tracking many interdependencies simultaneously. Reasoning models are significantly better at this than standard models.

**Multi-step agentic planning.** When an AI agent needs to figure out *how* to accomplish a complex, open-ended goal (not just execute a known process), reasoning models produce more reliable and complete plans.

### Stick With Standard Models For:

**Simple, factual questions.** "What's the capital of France?" doesn't benefit from extended thinking.

**High-throughput applications.** If you're processing thousands of requests at scale and each one is relatively simple, the latency and cost of reasoning models make them impractical.

**Tasks where fast iteration matters more than perfect accuracy.** Rapid prototyping, drafting, brainstorming — cases where speed of iteration beats precision.

**When manual chain-of-thought prompting already works — but test reasoning models without CoT too.** If a standard model with "think step by step" already solves your task reliably, you may not need a reasoning model. The caveat: always run a separate test with a reasoning model using *no* CoT instructions (see Section 4 — adding CoT to reasoning models actively hurts them). You're comparing two different things: standard model + manual CoT vs. reasoning model + no CoT. The reasoning model sometimes wins even when the standard + CoT baseline is acceptable.

> **Decision rule:** Always test a standard model first. If the output is shallow, misses important considerations, or fails on complex cases, that's your signal to try a reasoning model.

---

## How to Use Them in AI Systems

In real AI applications and agents, reasoning models aren't used for everything — they're used strategically at specific points in a larger system.

### As the Planning Layer

The most powerful use of reasoning models in agentic systems is as a **planning orchestrator** that figures out *what* to do, while faster, cheaper models handle execution.

Here's the architecture:

```
Complex task arrives
       ↓
[Reasoning Model] — Takes time to think through the problem.
                    Decomposes it into clear sub-steps.
                    Identifies dependencies and risks.
       ↓
Clear plan with specific sub-tasks
       ↓
[Standard Model A]  [Standard Model B]  [Standard Model C]
Execute sub-task 1  Execute sub-task 2  Execute sub-task 3
(fast, cheap)       (fast, cheap)       (fast, cheap)
       ↓
[Reasoning Model] — Reviews outputs. Synthesizes results.
                    Validates the overall outcome.
```

This architecture separates expensive thinking from cheap execution. You pay the reasoning tax only where judgment genuinely matters — planning and validation — while running the routine work at standard model costs.

---

### As a Judge or Evaluator

Reasoning models are particularly well-suited to evaluating AI outputs — assessing whether another model's response is accurate, well-reasoned, or follows the right format.

This enables a powerful **evaluator-optimizer loop**:
1. A standard model produces an output
2. A reasoning model evaluates it — not just "good/bad" but detailed feedback on *what* is wrong and *why*
3. The feedback is used to improve the prompt or the output
4. Repeat until quality is high enough

This is especially valuable when you're trying to evaluate nuanced outputs where simple metrics (like "does the answer contain the right keywords") are insufficient. Reasoning models can assess whether the *reasoning* in an answer is sound, not just whether the answer looks right.

---

### For Retrieval-Augmented Generation (RAG) on Complex Topics

Standard models can handle simple RAG — retrieve a document, answer a question about it. But some queries require multi-hop reasoning: finding information in document A, combining it with information in document B, and then drawing an inference that neither document explicitly states.

Reasoning models handle this multi-hop synthesis significantly better. You route complex analytical queries through the reasoning model while simpler lookups continue to use standard models — optimizing both cost and quality.

---

### For Visual Reasoning

Reasoning models with multi-modal capabilities (able to process images) can reason through visual problems with the same chain-of-thought approach. The model might "look" at an image, reason about what it sees, decide it needs a closer look at a specific area, virtually "zoom in," and then synthesize an answer.

---

## System Architecture Patterns

The previous section covers what reasoning models do well in isolation. This section covers how to actually wire them into a production system — the structural patterns that make reasoning models practical at scale.

The core problem is straightforward: reasoning models are slow and expensive. You can't put them in the hot path of every request without either degrading UX or going bankrupt on compute. Good system design solves this by routing intelligently and positioning reasoning models where their cost buys the most value.

---

### The Cascade Pattern (Default for High-Volume Systems)

A standard model handles the majority of calls quickly and cheaply. Only queries that fail a confidence threshold — or are explicitly flagged as complex — escalate to the reasoning model. This is the right default architecture when you're handling many requests and most of them don't actually need deep reasoning.

```
Request arrives
      ↓
[Standard model] — fast, cheap, handles most cases
      ↓
Confidence check / complexity classifier
      ↓
[Passes threshold] → return response immediately
[Fails threshold]  → escalate to reasoning model
                           ↓
                   [Reasoning model] — deep analysis
                           ↓
                   Return response
```

**Why this works:** In most real-world distributions, a small fraction of queries are genuinely hard. If 5% of your queries need reasoning-model depth and 95% don't, routing all of them through a reasoning model means you're paying reasoning prices for 95% of calls that didn't need it. The cascade lets you pay for reasoning compute only where it earns its cost.

**Practical implementation note:** The confidence threshold doesn't need to be sophisticated. It can be as simple as a classifier that looks for complexity signals (multi-constraint, contradictory requirements, explicit uncertainty, domain-specific jargon density) or a hard-coded list of query types. Start simple and refine based on where the standard model actually fails.

---

### Reasoning as Final Validator

The reasoning model is not in the hot path — it validates or synthesizes *after* standard models do first-pass work. This keeps latency acceptable for the majority of the pipeline while adding reasoning-depth quality control at the output gate.

```
Standard model drafts code
         ↓
[Reasoning model] reviews for correctness, edge cases, security
         ↓
Return to user (or loop back for revision)
```

This pattern is particularly effective for code generation, document drafting, and any task where first-pass output can be produced quickly but must meet a quality standard before delivery. The user's perceived latency is mostly the fast standard model; the reasoning model's time is spent on something valuable — catching errors that would have shipped.

---

### The Recovery Pattern

When a standard model fails on a task — wrong answer, bad format, returned an error, exceeded context cleanly — route that specific request to a reasoning model as the fallback. The reasoning model's extended thinking often resolves what the standard model missed, because it can take more inference steps and consider more alternatives before committing to an answer.

```
Standard model → fails (wrong answer, error, or explicit low confidence)
                     ↓
              [Reasoning model] — extended thinking, second attempt
                     ↓
              Return result (with or without confidence caveat to user)
```

This pairs well with an eval layer: if you have a way to detect failure (output format check, factual consistency check, user thumbs-down signal), you can use that signal to trigger recovery routing automatically.

---

### Timeout Handling — Non-Negotiable

Reasoning models can take 30–90+ seconds on hard problems. Any production system that uses them must implement a timeout with graceful degradation. Without this, a slow reasoning call becomes a hung request, and a hung request becomes a frustrated user or a failed SLA.

The pattern:

```
Send to reasoning model
         ↓
Timeout fires (set based on your SLA — e.g., 15 seconds)
         ↓
[Reasoning model responds in time] → return result
[Timeout fires first]              → return standard model's answer
                                     with a confidence caveat:
                                     "This answer is based on standard
                                     analysis; complex review unavailable."
```

The confidence caveat matters — it's honest, it manages user expectations, and it tells downstream systems that this answer didn't receive full reasoning review. Don't silently fall back; surface the degradation.

---

## How to Prompt Them — Key Differences

This is the section where most people go wrong. Reasoning models require a different prompting approach than standard models, and if you use standard prompting techniques, you'll actually get *worse* results.

### The Most Important Rule: Don't Tell Them How to Think

With standard models, it's common practice to prompt them to reason step by step: *"Think through this carefully. First consider X, then consider Y..."* This kind of manual chain-of-thought prompting helps standard models produce better reasoning.

With reasoning models, **this backfires.** Reasoning models already have native thinking built in — they're going to work through the problem internally regardless of whether you tell them to. When you also add manual chain-of-thought instructions, you're creating conflicting instructions that interfere with the model's native reasoning process. Quality degrades.

> **Rule:** With reasoning models, tell them *what* you want. Don't tell them *how* to think about it.

```
❌ Standard model approach (do NOT use with reasoning models):
"Think step by step. First, consider the user's requirements.
Then evaluate each option. Then weigh the tradeoffs. Finally,
provide your recommendation."

✅ Reasoning model approach:
"Evaluate these three architecture options for the given requirements
and recommend the best one. Return your answer as: recommendation,
reasoning, key tradeoffs, risks."
```

---

### Be Specific About What You Want

While you shouldn't tell reasoning models *how* to think, you should be very specific about:
- **What the task is** — clear definition of the problem
- **What the output should look like** — format, structure, length
- **What constraints apply** — any requirements or restrictions

Vague instructions cause two problems with reasoning models:
- **Overthinking:** The model spins through many considerations when a focused one was needed
- **Underthinking:** The model misunderstands the scope and reasons about the wrong problem

**Use few-shot examples when format matters.** If you need a very specific output format and describing it in prose is ambiguous, include 1-2 examples of input → output pairs. Reasoning models learn format and style from examples effectively.

---

### Output Format: XML vs JSON — Test Your Model

Some practitioners report XML being more robust with reasoning models for complex structured outputs — the argument being that JSON's strict syntax (missing commas, unclosed brackets) causes parse failures that XML's more forgiving structure avoids. However, **this is largely anecdotal and model-specific**. Frontier models (GPT-4o, Claude 3.7 Sonnet, Gemini 2.5) rarely fail at JSON generation, and JSON is often preferable for programmatic parsing downstream. Test both formats with your specific model and task before committing to either. If your model reliably produces valid JSON, don't switch to XML on principle.

---

### Descriptive Language Improves Outputs

Surprisingly, using more descriptive and specific language in your instructions produces higher quality outputs. Instead of "add styling," say "add hover states, smooth transitions on all interactive elements, and ensure consistent spacing." The specificity gives the model's reasoning more to work with.

---

## Thinking Effort: Controlling How Much They Think

Most reasoning model APIs let you control how much "thinking" the model does before responding. On the Anthropic API, this is the `budget_tokens` parameter — it sets the maximum number of tokens the model can use for its internal reasoning chain before producing its final response.

**Key mechanics of `budget_tokens`:**
- Minimum: 1,024 tokens (below this, the model can't engage in meaningful extended thinking)
- Maximum: varies by model — claude-sonnet-4-6 supports up to approximately 16,000 thinking tokens; Opus-class models support higher ceilings
- Thinking tokens are billed at the same per-token rate as output tokens — they are not free

Think of it like choosing between economy, business, and first class — you're paying for more compute time, which translates to more thorough internal reasoning.

| Tier | `budget_tokens` Range | What It Means | When to Use |
|---|---|---|---|
| **Low / Budget** | 1,024 – 3,000 | Minimal internal reasoning; fast, low cost premium | Straightforward multi-step reasoning, math checks, simple constraint problems |
| **Medium** | 5,000 – 10,000 | Moderate reasoning depth; balanced cost and quality | Code review, planning with moderate constraints, analytical tasks |
| **High / Extended** | 15,000 – 32,000 | Maximum reasoning time; highest accuracy on hard problems | Complex architecture decisions, research synthesis, adversarial reasoning. Latency: 30–90+ seconds. |

**Cost mental model:** At claude-sonnet-4-6 pricing (~$15/M output tokens as of 2025), 10,000 thinking tokens adds roughly $0.15 to the cost of a single call. For a low-volume, high-stakes use case — one architectural review, one security audit — that's negligible. At 10,000 calls per day, that's $1,500/day in thinking-token overhead alone. Know your volume before defaulting to Medium or High.

**The smart strategy:** Always start at Low. Evaluate whether the output meets your quality bar. Escalate to Medium or High only when it demonstrably doesn't. Tasks that *seem* complex often don't need maximum reasoning — the cost difference between Low and High is typically 5-10×.

A well-crafted prompt at Low thinking effort will often outperform a vague prompt at High thinking effort. Better prompts, not more thinking time, is usually the right first move.

**When to escalate — and when to stop:**
- If Low produces wrong or shallow answers on a task where you know the correct answer, move to Medium.
- If Medium still fails, move to High.
- If High consistently fails: this is the important signal. Stop escalating tokens and instead ask whether this is actually a reasoning problem. Many failures that look like "not enough thinking" are actually retrieval problems (the model doesn't have the right information in context) or task decomposition problems (the task is too coarsely specified). More tokens won't fix a missing knowledge problem. Diagnose before spending more.

---

## Special Case: Function-Calling Agents and the Reasoning Paradox

There's a surprising failure mode you'll encounter when using reasoning models in agentic systems: **excessive reasoning tokens actively degrade performance in function-calling tasks**.

On the surface, this seems backward. More thinking should be better, right? But in practice, when you give an agent unlimited tokens to reason before calling a function, something goes wrong: the agent overthinks the problem, second-guesses its own decisions, hallucinates functions that don't exist, and makes worse tool-calling choices than a model that reasons briefly.

**The empirical pattern (from a 2026 study on Qwen2.5-1.5B-Instruct):**

- **Brief reasoning (8–32 tokens)**: 45% relative accuracy improvement over no reasoning. Function routing works reliably.
- **Extended reasoning (128+ tokens)**: Accuracy collapses to 25%. Wrong function selections spike from 1.5% to 28%, and the model hallucinates nonexistent functions 18% of the time.

Why? The mechanism appears to be that **extended reasoning time allows the agent to talk itself out of good decisions**. With limited tokens, the agent commits to a function and executes. With extensive tokens, it cycles through uncertainty, explores alternative paths that don't actually exist in the tool set, and eventually calls something wrong out of accumulated confusion.

This contradicts the intuition from reasoning-model research that "more thinking helps." That's true for analytical tasks (research synthesis, complex debugging, architectural decisions). It's not true for structured tool-use loops where the agent needs to make fast, confident function-routing decisions.

**Practical implications:**

1. **Don't default to High thinking effort in agentic systems.** Start at Low. If the agent is misrouting functions, the issue is usually prompt clarity or tool ambiguity — not insufficient thinking. More tokens won't fix either.

2. **Prefer templated reasoning (FR-CoT) over free-form CoT.** The study found that a simple templated approach — structuring CoT output to separate reasoning from function calls — achieved equivalent accuracy to extended free-form reasoning while eliminating function hallucination entirely (0% hallucination rate). Constraint improves reliability.

3. **Separate orchestration from reasoning.** If your agent needs deep reasoning, route it upstream (let a standard model with a reasoning-class model review the plan). Don't embed extended thinking in the function-calling loop itself.

4. **Test your specific model.** This finding comes from a smaller model (1.5B parameters). Frontier models (Claude 3.7 Sonnet, GPT-4o, Gemini 2.5) may handle extended reasoning in function-calling better. Run your own tests before assuming it applies universally.

---

## Adaptive Reasoning Positioning: Thinking at the Right Moment

The function-calling paradox above establishes that *more reasoning isn't always better*. A 2026 paper (Jiang et al., arXiv:2603.29957) goes further: it asks not just *how much* to think, but *where during generation* to invoke reasoning at all.

Traditional reasoning models front-load their thinking. The model generates a full hidden reasoning chain before writing a single output token. This works well when the problem's full complexity is apparent upfront — mathematical proofs, architectural decisions, constraint analysis. Code generation behaves differently. Complexity emerges *during* writing — you often don't know at line 1 of a function that line 47 will require careful edge-case handling.

**The Think-Anywhere mechanism:** The model inserts `<thinkanywhere>` blocks mid-generation at points of highest token entropy — positions where the model is most uncertain about what comes next. Rather than one large upfront reasoning block, thinking is distributed across the generation trace at exactly the moments it's needed.

Two technical findings validate this:

*Where models invoke thinking (entropy analysis):* Researchers measured token entropy over 10 tokens following each `<thinkanywhere>` invocation. The differentials were "predominantly positive" — confirming the model genuinely places reasoning at higher-uncertainty positions, not randomly. The top invocation sites: assignment statements (most frequent), return statements, conditional blocks.

*Training:* Two-stage. First, Gemini 2.5 Flash generates ~5,000 synthetic examples of Think-Anywhere patterns (cold-start). Then GRPO reinforcement learning refines placement using a hierarchical reward: structure (correct `<think>` + at least one `<thinkanywhere>`) + correctness (passing test cases), weighted α=0.1 for structure.

**Benchmark results (Qwen2.5-Coder-7B-Instruct):**

| Method | LeetCode | LiveCodeBench | HumanEval | MBPP | Average |
|---|---|---|---|---|---|
| Base Model | 50.6 | 34.3 | 88.4 | 70.7 | 61.0 |
| GRPO | 67.3 | 36.0 | 88.6 | 81.7 | 68.4 |
| **Think-Anywhere** | **69.4** | **37.2** | **91.5** | **82.9** | **70.3** |

+9.3% absolute over baseline; +1.9% over GRPO. The method also generalizes outside code — on AIME 2024 mathematical reasoning, Think-Anywhere achieves 17.3% pass@1 vs. 5.3% base, suggesting the high-entropy positioning principle extends across domains.

**The key efficiency finding:** Think-Anywhere uses *fewer total tokens* than GRPO while outperforming it — each inline block adds only 22–23 tokens on average. By placing reasoning precisely at uncertain positions, it avoids the waste of applying thinking to code segments that don't need it.

**Ablation results (LeetCode pass@1):** Cold start alone: 47.9% (−21.5 pts vs. full). RLVR alone: 63.4% (−6.0 pts). Both are essential — cold start teaches *that* adaptive thinking is possible; RL teaches *when* to invoke it.

**The design principle for builders:** This introduces a third axis for reasoning model configuration:
1. **Whether to reason** — reasoning model vs. standard (Section 2)
2. **How much to think** — budget_tokens: Low / Medium / High (Section 6)
3. **Where to think** — upfront (current API default) vs. adaptive at high-entropy positions

> **Deployment status as of early 2026:** Think-Anywhere requires training — it's not an API parameter. It's a research finding to watch. When adaptive positioning becomes available in API-accessible models, the budget_tokens guidance in Section 6 will need a "position" dimension. The efficiency finding (precision > volume) is the durable takeaway.

---

## Limitations and What Goes Wrong

Reasoning models aren't magic. They have specific failure modes and limitations worth knowing before you rely on them.

### Output Quality Issues

**Mixed-language output** — If your prompt mixes languages or is ambiguous about which language to respond in, reasoning models can produce mixed-language responses. Always specify the output language explicitly if it matters.

**Repetition** — When instructions are conflicting or contradictory, reasoning models can get stuck and produce repetitive outputs as they try to satisfy multiple constraints simultaneously. Simplify and clarify when this happens.

---

### Reasoning Failure Modes

**Overthinking** — Given an ambiguous task, a reasoning model might work through an extremely broad set of considerations when you only needed a narrow answer. Being specific about scope prevents this.

**Underthinking** — On the other hand, if the model misunderstands what type of problem you're presenting, it might apply shallow reasoning when the task actually required deep analysis. This is usually a prompt clarity issue.

**Degraded performance with manual CoT** — As mentioned: adding "think step by step" style instructions to reasoning models reliably makes them worse, not better. Remove any chain-of-thought scaffolding from prompts before switching to reasoning models.

---

### Practical Constraints

**High cost** — Reasoning models cost significantly more per task, especially at High thinking effort. Use them where the quality improvement justifies the cost, not as a blanket upgrade.

**High latency** — Extended thinking can take 30-90 seconds. Don't use reasoning models in any user-facing flow where fast response time is important unless you're okay with that wait.

**Unreliable parallel tool-calling** — This deserves more than a footnote because it regularly catches practitioners off guard.

Reasoning models generate a sequential thinking chain and then produce a response. This architecture doesn't naturally support parallel tool calls mid-reasoning the way standard models can batch multiple tool calls in a single response turn. The practical result: if you send a reasoning model a prompt that requires calling three tools in parallel, it will call them sequentially. Your expected parallelism disappears, and your pipeline is slower than projected — sometimes by a factor of 3-5× on tool-heavy tasks.

Three workarounds, in order of preference:

**1. Design for sequential tool calls with caching.** Structure your pipeline so each tool's result informs the next. The thinking chain actually benefits from seeing each result in order — the model can incorporate what it learned from tool 1 when deciding how to use tools 2 and 3. This turns a limitation into a feature.

**2. Separate orchestration from reasoning.** Use a standard (non-reasoning) model to orchestrate parallel tool calls and aggregate the results. Once all tool outputs are assembled, pass the full context to the reasoning model for synthesis. This gets you parallelism on the data-fetching side and deep reasoning on the analysis side without fighting the architecture.

```
[Standard model] → call tools A, B, C in parallel → aggregate results
                                                             ↓
                                              [Reasoning model] → synthesize
```

**3. Minimize tool count in reasoning calls.** Give reasoning models fewer, more focused tools. They reason better with 3 relevant tools than 15 available tools. More tools create more sequential overhead and more surface area for the model to reason about which tool to call when — time better spent on the actual problem.

---

---

### Backdoor Vulnerabilities in Reasoning Models

Reasoning-oriented models, such as those in the DeepSeek-R1 or Qwen-MoE families, exhibit unique vulnerabilities to weight-level backdoors that target long-form chain-of-thought (CoT) traces. These "BadChain" attacks manipulate the reasoning path rather than just the final answer. 

Standard inference-time defenses like TIGS (Tail-Risk Intrinsic Geometric Smoothing) effectively neutralize these triggers during the prefill stage, but the long decoding chains inherent to reasoning models can lead to "temporal dilution," where the defensive effect weakens as the CoT sequence grows. For these models, practitioners should consider extending the attention intervention into the first 32 decoding steps. This configuration has been shown to reduce Attack Success Rates from ~20% to ~12.5% on reasoning benchmarks like GSM8K, though it increases latency to approximately 18.4% compared to a prefill-only approach.
## Step-by-Step: Deciding Whether to Use One

Here's a practical decision process for whether to reach for a reasoning model:

**1. Start with a standard model.** Run your task. Evaluate whether the output quality meets your bar.

**2. Look for signals of reasoning limitations:**
- The answer misses important edge cases or considerations
- The reasoning chain has gaps or logical errors
- The model oversimplifies a genuinely complex tradeoff
- Multi-step problems are getting the intermediate steps wrong

**3. If signals are present, switch to a reasoning model at Low effort.** Don't start at High — you'll burn cost unnecessarily.

**4. Fix your prompt first.** Before escalating thinking effort, refine your instructions:
- Remove any manual chain-of-thought instructions
- Be more specific about the task, output format, and constraints
- Add few-shot examples if format is the issue

**5. Escalate thinking effort only if needed.** Go Low → Medium → High, evaluating at each step.

**6. Measure cost vs. quality gain.** A 10% quality improvement for a 5× cost increase may not be worth it. Always evaluate the tradeoff explicitly.

**7. Deploy in the right layer.** Use reasoning models for planning, evaluation, and synthesis. Use standard models for execution, simple lookups, and high-throughput steps.

---

## The Broader Context: Two Axes of Compute Scaling

Reasoning models represent one axis of a broader trend in how the field is thinking about compute and intelligence.

**Axis 1 — More compute per token (what reasoning models do):** Extended thinking allocates additional compute to each output by generating a hidden reasoning chain before the final response. The model produces fewer tokens in the final answer but burns more compute arriving at it. Budget_tokens is the control knob.

**Axis 2 — Fewer tokens per unit of meaning (what emerging architectures chase):** Research like CALM (Continuous Autoregressive Language Models, 2025) tries to reduce the number of autoregressive steps needed by compressing multiple tokens into single prediction steps — continuous vectors representing K-token chunks rather than one discrete token at a time.

These are complementary, not competing:
- Reasoning models: same number of steps, deeper thinking per step
- Continuous-space models: fewer steps, each step covers more semantic ground
- The goal in both cases: more intelligence per unit of compute

A future system might combine both — a model that thinks in compressed semantic chunks (fewer steps) with extended reasoning (more depth per step). Whether that's achievable depends on whether continuous-space training methods mature to production scale.

For the architectural picture: see `LEARNING/FOUNDATIONS/emerging-architectures/emerging-architectures.md`

---

## Key Takeaways

Reasoning models represent a fundamentally different approach to language model inference — they think before they answer. This makes them dramatically better at genuinely complex problems, but wasteful and unnecessarily slow for simple ones.

The core disciplines for working with them:

1. **Don't use them for everything** — reserve them for planning, evaluation, and synthesis in larger systems
2. **Never add manual chain-of-thought prompting** — it conflicts with native reasoning and degrades output
3. **Be specific about what, not how** — describe the task and desired output clearly; let the model figure out the reasoning
4. **Start at Low thinking effort** — escalate only when you have evidence that it's needed
5. **Measure the cost/quality tradeoff** — always validate that the improvement justifies the expense
6. **Account for latency** — extended reasoning takes time; design your system accordingly
