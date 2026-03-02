# Reasoning LLMs

**Sources:** Prompting Guide — Reasoning LLMs *(2025)*

---

## Table of Contents

1. [What Makes a Reasoning Model Different?](#what-makes-a-reasoning-model-different)
2. [When Should You Use One?](#when-should-you-use-one)
3. [How to Use Them in AI Systems](#how-to-use-them-in-ai-systems)
4. [How to Prompt Them — Key Differences](#how-to-prompt-them--key-differences)
5. [Thinking Effort: Controlling How Much They Think](#thinking-effort-controlling-how-much-they-think)
6. [Limitations and What Goes Wrong](#limitations-and-what-goes-wrong)
7. [Step-by-Step: Deciding Whether to Use One](#step-by-step-deciding-whether-to-use-one)

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

Most reasoning model APIs let you control how much "thinking" the model does before responding. This is typically called the **thinking budget** or **effort level**.

Think of it like choosing between economy, business, and first class — you're paying for more compute time, which translates to more thorough internal reasoning.

| Tier | What It Means | When to Use |
|---|---|---|
| **Low / Budget** | Minimal internal reasoning; faster and cheaper | Start here. Many "complex" tasks succeed at Low. |
| **Medium** | Moderate reasoning depth; balanced cost/quality | Step up when Low produces incomplete or shallow answers |
| **High / Extended** | Maximum reasoning time; most thorough | Reserve for genuinely hard problems or high-stakes decisions |

**The smart strategy:** Always start at Low. Evaluate whether the output meets your quality bar. Escalate to Medium or High only when it demonstrably doesn't. This is important because tasks that *seem* complex often don't actually need maximum reasoning to get a good answer — and the cost difference between Low and High can be 5-10×.

A well-crafted prompt at Low thinking effort will often outperform a vague prompt at High thinking effort. Better prompts, not more thinking time, is usually the right first move.

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

**Unreliable parallel tool-calling** — Many reasoning models don't reliably call multiple tools in parallel (simultaneously). They tend to call tools sequentially instead. If your workflow depends on parallel tool calls for performance, test this assumption carefully before deploying with a reasoning model.

---

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

## Key Takeaways

Reasoning models represent a fundamentally different approach to language model inference — they think before they answer. This makes them dramatically better at genuinely complex problems, but wasteful and unnecessarily slow for simple ones.

The core disciplines for working with them:

1. **Don't use them for everything** — reserve them for planning, evaluation, and synthesis in larger systems
2. **Never add manual chain-of-thought prompting** — it conflicts with native reasoning and degrades output
3. **Be specific about what, not how** — describe the task and desired output clearly; let the model figure out the reasoning
4. **Start at Low thinking effort** — escalate only when you have evidence that it's needed
5. **Measure the cost/quality tradeoff** — always validate that the improvement justifies the expense
6. **Account for latency** — extended reasoning takes time; design your system accordingly
