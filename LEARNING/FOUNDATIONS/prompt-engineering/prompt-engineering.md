# Prompt Engineering

**Table of Contents**
1. [What Prompt Engineering Is](#1-what-prompt-engineering-is)
2. [LLM Output Configuration — The Dials You Control](#2-llm-output-configuration--the-dials-you-control)
3. [Prompting Techniques](#3-prompting-techniques)
   - [Zero-Shot](#zero-shot)
   - [One-Shot and Few-Shot](#one-shot-and-few-shot)
   - [System, Role, and Contextual Prompting](#system-role-and-contextual-prompting)
   - [Step-Back Prompting](#step-back-prompting)
   - [Chain of Thought (CoT)](#chain-of-thought-cot)
   - [Self-Consistency](#self-consistency)
   - [Tree of Thoughts (ToT)](#tree-of-thoughts-tot)
   - [ReAct (Reason + Act)](#react-reason--act)
   - [Automatic Prompt Engineering (APE)](#automatic-prompt-engineering-ape)
4. [Advanced & Automated Techniques](#4-advanced--automated-techniques)
   - [Auto-CoT](#auto-cot)
   - [Reprompting via Gibbs Sampling](#reprompting-via-gibbs-sampling)
   - [Chain of Draft (CoD)](#chain-of-draft-cod)
   - [Rephrase and Respond (RaR)](#rephrase-and-respond-rar)
   - [OPRO — Optimization by Prompting](#opro--optimization-by-prompting)
5. [Code Prompting](#5-code-prompting)
6. [Best Practices](#6-best-practices)
7. [Documentation — The Practice Most People Skip](#7-documentation--the-practice-most-people-skip)
8. [Anti-Patterns](#8-anti-patterns)

---

## 1. What Prompt Engineering Is

A large language model is, at its core, a prediction engine. It takes text as input and predicts — token by token — what the most likely next word should be, based on patterns in the enormous amount of text it was trained on. Every word it generates becomes the new end of the sequence, and then it predicts the next word again, and so on.

When you write a prompt, you are setting up that prediction engine to head in a particular direction. A well-crafted prompt is like pointing a very powerful engine down a specific road. A poorly crafted prompt is like starting the engine and hoping it finds the right destination on its own.

**Prompt engineering** is the discipline of designing those prompts — iteratively, deliberately, and systematically — to get the outputs you actually want. It's not programming in the traditional sense; you're not writing logic. You're writing *inputs that steer probabilistic prediction*. That distinction matters because the same instruction phrased three different ways can yield meaningfully different results.

Anyone can write a prompt. The skill is in writing prompts that reliably produce good outputs, across different inputs, on the first or second try rather than the fifteenth.

The quality of your prompt depends on: the model you choose, the model's training data, the configuration settings (temperature, sampling), your word choice, tone, structure, and how much context you provide. Prompting is inherently iterative — you try, observe, adjust, and repeat.

---

## 2. LLM Output Configuration — The Dials You Control

Before writing a single word of prompt text, it helps to understand the configuration settings that shape how the model generates its response. These aren't minor tweaks — they fundamentally change what kind of output the model produces.

### Output Length

Every response has a token limit — the maximum number of tokens the model will generate. Setting this limit is important: more tokens mean more computation, higher cost, and slower responses. But a limit that's too tight will cut off the answer mid-thought.

Crucially, restricting the output length does *not* make the model more concise in its thinking — it just makes it stop writing sooner. If you want genuinely short output, you need to both set a low token limit *and* ask for brevity in the prompt itself.

### Temperature — How Creative vs. How Predictable

Temperature is the most widely discussed setting, and for good reason. It controls how "random" the model's word choices are.

Think of it this way: when the model is deciding what word comes next, it has a probability distribution across thousands of possible words. Temperature controls how peaked or flat that distribution becomes before sampling from it.

- **Low temperature (0–0.3)**: The distribution is very peaked. The highest-probability word dominates, so the model almost always picks the "safest" most predictable option. Good for factual tasks, classification, math, and anywhere there's a single right answer.
- **High temperature (0.7–1.0+)**: The distribution flattens. Lower-probability words become plausible options, so the model can surprise you — for better or worse. Good for creative writing, brainstorming, generating variety.
- **Temperature = 0**: Fully deterministic (greedy decoding) — always picks the single highest-probability token. Use this for CoT reasoning and tasks with one correct answer.

**The repetition loop bug**: At both extremes, temperature can cause the model to get stuck repeating the same words or phrase endlessly. At low temperature, the deterministic path loops back on itself. At high temperature, random chance eventually lands on words that lead back to the same place. The fix is usually careful tuning of temperature together with top-K and top-P.

**Good starting points:**
- Balanced creative/coherent: temperature 0.2, top-P 0.95, top-K 30
- Highly creative: temperature 0.9, top-P 0.99, top-K 40
- Conservative/factual: temperature 0.1, top-P 0.9, top-K 20
- Single correct answer: temperature 0

### Top-K and Top-P — Narrowing the Candidate Pool

While temperature reshapes the entire probability distribution, top-K and top-P add a filter *before* sampling occurs — they restrict which words are even eligible to be selected.

**Top-K** keeps only the K most probable next tokens. Setting K to 1 is equivalent to temperature 0 (always pick the top word). Setting K to the full vocabulary size effectively disables the filter.

**Top-P** (also called nucleus sampling) keeps tokens until their cumulative probability reaches the threshold P. If P is 0.9, the model picks from whichever tokens collectively account for 90% of the probability mass. This adapts automatically — if one word dominates, only that word might be included; if the distribution is spread out, more words are included.

**How they interact with temperature:** When all three are active, tokens must pass both the top-K and top-P filters *before* temperature is applied to sample among the survivors. At extreme settings, they cancel each other out — temperature 0 makes top-K and top-P irrelevant; top-K of 1 makes everything else irrelevant.

The key practical lesson: **experiment with settings together**, not in isolation. Changing one affects how the others behave.

---

## 3. Prompting Techniques

### Zero-Shot

The simplest possible prompt — no examples, just a task description. You're relying entirely on the model's general knowledge and training.

```
Classify movie reviews as POSITIVE, NEUTRAL, or NEGATIVE.

Review: "Her" is a disturbing study revealing the direction humanity is
headed if AI is allowed to keep evolving, unchecked. I wish there were
more movies like this masterpiece.

Sentiment:
```

Zero-shot works when the task is common enough that the model has seen many examples in training. It fails when the task is unusual, requires specific format conventions, or has edge cases the model can't anticipate on its own. When zero-shot fails, reach for few-shot.

### One-Shot and Few-Shot

You give the model one (one-shot) or several (few-shot) examples of the desired input-output pattern. The model then follows that pattern for the new input.

This works because of something remarkable in how LLMs are trained: they can recognize and generalize from patterns shown *within the prompt itself*, without any retraining. The examples act as a live teaching signal.

**Why it matters:** Even one good example can dramatically improve output format and quality. Multiple examples increase the chance the model learns the actual pattern rather than overfitting to surface features of a single example.

**How many examples?** Three to five is a good starting rule. Use more for complex tasks; you may need fewer if the model is very capable and the task is clear.

**Practical tips for few-shot:**
- Use examples that cover the range of variation you expect in real inputs
- Include edge cases if they're likely
- For classification tasks, mix up the classes across examples — don't put all the "positive" examples first, or the model may latch onto order rather than meaning
- Start with six examples and dial back if the context gets too long

```
Parse pizza orders into JSON:

EXAMPLE:
"I want a small pizza with cheese and pepperoni."
{"size": "small", "ingredients": ["cheese", "pepperoni"]}

EXAMPLE:
"Large pizza, tomato sauce and mozzarella please."
{"size": "large", "ingredients": ["tomato sauce", "mozzarella"]}

Now parse: "I'd like a large pizza, first half cheese and mozzarella,
other half ham and pineapple."
```

### System, Role, and Contextual Prompting

These three techniques all shape *how the model approaches a task*, but each from a different angle.

**System prompting** defines the overall task and output format. It's the "big picture" instruction — telling the model what it is fundamentally supposed to do. It's especially useful for enforcing output structure (return JSON, use only one word, be concise) and for safety/tone guidelines ("always be respectful in your answers").

**Role prompting** assigns a persona or identity to the model. This shapes the tone, vocabulary, level of detail, and perspective. "You are a kindergarten teacher" produces different explanations than "you are a PhD researcher." The role provides an implicit style guide. You can layer personality on top: "Act as a travel guide, but with a humorous tone."

Available styles worth experimenting with: Confrontational, Descriptive, Direct, Formal, Humorous, Influential, Informal, Inspirational, Persuasive.

**Contextual prompting** provides specific background information for the current task. Unlike a system prompt (which is relatively stable), context is dynamic — it changes per request. "You are writing for a blog about retro 80s arcade games" tells the model what to assume about the audience and subject matter without having to spell out every constraint explicitly.

These three overlap significantly in practice. A single prompt can include all three layers: a system instruction, a role assignment, and specific context for the current task. The value of keeping them conceptually distinct is that it gives you a framework for diagnosing when something goes wrong — was it the system setup, the role framing, or the missing context?

### Step-Back Prompting

Step-back prompting is a two-stage technique that activates broader knowledge before tackling a specific task.

The problem it solves: when you ask a model a narrow, specific question, it tends to pattern-match to similar specific questions in its training data. This can produce generic or templated answers. But if you first ask a more general question — one step removed from the specific task — the model activates richer background knowledge, which then improves the specific answer.

**The workflow:**
1. Identify the general principle behind your specific task
2. Ask the model about the general principle first
3. Feed the model's answer back in as context for the specific task

**Example:** Instead of directly asking "Write a storyline for a first-person shooter level," first ask "What are the five most engaging settings in first-person shooter games?" Then feed those settings back in as context: "Using these settings, write a storyline for one level."

The result is more specific, more grounded, and more creatively rich than if you'd asked directly. Step-back prompting is particularly useful for creative tasks, domain-specific problems, and any case where the model's default response feels generic or shallow.

### Chain of Thought (CoT)

LLMs are surprisingly bad at math. Ask a model a simple age-difference problem with no guidance, and it often gives the wrong answer. Ask it to "think step by step," and it suddenly gets it right. This is the core insight behind Chain of Thought prompting.

CoT prompting instructs the model to generate *intermediate reasoning steps* before arriving at a final answer. By making the model articulate its reasoning, you force it to slow down, catch errors, and build conclusions from a logical chain rather than pattern-matching directly to a guess.

```
# Without CoT:
When I was 3, my partner was 3 times my age. I'm now 20. How old is my partner?
→ Output: 63 (wrong)

# With CoT:
...How old is my partner? Let's think step by step.
→ Output: When I was 3, partner was 9. Difference is 6. Now I'm 20, so partner is 26. ✓
```

**Why this works:** The intermediate steps become part of the input for predicting the next token. When the model writes "the difference is 6," that fact is now *in the context* when it predicts the final answer. It's not magic — it's the model being forced to construct its own scaffolding.

**Advantages of CoT:**
- Low effort, high effectiveness — just add "Let's think step by step" or show an example with reasoning
- Works out of the box with any capable LLM without fine-tuning
- Makes the reasoning visible and debuggable — you can see where the logic went wrong
- More robust across different model versions — reasoning chains drift less than direct prompts when you upgrade models

**Disadvantage:** More output tokens = higher cost and latency. The reasoning appears in the response, which means you're paying for it.

**Zero-shot CoT** uses just the phrase "Let's think step by step." Research by Kojima et al. (2023) showed this single phrase — with no examples at all — produces dramatic improvements: on MultiArith, accuracy jumped from 17.7% to 78.7%; on GSM8K (grade-school math), from 10.4% to 40.7%. The model was already capable of this reasoning; it just needed a trigger to activate it.

Zero-shot CoT uses a two-stage process to work reliably:
1. **Reasoning extraction**: Append "Let's think step by step." The model generates a full reasoning chain.
2. **Answer extraction**: Feed the reasoning chain back in with "Therefore, the answer (in numerals) is" to reliably extract the final answer in the correct format.

This two-step approach matters because asking the model to both reason and extract the answer in one shot leads to format errors. Separating reasoning from answer extraction keeps each step clean.

**Few-shot CoT** shows one or more complete examples including the reasoning chain — this is more powerful for complex tasks. The zero-shot version is the minimal baseline that works surprisingly well; the few-shot version is the gold standard.

**Critical best practice:** For CoT, always set temperature to 0. You're looking for the single correct reasoning path, not creative variation. The one exception: self-consistency (see below) deliberately uses higher temperature to generate diverse paths for voting.

### Self-Consistency

Self-consistency extends CoT by running the same prompt multiple times (with a higher temperature to generate variety) and then selecting the most commonly occurring final answer.

The intuition: if you ask ten people to independently work through a hard problem and eight of them arrive at the same answer, that answer is probably right. Self-consistency applies this voting logic to LLM responses.

**The process:**
1. Send the same CoT prompt multiple times with temperature 0.7–0.9 (so each run explores a different reasoning path)
2. Extract the final answer from each response
3. Take the majority vote — simply select the most frequently occurring answer

**What the research shows** (Wang et al., ICLR 2023): across PaLM-540B and GPT-3, self-consistency improved CoT accuracy by significant margins — GSM8K +17.9%, SVAMP +11.0%, AQuA +12.2%, StrategyQA +6.4%, ARC-challenge +3.9%. The gains are more dramatic for larger models: smaller models see +3–6%; larger models see +9–23%.

**Key finding on aggregation:** Simple majority vote (counting the most common answer) works just as well as probability-weighted voting. This is because the model assigns nearly identical probabilities to its various reasoning paths — it genuinely can't distinguish its own good from bad reasoning. The external vote does what the model can't do for itself.

**Practical sampling settings:** Temperature 0.7, top-K 40 for most tasks. Sample 40 paths per question for stable estimates. The researchers used UL2-20B at temp=0.5 and PaLM-540B at temp=0.7.

This is expensive — you're paying for 10–40 completions — but it provides a pseudo-probability measure of how confident the model is. If 9 out of 10 runs agree, that's meaningful signal. If it's 5/10, you know the question is genuinely ambiguous or the prompt needs work.

Self-consistency is most valuable when a single wrong reasoning path could lead to confidently wrong answers — it catches those cases by making them statistically rare. It's also robust to imperfect prompts: even with slightly flawed CoT examples, self-consistency often recovers the right answer.

### Tree of Thoughts (ToT)

Where CoT follows a single reasoning chain (linear) and self-consistency runs multiple parallel chains independently, Tree of Thoughts lets the model explore a branching tree of reasoning paths — considering multiple approaches at each decision point and evaluating which branches are most promising.

Imagine solving a complex puzzle. CoT says "here's my one attempt." Self-consistency says "here are ten independent attempts." Tree of Thoughts says "let me explore three approaches, evaluate each, pick the most promising one to develop further, explore branches from there, and prune the ones that aren't working."

ToT is the most powerful of the three for tasks that require genuine exploration — puzzle solving, multi-step planning, creative problem-solving. It's also the most computationally expensive and requires more sophisticated implementation than just modifying a text prompt.

### ReAct (Reason + Act)

All the techniques above operate purely in language — the model thinks and generates text. ReAct is the bridge to the real world: it combines reasoning with action, allowing the model to use external tools (search engines, calculators, APIs, databases) mid-response.

ReAct mimics how humans actually solve hard problems. We don't just think — we look things up, check our work, gather data, then think again based on what we found.

**The thought-action loop:**
1. Model reasons about the problem and decides what action to take
2. Action is executed (e.g., a web search)
3. Observation (the result) is fed back in
4. Model reasons again based on what it learned
5. Repeat until a final answer is reached

**Example — "How many children do Metallica's band members have?"**
```
Thought: Metallica has 4 members. I need to look up each one.
Action: Search "How many kids does James Hetfield have?"
Observation: Three children
Thought: 1/4 members = 3 children total so far
Action: Search "How many kids does Lars Ulrich have?"
Observation: 3
...
Final Answer: 10
```

ReAct is the foundation for tool-using agents. It's what makes the difference between a model that knows things and a model that can *find out* things dynamically. When combined with skill prompts and MCP servers (see the Skills knowledge base doc), ReAct-style reasoning is how agents orchestrate complex multi-step workflows.

### Automatic Prompt Engineering (APE)

At a certain point, you might wonder: can you prompt the model to write better prompts? Yes — this is Automatic Prompt Engineering.

Rather than hand-crafting your prompt, you give the model a few input-output examples of the task you want to accomplish, and it generates candidate instruction prompts automatically. The best candidate is selected by scoring each on held-out examples.

**The APE workflow** (Zhou et al., ICLR 2023):
1. Provide a small set of input-output demonstrations for your task (e.g., "direct" → "indirect"; "on" → "off")
2. Use an LLM as an *inference model*: give it the demonstrations and ask it to generate candidate instructions that would produce these outputs (e.g., "write the antonym of the word", "give the opposite of the input")
3. Score each candidate instruction on a validation set using zero-shot performance
4. Keep the top-K candidates; optionally use an LLM to generate *variations* of those candidates (paraphrasing, rephrasing) for a second round of refinement
5. Select the highest-scoring instruction as your final prompt

**What the research shows:** APE-generated instructions outperform human-written prompts on 24/24 instruction induction tasks and 17/21 BIG-Bench tasks. Across 24 NLP tasks, APE using InstructGPT surpassed human prompt engineer performance as measured by interquartile mean. A notable secondary finding: APE can also discover better zero-shot CoT triggers than "Let's think step by step" — for some tasks, phrases like "Let's work this out in a step by step way to be sure we have the right answer" score higher.

**Practical use:** APE is most valuable when you're building a reusable prompt for a specific production task — a classifier, an extractor, a standard response format — and you want the best possible instruction without being limited by your own phrasing instincts.

The limitation: APE is only as good as your evaluation metric. If you can't clearly measure what "better" means for your task, it's hard to know which generated prompt actually wins.

---

## 4. Advanced & Automated Techniques

The techniques in the previous section are building blocks. The techniques here are more advanced — often research-originated, sometimes requiring more setup — but represent where the field is pushing the boundaries of what automated prompting can accomplish.

### Auto-CoT

The problem with few-shot CoT is that someone has to write the reasoning examples by hand. Auto-CoT eliminates that labor by automatically generating CoT demonstrations.

**How it works:**
1. Use "Let's think step by step" (zero-shot CoT) to generate reasoning chains for a diverse set of questions from the training set
2. Cluster the questions by semantic similarity
3. Sample one representative question from each cluster along with its auto-generated reasoning chain
4. Use these auto-generated demonstrations as the few-shot examples for a new CoT prompt

The intuition is that diverse examples (one per cluster) avoid redundancy, while auto-generation eliminates the need for human annotation. Zhang et al. (2022) showed Auto-CoT outperforms the CoT baseline by an average of 1.33% and 1.5% on arithmetic and symbolic reasoning tasks with GPT-3.

**When to use it:** When you need CoT demonstrations for a new task but don't want to hand-write reasoning chains. This is the automated pipeline version of few-shot CoT.

---

### Reprompting via Gibbs Sampling

Reprompting takes the automation even further — it automatically *learns* which CoT reasoning style works best for a given model and task, without any human-written demonstrations at all.

The starting insight: different models have different "styles" of reasoning that work best for them. What works in human-written CoT for GPT-3 may not be optimal for a different model. And writing model-specific CoT demonstrations requires both domain expertise *and* expertise in how prompting works — a rare combination.

**How Reprompting works** (Xu et al., ICML 2024):

Think of it as an evolutionary process for CoT reasoning chains:

1. **Initialize**: Generate zero-shot reasoning chains (CoT "recipes") for a small set of training examples — you get a diverse but rough population of reasoning styles
2. **Evolve**: Iteratively "breed" new recipes — pick a problem, use other problems' current recipes as parent prompts to generate a new recipe for it; if the new recipe leads to the correct answer, keep it; otherwise, occasionally keep it anyway (avoiding local optima)
3. **Select**: After many iterations, select the recipes that work consistently well across training examples as your few-shot demonstrations
4. **Test**: Apply those evolved demonstrations to unseen test problems

**What the research shows:** Reprompting outperforms human-written CoT by +9.4 points on average across 20 challenging reasoning tasks. It beats self-consistency by 11+ points and Auto-CoT by 11+ points on the same benchmarks. An interesting bonus: using ChatGPT to initialize and InstructGPT to sample can yield up to +71 point improvements over InstructGPT alone — the stronger model's reasoning style helps the weaker one.

**When to use it:** When you need to optimize CoT for a specific model at scale and don't want to invest in writing task-specific demonstrations. The setup cost is higher (you need training examples with ground-truth answers), but the resulting demonstrations are model-specific and systematically optimal.

---

### Chain of Draft (CoD)

Standard CoT prompting dramatically improves accuracy — but it's verbose by design. Every reasoning step is spelled out in full, which increases both latency and token cost. Chain of Draft proposes a different approach: what if the reasoning steps were concise by design?

The observation behind CoD: when humans solve problems, we don't write out every step in full prose — we jot down just the essential information. CoD prompts the model to generate short, information-dense "drafts" at each step rather than full sentences.

**The result** (Xu et al., 2025): CoD matches CoT accuracy in most cases while using dramatically fewer tokens. On some tasks, the accuracy is equivalent while output tokens are reduced by up to 80% — with average latency reduction of 76.2%. This makes CoD particularly valuable in production applications where response time matters.

**How to use it:** In your CoT prompt examples, show brief, note-like intermediate steps rather than verbose prose reasoning. The model will imitate the concise style.

**When to use it:** Production applications where you need CoT-level accuracy but can't afford CoT-level latency or cost. Also useful when the output's reasoning chain will be visible to end users — nobody wants to read paragraphs of reasoning.

---

### Rephrase and Respond (RaR)

Sometimes the problem isn't the model's reasoning — it's the way the question was phrased. Human thought frames and LLM thought frames don't always align. A casually phrased question that's perfectly clear to a human can be ambiguous or poorly structured for an LLM's generative process.

Rephrase and Respond (RaR) addresses this by letting the LLM improve the question before answering it.

**The process:**
1. Add "Rephrase and expand the question, and respond" (or similar) to your prompt
2. The model first rewrites your question with improved clarity and precision
3. The model then answers the rephrased version

**Why it works:** The act of rephrasing forces the model to clarify implicit assumptions and resolve ambiguity before it commits to a reasoning direction. The rephrased question captures what you actually meant, even if your original wording was imprecise.

**Two-step variant:** For maximum effect, separate the rephrasing and answering into two prompts. Use one LLM call to rephrase, then a second call to answer the rephrased question. This gives you visibility into how the model interpreted your question.

**When to use it:** When you suspect the question's wording is causing the model to misinterpret your intent. Also useful as a general-purpose improvement for any prompt that produces unexpectedly off-target responses.

---

### OPRO — Optimization by Prompting

OPRO (Yang et al., 2023) takes the meta-prompting idea even further than APE. Rather than just generating and selecting candidate prompts, OPRO uses an LLM as an *optimizer* that iterates in a loop — proposing solutions, observing how well they work, and generating improved solutions based on that feedback.

**The core idea:** Provide the LLM with a "meta-prompt" that contains:
- A description of the optimization problem
- Past solutions tried and their scores (a running log)
- A request to generate a new solution that improves on the best ones so far

The LLM sees what's worked and what hasn't, reasons about patterns in that history, and proposes the next candidate. This is gradient descent without gradients — pure language-based optimization.

**What the research shows:** OPRO-optimized prompts outperform human-designed prompts by up to 8% on GSM8K and up to 50% on challenging BIG-Bench tasks. The most effective prompts discovered by OPRO are sometimes counterintuitive — phrases that a human would never write but that happen to trigger better performance in the model.

**When to use it:** Maximum-effort prompt optimization for high-value production tasks. OPRO requires many LLM calls (each iteration is a call), so it's expensive but systematic. Think of it as professional-grade prompt tuning rather than everyday engineering.

---

### Graph of Thoughts (GoT)

Where Chain of Thought is linear and Tree of Thoughts is branching, **Graph of Thoughts** represents reasoning as a directed acyclic graph — nodes are individual thought units, edges represent the relationships between them. This allows non-linear thinking patterns that neither chains nor trees can capture: a thought can be informed by multiple prior thoughts from different branches, and different reasoning paths can converge and recombine.

The practical implication: GoT is suited for problems where partial results from multiple separate reasoning lines need to be synthesized. A chain produces one answer. A tree explores alternatives independently. A graph allows those alternatives to feed into each other. Current implementations use a two-stage framework: first generating rationale nodes (individual reasoning steps), then combining selected rationale nodes to produce the final answer. GoT is more computationally expensive than ToT and requires more sophisticated orchestration — but it better models how human problem-solving actually works, where insights from one direction inform exploration in another.

**When to use it:** Complex synthesis tasks where you need to combine partial insights from multiple independent reasoning directions. For most production use cases, CoT or self-consistency delivers sufficient improvement at lower cost.

---

### Chain-of-Verification (CoVe)

**Chain-of-Verification** addresses hallucination at the reasoning level. The model generates an initial response, then constructs and answers a series of independent verification questions designed to fact-check the original response — without access to the original answer to avoid anchoring bias. Finally, it generates a corrected final response incorporating what it learned from the verification queries.

The key design principle is the independence of the verification step: the model answers verification questions as if approaching the topic fresh, rather than defending the original answer. This prevents the model from rationalizing errors it just made. The pattern:

1. Generate an initial draft response
2. Derive specific, focused verification questions from the claims in the draft ("What year was X founded?" rather than "Is the answer correct?")
3. Answer those verification questions independently
4. Produce a final revised response that incorporates corrections

CoVe is most valuable for responses that make specific factual claims — names, dates, figures, causal relationships — where incorrect initial guesses are likely. For creative or open-ended tasks, the verification step adds latency without meaningful benefit.

---

### ART — Automatic Multi-step Reasoning and Tool-use

**ART** combines chain-of-thought prompting with automatic tool use, generalizing both into a single zero-shot framework. Given a new task, ART automatically retrieves task-relevant demonstrations from a library of existing few-shot CoT examples, uses those demonstrations to generate intermediate reasoning steps, and integrates external tool calls at appropriate points during inference — without requiring task-specific human annotation.

The conceptual contribution: ART treats tool selection as part of the reasoning decomposition, not as a separate layer. When a reasoning step requires computation or lookup, ART routes to a tool; when the result is returned, reasoning resumes. The tool library can include calculators, code interpreters, search engines, and domain APIs. ART achieves zero-shot generalization by relying entirely on the retrieved library demonstrations rather than task-specific examples — the quality of the library is what limits performance.

**When to use it:** When you want ReAct-style tool integration for a new task type without writing custom demonstrations. ART's library-retrieval approach means it can adapt to new tasks that resemble previous ones, at the cost of being limited by what's in the library.

---

### Active Prompting

Standard few-shot prompting uses fixed human-annotated examples for all queries. **Active Prompting** improves on this by identifying which examples are most uncertain — and therefore most valuable to have annotated — rather than using a static set.

The process: query the model multiple times (k times) on the training examples without demonstrations, and measure disagreement across the k responses. High disagreement indicates that the model is uncertain on that example, which makes it a high-value annotation target. Humans then annotate the most uncertain examples with chain-of-thought reasoning, and those annotated examples become the few-shot demonstrations.

The result: demonstrations that cover the failure modes and ambiguous cases the model actually struggles with, rather than examples that happen to be easy for the human to write. This is essentially active learning applied to prompt engineering — prioritizing annotation effort where it has the most impact. The tradeoff is that it requires the initial round of model queries before you can select which examples to annotate, adding overhead to the setup process.

---

### Chain-of-Knowledge (CoK)

Standard retrieval-augmented generation retrieves from a single knowledge source. **Chain-of-Knowledge** extends this to grounding reasoning across multiple heterogeneous knowledge sources — structured databases, unstructured text corpora, domain-specific knowledge bases — within a single generation process.

CoK operates in three stages: **reasoning preparation** (analyzing the query to determine what types of knowledge are needed and from which sources), **dynamic knowledge adapting** (retrieving from those sources and incrementally refining the rationale as each source adds information), and **answer consolidation** (synthesizing the refined rationale into a final grounded answer). Each stage can refine the previous one — if initial rationale from one source is contradicted by a second source, the model updates its working rationale before consolidating.

The practical value: CoK is appropriate when answering a question requires combining structured data (a product database) with unstructured context (support documentation) and domain knowledge (technical specifications). Single-source RAG retrieves from one vector store; CoK orchestrates across multiple sources with explicit rationale refinement between stages.

---

## 5. Code Prompting

LLMs trained on large amounts of code are remarkably effective at generating, explaining, translating, and debugging code. The same prompting principles apply, but with a few specific patterns worth knowing.

### Writing Code

Be specific about the language, the exact task, and any constraints. Vague prompts produce vague code.

```
Write a Bash script that asks for a folder name, checks if it exists,
then prepends "draft_" to every filename inside it.
```

**Always read and test the output.** LLMs reproduce patterns from training data; they don't reason about execution. They can produce code that looks correct but has subtle bugs. Think of them as a very fast first draft, not a trusted engineer.

### Explaining Code

Drop in unfamiliar code and ask the model to walk through what each part does. This is faster than reading documentation, especially for languages you don't use daily. Works well for understanding someone else's code or revisiting your own code after time away.

### Translating Code

LLMs can translate between programming languages with surprising fidelity — Bash to Python, JavaScript to TypeScript, SQL dialects. The prompt is simply: "Translate this [language A] code to [language B]" followed by the code block.

Review the output carefully. The model may use idioms from one language that don't map cleanly to the other, or miss library equivalents.

### Debugging and Reviewing Code

Paste the broken code and the error message together. Ask the model to explain what's wrong and how to fix it. LLMs are particularly good at this because they've seen thousands of variations of common bugs — they often recognize the pattern instantly.

Beyond fixing the immediate error, ask for a general code review: "Are there other issues with this code?" You'll often get suggestions for robustness, error handling, and readability improvements beyond the original bug.

---

---

The utility of a demonstration in a prompt is measured by its **In-context Influence (ICI)**—the degree to which providing a specific example reduces the model’s difficulty in answering a target query. Selecting effective demonstrations requires a shift away from complexity; research shows that the most difficult samples in a dataset are rarely the best teachers. Effective prompt engineering should prioritize examples that are semantically relevant to the user's task but clear enough to substantially lower the model's instruction-following difficulty. Using demonstrations that have high "influence" on diverse peer tasks has been shown to improve model performance more effectively than selecting examples based on length or raw complexity.
## 6. Best Practices

### Provide Examples — The Single Most Effective Technique

If you do nothing else, add examples. One-shot or few-shot examples are the most reliable way to improve output quality, format, and accuracy. They act as live teaching — the model sees exactly what good output looks like and imitates it.

### Design with Simplicity

If a prompt is confusing to you, it's confusing to the model. Plain language outperforms complex language. Remove anything that isn't essential.

Before: "I am visiting New York right now, and I'd like to hear more about great locations. I am with two 3 year old kids. Where should we go during our vacation?"

After: "Act as a travel guide. Suggest great places to visit in New York Manhattan with a 3-year-old child."

Use action verbs to be precise: Act, Analyze, Categorize, Classify, Compare, Create, Describe, Evaluate, Extract, Generate, Identify, List, Parse, Rank, Recommend, Summarize, Translate, Write.

### Be Specific About the Output

Vague prompts produce vague outputs. Specify the format, length, tone, and structure you want.

- "Write a blog post about consoles" → too open
- "Write a 3-paragraph blog post about the top 5 video game consoles, in a conversational style, for a general audience" → clear

### Use Instructions Over Constraints

Tell the model what *to do*, not what *not to do*. Instructions communicate desired outcomes directly; constraints leave the model guessing about what's still allowed. A list of constraints can also conflict with each other.

- Constraint: "Don't mention specific game titles."
- Instruction: "Discuss only the console hardware, the company, the release year, and total sales."

The instruction is clearer, more actionable, and less likely to produce unexpected edge-case behavior. Use constraints only when you genuinely need to prevent specific harmful or off-topic content.

### Use Variables in Prompts

When you'll reuse a prompt template with different inputs, use placeholders:

```
You are a travel guide. Tell me one interesting fact about the city: {city}
```

Variables make prompts maintainable, reusable in applications, and easier to test systematically across different inputs.

### Control Length in the Prompt, Not Just the Config

Setting a max token limit tells the model when to stop — it doesn't make responses more concise. If you want a short response, say so: "Explain quantum physics in one sentence." or "Summarize this in 50 words."

### Experiment with Output Formats

For non-creative tasks — extraction, classification, parsing, summarization of structured data — requesting JSON output has meaningful advantages:

- Always returns in the same shape, making it easy to parse programmatically
- Forces the model to think in terms of structure, which reduces hallucinations
- Makes relationships between pieces of data explicit
- Enables sorting, filtering, and downstream use without reformatting

Provide a schema alongside the request for best results. The schema acts as a blueprint that keeps the model's output disciplined.

**JSON repair:** If the model hits the token limit mid-JSON, the output will be malformed. The `json-repair` Python library can automatically fix truncated JSON — useful in production pipelines.

### For CoT: Always Temperature 0

Chain of thought reasoning should be deterministic. You want the most probable reasoning chain, not creative variation. Set temperature to 0 for any CoT prompt.

Also: put the answer *after* the reasoning. The generation of the reasoning changes the token context that the model uses to predict the final answer. Reversing the order defeats the purpose.

### Experiment Together

Prompt engineering is partly subjective — what works best varies by model, task, and context. If you're working in a team, have multiple people write independent prompts for the same task and compare results. Different instincts surface different approaches; the best prompt often emerges from combining elements from several attempts.

---

## 7. Documentation — The Practice Most People Skip

Prompt outputs vary across models, across sampling settings, and even across identical prompts to the same model (when token probabilities are tied, tie-breaking is random). Without documentation, you lose track of what you tried, can't reproduce good results, and can't understand why a previously working prompt broke after a model update.

The recommended format for tracking every prompt attempt:

| Field | What to Record |
|---|---|
| Name & version | A unique identifier for this attempt |
| Goal | One sentence on what this prompt is trying to achieve |
| Model | Name and version |
| Temperature | Exact value |
| Token limit | Exact value |
| Top-K | Value or N/A |
| Top-P | Value or N/A |
| Full prompt | The entire prompt text, exactly as sent |
| Output | The actual output(s) received |
| Result | OK / NOT OK / SOMETIMES OK |
| Notes | What worked, what didn't, what to try next |

**Additional tips:**
- Save prompts in separate files from application code — they're maintained on a different cadence than logic
- When working with RAG systems (retrieval-augmented generation — where you inject retrieved documents into the prompt), also record the query, chunk settings, and what content was actually injected
- Once a prompt is production-ready, add it to automated evaluation pipelines so you catch regressions when models update

### Testing Output Format Expectations

Before declaring a prompt "done," explicitly test that the LLM's output matches your format requirements. This is the most commonly skipped step and causes cascading failures downstream.

**Why this matters:** LLMs generate probabilistic text. Even with explicit instructions like "output JSON" or "format as markdown," the model may occasionally deviate—outputting partial JSON, adding prose before the JSON block, using invalid markdown syntax, or mixing formats. These edge cases are silent failures: the prompt runs, but downstream parsing breaks.

**How to test it:**

1. **Run the prompt 5–10 times** with the same model and temperature you'll use in production. Record every output, even the good ones.

2. **Check for format violations:**
   - Does the JSON parse cleanly with `json.loads()`? Or does it have trailing commas, extra newlines, or preamble text?
   - Does the markdown render without syntax errors? (Unmatched brackets, missing pipes in tables, etc.)
   - For CSV: does every row have the same number of columns? No quote escaping issues?

3. **Test edge cases:**
   - Ask for output when the task has no valid results ("generate 5 email templates" when the context is empty). Does it gracefully return an empty array, or does it return malformed JSON?
   - Vary inputs: short vs. long, simple vs. complex, edge-case domains. Output format can degrade with extremes.

4. **Establish a fallback strategy:** If the LLM occasionally fails format validation, decide in advance whether you'll retry, use a fallback model, or surface the error to the user. Document this choice in your prompt file.

**Real example:** A prompt asked GPT-4 to output a JSON object. 95% of the time, it works perfectly. But roughly 1 in 20 runs, the model adds a prose preamble: `"Before I provide the JSON, I should mention..."` followed by the JSON. A naive parser expecting JSON at position 0 crashes. Testing with 10 runs would have caught this; without testing, it only surfaced in production.

---

## 8. Anti-Patterns

**Assuming the first prompt is the final prompt.** Prompt engineering is explicitly iterative. Expecting a correct output from the first attempt is like expecting compiled code to work without testing. Budget for multiple rounds.

**Vague output specifications.** "Write something about AI" is not a prompt — it's a topic. Always specify length, format, tone, and what you actually want the output to do.

**Using constraints instead of instructions.** "Don't be too long" is harder for a model to act on than "Write exactly two paragraphs." Positive instructions are consistently more effective than negative constraints.

**Skipping examples because they take time.** The time spent writing two or three good examples is almost always recovered in reduced iteration time and better output quality.

**Ignoring temperature for the task type.** Using high temperature for math or classification tasks, or low temperature for creative brainstorming, often produces exactly the wrong result. Match the setting to the task.

**Not reading code outputs before running them.** LLMs produce plausible-looking code that can have real bugs. Always review before executing, especially for scripts that touch files, networks, or databases.

**Not documenting prompt iterations.** You will revisit your prompts. Models update, tasks evolve, edge cases surface. The documentation you skip now will cost you much more time later when you're trying to reconstruct what you did and why.

---

*Primary sources: Lee Boonstra, "Prompt Engineering" (Google / Vertex AI whitepaper, Feb 2025) · White et al., "A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT" (Vanderbilt, 2023) · Kojima et al., "Large Language Models are Zero-Shot Reasoners" (NeurIPS 2022) · Wang et al., "Self-Consistency Improves Chain of Thought Reasoning" (ICLR 2023) · Zhou et al., "Large Language Models are Human-Level Prompt Engineers" (ICLR 2023) · Xu et al., "Reprompting: Automated Chain-of-Thought Prompt Inference Through Gibbs Sampling" (ICML 2024) · Sahoo et al., "A Systematic Survey of Prompt Engineering in Large Language Models" (2024) · Schulman et al., "What's in My Big Data?" (arXiv 2409.13342, 2024)*
