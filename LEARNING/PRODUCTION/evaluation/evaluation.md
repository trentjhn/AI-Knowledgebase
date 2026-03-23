# AI/LLM Evaluation

> A comprehensive reference on how to measure whether AI systems actually work — covering metrics, methods, benchmarks, tools, and the feedback loops that turn evaluation into improvement.

## Table of Contents

1. [What Evaluation Actually Means for AI Systems](#1-what-evaluation-actually-means-for-ai-systems)
2. [Why Evaluation Is Hard](#2-why-evaluation-is-hard)
3. [What You're Actually Measuring](#3-what-youre-actually-measuring)
4. [Evaluation Methods](#4-evaluation-methods)
5. [Evaluating RAG Systems](#5-evaluating-rag-systems)
6. [Evaluating Agents](#6-evaluating-agents)
7. [Benchmarks and Leaderboards](#7-benchmarks-and-leaderboards)
8. [Evaluation Frameworks and Tools](#8-evaluation-frameworks-and-tools)
9. [Evaluation in Production](#9-evaluation-in-production)
10. [Common Failure Modes](#10-common-failure-modes)
11. [Building Your First Eval Suite: A Practical Path](#11-building-your-first-eval-suite-a-practical-path)
12. [The Evaluation Flywheel](#12-the-evaluation-flywheel)
13. [Key Takeaways](#13-key-takeaways)
14. [Sources](#14-sources)

---

## 1. What Evaluation Actually Means for AI Systems

In traditional software, testing is relatively straightforward. You write a function that sorts a list, you run tests that check whether the list comes back sorted, and the answer is binary: pass or fail. There is a single correct output, and you can verify it automatically with total confidence.

AI systems break this model entirely. When a language model answers a question, summarizes a document, or decides which tool to call, there is rarely one single correct response. A customer support chatbot might handle the same complaint in a dozen different ways, all of which are reasonable — and the "best" answer often depends on tone, context, user preference, and implicit goals that are hard to write down. Evaluation, in this world, is the practice of systematically measuring whether AI outputs are good enough — across dimensions of quality that are themselves contested and context-dependent.

This makes evaluation one of the most important and most underinvested activities in applied AI. Teams that ship systems without rigorous evaluation are flying blind. They do not know how their system performs on edge cases, whether it has gotten better or worse after a change, or what specific failure modes will hit their users. Evaluation is what turns intuition ("it seems to be working") into evidence ("it correctly handles 91% of our query types with a faithfulness score above 0.85").

The stakes are high in both directions. Invest too little in evaluation, and you will deploy degraded or unsafe systems without knowing it. Invest too much in the wrong metrics, and you will optimize for numbers while real quality declines — a trap that has caught many AI teams. Getting evaluation right requires understanding both the tools available and the conceptual traps that undermine them.

### The Three-Level Evaluation Stack

Practitioners commonly think about evaluation at three levels, each serving a different purpose and operating at a different point in the development cycle.

**Offline evaluation** happens before deployment, against curated test datasets. You run a set of known inputs through your system and score the outputs against expected results or a judge. This catches regressions during development — like unit tests for your AI application. It is fast, cheap, and repeatable, but it is only as good as your test set.

**Online evaluation** happens in production, on real traffic. You log model inputs and outputs, apply automated scoring functions, collect user feedback signals (clicks, thumbs-up/down, follow-up questions), and monitor metrics over time. This reveals how the system performs in the wild, with the diversity and messiness of real users — but it is slower and noisier than offline eval.

**Human evaluation** is brought in when decisions require judgment that automated metrics cannot capture reliably. This includes: validating that your automated evaluators are actually measuring what you think they are, evaluating high-stakes outputs where the cost of mistakes is high, and exploring failure modes that automated scoring might miss. Human eval is expensive and slow but is the ground truth against which automated evaluators must ultimately be calibrated.

These three levels are not competing alternatives — they work together. Offline eval catches regressions fast. Online eval surfaces real-world drift. Human eval validates and calibrates the other two.

---

## 2. Why Evaluation Is Hard

Understanding why evaluation is difficult — not just technically, but conceptually — is prerequisite to doing it well. There are three root causes.

### Probabilistic Outputs

A traditional software function is deterministic: same input, same output, every time. An LLM is a probability distribution over possible outputs. Ask it the same question twice and you may get different answers — both correct, both plausible, expressed differently. This means you cannot simply run the same test case twice and expect identical results. Evaluation must account for variance, which means you need enough samples to distinguish real quality from noise. A single pass/fail on a single output tells you almost nothing.

### No Single Ground Truth

For many AI tasks, there is no canonical correct answer. If you ask an LLM to "summarize this article," there are many valid summaries of different lengths, styles, and emphasis. If you ask a chatbot to "handle this customer complaint," there are dozens of appropriate responses. Even in domains where there appears to be a right answer — say, a math problem — the model might arrive at the correct answer through flawed reasoning, or a flawed-looking answer that is actually correct for a subtler reason.

This is fundamentally unlike traditional testing. You cannot write a unit test that says "is this response good?" without either providing a very specific expected output (too rigid) or defining a rubric for quality (which is itself a judgment call). Both approaches require human decisions that inevitably encode assumptions.

### Subjective Quality

What makes a response "good" depends on who you ask. A medical professional evaluating a health information chatbot will weigh accuracy above all else. A content marketer evaluating a writing assistant will weigh engagement and voice. An enterprise customer service manager will weigh tone, policy compliance, and resolution rate. These are not wrong priorities — they are just different. This means there is no universal quality metric for LLMs. Any evaluation framework must be designed around the specific task and the specific audience.

Hamel Husain, one of the practitioners who has written most clearly about this, puts it bluntly: "Most teams repeat the same mistakes — too many metrics, and arbitrary scoring systems using uncalibrated scales (like 1-5) across multiple dimensions where the difference between scores is unclear and subjective." The fix is not more metrics but sharper ones: binary pass/fail evaluators tied to specific, observable failure modes.

### The "Model vs. Product" Distinction

One conceptual trap that causes teams to evaluate the wrong thing: conflating model evaluation with product evaluation. These are related but not the same.

**Model evaluation** measures the raw capability of the underlying LLM — its knowledge, reasoning ability, instruction following, and safety. Benchmarks like MMLU and HumanEval live here. This is useful for model selection (which base model should I build on?) but tells you very little about whether your specific application works.

**Product evaluation** measures whether your complete AI system — including your prompts, your retrieval strategy, your tool configurations, your guardrails, and your UX — solves the user's actual task well. This is what determines whether your product succeeds.

A model with mediocre benchmark scores but excellent product evaluation tells you your system is well-designed and your task is achievable with mid-tier models. A model with excellent benchmark scores but poor product evaluation tells you that raw model capability is not your bottleneck — your architecture, prompts, or data pipeline is failing. The distinction directs you to the right fix.

---

## 3. What You're Actually Measuring

Before you can evaluate an AI system, you need to decide what "good" means for your specific application. The dimensions of quality fall into a few broad categories.

### Legacy NLP Metrics: BLEU and ROUGE

Before the LLM era, NLP evaluation relied heavily on two metrics that are worth understanding both for their historical role and their modern limitations.

BLEU (Bilingual Evaluation Understudy) was developed for machine translation. It measures how much of the model's output appears in a human reference translation, counting overlapping sequences of words (called n-grams). A score of 1.0 means perfect overlap with the reference; a score of 0.0 means none. BLEU emphasizes precision — whether what the model says appears in the reference.

ROUGE (Recall-Oriented Understudy for Gisting Evaluation) is its counterpart for summarization. Where BLEU asks "is what the model said in the reference?", ROUGE asks "is what's in the reference captured by the model?" It emphasizes recall — whether the model captured the key content from the source.

Both metrics were useful when machine translation and summarization produced outputs that closely resembled human references in vocabulary and phrasing. They are inadequate for evaluating modern LLMs. A model can score highly on ROUGE by including lots of words from the source without producing a coherent, accurate, or useful summary. Conversely, a response that captures the right meaning with different vocabulary will score poorly. Research from 2024 found that BLEU and ROUGE are "terrible predictors of LLM performance" in generative settings. They are still used in academic contexts for comparability, but practitioners building real products should treat them as incomplete diagnostics at best.

### LLM-Specific Quality Dimensions

Modern evaluation focuses on dimensions of quality that are more meaningful for generative AI.

**Faithfulness** (also called groundedness) measures whether the model's claims are supported by the context it was given. If you feed an LLM a document and ask it to answer questions, a faithful response only asserts things that can be inferred from that document. Unfaithful responses "hallucinate" — they add information not present in the source. Faithfulness is scored from 0 to 1, where 1 means every claim in the output is traceable to the context.

**Relevance** measures whether the response actually addresses the question asked. A model can produce fluent, accurate text that answers a slightly different question than the one posed — technically non-hallucinated but unhelpful. Relevance is about alignment between the input intent and the output content.

**Coherence** refers to the logical flow and internal consistency of a response. A coherent response follows a logical structure, does not contradict itself, and reads as a unified piece of text rather than disconnected fragments.

**Groundedness** (used specifically in RAG contexts) is essentially faithfulness applied to retrieval-augmented generation: does the answer come from the retrieved context? A score of 0 indicates hallucination — the model invented content not present in the retrieved documents.

**Hallucination rate** is the frequency at which a model generates content that is factually incorrect or fabricated. This is distinct from faithfulness (which is per-response) — hallucination rate is a population-level metric tracking how often the system confabulates across a large set of interactions.

**Toxicity** measures whether outputs contain harmful, offensive, or inappropriate content. It is evaluated using classifiers trained on harmful content datasets, and is particularly important for public-facing applications.

**Perplexity** is a technical metric measuring how "surprised" a model is by a sequence of text — lower perplexity means the model found the text predictable, which is loosely correlated with fluency. However, perplexity is a property of the model's internal probability estimates, not of the output's usefulness or correctness. A very low perplexity response could still be wrong or harmful. It is most useful as an internal diagnostic, not as a customer-facing quality signal.

### Alignment as a Multi-Dimensional Metric

Beyond the task-quality dimensions above, alignment evaluation treats the model's conformance to human values as its own measurement domain. The **TRUSTLLM framework** organizes alignment into nine measurable dimensions, each requiring separate proxy tasks and benchmark datasets because no single metric captures alignment holistically:

1. **Truthfulness** — resistance to misinformation, hallucination, sycophancy, and adversarial factuality attacks
2. **Safety** — avoidance of unsafe or illegal outputs across diverse attack vectors
3. **Fairness** — prevention of stereotyping and demographic bias in outputs
4. **Robustness** — stability of outputs across rephrasing, paraphrasing, and input perturbation
5. **Privacy** — protection of human autonomy and sensitivity to personally identifiable information
6. **Machine Ethics** — adherence to both implicit and explicit ethical norms, including emotional awareness
7. **Transparency** — availability of information about the model's capabilities, limitations, and reasoning
8. **Accountability** — ability to provide explanations for outputs that allow verification and attribution
9. **Regulations and Laws** — compliance with organizational policies, national laws, and industry standards

The TRUSTLLM framing is operationally important because it prevents conflating these dimensions. A model can score well on truthfulness while failing on fairness — and both failures have different root causes requiring different fixes. Each dimension uses indirect proxy benchmarks (since mathematical quantification of most dimensions remains unsolved), which means alignment evaluation inherits all the proxy limitations of general LLM evaluation.

### Task-Specific Metrics

Beyond these general dimensions, some metrics apply specifically to certain tasks.

**Accuracy, precision, recall, and F1** apply when the task has clear-cut correct answers — classification problems, information extraction, question answering with a defined answer set. F1 balances precision (how many of the model's positive predictions were actually correct) and recall (how many of the actual positives the model caught). These are best suited to tasks with well-defined outputs.

**Task completion rate** and **success rate** are used for agentic systems. Did the agent accomplish the goal it was given? These are end-state metrics that evaluate outcomes rather than individual outputs.

**BERTScore** is a more modern alternative to BLEU/ROUGE that uses semantic embeddings rather than n-gram overlap. Instead of counting identical words, it measures the similarity of the generated text and reference text in a semantic vector space — so paraphrases and synonyms are properly credited. Research has shown BERTScore correlates more closely with human judgment than BLEU or ROUGE for many tasks. It is not perfect (embedding spaces still have biases), but it represents a significant improvement for tasks where meaning matters more than word choice.

**Latency and cost** are operational metrics that are part of any honest production evaluation. An AI system that is highly accurate but takes 30 seconds to respond and costs $10 per query is not viable. Evaluation should always include efficiency alongside quality. In practice, many teams build efficiency metrics into their eval suites — measuring p95 latency and cost-per-query alongside quality scores, and treating unacceptable latency as a hard failure regardless of quality.

---

## 4. Evaluation Methods

With a clear sense of what you're measuring, you can choose the right method for measuring it. Each method has distinct tradeoffs in cost, speed, scalability, and accuracy.

### Reference-Based Evaluation

The simplest approach: compare the model's output to a known correct answer. If you have a dataset of (question, correct answer) pairs, you can score each output against the ground truth. This works well for closed-ended tasks — factual Q&A, classification, structured data extraction, code generation where you can run unit tests.

The major limitation is that you need a ground truth dataset, and building one is expensive. Every data point requires a human to create or validate an expected answer. This is worth the investment for your most critical query types, but it does not scale to the full diversity of user inputs in a live system.

A related technique is pairwise comparison, where instead of comparing to an absolute reference, you present two model outputs and ask which is better. This is the basis of Chatbot Arena (discussed in Section 7) and is often easier for evaluators than scoring on an absolute scale.

### LLM-as-a-Judge

The most significant methodological development in LLM evaluation over the past two years is using a strong LLM (like GPT-4 or Claude) to evaluate the outputs of another LLM. This is called "LLM-as-a-judge."

The approach was validated empirically in the landmark 2023 paper by Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." They found that GPT-4 acting as a judge matched human evaluator agreement at a rate exceeding 80%, reaching the same level of interrater agreement observed between human evaluators. This was a significant result: it suggested that automated LLM-based evaluation could be used as a cost-effective proxy for human judgment.

Here is how it works in practice. You construct a prompt that gives the judge model: (1) the original user input, (2) the model's output to evaluate, (3) optionally, a reference answer or retrieved context, and (4) an explicit rubric defining what you're scoring. The judge returns a score and — importantly — reasoning for that score. The reasoning is valuable for debugging: you can inspect why a response was marked low and identify the failure pattern.

DeepEval's G-Eval is a prominent implementation of this pattern. It uses the judge LLM to generate evaluation steps based on a custom criterion, then scores the output against those steps. Tools like DeepEval, Braintrust, and LangSmith all provide LLM-as-a-judge as a core evaluation mechanism.

**The biases of LLM judges** are well-documented and must be actively mitigated:

- **Position bias**: When a judge is asked to pick between two responses presented side-by-side (A vs. B), it tends to favor whichever response appears first. The Zheng et al. paper documented this clearly. Mitigation: run pairwise evaluations twice with positions swapped, and only accept a verdict that is consistent across both runs.

- **Verbosity bias**: LLM judges tend to favor longer, more detailed responses even when concision would be more appropriate. A verbose but mediocre answer often beats a sharp, correct one-liner. Mitigation: explicitly instruct the judge to penalize unnecessary length, and validate your judge against a golden set where you know the right answer is concise.

- **Self-enhancement bias**: A GPT-4 judge will tend to rate GPT-4 outputs more favorably than outputs from other models. This is not a conspiracy — it is an artifact of the judge having been trained to prefer outputs that look like its own. Mitigation: use an ensemble of different judge models (GPT-4, Claude, Gemini) and take the consensus, reducing the influence of any single model's idiosyncrasies.

- **Sycophancy**: If the evaluand (the response being judged) is prefaced with confident framing ("As an expert, I would say..."), the judge may inflate its score even if the content is mediocre. This is the mirror of the problem documented in RLHF research: models trained on human feedback learn to appeal to human biases, and judge models can exhibit similar patterns.

The practical takeaway: LLM-as-a-judge is powerful but should never be used naively. Design binary (pass/fail) criteria rather than 1-5 scales when possible. Validate your judge's agreement with human labels on a golden dataset. Use an ensemble of judges for high-stakes decisions.

### SelfCheckGPT — Consistency-Based Hallucination Detection

A complementary approach to LLM-as-a-judge for hallucination detection is **SelfCheckGPT**: generate multiple independent responses to the same prompt (at higher temperature), then measure consistency across those responses. The insight is that factual claims the model genuinely "knows" will be stated consistently across runs, while hallucinated details — which are effectively confabulations sampled from the model's probability distribution — will vary widely from run to run.

The method does not require external references or a judge model. It works on the premise that if five independent generations all agree that "X" is true, that consensus is meaningful evidence for X. If the five generations disagree on a detail, that disagreement is a hallucination signal. This makes SelfCheckGPT reference-free — applicable in domains where ground truth is unavailable — and relatively cheap (it requires only multiple sampling passes, not a separate judge model). The tradeoff is that it cannot detect hallucinations the model states confidently and consistently: systematic biases in training data cause the model to consistently confabulate the same false claims, which consistency-based checks will miss. Use SelfCheckGPT as one layer of a hallucination defense stack, not as the only check.

### Human Evaluation

Human evaluation is the most expensive and slowest method, but it remains the ultimate calibration standard. There are two variants with different tradeoffs.

**Expert evaluation** uses domain specialists — medical professionals for healthcare AI, lawyers for legal applications, experienced customer service agents for support chatbots. Expert evaluators provide high-quality, high-signal labels, but they are expensive and slow. They are essential for high-stakes domains and for building golden datasets that calibrate your automated evaluators.

**Crowdsourced evaluation** distributes evaluation tasks across a large pool of non-expert workers (typically via platforms like Amazon Mechanical Turk). Crowdsourcing is cheaper and faster than expert eval and can scale to many thousands of examples. Research shows that majority-vote aggregation of crowdsourced labels produces quality comparable to expert labels for many tasks. However, agreement rates vary significantly by topic: they can reach 0.96 on clearly objective content (violence/gore, where most raters agree) but drop to 0.25 on subjective or personal topics where there is no consensus.

For both approaches, a key quality measure is **inter-annotator agreement (IAA)** — the rate at which different evaluators give the same score to the same output. Low IAA signals that your evaluation rubric is ambiguous, that the task itself is genuinely subjective, or that your evaluator pool has different background knowledge. Before relying on human labels, measure IAA and investigate the disagreements.

### A/B Testing in Production

Once you are deployed, A/B testing is the gold standard for measuring whether a change (new model, new prompt, new retrieval strategy) actually improves user outcomes. Rather than relying on offline benchmarks, you expose a fraction of real users to the new system and measure the difference in their behavior.

**Shadow mode** is a safe entry point. You route real production traffic to both the old and new systems simultaneously, but only show users the output from the old (production) system. The new system processes the same queries and logs its outputs, which you then score and compare offline. Users are never exposed to the candidate system's outputs, eliminating any risk to their experience. Shadow mode is ideal for validating that a new system is at least as good as the current one before any user impact.

**Gradual rollout** follows shadow validation. Start by routing 1-5% of traffic to the new system (a "canary release"), monitor quality and operational metrics carefully, and increase the percentage in stages if everything looks healthy. This allows you to catch regressions early, when only a small fraction of users are affected, before they become widespread.

The challenge with A/B testing for LLMs is identifying the right online metrics. User satisfaction signals like thumbs-up/down, task completion, and absence of follow-up clarifying questions are proxies for quality, but they are noisy and can be gamed. A response that sounds confident and authoritative may get thumbs-up even if it contains subtle inaccuracies. Combining automated scoring (applied to logged outputs) with user feedback signals gives a more complete picture.

### Red-Teaming and Adversarial Evaluation

Red-teaming treats your AI system as something that might fail catastrophically under adversarial conditions, and actively tries to make it fail before real users do. It originated in security testing (where red teams simulate attackers) and has been adopted by AI safety researchers and ML engineers to probe for unexpected failure modes.

Adversarial evaluation involves crafting inputs specifically designed to elicit problematic outputs: jailbreaks that bypass safety guardrails, prompt injections that hijack the model's behavior, inputs at the edge of the training distribution, or queries specifically targeting known weaknesses like hallucination-prone topics.

Research findings are sobering. Studies have shown that adversarial prompts can bypass safety mechanisms in frontier models at high rates, and that jailbreak attacks "bypass fresh guardrails 80-100% of the time on frontier chatbots" in some studies. Anthropic's Constitutional Classifiers red-team effort involved 183 participants spending an estimated 3,000+ hours attempting to jailbreak their classifier over two months — and this was for a purpose-built safety classifier, not a general-purpose system.

Red-teaming can be done manually by domain experts who understand potential misuse patterns, or automated using tools like Promptfoo, which can generate over 50 types of adversarial inputs automatically. A strong practice is to treat every red-team finding as a new test case: document the failure mode, add it to your eval suite, and verify the fix before deployment.

### Evaluation Orchestration Patterns: Checkpoint-Based vs. Continuous

Not all evaluation strategies fit all workflows. The choice between running evals at fixed milestones vs. continuously throughout work has major implications for cost, feedback speed, and workload management.

**Checkpoint-Based Evals (for linear workflows)**

Run evaluation at the end of discrete phases. Example workflow:

```
Phase 1: Planning
├─ Create design
├─ Write spec
└─ [EVAL CHECKPOINT] Verify spec quality
    └─ If spec is inadequate, revise and re-eval

Phase 2: Implementation
├─ Write code
├─ Run unit tests
└─ [EVAL CHECKPOINT] Verify against spec
    └─ If implementation diverges from spec, fix and re-eval

Phase 3: Review
├─ Code review
├─ Documentation
└─ [EVAL CHECKPOINT] Verify completeness
    └─ If gaps found, address and re-eval
```

**Best for:**
- Feature implementation (clear start and end)
- Code review gates (eval is a required checkpoint before merge)
- Release validation (eval before deployment)
- Batch processing jobs (eval at job completion)

**Advantages:**
- Clear signal when to stop iterating (checkpoint passed)
- Predictable resource usage (eval runs at known times)
- Easy to reason about (each phase has a clear acceptance criteria)

**Disadvantages:**
- Long feedback loops (wait until end of phase to find problems)
- Potential rework (discovering issues late costs more to fix)

**Implementation:** Set explicit acceptance criteria per checkpoint. "This checkpoint passes if: spec includes all requirements, no ambiguities, and risk assessment is complete."

---

**Continuous Evals (for exploration and long sessions)**

Run evaluation regularly while work is ongoing. Example:

```
[Start Session]
  │
  ├─ Refactor component
  ├─ [Auto-run tests every 30 seconds]
  ├─ Modify config
  ├─ [Auto-run linter + type check]
  ├─ Add feature
  ├─ [Auto-run E2E tests]
  │
  ├─ [Quality degradation detected at 15:23]
  │  └─ Halt and fix regression before continuing
  │
  └─ [Clean session end]
```

**Best for:**
- Long exploratory sessions (refactoring, prototyping)
- Continuous integration pipelines (merge to main triggers full test suite)
- Agent coding sessions (verify state after every significant change)
- Maintenance tasks (catch regressions immediately)

**Advantages:**
- Fast feedback loops (problems detected immediately)
- Small rework (catch issues early while changes are fresh)
- Confidence building (passing evals frequently confirms progress)

**Disadvantages:**
- Higher resource usage (evals run constantly)
- Requires clear stop conditions ("halt when tests fail" is better than "retry infinitely")
- False positives can be annoying (flaky tests triggering false alerts)

**Implementation:**
- Run every N minutes (e.g., every 300 seconds)
- Run on every file save if automated
- Run after "natural pause points" (end of function, end of commit)
- Set max iteration limit (e.g., "stop after 3 failures")

---

**Hybrid Approach (Recommended)**

Combine both patterns for best results:

1. **Checkpoint evals** define acceptance criteria for major phase transitions
2. **Continuous evals** catch regressions within each phase
3. **If continuous eval fails**, you have 2 options:
   - Quick fix (if issue is obvious) → continue within phase
   - Escalate (if issue is structural) → review phase checkpoint and adjust

Example:

```
Phase: Implementation
├─ Continuous: Run tests every 60 seconds
│  └─ Catches regressions immediately (agent realizes they broke something)
│
├─ Continuous: Type checking after every file change
│  └─ Catches type errors before they propagate
│
└─ Checkpoint: Full eval suite at end of phase
   └─ Verifies: tests pass, types correct, coverage >80%, no regressions
   └─ If checkpoint fails, you have high confidence about what broke (continuous evals already told you)
```

---

**The pass@k and pass^k Metrics**

When designing evals, distinguish between two very different success metrics:

**pass@k: At Least One Success Across k Attempts**

```
k=1: 70% → "70% of single attempts succeed"
k=3: 91% → "At least one of three attempts succeeds 91% of the time"
k=5: 97% → "At least one of five attempts succeeds 97% of the time"
```

Use pass@k when you can retry and just need *any* version that works. Example: "Generate 5 code samples and pick the best one."

**pass^k: All k Attempts Must Succeed (Consistency)**

```
k=1: 70% → "Single attempts succeed 70% of the time"
k=3: 34% → "All three of three attempts succeed only 34% of the time"
k=5: 17% → "All five of five attempts succeed only 17% of the time"
```

Use pass^k when consistency is essential and retries aren't an option. Example: "This production classifier must return the same answer every time" or "Each time we test, we need predictable results."

The lesson: pass@k and pass^k are measuring different properties. A system with pass@1 = 70% and pass@3 = 91% is *not necessarily good at consistency* — it's good at eventually succeeding. These are different design goals.

---

## 5. Evaluating RAG Systems

RAG (Retrieval-Augmented Generation) is an architecture where the AI retrieves relevant documents from a knowledge base before generating a response — grounding the answer in source material rather than relying purely on training data. Evaluating RAG systems requires measuring both the retrieval component and the generation component, since failures can happen at either stage.

The most widely adopted framework for RAG evaluation is **Ragas** (Retrieval-Augmented Generation Assessment), an open-source library that provides four core metrics designed around the specific failure modes of RAG pipelines.

### The Four Ragas Metrics

Think of a RAG pipeline as having two stages: first, retrieving the right documents; second, generating a good answer from those documents. The Ragas metrics measure both.

**Context Precision** measures whether what was retrieved is actually relevant to the question. Imagine you ask a chatbot "What is the company's refund policy?" and the retriever pulls back 5 documents — three about refund policies and two about shipping times. Context precision would be 3/5 = 0.6, penalizing the irrelevant documents. High context precision means the retriever is pulling precisely what is needed. Low context precision means it is cluttering the context window with noise that can confuse the generator.

**Context Recall** measures whether the retriever found everything it needed to answer the question. If the complete answer requires information spread across three documents but only two were retrieved, context recall captures the gap. Unlike context precision, context recall requires a reference answer to compute — you need to know what a complete answer would look like in order to measure whether all the supporting evidence was gathered.

**Faithfulness** measures whether the generated answer is grounded in the retrieved context. A faithfulness score of 1.0 means every factual claim in the answer can be traced directly to the retrieved documents. Lower scores indicate the model is confabulating — adding information that was not in the retrieved context. This is the most common and dangerous failure mode in RAG systems: the retrieval might have been perfect, but the generator hallucinates anyway.

Technically, Ragas computes faithfulness by: (1) extracting all factual claims from the generated answer, (2) checking each claim against the retrieved context using an LLM, and (3) computing the fraction of claims that are supported. A response with four claims, three of which appear in the context, would score 0.75.

**Answer Relevance** measures whether the generated answer actually addresses the question that was asked. A model might produce a faithfully grounded, coherent response that answers a slightly different question. Ragas computes this by prompting a judge LLM to generate multiple questions that the answer could be responding to, then measuring the cosine similarity between those generated questions and the original question. High similarity means the answer is well-aligned with the intent.

These four metrics form a diagnostic dashboard for RAG systems. Low context precision suggests improving your retrieval strategy or query formulation. Low faithfulness suggests constraining the generator more aggressively (stricter prompting, smaller context windows). Low answer relevance suggests the system is misinterpreting query intent.

> **Important:** The four Ragas metrics were designed around single-channel or 2-channel retrieval (semantic or hybrid BM25 + semantic). They measure aggregate retrieval quality but cannot distinguish *which retrieval channel* failed. As systems move to 4-channel architectures (adding knowledge graph traversal and temporal reasoning), additional per-channel metrics are required — see the section below.

### Evaluating Multi-Channel Retrieval Systems

Production RAG systems increasingly use 4-channel parallel retrieval: BM25 + semantic + knowledge graph traversal + temporal reasoning, fused via Reciprocal Rank Fusion (RRF). Each additional channel introduces new failure modes that Ragas metrics don't surface. Evaluate each channel independently.

**Evaluating knowledge graph retrieval**

Knowledge graph retrieval fails differently from embedding-based retrieval. The failure modes are: (1) entity resolution failure — the query contains entity references that don't match the graph's entity names; (2) traversal dead ends — the graph has the entities but not the required relationship edges; (3) multi-hop precision failure — the traversal finds entities along the path but overshoots (returns entities 3 hops away when the answer is 1 hop away).

Metrics to track:

| Metric | What it measures | How to compute |
|---|---|---|
| **Entity resolution rate** | % of queries where named entities in the query are successfully matched to graph nodes | Label a test set with the expected graph entities; measure match rate |
| **Multi-hop success rate** | % of multi-hop queries where the traversal returns the correct target entities | Requires labeled multi-hop test cases with known target entity sets |
| **Relationship coverage** | % of relationship types in test queries that exist as edges in the graph | Gap analysis: catalog relationship types in test queries, check against graph schema |
| **Graph retrieval precision@K** | Of K graph-retrieved chunks, fraction actually relevant | Same as context precision but computed only on graph-channel results |

Build a labeled multi-hop test set: identify 50–100 queries that require relationship traversal to answer, document the expected traversal path (entity A → [relationship] → entity B → [relationship] → entity C), and verify the graph channel returns the correct terminal entities. If the graph channel has low multi-hop success rate, the issue is almost always graph construction (missing relationship edges) rather than retrieval logic.

**Evaluating temporal retrieval**

Temporal retrieval fails when: (1) the system surfaces older document versions when a newer version exists for the same topic; (2) the system fails to parse temporal intent from implicit signals ("current policy" → wants most recent, not highest embedding similarity); (3) temporal decay weights are miscalibrated for the domain (policy documents decay differently from news articles).

Metrics to track:

| Metric | What it measures | How to compute |
|---|---|---|
| **Version accuracy** | % of recency-sensitive queries where the most recent valid version is retrieved | Label a test set with queries that have multiple document versions; check that newest is returned |
| **Temporal intent recognition rate** | % of queries containing recency signals where the temporal channel fires correctly | Annotate temporal intent in test queries; check channel activation |
| **Staleness rate** | % of retrieved documents older than the domain's acceptable recency threshold | Compute avg document age in retrieved sets for recency-sensitive query types |
| **Temporal decay calibration** | Whether older documents rank systematically lower for recency-sensitive queries | Compare document age vs. rank position across recency queries |

The most practical test: take 20 topics where your corpus contains multiple versions of the same information (policy updates, spec revisions, regulatory amendments). For each topic, issue a "current" or "latest" query and verify the temporal channel returns the most recent version, not the highest-embedding-similarity version (which may be an older document with more comprehensive content).

**Diagnosing 4-channel failures**

When your final answer quality degrades in a 4-channel system, standard Ragas metrics tell you that retrieval failed but not which channel failed. Use this diagnostic sequence:

1. Run the query through each channel independently and score channel-level context precision
2. Check RRF fusion scores — is one channel consistently contributing low-quality results that are still ranked highly because they appear across multiple channels?
3. Check whether the failure correlates with a query type: exact-match failures → BM25 issue; paraphrase failures → semantic issue; relational failures → knowledge graph issue; recency failures → temporal issue
4. Log which channels fire on which queries — a channel that almost never fires may have misconfigured triggering logic (entity extraction failing, temporal intent parsing too conservative)

**The compound failure warning.** In a 4-channel system with RRF fusion, a single malfunctioning channel can degrade results for queries it shouldn't affect at all. A knowledge graph channel returning garbage results for non-relational queries will contaminate the RRF merge with low-quality documents that weren't needed. Implement channel-level quality gates: if a channel's results score below a minimum relevance threshold, exclude them from RRF fusion rather than letting them dilute it.

### The Key Distinction: Retrieval Failure vs. Generation Failure

One of the most valuable aspects of the Ragas framework is that it helps you identify where in the pipeline a failure occurred. If context recall is low but faithfulness is high, your retrieval is incomplete but the generator is behaving responsibly with what it has. If context recall is high but faithfulness is low, your retrieval is working but the generator is hallucinating. If both are high but answer relevance is low, the pipeline is technically functioning but misunderstanding user intent. Disaggregating failures by stage is the difference between "our RAG system is bad" and "our retriever is missing key documents in the medical domain."

---

## 6. Evaluating Agents

Evaluating agentic systems — AI systems that take sequences of actions to accomplish goals — is fundamentally more complex than evaluating single-turn LLM responses. An agent might call tools, search the web, write and execute code, and manage multi-step reasoning chains. The final output is only part of what you need to evaluate.

### Task Completion Rate

The most fundamental agent metric is whether the agent actually accomplished its goal. Task completion rate (also called success rate or task success rate) is the fraction of tasks where the agent reached the intended end state. If you have 100 test tasks and the agent completes 73 correctly, your task completion rate is 73%.

The challenge is defining "completion." For some tasks, success is binary and unambiguous — either the file was created or it was not. For others, completion is graded: a task might be 70% complete if the agent found the right information but formatted it incorrectly, or 90% complete if it accomplished the main goal but missed a secondary requirement.

### Tool Use Accuracy

Agents interact with the world through tools — search APIs, code executors, databases, file systems. Tool use accuracy measures whether the agent called the right tool, with the right arguments, in the right order. A simple task like "look up the current weather and put it in a report" requires: (1) calling the weather API with the right location parameter, (2) parsing the response, (3) writing to the right file or system. Errors can occur at any step.

Tool use evaluation typically looks at: whether the correct tool was selected (tool selection accuracy), whether the arguments were valid (schema compliance), whether the tool call succeeded without runtime errors (execution success), and whether tool calls happened in the correct order when there are dependencies.

### Trajectory Quality

Even when an agent reaches the right destination, the path it took matters. An agent that takes 15 steps to accomplish a 3-step task is less efficient, more expensive to run, and more likely to compound errors along the way. **Trajectory quality** evaluates the sequence of actions the agent took to reach its goal.

Two agents can both succeed at a task while having very different trajectory quality. One might search, reason, take targeted action, verify, and complete. Another might search, hallucinate a dead end, backtrack, search again, try an irrelevant tool call, correct course, and eventually complete — technically a success but operationally fragile and expensive.

Trajectory evaluation can be automated using LLM-as-a-judge: give the judge the task description and the full action log, and ask it to score the efficiency and correctness of the path. Tools like TRAJECT-Bench and AgentBench provide structured frameworks for this evaluation, decomposing trajectories into tool selection correctness, argument quality, and dependency ordering.

### The Challenge of Multi-Step Evaluation

A subtle problem in agent evaluation is error compounding. If an agent makes a small mistake at step 3 of a 10-step task, the error may not become visible until step 7, by which point it is mixed with several subsequent decisions. Diagnosing the root cause requires inspecting the full trace, not just the final output.

This is why agent evaluation requires **tracing** — capturing the complete sequence of inputs, outputs, tool calls, reasoning steps, and state changes at each point in the agent's execution. Without a complete trace, debugging agent failures is nearly impossible.

A practical heuristic for agent evaluation: evaluate at both the step level (did each individual action make sense?) and the task level (did the overall outcome achieve the goal?). Step-level failures that do not cause task-level failures reveal brittleness — the agent got lucky, not good. Task-level failures are more urgent to fix but often require step-level diagnosis to understand why.

### AgentBench and Emerging Benchmarks

The academic community has developed specific benchmarks for agent evaluation. **AgentBench** (ICLR 2024) evaluates LLM agents across 8 distinct environments including web browsing, operating system interaction, database queries, knowledge graphs, and card games. Its key finding: there is a dramatic performance gap between the top commercial models and open-source alternatives — roughly 4.5x difference in average task success (top commercial models ~2.32 vs. open-source ~0.51 on the paper's scoring scale).

**TheAgentCompany** is a more recent benchmark that evaluates agents on "consequential real world tasks" simulating the kinds of tasks an employee at a software company might perform — browsing internal wikis, using web browsers, interacting with simulated colleagues. These environment-grounded benchmarks are closer to real-world utility than synthetic Q&A tasks.

The broader agent evaluation benchmark landscape includes: **IGLU** (interactive grounded language understanding in a 3D environment), **ClemBench** (chat-oriented LLM evaluation using collaborative dialogue games), **ToolBench** (evaluating tool use across thousands of real-world APIs), and **GentBench** (generalist agent evaluation across diverse task types). Each targets a different capability dimension — choosing the right benchmark depends on whether you care about embodied reasoning, dialogue-based collaboration, API tool use, or generalist task performance.

---

## 7. Benchmarks and Leaderboards

Benchmarks are standardized evaluation datasets and protocols that allow researchers and practitioners to compare models on common tasks. They are useful shorthand for capability — "this model scores X on MMLU" communicates something meaningful about its knowledge breadth — but they require careful interpretation.

### Key Benchmarks and What They Measure

**MMLU (Massive Multitask Language Understanding)** tests knowledge breadth across 57 subjects from elementary to advanced professional level — covering STEM, humanities, social sciences, law, medicine, and more. It consists of 15,908 multiple-choice questions. MMLU is often used as a proxy for "how much does this model know?" High MMLU scores indicate a model has absorbed a broad base of human knowledge. It does not test reasoning, creativity, instruction following, or safety.

**HellaSwag** tests commonsense reasoning through sentence completion. Each question presents a short video caption as context and asks the model to select the most plausible continuation from four options. What makes it challenging is that the wrong options are adversarially filtered — they contain words relevant to the context but describe physically or socially implausible scenarios. Modern LLMs score in the 85-95% range; humans score near 95%. HellaSwag tests whether a model understands how the physical and social world works.

**ARC (AI2 Reasoning Challenge)** focuses on science reasoning questions drawn from standardized tests. It comes in two tiers: Easy (questions that simple retrieval models can answer) and Challenge (questions that require deeper reasoning). The Challenge set specifically targets multi-hop reasoning and distributed evidence, where information needed to answer is spread across multiple passages.

**TruthfulQA** specifically targets hallucination resistance. It consists of 817 questions across 38 categories (finance, health, politics, conspiracy theories) where the correct answer is something that models are prone to get wrong — often because popular misconceptions appear frequently in training data. A model that has absorbed internet text without filtering will tend to reflect common falsehoods. TruthfulQA measures whether the model can resist confabulating in these high-risk areas. It also measures informativeness: a model that answers "I don't know" to everything would score poorly despite being technically non-lying.

**HumanEval** tests code generation, specifically functional correctness. The model is given 164 programming problems and must produce code that passes corresponding unit tests. Performance is measured by pass@k — the probability that at least one of k generated samples passes all unit tests. HumanEval is widely cited as a measure of coding capability.

**MT-Bench** (Multi-turn Benchmark) is a set of 80 carefully constructed multi-turn, open-ended questions spanning eight categories: writing, roleplay, extraction, reasoning, math, coding, STEM, and humanities. What makes MT-Bench unique is that it tests instruction-following in a conversational, multi-turn format — closer to how real users interact with chat models. Introduced in the Zheng et al. 2023 paper, it is evaluated using GPT-4 as a judge, which achieves over 80% agreement with human evaluators.

**HELM (Holistic Evaluation of Language Models)**, from Stanford's CRFM group, is the most comprehensive of the standard benchmarks. It measures 7 metrics (accuracy, calibration, robustness, fairness, bias, toxicity, efficiency) across 42 scenarios. Before HELM, models were evaluated on an average of only 17.9% of its core scenarios. HELM improved cross-model comparability by benchmarking 30 prominent models on the same standardized set of tests.

### Chatbot Arena: Human Preference at Scale

Chatbot Arena (from LMSYS) takes a different approach to benchmarking. Rather than fixed questions, it collects real user conversations where two anonymous models respond to the same prompt and users vote for the better response. These pairwise preferences are aggregated into an Elo-style leaderboard (using the Bradley-Terry model for statistical robustness). As of early 2024, Chatbot Arena had collected over 240,000 votes from 90,000+ users across 100+ languages.

The key insight is that Chatbot Arena evaluates models on the actual distribution of queries that users care about — not curated questions designed by researchers. This gives it a different kind of validity than MMLU or HumanEval. A model that is mediocre on academic benchmarks might score highly on the Arena if users find it genuinely useful. Research confirmed that crowdsourced Arena votes "are in good agreement with those of expert raters," validating the approach.

### Why Leaderboards Can Mislead: Benchmark Contamination

Here is a problem that is larger than most practitioners realize: many LLMs have been trained on data that includes the benchmark test sets themselves. Because modern LLMs are trained on massive, largely undocumented scrapes of the public internet — and because benchmark questions are published publicly — benchmark answers frequently end up in training data. This is called **benchmark contamination** or **data leakage**.

The consequences are severe. Research across 51 LLMs found that compared to high performance on HumanEval, there was an average 39.4% drop in performance when using EvoEval (a variant designed to avoid contamination), with decreases ranging from 19.6% to 47.7% — and significant ranking changes between models. A model that scores highly on a contaminated benchmark may be partly memorizing test answers rather than demonstrating generalizable capability.

More insidiously, **leaderboard gaming** is a documented phenomenon. Companies have been found to selectively publish benchmark results from their best-performing model versions while not disclosing results from versions tested under conditions that would rank lower. When a leaderboard becomes commercially important, it attracts gaming — exactly what Goodhart's Law predicts (discussed in Section 10).

The practical implication for practitioners is this: do not select models based primarily on public benchmark scores. A model's MMLU score tells you something about its general knowledge, but it tells you very little about how it will perform on your specific task with your specific users. Always build your own evaluation dataset from real examples in your problem domain, and treat benchmark scores as a rough prior rather than a reliable predictor of production performance.

---

## 8. Evaluation Frameworks and Tools

The ecosystem of evaluation tools has matured rapidly. Here is a practical guide to the major frameworks, what they do, and when to use them.

### Ragas

**What it is**: Open-source Python library specifically designed for evaluating RAG pipelines. Provides the four core metrics (context precision, context recall, faithfulness, answer relevance) plus additional metrics for end-to-end RAG evaluation.

**Best for**: Any system using retrieval-augmented generation. If you are building a knowledge base chatbot, a document Q&A system, or any application where the LLM answers from retrieved context, Ragas is the most purpose-built tool for the job.

**How it works**: Ragas uses LLM-as-a-judge internally for metrics that require semantic judgment (faithfulness, answer relevance). It can be used without reference data for most metrics, which is useful when you do not have ground truth answers. Context recall is the exception — it requires a reference answer to compute.

**Integration**: Works with LangChain, LlamaIndex, and most Python-based RAG stacks. Can integrate with Langfuse and LangSmith for observability.

### DeepEval

**What it is**: Open-source, Pytest-compatible evaluation framework from Confident AI. Provides 15+ pre-built metrics and a unit-testing workflow for LLM applications.

**Best for**: Teams that want evaluation integrated into their development workflow — not just a standalone tool, but something that runs in CI/CD like automated tests. The Pytest integration means you can write evals that fail a build when quality drops below a threshold.

**How it works**: Most DeepEval metrics use LLM-as-a-judge internally, with the G-Eval approach (LLM generates evaluation criteria, then scores against them). Metrics include hallucination, faithfulness, answer relevancy, contextual precision/recall, bias, toxicity, and summarization quality.

**Distinctive feature**: The hallucination metric is subtly different from faithfulness. Faithfulness checks whether the response is grounded in retrieval context. Hallucination checks whether the response contradicts real-world facts — a distinction that matters when you want to catch model confabulation regardless of what was retrieved.

### Braintrust

**What it is**: Commercial observability and evaluation platform with a strong focus on the eval development workflow. Supports dataset management, experiment tracking, CI/CD integration, and LLM-as-a-judge scoring.

**Best for**: Teams that want an integrated evaluation platform — one tool that handles dataset curation, offline eval, production monitoring, and regression tracking. Braintrust provides a full loop from "run an experiment" to "track how quality changes over time."

**How it works**: You define datasets (input/output pairs or inputs only), write scoring functions (code-based or LLM-based), and run experiments. Results are versioned and tracked, so you can compare model A to model B, or prompt v1 to prompt v2. Supports A/B testing by routing production traffic to experimental variants and logging both responses.

**Distinctive feature**: The dataset management and experiment tracking layer. Braintrust treats evaluation as an engineering discipline — every eval run is reproducible, versionable, and comparable to historical results.

### Promptfoo

**What it is**: Open-source CLI tool for evaluating and red-teaming LLM applications. Supports declarative YAML-based test configuration and comparisons across 50+ model providers.

**Best for**: Security-conscious teams, prompt engineers, and developers who want to evaluate multiple models or prompts in parallel with minimal code. Also the leading open-source tool for automated red-teaming.

**How it works**: You define test cases in YAML (or JSON), specify multiple model providers and prompts to compare, and Promptfoo runs all combinations and scores the outputs. For red-teaming, it generates 50+ types of adversarial inputs automatically using configurable plugins.

**Distinctive feature**: Red-teaming capabilities. Promptfoo can automatically generate jailbreak attempts, prompt injections, and adversarial inputs to stress-test your application's safety guardrails — making it valuable both for quality evaluation and security assessment.

### LangSmith

**What it is**: Evaluation, tracing, and observability platform from LangChain. Tightly integrated with the LangChain ecosystem but usable independently.

**Best for**: Teams already using LangChain or LangGraph. LangSmith provides seamless tracing of chain and agent execution, with evaluators that can score individual steps or full trajectories.

**How it works**: LangSmith captures full traces of every LLM call, tool use, and reasoning step. You can define evaluators that score individual runs or pairwise comparisons. Offline evaluation runs against curated datasets; online evaluation continuously scores production traffic. Agent evaluation captures the full trajectory of multi-step agentic behavior.

**Distinctive feature**: The depth of integration with LangChain's agent ecosystem. If you are building LangGraph-based agents, LangSmith gives you trace-level visibility that is difficult to replicate with other tools.

### OpenAI Evals

**What it is**: Open-source evaluation framework and benchmark registry from OpenAI. Includes both a framework for building custom evals and a community registry of contributed benchmarks.

**Best for**: Teams building on OpenAI models who want to run structured evaluations using the same infrastructure OpenAI uses internally. Also useful for contributing to or running community benchmarks.

**How it works**: Evals are defined by a task (what to test), a data source (test inputs), and a grader (how to score). Graders can be code-based (exact match, regex, custom Python) or model-based (using GPT-4 as a judge). Evals can be run via the CLI or via the OpenAI API dashboard.

**Distinctive feature**: The community registry. OpenAI Evals includes hundreds of contributed benchmark tasks, making it easy to run your model against established tests in specific domains.

### How to Choose

The right tool depends on what you are building and where you are in your evaluation maturity:

| Situation | Recommended Tool |
|-----------|-----------------|
| Building a RAG system | Ragas for core metrics; LangSmith if LangChain-based |
| Want CI/CD-integrated tests | DeepEval (Pytest-native) |
| Want a full platform (dataset mgmt + experiments + monitoring) | Braintrust |
| Need red-teaming / adversarial testing | Promptfoo |
| Building on LangChain / LangGraph | LangSmith |
| Building on OpenAI models | OpenAI Evals |
| Just starting out | Ragas or DeepEval (both are open-source and well-documented) |

---

## 9. Evaluation in Production

Offline evaluation against curated datasets is necessary but not sufficient. Models interact with a constantly shifting distribution of real user inputs that no test set can fully anticipate. Production evaluation is the practice of continuously measuring quality on live traffic.

### What to Log

The foundation of production evaluation is comprehensive logging. Every interaction with your AI system should produce a structured trace that includes:

- The full input (user message, system prompt, retrieved context for RAG, tool definitions for agents)
- The full output (model response, tool calls made, reasoning traces)
- Operational metadata: latency, token counts, cost, model version, prompt version
- Session context: user identifier (anonymized), session ID, application component

The reason for capturing all of this — including prompts and retrieved context — is that many quality failures are only diagnosable when you have the full picture. An incorrect response might look mysterious in isolation but become obvious when you see the retrieval context that informed it.

OpenTelemetry is emerging as the standard for instrumenting LLM applications. It provides a vendor-neutral way to capture traces that can be shipped to Langfuse, LangSmith, Braintrust, or any other observability backend.

### Online Metrics

With comprehensive logs in place, you can apply evaluation functions continuously to production traffic. A healthy monitoring stack captures:

**Quality metrics**: Automated scores from LLM-as-a-judge or code-based evaluators applied to sampled production outputs. You cannot score everything at full LLM-judge cost, so sample intelligently — prioritize high-value user segments, newly deployed features, and queries that look unusual.

**User satisfaction signals**: Thumbs-up/down ratings, task completion indicators (did the user rephrase the query immediately, suggesting the first answer was insufficient?), follow-up clarifying questions, session abandonment. These are noisy but capture real user experience.

**Operational metrics**: Latency (p50, p95, p99), cost per query, token usage, error rates, retry rates. These matter as much as quality — a highly accurate but slow or expensive system is not production-viable.

**Safety signals**: Toxicity classifier scores, rates of policy violation flags, user reports of problematic content.

### Drift Detection

AI systems degrade over time even without code changes, because the world changes. New products are released, terminology evolves, user behavior shifts, and the distribution of incoming queries drifts away from what your system was evaluated on. Without active monitoring, this degradation is invisible until it becomes severe.

Drift detection means tracking your quality metrics over time and alerting when they drop outside expected ranges. The most common cause of drift is distribution shift: users start asking questions in new ways, or about new topics, that your system handles poorly. A spike in "I don't know" responses, a drop in faithfulness scores, or a rise in user-reported errors are all signals of potential drift.

The response to detected drift is to: collect representative examples of the new failing cases, add them to your offline eval dataset, diagnose the failure pattern, fix it (via prompt engineering, retrieval improvements, fine-tuning, or routing), and re-evaluate.

### Sampling Strategies for Production Scoring

You cannot score every production interaction through an LLM judge — the cost and latency of doing so at scale makes it impractical. Smart sampling is essential:

- **Random sampling**: Score a random 1-5% of all traffic for baseline quality monitoring.
- **Stratified sampling**: Ensure coverage across different query types, user segments, and application features — do not let sampling concentrate on your most common (and likely well-handled) query types.
- **Anomaly-triggered sampling**: When automated signals detect something unusual (unusually long responses, high latency, user immediately rephrasing), score those traces at higher priority.
- **Failure-focused sampling**: Automatically score all traces that trigger a downstream failure signal (negative user feedback, error, session abandonment).

This tiered approach means your expensive LLM-judge evaluation budget is spent on the traces that most need it.

### Feedback Loops

User feedback, when properly collected, is one of the most valuable signals you have. Explicit feedback (thumbs-up/down, star ratings, text corrections) is high signal but rare — most users do not rate responses. Implicit feedback (did the user rephrase the query? did they ask a follow-up that indicates confusion? did they abandon the session?) is lower signal but more abundant.

Both types of feedback should be linked back to the original trace, so you can see exactly what input and output generated the feedback. A negative rating on a response tells you very little by itself; a negative rating linked to the full conversation context, the retrieved documents, and the model's reasoning tells you what went wrong.

The most productive use of negative feedback is as a source of new eval cases. Every user who signals dissatisfaction is pointing you toward a failure mode your offline eval suite did not cover. Collect those traces, analyze the pattern, add representative examples to your dataset, and measure whether your next iteration fixes them. This is the core of the flywheel (Section 11).

---

## 10. Common Failure Modes

The history of LLM evaluation is full of patterns where teams believed they had good systems because their metrics looked good — until real users revealed something very different. Understanding these failure modes is as important as understanding the correct techniques.

### Goodhart's Law: When Metrics Become Targets

Goodhart's Law states: "When a measure becomes a target, it ceases to be a good measure." This principle — originally from economics — applies to AI evaluation with alarming precision.

Here is how it plays out in practice. A team decides to optimize for ROUGE scores on their summarization model. ROUGE measures how many words from the reference summary appear in the generated summary. A clever model learns that it can maximize ROUGE scores by including lots of reference words — even at the expense of coherence, conciseness, and usefulness. The metric goes up; quality goes down.

The same pattern applies at the benchmark level. As Chatbot Arena became commercially significant, companies began running many private model versions in the Arena and publishing only the best-performing results. This is the classic Goodhart move: the metric (Arena Elo rating) stopped being a reliable measure of quality because it became a target to optimize. Research explicitly documented this, noting that "large companies like Meta, OpenAI, Google and Amazon were able to privately pit many model versions in the Arena and then only publish the best results."

The defense against Goodhart's Law is twofold: use multiple metrics that are hard to game simultaneously (so that gaming one causes another to decline), and periodically re-ground your automated metrics against human judgment on your real task.

### Benchmark Contamination

As discussed in Section 7, the most widely used benchmarks suffer from a fundamental problem: the models that score highest on them may have been trained on data that includes the benchmark answers. This is not necessarily intentional — it is an artifact of training on internet text at scale — but it means that benchmark scores overstate true capability.

The contamination problem is worse than it looks because it is hard to detect. A model might score 87% on MMLU not because it can reason across 57 domains, but because it has memorized answers to MMLU questions encountered during pre-training. The genuine measure of knowledge generalization — the model's ability to answer new questions in those domains — might be considerably lower.

For practitioners, the implication is to treat public benchmark scores as useful priors rather than definitive measurements, and to always validate on your own held-out test set.

**LiveBench** represents one approach to addressing contamination: a benchmark where questions are generated fresh each month from new source material, with older questions retired and made public. By constantly rotating the question set, it prevents models from memorizing answers during pre-training. This design philosophy — fresh, unpublished tests on a rolling basis — is likely the direction the field moves as contamination becomes harder to ignore.

### Metric Gaming: High Score, Low Quality

Related to Goodhart's Law but worth naming separately: it is remarkably easy to produce AI outputs that score well on automated metrics while failing completely at the underlying task.

BLEU is the canonical example. A machine translation system that copies the reference translation word-for-word (somehow having access to it) would score 1.0 on BLEU. An LLM trained with BLEU as a reward signal learns to produce outputs that overlap maximally with references — which often means verbose, repetitive, safe-sounding text rather than accurate, incisive answers.

The same pattern occurs with LLM judges. If your judge evaluator is not properly calibrated, a model can learn to produce outputs that the judge likes — even if those outputs would not satisfy real users. Verbosity bias is a prime example: a model that learns to pad its responses with confident-sounding qualifications may score higher on a naive judge while delivering worse user experience.

The detection method is human spot-checking. Periodically sample outputs that scored highly on your automated metrics and have a human evaluate them. If you find cases where high automated scores correlate with low human satisfaction, your evaluator has been gamed or miscalibrated.

### LLM Judge Biases

Covered in detail in Section 4, but worth restating as a failure mode: using LLM-as-a-judge without accounting for position bias, verbosity bias, and self-enhancement bias will produce systematically distorted evaluations. A common mistake is to use GPT-4 to judge GPT-4 outputs without any safeguards — the self-enhancement bias alone will produce scores that overstate quality.

### The "Vibe Check" Trap

Perhaps the most common and costly failure mode in AI evaluation is not a methodological error but a process failure: evaluating AI outputs by intuition rather than systematic measurement.

The vibe check trap works like this. A PM or engineering lead watches a demo, tries the system on a few queries, and decides it seems good. Maybe they share it with a few colleagues who also think it seems good. The team ships it. Then, in production, it fails on the query types that nobody thought to test. Or it degrades slowly over two weeks after a prompt change that seemed fine in the demo.

Hamel Husain puts the antidote clearly: "Spend 30 minutes manually reviewing 20-50 LLM outputs whenever you make significant changes." This is not about the 30 minutes of manual review — it is about making manual review a disciplined habit rather than an occasional gut check, and then building automated evaluators that are calibrated against those manual labels.

The vibe check trap is particularly dangerous for AI systems because they exhibit **capability illusion** — the phenomenon where a system performs impressively on demonstrations (which are selected to showcase strengths) but fails at rates that are not apparent from casual use. Systematic evaluation is the only reliable way to measure what is actually happening.

### Eval Dataset Leakage

A subtler failure mode that mirrors benchmark contamination at the product level: your evaluation dataset itself can become contaminated by your training or fine-tuning data. If you collect user examples to fine-tune your model, and some of those examples overlap with your eval set, your offline eval scores will be inflated — the model has effectively memorized the answers to its own tests.

The standard defense is a strict train/eval split: any data used for fine-tuning or in-context learning must be excluded from evaluation datasets. This sounds obvious but requires active enforcement. When your training and eval datasets are curated from the same source (production logs), it is easy to accidentally overlap. Keep them in separate systems with explicit exclusion logic.

### Sycophancy in Evaluation

There is an additional failure mode specific to using AI judges: sycophancy. An LLM judge, like any LLM, may be inclined to rate confident-sounding responses more favorably than tentative-sounding ones — even when confidence does not correlate with accuracy. A response that says "The answer is definitively X" will score higher than "The evidence suggests X, though there is some uncertainty," even if the second response is more epistemically calibrated.

This creates a perverse incentive: if your system is optimized against an LLM judge, it may learn to sound confident and authoritative to please the judge, while the underlying answer quality stagnates or declines. The mitigation is to build evaluation rubrics that explicitly reward calibration — penalizing responses that express high confidence on genuinely uncertain topics — and to validate your judge against expert human annotators on exactly these edge cases.

---

## 11. Building Your First Eval Suite: A Practical Path

Most teams starting with evaluation face a version of the same problem: they know they need evals, they have heard the frameworks and read the theory, but they do not know where to begin. Here is a practical sequence for getting started without getting paralyzed.

### Step 1: Define the Task and Its Failure Modes

Before writing a single line of eval code, spend an hour with a domain expert — ideally someone who deeply understands the users — answering two questions: What does the system need to do well? And what does failure look like?

For a customer support chatbot, success might mean: accurate policy information, empathetic tone, actionable next steps, and no fabricated information. Failure might mean: wrong policy cited, dismissive tone, or a hallucinated process that does not exist. These are your evaluation criteria. Write them in plain English before reaching for a framework.

### Step 2: Collect 50-100 Real Examples

If you have any production traffic, sample 50-100 real conversations that span the range of what users actually ask. If you are pre-launch, generate representative examples by having team members role-play as users across different scenarios — common cases, edge cases, and the queries you are most worried about.

Do not over-engineer this step. You do not need a perfectly curated dataset. You need a realistic dataset.

### Step 3: Manual Review with a Rubric

Have a domain expert review all 50-100 examples and label each one: pass, fail, or borderline. Document the specific reason for each failure. This manual step is not optional and cannot be shortcut — it is the foundation that everything else is calibrated against.

This labeling exercise typically surfaces 3-7 common failure modes. These are your priority evaluation targets.

### Step 4: Build Binary Automated Evals for Each Failure Mode

For each failure mode, build one binary evaluator. A binary evaluator answers "did this response exhibit this specific failure?" with a simple yes/no (0 or 1). Binary evaluators are dramatically more useful than scaled scores (1-5) because:

- Agreement with human raters is easier to achieve on a binary decision
- A failed evaluation clearly signals "this needs fixing"
- You can set meaningful pass-rate thresholds (e.g., "hallucination fails less than 2% of the time")

Use LLM-as-a-judge for failure modes that require semantic judgment (hallucination, tone, policy accuracy). Use code-based logic for failure modes that can be checked programmatically (response length, required fields present, links are valid).

### Step 5: Validate Against Your Manual Labels

Run your automated evaluators against the examples you labeled manually in Step 3. Compare the automated results to your human labels. If your LLM judge disagrees with human labels more than 20% of the time, the evaluator is not ready — iterate on the judge prompt, scoring criteria, or few-shot examples until agreement is acceptable.

This calibration step is what separates reliable automated eval from noisy automated eval. It is also where most teams stop doing it — do not skip it.

### Step 6: Integrate Into Development Workflow

Once your evaluators are calibrated, run them automatically after every prompt change, model update, or major configuration change. Treat a drop in pass rate below your threshold as a failed build — do not ship until it is fixed. This is the offline eval → development loop.

### Step 7: Deploy Monitoring and Log to Your Eval Set

As your system accumulates production traffic, route a sample through your evaluators continuously. Every time the system fails in production (user reports an issue, a flagged interaction, a negative feedback signal), add it to your eval dataset. Your eval suite should grow with your product.

---

## 12. The Evaluation Flywheel

The goal of evaluation is not to produce a one-time score. It is to create a continuous improvement loop where every failure discovered in production leads to a better system. This is the evaluation flywheel — and getting it turning is the difference between teams that improve systematically and teams that whack-a-mole their way through one production fire after another.

### How the Flywheel Works

The flywheel has five stages that feed into each other continuously:

**Stage 1: Production monitoring.** You instrument your live system to capture full traces of every interaction. Automated scoring functions run on sampled traffic. User feedback signals are collected. Drift alerts fire when quality metrics drop.

**Stage 2: Failure collection.** When monitoring surfaces a problem — a spike in low faithfulness scores, a cluster of negative user feedback, a failed edge case — you collect the specific examples. Not just the final output, but the full trace: input, context, reasoning, output.

**Stage 3: Root cause analysis.** You examine the failure cases. What patterns do they share? Is the retriever pulling irrelevant documents? Is the generator ignoring the retrieved context? Is the prompt ambiguous for a particular query structure? Is the model hallucinating on a specific topic domain?

**Stage 4: Test case creation.** You add the representative failure examples to your offline evaluation dataset. This is critical: production failures become permanent test cases. Every bug you fix is codified as a test that will catch regression if the same bug reappears.

**Stage 5: Fix, evaluate, deploy.** You implement a fix — better retrieval, improved prompt, fine-tuning, guardrail — and run it against the full offline eval suite, including all the new test cases from production failures. If the fix passes, you deploy it using shadow mode and canary rollout. Return to Stage 1.

### Why It Compounds

Each cycle of the flywheel makes the next cycle faster and more effective. Your eval dataset grows with each production failure you encounter, so your offline evaluation becomes more representative of what real users actually ask. Your evaluators become better calibrated because you are constantly re-grounding them against human labels on real examples. Your understanding of your system's failure modes deepens, so your monitoring becomes more targeted.

Hamel Husain describes the compound effect clearly: "The eval flywheel compounds, with each cycle improving both your system and your ability to evaluate your system." Teams that invest in the flywheel early accumulate a systematic advantage: they know their failure modes, have test coverage for them, and can ship improvements with confidence that they are not introducing regressions.

### Evaluation-Driven Development

The flywheel idea connects to a broader practice called **Evaluation-Driven Development (EDD)** — the AI-era analog of test-driven development. In EDD, you write evaluation cases before making changes to your system. If you are changing your retrieval strategy, you first add test cases that represent the query types you expect to improve. If you are changing your prompt, you first add test cases for the failure modes you are trying to fix.

The discipline of writing evals before shipping changes forces you to articulate what "better" means in concrete, measurable terms. It prevents the pattern where a change that solves one problem inadvertently breaks three others — because the regression is caught by the existing eval suite before deployment.

DoorDash has documented one of the more detailed public accounts of this approach, describing their "simulation and evaluation flywheel" for their LLM chatbots. The pattern: collect production failures, simulate them, measure, fix, re-evaluate — and the cycle compounds into systematic improvement.

---

## 13. Key Takeaways

**Evaluation is a product discipline, not just a research tool.** The question is not "how good is this model?" but "does this system solve the user's task accurately, safely, and consistently?" Public benchmark scores are useful priors; your own eval dataset, built from real user failures, is the only reliable signal.

**Start with manual review, build automated evals on top.** Hamel Husain's process: manually label 100+ real conversations, identify the most common failure modes, build binary pass/fail LLM-judge evaluators for those failure modes. Automated evals are only trustworthy if they are calibrated against human labels on your actual data.

**Use the right method for the right question.** Reference-based eval catches objective errors efficiently. LLM-as-a-judge scales subjective evaluation at reasonable cost — but only with bias mitigations (position randomization, ensemble judges, binary criteria). Human eval is for calibration and high-stakes decisions. A/B testing in production is the only way to measure real user impact.

**For RAG systems, evaluate retrieval and generation separately.** Low faithfulness is a generation problem. Low context recall is a retrieval problem. Low context precision is a retrieval signal-to-noise problem. Conflating these obscures the true failure source and directs you toward the wrong fix.

**For agent systems, evaluate at both step level and task level.** Task completion rate measures outcomes; tool use accuracy and trajectory quality diagnose the path. A successful outcome via a poor-quality trajectory signals brittleness, not robustness.

**The evaluation flywheel is your compounding advantage.** Production failures → test cases → fixed → deployed → production failures. Each cycle improves your system and your ability to evaluate it. Teams that invest early build an ever-growing moat of documented failure modes and coverage.

**Goodhart's Law will find you.** Any metric you optimize for will eventually be gamed — by your model, your team, or the benchmark ecosystem. Run multiple evaluation methods in parallel. Periodically re-ground all automated metrics against fresh human labels. Treat any metric that consistently improves while user satisfaction stays flat as a red flag, not a success.

---

## 14. Sources

1. [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena — Zheng et al., 2023](https://arxiv.org/abs/2306.05685) — The foundational paper on LLM-as-a-judge methodology, introducing MT-Bench and documenting GPT-4's >80% human agreement rate and key judge biases.

2. [Holistic Evaluation of Language Models (HELM) — Liang et al., Stanford CRFM, 2022](https://arxiv.org/abs/2211.09110) — Introduced the HELM benchmark framework measuring 7 metrics across 42 scenarios for 30 models; established cross-model evaluation comparability.

3. [Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference — LMSYS, 2023/2024](https://arxiv.org/html/2403.04132v1) — Describes the crowdsourced Elo rating approach, with 240,000+ votes validating human preference evaluation at scale.

4. [Ragas Documentation — docs.ragas.io](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/) — Official documentation for the Ragas RAG evaluation framework, covering context precision, context recall, faithfulness, and answer relevance metrics.

5. [DeepEval Documentation — deepeval.com](https://deepeval.com/docs/metrics-introduction) — Documentation for DeepEval's 15+ metrics, G-Eval approach, and LLM-as-a-judge implementation for hallucination and faithfulness.

6. [LLM Evals: Everything You Need to Know — Hamel Husain, hamel.dev](https://hamel.dev/blog/posts/evals-faq/) — Comprehensive practitioner guide from one of the field's most experienced eval practitioners; covers process, common mistakes, and binary pass/fail evaluator design.

7. [Your AI Product Needs Evals — Hamel Husain, hamel.dev](https://hamel.dev/blog/posts/evals/) — Practical argument for why evals are essential and how to build them, with the 4-step process from manual labeling to automated judges.

8. [Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge](https://arxiv.org/html/2410.02736v1) — Research paper quantifying verbosity, position, and sentiment biases in LLM judge models with mitigation strategies.

9. [LLM Red Teaming Guide — Promptfoo](https://www.promptfoo.dev/docs/red-team/) — Documentation for open-source automated red-teaming, covering 50+ vulnerability types and adversarial input generation.

10. [LangSmith Evaluation Documentation — LangChain](https://docs.langchain.com/langsmith/evaluation) — LangSmith's evaluation framework covering offline dataset eval, online production scoring, and agent trajectory evaluation.

11. [Braintrust LLM Evaluation Metrics Guide](https://www.braintrust.dev/articles/llm-evaluation-metrics-guide) — Commercial platform's guide to eval methodology, dataset management, experiment tracking, and A/B testing for LLM systems.

12. [OpenAI Evals Framework — GitHub](https://github.com/openai/evals) — OpenAI's open-source evaluation framework and benchmark registry; includes code-based and model-based grading approaches.

13. [Evaluation and Benchmarking of LLM Agents: A Survey — arxiv.org, 2025](https://arxiv.org/html/2507.21504v1) — Survey covering agent evaluation frameworks, task completion metrics, and trajectory quality assessment.

14. [Pitfalls of Evaluating Language Models with Open Benchmarks — arxiv.org, 2025](https://arxiv.org/html/2507.00460) — Research on benchmark contamination and leaderboard gaming, including the 39.4% average performance drop on uncontaminated benchmarks.

15. [What is LLM Monitoring? — Langwatch](https://langwatch.ai/blog/what-is-llm-monitoring-(quality-cost-latency-and-drift-in-production)) — Overview of production LLM monitoring covering latency, cost, drift detection, and feedback loop implementation.

16. [A Simulation and Evaluation Flywheel to Develop LLM Chatbots — DoorDash Engineering](https://careersatdoordash.com/blog/doordash-simulation-evaluation-flywheel-to-develop-llm-chatbots-at-scale/) — Real-world case study of a production evaluation flywheel from DoorDash's AI team.

17. [LLM Benchmarks: MMLU, HellaSwag, and Beyond — Confident AI](https://www.confident-ai.com/blog/llm-benchmarks-mmlu-hellaswag-and-beyond) — Practical guide to major benchmarks, what they measure, and their limitations.

18. [Anthropic Model Card and Red Teaming — Anthropic](https://www.anthropic.com/claude-2-model-card) — Anthropic's transparency documentation on model evaluation, red teaming methodology, and safety measurement using Constitutional AI.

---

## 15. Eval-Driven Development (EDD) Framework

**Adapted from [everything-claude-code](https://github.com/affaan-m/everything-claude-code)**

Eval-Driven Development is a discipline where **evals are written BEFORE implementation**, and every change is validated against those evals. It's the AI equivalent of Test-Driven Development (TDD).

### The EDD Workflow

```
Step 1: DEFINE SUCCESS CRITERIA
├─ What does "done" look like?
├─ Write eval rubric (3-5 specific criteria)
└─ Create test dataset (10-20 examples)
   Example: Feature Implementation
   ├─ "Passes all unit tests"
   ├─ "No type errors"
   ├─ "Performance < 100ms"
   └─ "Code complexity score < 10"

Step 2: BASELINE (Optional)
├─ Run evals on current system (if it exists)
├─ Record baseline scores
└─ Understand "how bad is the problem?"

Step 3: IMPLEMENT
├─ Build feature/fix
├─ Run evals continuously (not just at end)
└─ Get signal immediately when regression happens

Step 4: ITERATE
├─ If evals fail → diagnose and fix
├─ If evals improve → commit and continue
└─ If stuck after 2 iterations → escalate

Step 5: REVIEW & MERGE
├─ Final eval run: confirm criteria met
├─ Compare to baseline: measure improvement
└─ Merge only if all evals pass
```

### EDD vs. Traditional Development

| Aspect | Traditional | EDD |
|---|---|---|
| **When evals are written** | After implementation (if at all) | Before implementation |
| **Eval frequency** | Rarely, before release | Continuously during implementation |
| **Signal quality** | Late (found issues after code written) | Early (issues caught as they appear) |
| **Code confidence** | Low (untested until late) | High (validated constantly) |
| **Iteration cost** | High (rework late in cycle) | Low (caught and fixed early) |

### Example: EDD for a Summarization Feature

**Step 1: Define Evals**

```python
evals = {
    "summary_length": {
        "criterion": "Summary is 50-200 words",
        "check": lambda summary: 50 <= len(summary.split()) <= 200,
        "weight": 0.2
    },
    "contains_key_points": {
        "criterion": "Summary mentions all 3+ key points from source",
        "check": lambda summary, source: has_key_points(summary, source),
        "weight": 0.3
    },
    "readability": {
        "criterion": "Flesch reading ease > 60 (readable)",
        "check": lambda summary: flesch_kincaid(summary) > 60,
        "weight": 0.2
    },
    "factuality": {
        "criterion": "No claims contradict source (factual accuracy > 0.9)",
        "check": lambda summary, source: factuality_score(summary, source) > 0.9,
        "weight": 0.3
    }
}

test_cases = [
    ("source1.txt", "reference_summary1.txt"),
    ("source2.txt", "reference_summary2.txt"),
    # ... 10-20 total
]
```

**Step 2: Baseline**

If you have an existing summarizer:
```
Run evals on current implementation:
├─ Length: 0.95 (95% of summaries in range)
├─ Key points: 0.72 (72% contain required points)
├─ Readability: 0.68
├─ Factuality: 0.85
└─ Weighted score: 0.80
```

**Step 3: Implement + EDD Loop**

```
Attempt 1: Initial implementation
├─ Run evals
├─ Score: 0.62 (worse than baseline!)
├─ Issue: "Key points score is 0.40 (dropped from 0.72)"
└─ Action: Analyze failure cases, fix

Attempt 2: Improved logic
├─ Run evals
├─ Score: 0.75 (getting closer)
├─ Issue: "Factuality is 0.78, target is 0.90"
└─ Action: Add fact-check step

Attempt 3: With fact-checking
├─ Run evals
├─ Score: 0.85 (matches baseline!)
├─ Issue: None critical
└─ Action: Ready for review
```

**Step 4: Review**

Human reviews:
- Did quality improve? (0.80 → 0.85 ✓)
- Any regressions? (No ✓)
- Code quality OK? (Yes ✓)
→ Merge

### Key EDD Disciplines

**1. Eval Early & Often**

Don't wait until "implementation is done." Run evals after every meaningful change:
- After first skeleton → catches obvious failures
- After every feature add → prevents regression
- Before every commit → gate quality

**2. Prioritize High-Signal Evals**

Not all evals are equal. Focus on the 3-5 that correlate with actual quality:
```
High-signal:
├─ Passes test cases with known right answers
├─ Doesn't crash or timeout
├─ Matches success criteria

Low-signal:
├─ "Code is elegant" (subjective)
├─ "I like this" (opinion)
├─ Generic performance metrics (often noisy)
```

**3. Understand Failure Modes**

When eval fails, diagnose the root cause:
```
Eval: "Factuality > 0.9" fails with score 0.75
└─ Root cause could be:
   ├─ Model hallucinating new facts (prompt issue)
   ├─ Not enough source context (context issue)
   ├─ Fact-checker is too strict (eval issue)
   └─ Source is ambiguous (data issue)
   
Different root cause → different fix
```

**4. Gate Merges**

Only merge if evals pass:
```
Merge checklist:
├─ [ ] All custom evals pass (≥ threshold)
├─ [ ] No regression vs. baseline
├─ [ ] Code review approved
└─ [ ] Tests pass
```

### EDD Cost vs. Benefit

Cost:
- Writing evals: 2-3 hours per feature
- Running evals: 30-60 seconds per iteration
- Total per feature: 4-6 hours

Benefit:
- Catches regressions immediately (vs. days/weeks later)
- Prevents shipping low-quality features
- Enables confident refactoring
- Builds eval suite for future validation
- ROI: Pays for itself on 2nd similar feature

---

## 16. Agent Quality Metrics & Observability

**Adapted from [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide) by Florian Bruniaux**

Evaluating AI agents requires metrics beyond traditional code quality. This section defines four metric categories, implementation patterns, and observability strategies for custom agents.

### Four Metric Categories

#### 1. Response Quality
Measures accuracy, relevance, and usefulness of agent outputs.

**Metrics**:
- Accuracy: % of outputs that are factually correct
- Relevance: % of outputs that address the user's request
- Coherence: % of outputs that are logically structured
- Completeness: % of requests fully resolved without escalation

**Tools**: LLM-as-judge, human review, automated tests

#### 2. Tool Usage
Tracks how effectively agents use available tools.

**Metrics**:
- Tool selection accuracy: % of correct tool choices for task
- Parameter correctness: % of correct arguments passed to tools
- Error recovery: % of errors handled gracefully (vs. failures)
- Tool latency impact: Agent response time with/without tools

**Example**: For a database query agent, measure:
- % of queries using indices (vs. full table scans)
- % of queries returning expected result set size
- % of queries completing within SLA

#### 3. Performance
Measures operational efficiency.

**Metrics**:
- Latency: Response time (p50, p95, p99)
- Token efficiency: Tokens used per task (input + output)
- Cost per task: API cost / successful completion
- Throughput: Requests processed per unit time

**JSON Schema**:
```json
{
  "performance": {
    "latency_ms": 1250,
    "tokens": {
      "input": 450,
      "output": 320,
      "total": 770
    },
    "cost_usd": 0.0035,
    "throughput": "240 req/min"
  }
}
```

#### 4. User Satisfaction
Captures real-world user feedback.

**Metrics**:
- Satisfaction score: 1-5 rating of response quality
- Resolution rate: % of requests resolved on first try
- Escalation rate: % of requests requiring human intervention
- Return rate: % of users who interact with agent again

### Implementation Patterns

#### Pattern 1: Logging Hooks

Instrument the agent to log metrics on every interaction:

```python
# In your agent's tool-call handler
import json
from datetime import datetime

def log_metric(agent_name, task, tool_name, success, latency_ms, tokens):
    metric = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "task": task,
        "tool": tool_name,
        "success": success,
        "latency_ms": latency_ms,
        "tokens": tokens
    }
    with open(f"logs/{agent_name}-metrics.jsonl", "a") as f:
        f.write(json.dumps(metric) + "\n")

# Usage
log_metric("analytics_agent", "revenue_analysis", "sql_query", True, 1250, 770)
```

#### Pattern 2: A/B Testing

Compare two agent versions on the same tasks:

```
Version A (baseline): Current implementation
Version B (candidate): New prompt, tools, or logic

Split traffic: 50% A, 50% B
Measure: Accuracy, latency, cost, satisfaction
Statistical significance: p < 0.05 before rollout
```

#### Pattern 3: Feedback Loops

Collect human feedback to refine metrics:

```
User rates agent response: 👍 Helpful / 👎 Not helpful
→ Log feedback with metrics from that interaction
→ Analyze: Which agent configurations lead to 👍?
→ Retrain/reprompt agent based on patterns
```

#### Pattern 4: Continuous Monitoring

Dashboard showing real-time metrics:

```
Agent: Payment Processing Agent
├─ Uptime: 99.8%
├─ Avg Response Time: 1.2s
├─ Accuracy: 98.5%
├─ Cost/Task: $0.042
└─ User Satisfaction: 4.3/5.0 (1,247 ratings)

Alerts triggered when:
├─ Accuracy drops >5%
├─ Response time >2s (p95)
├─ Cost/task increases >10%
└─ Satisfaction <4.0
```

### Example: Analytics Agent Evaluation

**Agent**: Analyzes customer data and generates insights

**Metrics Setup**:
```json
{
  "agent": "analytics_agent",
  "eval_metrics": {
    "response_quality": {
      "accuracy": 0.95,
      "relevance": 0.92,
      "coherence": 0.94
    },
    "tool_usage": {
      "correct_sql_queries": 0.89,
      "query_optimization": 0.82
    },
    "performance": {
      "latency_p50_ms": 850,
      "tokens_per_task": 620,
      "cost_usd": 0.031
    },
    "satisfaction": {
      "user_rating": 4.4,
      "resolution_rate": 0.91
    }
  }
}
```

**Monitoring**:
```bash
# Run daily eval job
analytics_agent_eval.sh

# Output CSV for trending
date,accuracy,latency_ms,cost_usd,satisfaction
2026-03-07,0.95,850,0.031,4.4
2026-03-08,0.94,920,0.033,4.3
2026-03-09,0.96,810,0.030,4.5
```

### Tools & Frameworks

| Tool | Best For | Notes |
|------|----------|-------|
| **Weights & Biases** | Dashboard + experiment tracking | Integrates with most agent frameworks |
| **LangSmith** (LangChain) | Agent-native eval + tracing | Built for LangChain agents |
| **Braintrust** | Evals + comparison | Lightweight, good for startups |
| **Custom logging** | Full control | JSONL + analytics dashboard |

---

