# Specification Clarity and Requirements Engineering for AI

**Table of Contents**
1. [What This Is About and Why It Matters](#1-what-this-is-about-and-why-it-matters)
2. [The Anatomy of a Good Spec — What Makes AI Reliably Execute](#2-the-anatomy-of-a-good-spec--what-makes-ai-reliably-execute)
3. [Requirements Engineering Fundamentals — What Transfers from Software to AI](#3-requirements-engineering-fundamentals--what-transfers-from-software-to-ai)
4. [Acceptance Criteria as a Precision Tool](#4-acceptance-criteria-as-a-precision-tool)
5. [Constraint Architecture — Specifying What You Don't Want](#5-constraint-architecture--specifying-what-you-dont-want)
6. [Problem Statement Structure](#6-problem-statement-structure)
7. [Domain-Driven Design and Shared Language](#7-domain-driven-design-and-shared-language)
8. [The Shape Up Methodology Applied to AI Tasks](#8-the-shape-up-methodology-applied-to-ai-tasks)
9. [The Decomposition Problem — Atomic vs. Holistic Tasks](#9-the-decomposition-problem--atomic-vs-holistic-tasks)
10. [Failure Mode Catalog — What Goes Wrong with Unclear Specs](#10-failure-mode-catalog--what-goes-wrong-with-unclear-specs)
11. [Writing Techniques — Concrete Moves for Clearer Specs](#11-writing-techniques--concrete-moves-for-clearer-specs)
12. [Decision Frameworks — Scoping and Granularity Decisions](#12-decision-frameworks--scoping-and-granularity-decisions)
13. [Evaluation Design — Specifying What "Done" Looks Like](#13-evaluation-design--specifying-what-done-looks-like)
14. [Key Takeaways for the AI Practitioner and AI PM](#14-key-takeaways-for-the-ai-practitioner-and-ai-pm)
15. [Anti-Patterns](#15-anti-patterns)

---

## 1. What This Is About and Why It Matters

Every AI system ultimately executes on instructions. Whether you're writing a system prompt for a customer-facing chatbot, a task description for an autonomous agent, acceptance criteria for an AI-assisted feature, or a brief to hand off to an engineering team building with LLMs — you are writing a *specification*. The quality of that specification determines the quality of what comes out.

This is one of the most underestimated skills in AI work. Most people focus on the AI system itself — the model, the architecture, the infrastructure. But experienced practitioners consistently find that the single largest driver of output quality is upstream: how precisely the problem and the desired outcome were articulated in the first place.

The problem has two faces. The first is communicating clearly enough for AI systems to execute your intent reliably — this is about prompt design, system prompt architecture, agent task specifications, and multi-step pipeline briefs. The second is writing requirements and acceptance criteria for AI-assisted software development — this is about product spec writing, user stories, and the specifications that human teams (using AI tools) build from.

Both faces share the same underlying challenge: natural language is inherently ambiguous, and the gap between what you meant and what you said is where most failures live.

### Why the Stakes Are Higher with AI

With a human engineer, ambiguity gets resolved through conversation. You write a vague requirement, they ask a clarifying question, and the gap closes. With an AI system — particularly an autonomous agent executing a multi-step pipeline — there may be no opportunity for clarification. The system interprets your spec at face value, makes its best guess about what you meant, and proceeds. If that guess is wrong, you may not know until several expensive steps later.

Research published by CMU in 2025 put a number on this fragility. Their analysis of "underspecified prompts" (prompts that leave requirements implicit) found that while LLMs can often *guess* the implied requirement (41.1% of the time), underspecified prompts are **2x more likely to regress** across model or prompt changes, with accuracy drops exceeding 20% in some cases. The system worked fine — until you changed something, and suddenly it didn't. The invisible assumption had been doing quiet load-bearing work the whole time. (Source: [What Prompts Don't Say, CMU 2025](https://arxiv.org/abs/2505.13360))

This matters enormously for AI PMs and practitioners because the AI industry is moving fast. Models change. Providers change. Pipelines evolve. Specifications built on implicit assumptions break when anything in that chain shifts.

The deeper insight: specification clarity is not a nice-to-have quality. It is a *stability property* of your system.

---

## 2. The Anatomy of a Good Spec — What Makes AI Reliably Execute

Think of a specification as the AI's entire world for a given task. If the spec doesn't contain something, the AI either makes it up, borrows from its training data defaults, or fails silently. A well-formed spec is self-contained: everything the AI needs to act correctly is present in the spec itself.

Drawing from IEEE 830 software requirements standards, Karl Wiegers' work on software requirements, and Anthropic's own prompt engineering guidance, a well-formed specification has the following properties.

### The Seven Properties of a Executable Spec

**1. Complete.** Every piece of information needed to execute the task is present. The AI doesn't need to assume context it doesn't have. There are no blank spots where a human would intuitively fill in common sense.

What this means in practice: before finalizing a spec, ask yourself "what would a smart but completely uninformed person misunderstand about this?" The answer points to what's missing.

**2. Unambiguous.** Every term has one and only one reasonable interpretation in context. This is harder than it sounds. Words like "recent," "large," "complete," "professional," "short," and "appropriate" all carry inherent vagueness. IEEE 830 is explicit: "An SRS is unambiguous if, and only if, every requirement stated therein has only one interpretation. As a minimum, this requires that each characteristic of the final product be described using a single unique term." ([IEEE 830, via IEEE Xplore](https://ieeexplore.ieee.org/document/720574))

What this means in practice: when you catch yourself using relative terms ("make it better," "add some context," "be thorough"), replace them with operationalized ones ("increase score from X to Y," "add two sentences of background on the user's role," "cover all three edge cases listed below").

**3. Consistent.** No requirement contradicts another. Conflicting instructions don't get resolved by an AI through negotiation — the model picks one interpretation and runs with it, often unpredictably.

What this means in practice: review your spec for constraint conflicts. "Be concise but thorough" and "cover every possible edge case in detail" are in tension. Pick one, or define the priority order.

**4. Verifiable.** The output can be objectively tested against the spec. If you can't write a test for a requirement, you can't know if it was met. This is the discipline that BDD (Behavior-Driven Development) enforces with its Given/When/Then format: if you can't express the requirement as a testable scenario, the requirement isn't clear enough yet.

What this means in practice: for every requirement, ask "how would I check, in 30 seconds, whether this was satisfied?" If you can't answer that, the requirement is still vague.

**5. Bounded.** The scope is explicitly defined, including what's out of scope. A spec without explicit boundaries invites the AI to fill in the gaps with whatever seems reasonable. Defining what you're *not* asking for is often as valuable as defining what you are.

What this means in practice: use explicit "no-go" language. "Do not include X." "This does not cover Y." "For this pass, ignore Z."

**6. Prioritized.** When multiple requirements exist, their relative importance is stated. This tells the AI what to optimize for when trade-offs are necessary.

What this means in practice: use explicit priority language. "The primary goal is X. Secondary goal is Y. If you must choose, prefer X." Or tier them: "Must have / Nice to have / Out of scope."

**7. Grounded.** Abstract goals are connected to concrete examples. Examples do more than illustrate — they constrain the interpretation space. An abstract instruction has many valid interpretations; a concrete example anchors the AI to one cluster of them.

What this means in practice: include at least one concrete example of what success looks like, preferably two (one clear success, one edge case).

---

## 3. Requirements Engineering Fundamentals — What Transfers from Software to AI

Requirements engineering is a 50-year-old discipline. Most of its lessons were developed for human developers working on software systems, but a surprising proportion transfer directly to working with AI. Understanding the foundational concepts gives you a vocabulary and toolkit that the field has already debugged.

### What Karl Wiegers Teaches Us

Karl Wiegers spent decades studying why software requirements fail. His book *Software Requirements* (3rd ed.) is the standard reference for software business analysts. Three of his core lessons translate directly to AI specification work.

**Weak words signal weak requirements.** Wiegers explicitly calls out "weasel words" — terms that sound precise but aren't. Words like *should*, *usually*, *often*, *as appropriate*, *fast*, *reliable*, *user-friendly*, and *minimal* all create interpretive latitude. In software requirements, they give developers room to do less than was intended. In AI specifications, they give the model room to interpret the requirement in whatever way its training biases favor.

The fix: replace every weasel word with a measurable criterion. "The response should be fast" becomes "the response must complete within 5 seconds." "The summary should be concise" becomes "the summary must not exceed 150 words." This isn't pedantry — it's what makes a requirement actually checkable.

**Always record the rationale.** One of Wiegers' most practical pieces of advice is to document not just what the requirement is, but why it exists. This matters especially when requirements need to be adjusted, traded off, or interpreted in an edge case. When a developer — or an AI agent — encounters a situation the spec didn't anticipate, the rationale gives them a principled basis for judgment.

In AI agent design, this translates to including "goal context" in your system prompts. Instead of just saying "always respond in under 200 words," say "respond in under 200 words because users read on mobile in short sessions and abandon longer responses." The rationale is meta-context that improves decisions in edge cases.

**Requirements have levels.** Wiegers distinguishes business requirements (the why), stakeholder requirements (what specific people need), and functional requirements (what the system must do). Conflating levels is a major source of spec failure — writing a functional instruction when what you really mean is a business goal, and vice versa.

Applied to AI: writing "summarize the document" is a functional requirement. Writing "help the user quickly understand the key decisions in this document so they can respond to their manager intelligently" is a stakeholder requirement. The second gives the AI vastly more basis for judgment about what to include, what to skip, and how to frame things.

### What IEEE 830 Standardizes

The IEEE 830 standard (later superseded by ISO/IEC/IEEE 29148:2011) established the canonical properties of a well-formed software requirements specification. Its quality model is built on four assessable properties: **completeness, correctness, preciseness, and consistency.** ([IEEE 830, IEEE Xplore](https://ieeexplore.ieee.org/document/720574))

These four map cleanly onto AI specification:

- Completeness: does the spec contain everything needed?
- Correctness: do the requirements accurately reflect the actual goal?
- Preciseness: are all terms operationalized and unambiguous?
- Consistency: do no requirements contradict each other?

A useful exercise: run your AI spec through this four-lens checklist before deploying it. Most first drafts fail at least one dimension.

### What Cockburn's Use Cases Add

Alistair Cockburn's *Writing Effective Use Cases* adds a structural discipline that prompt engineers would benefit from adopting. Cockburn's use case template includes: **goal level, preconditions, success postconditions, failure postconditions, and main success scenario.**

The most powerful concept here is the explicit documentation of **preconditions** — what must be true before the task begins — and **postconditions** — what must be true for the task to be considered complete. This maps directly to AI agent design.

Preconditions for an AI task tell the agent what state the world is in when it starts. Without this, the agent may make incorrect assumptions about what data is available, what prior steps have been completed, or what constraints are active. Postconditions tell the agent — and the designer — precisely what success looks like. A use case without an explicit success postcondition is a task without a finish line.

Goal levels are equally useful. Cockburn distinguishes "sea level" goals (what a user is trying to accomplish in one session) from "cloud level" goals (the broader business objective) and "fish level" goals (implementation steps). The insight: most AI tasks should be specified at sea level. Too abstract (cloud level) and the AI lacks direction; too granular (fish level) and you're micromanaging a system that does better with autonomy.

---

## 4. Acceptance Criteria as a Precision Tool

Acceptance criteria are the specific, testable conditions that must be satisfied for a piece of work to be considered complete. In software development, they're typically written alongside user stories. In AI work, they serve the same function: they operationalize "done" in a way that removes ambiguity from both the AI's execution and the human's evaluation of that execution.

### Why Acceptance Criteria Matter More Than You Think

The research is clear that unclear "done" definitions are among the leading causes of project failure. The Project Management Institute found that in projects failing to meet business objectives, half traced the failure to ineffective communication — and unclear success criteria sit at the center of that failure. In AI systems, this failure mode is amplified because there's no negotiation mid-execution. The AI treats the absence of a success criterion as permission to use its own judgment.

### The Given/When/Then (Gherkin) Pattern

The most widely used format for acceptance criteria in software engineering is Gherkin's Given/When/Then structure, codified by the BDD (Behavior-Driven Development) community and used in tools like Cucumber. Its structure is:

```
Given [a specific starting state or precondition]
When [a specific action or event occurs]
Then [a specific, observable outcome follows]
```

This format is powerful because it enforces three things simultaneously:
- **Specificity of context** (Given): you must say exactly what state the system is in
- **Specificity of trigger** (When): you must say exactly what causes the behavior
- **Specificity of outcome** (Then): you must say exactly what the observable result is

The observable outcome is the hardest and most important. "Then the user is satisfied" is not an observable outcome — it's a hope. "Then the response contains exactly three bullet points, each under 20 words, and no preamble text" is observable. You can check it mechanically. ([Cucumber Gherkin Reference](https://cucumber.io/docs/gherkin/reference/))

**Applying this to AI prompting:** the Given/When/Then structure maps directly onto task specification for AI agents:

```
Given: [state of the world, what data/context exists, what has already happened]
When: [the user action or trigger that initiates the AI task]
Then: [the specific, verifiable output the AI must produce]
```

**Example (weak):** "Summarize customer feedback."

**Example (Gherkin-style):** "Given a set of customer support tickets from the last 30 days, each tagged with a category, when a support manager requests a summary, then produce a bulleted list of the top 5 complaint categories by volume, with the percentage share of each category and one representative verbatim quote per category."

The second version leaves almost nothing to interpretation. The structure forces you to be specific.

### The INVEST Criteria for Atomic Specs

The INVEST criteria — originally developed by Bill Wake for user stories — provide a checklist for evaluating whether a specification is well-formed. A good spec is:

- **Independent**: self-contained, doesn't depend on unstated assumptions
- **Negotiable**: describes the outcome, not a prescribed implementation
- **Valuable**: delivers something meaningful
- **Estimable**: specific enough that effort can be assessed
- **Small**: scoped tightly enough to be testable as a unit
- **Testable**: there exists a concrete way to verify completion

([Agile Alliance: INVEST](https://agilealliance.org/glossary/invest/))

Applied to AI specs: if you can't tell whether a spec is testable (the T in INVEST), it isn't specific enough yet. If you can't tell whether it's small (the S), it probably needs to be decomposed into multiple specs.

### Spec-Driven Evaluation

One of the most underutilized practices in AI development is writing evaluation criteria before writing the prompt, just as test-driven development writes tests before writing code. If you write your acceptance criteria first, the spec almost writes itself — you're reverse-engineering from the desired outcome. This catches underspecification early, when it's cheap to fix.

---

## 5. Constraint Architecture — Specifying What You Don't Want

One of the most consistently underused tools in specification is the **negative constraint** — explicitly stating what you do *not* want, what is out of scope, and what behaviors are prohibited. Most specifications are purely positive: they describe what should happen. Negative specifications describe the boundary of what should not happen, and they are often more important than the positive ones.

### Why Negative Specifications Exist

Think of a positive specification like describing the shape of a hole by saying what goes into it. A negative specification describes the shape of the hole by saying what doesn't fit. Both are necessary for precision.

In AI systems, negative specifications serve a specific function: they prevent the model from "helpfully" extending beyond what you asked for. LLMs are trained to be helpful. Left unconstrained, they will add context you didn't ask for, make decisions you didn't authorize, format output in ways that seem useful to them, and generally optimize for what a well-intentioned AI thinks you probably want. Negative constraints cut off these well-intentioned overreaches.

Ryan Singer's Shape Up methodology makes this explicit with the concept of **no-gos**: "anything specifically excluded from the concept — functionality or use cases we intentionally aren't covering to fit the appetite or make the problem tractable." Shape Up treats no-gos as a first-class element of every specification, not an afterthought. ([Shape Up, Basecamp](https://basecamp.com/shapeup/1.5-chapter-06))

### Types of Constraints

**Behavior constraints** prohibit specific actions or outputs: "Do not recommend competitor products." "Do not include PII in the output." "Do not ask clarifying questions — make your best judgment."

**Format constraints** restrict what the output looks like: "Do not use headers." "Do not produce more than 5 items." "Do not use bullet points — write in prose."

**Scope constraints** define what topics or domains are out of bounds: "Do not address pricing — escalate to the sales team." "This covers only the onboarding flow, not the checkout flow."

**Temporal constraints** restrict when something should or shouldn't happen: "Do not suggest major changes to existing copy — only add new sections."

**Source constraints** restrict what information the AI can draw on: "Answer only from the documents provided — do not use general knowledge."

### Constraint Architecture as Defense in Depth

In AI security and reliability, constraint architecture is a layered defense strategy. The research from AWS on AI guardrails describes this as multiple controls applied across the request path — from API entry to output validation — with each layer removing a different class of risk. No single constraint covers everything, but layered constraints cover the most critical failure modes.

Practically: write your positive specification first. Then ask "what would a well-intentioned AI do with this that would be wrong?" Each answer is a negative constraint you should add. Then ask "what could go wrong in an edge case?" Each answer is another constraint or a rabbit hole to address explicitly.

---

## 6. Problem Statement Structure

The problem statement is the foundation beneath the specification. A well-structured problem statement is what makes a specification *decomposable* — it gives you a clear enough picture of the goal that you can identify the sub-tasks, the constraints, and the success criteria. A weak problem statement produces specifications that seem complete but are actually built on undefined assumptions.

### The Self-Contained Problem Statement

The goal of a self-contained problem statement is that a completely uninformed reader could understand the problem, understand the goal, and make reasonable decisions without asking any follow-up questions. This standard is higher than most people apply. Most problem statements assume shared context that exists only in the writer's head.

A well-structured problem statement for AI work has these elements:

**Background.** Who is involved? What is the existing state of the world? What is the history or context that makes this problem exist? The background is not the problem itself — it's the setup that explains why the problem matters and what the relevant landscape looks like.

**Goal.** What outcome are you trying to achieve? This is the highest-level statement of success. It should be at "sea level" in Cockburn's terms — specific enough to direct action, abstract enough to not prescribe implementation.

**Problem.** What specific obstacle stands between the current state and the goal? This is distinct from the goal. The goal is where you want to be; the problem is what's blocking you. Many specs skip this distinction and jump straight to solution, which means the solution may be solving the wrong problem.

**Constraints.** What boundaries does any solution operate within? Time, resources, existing systems, regulatory requirements, user needs, technical limitations.

**Success criteria.** How will you know when the goal is achieved? These should be measurable or at least observable. This is where acceptance criteria live.

**Out of scope.** What is explicitly not part of this problem? A boundary statement prevents scope creep and keeps the problem tractable.

### Why Problem Clarity Enables Decomposability

A problem statement that clearly separates goal, problem, and constraints enables decomposition because each element can be addressed independently. You can break the problem into sub-problems (each of which inherits the constraints), break the success criteria into sub-criteria (each of which can be tested independently), and break the goal into sub-goals (each of which can be delegated to a separate agent or step).

Google's ML Problem Framing guide formalizes this for machine learning contexts: "To frame a problem in ML terms, you complete the following tasks: define the ideal outcome and the model's goal, identify the model's output, and define success metrics." ([Google ML Problem Framing](https://developers.google.com/machine-learning/problem-framing)) This three-part structure — outcome, output, metric — is a minimal well-formed problem statement for any AI task.

---

## 7. Domain-Driven Design and Shared Language

One of the most insightful tools in the entire specification literature is Eric Evans' concept of **Ubiquitous Language** from Domain-Driven Design (DDD). The insight is simple but profound: precision in specification requires a shared vocabulary. When the writer of a spec and the executor of a spec use the same word to mean different things, every ambiguity that results was invisible at the time of writing.

### What Ubiquitous Language Means

In DDD, the ubiquitous language is the set of terms that both technical and non-technical stakeholders have agreed upon, defined precisely, and use consistently across all artifacts — conversations, code, documentation, and tests. The language comes from the domain model: the specific vocabulary of the business domain being modeled.

Martin Fowler describes it this way: "The ubiquitous language is a set of unambiguous vocabulary shared by all members and stakeholders of a product team." ([Martin Fowler: Domain Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)) The critical word is "unambiguous." A ubiquitous language is not just a glossary — it's a *binding contract* about meaning.

The absence of a shared language creates the most pernicious form of specification failure: invisible disagreement. Both the writer and the reader think they're in agreement, but they're using the same words to mean different things. The failure only becomes visible at execution time, which is the most expensive possible moment.

### Applying This to AI Specification

When writing specs for AI systems, ubiquitous language has a specific application: the terms in your spec must be precisely defined, and those definitions must be either explicit in the spec or reliably present in the model's training. If you use a term that has multiple meanings and you intend only one, your spec has a latent ambiguity.

**Example:** "Classify the email as urgent." What is "urgent"? A sales email with a time-sensitive offer? A support ticket from an enterprise customer? A message with the word "urgent" in the subject line? These are all reasonable interpretations. If you haven't defined "urgent" specifically, the model will use whatever its training biases toward.

The fix is domain glossary injection: include a mini-glossary at the top of your specification or system prompt that defines the terms you use in a specific sense. "For this task: 'urgent' means the email requires a response within 4 hours to avoid customer impact. 'High priority' means response within 24 hours. 'Routine' means response within 3 business days."

This technique — borrowed directly from DDD — is one of the highest-leverage moves available for reducing specification ambiguity.

### Language as a Diagnostic Tool

Ubiquitous language also serves as a diagnostic. If you can't define a term precisely enough to write it into a glossary, that term is not well enough understood to appear in a specification. The discipline of trying to write the glossary often reveals that you don't understand the problem as well as you thought. This is uncomfortable but valuable — better to discover the conceptual gap now than after you've built the system.

---

## 8. The Shape Up Methodology Applied to AI Tasks

Basecamp's Shape Up methodology, developed by Ryan Singer, was originally designed for software product development. Its core insight — that you must do serious design work *before* giving a project to a team, not *during* — transfers directly to AI task specification.

### The Core Problem Shape Up Solves

Most specifications fail because they jump from problem to task assignment without doing the hard work of solution design first. Teams (or AI agents) receive a problem and are expected to figure out the solution themselves. This creates unpredictable results, rabbit holes, and scope creep. Shape Up's answer is to do enough solution design upfront that the executor can be confident about the scope and approach, while leaving enough flexibility for the executor to make implementation decisions.

For AI agents, this is especially relevant: an agent handed a vague goal will wander. An agent handed a shaped problem with a clear solution sketch, explicit rabbit holes identified, and firm no-gos will execute much more reliably.

### The Five Pitch Elements

Shape Up's deliverable is a "pitch" — the specification handed to the team. Every pitch has five elements: ([Shape Up, Basecamp](https://basecamp.com/shapeup/1.5-chapter-06))

**1. Appetite.** How much effort (time/compute/tokens) is this worth? The appetite is a constraint on the solution, not an estimate of required effort. This is a critical shift in thinking. Rather than asking "how long will this take?", you decide upfront "how much are we willing to invest?" The solution must fit within the appetite. Applied to AI: how many LLM calls? How many agent steps? How much context? Setting an explicit appetite prevents scope creep by creating a forcing function.

**2. Problem.** A description of the real problem, from the user's or stakeholder's perspective. Not a list of features. Not a proposed solution. The raw problem that needs solving. The point is that you can't evaluate whether a solution is good without knowing what it's solving for.

**3. Solution.** A rough sketch — not a wireframe, not a detailed spec — of the core elements of the approach. The shape of the solution. "Rough" is intentional: you want to communicate direction without locking in implementation details the executor should handle.

**4. Rabbit holes.** The known risks, open questions, and traps that the executor might fall into. By identifying these upfront, you prevent the executor from discovering them mid-execution and either getting stuck or making a bad choice under pressure. For AI agents, rabbit holes include: edge cases the model might handle poorly, tools the agent might incorrectly invoke, third-party dependencies with unclear behavior.

**5. No-gos.** Explicit exclusions. What this solution intentionally does not do. This is perhaps the most valuable element of a pitch for AI work, because it prevents the model from "helpfully" expanding scope in directions that weren't intended.

### How Shape Up Prevents the Most Common AI Failure Mode

The most common failure mode when giving AI agents complex tasks is underspecification of scope — the agent doesn't know what to do when it reaches a decision point, so it guesses. Shape Up's solution is to *preemptively address the decision points* — identifying the rabbit holes before you hand off the task, so the agent has explicit guidance when it reaches them.

This requires upfront thinking, which is the uncomfortable part. But as Singer writes, the alternative is giving a half-baked idea to a team and letting them figure it out — which leads to unpredictable results, scope creep, and wasted effort. The investment in specification quality happens at the cheapest possible time: before execution begins.

---

## 9. The Decomposition Problem — Atomic vs. Holistic Tasks

Task decomposition is the practice of breaking a complex goal into a sequence of smaller, independently executable sub-tasks. It is one of the most powerful tools in AI agent design — and one of the most misused. Knowing when to decompose and when to keep a task holistic is as important as knowing how to decompose.

### Why Decomposition Exists

LLMs have limited "attention" within a single context. Very complex, multi-part tasks tend to produce worse results than simpler, focused ones — the model loses track of constraints, drops requirements, or optimizes for one part at the cost of another. Decomposition is the engineering solution: break the big task into small tasks, each of which can be executed reliably, and assemble the results.

Research at Amazon Science found that "task decomposition using multiple smaller models can make AI more affordable" — smaller, focused calls to smaller models can outperform a single expensive call to a large model for many task types. ([Amazon Science: Task Decomposition](https://www.amazon.science/blog/how-task-decomposition-and-smaller-llms-can-make-ai-more-affordable)) The principle is that specificity and focus trade off against generality and flexibility, and for structured tasks, focus wins.

### The Cost of Decomposing Too Much

The trap is over-decomposition. The 2024 TDAG research paper found that "excessive decomposition can increase complexity and coordination overhead, and risks sacrificing the novelty and contextual richness that LLMs can provide by capturing hidden relationships within the complete context of the original task." ([TDAG: Multi-Agent Task Decomposition, arXiv](https://arxiv.org/abs/2402.10178))

The classic example: decomposing a creative writing task into "write a topic sentence," then "write the body," then "write a conclusion" will produce a worse piece of writing than simply asking for the piece whole. The holistic context is part of what makes the output good. Breaking it up breaks the coherence.

Similarly, in multi-agent pipelines, decomposition introduces coordination overhead: hand-off points where context can be lost, where mismatched assumptions between steps can compound, and where errors in one stage propagate to subsequent stages. Each decomposition boundary is a potential failure point.

### The Decision Framework: When to Decompose

Decompose when:
- The task has genuinely independent sub-parts (results from step A and step B don't affect each other)
- Different steps require different tools, models, or expertise
- The aggregate task is too large to fit meaningfully within a context window
- The task requires different reasoning modes at different stages (e.g., research vs. synthesis vs. editing)
- You need a human or automated checkpoint between stages

Keep holistic when:
- The quality of the output depends on coherence across the whole (creative writing, strategic analysis)
- The steps are heavily interdependent and the model needs global context to make each local decision
- The task is genuinely atomic (you can't break it without losing the essential character of the task)
- The coordination overhead of decomposition exceeds the benefit

### Granularity: The Right Level of Specificity

The TDAG research found that the right granularity is "specific enough to be actionable by the LLM or a tool but not so fine-grained that the plan becomes overly long." This is inherently context-dependent, but a useful heuristic: each sub-task should be completable in one focused LLM call without losing important global context.

Represent dependencies between sub-tasks explicitly. A Directed Acyclic Graph (DAG) representation — where sub-tasks are nodes and dependencies are directed edges — makes it clear which tasks can run in parallel and which must wait on others. This also makes the specification more debuggable: when something goes wrong, you can trace back along the dependency graph to find the source.

---

## 10. Failure Mode Catalog — What Goes Wrong with Unclear Specs

The research literature across requirements engineering, AI alignment, and production LLM systems has converged on a set of recurring failure modes. Understanding these patterns lets you audit your specifications against the most common causes of failure before executing them.

### Failure Mode 1: Lexical Ambiguity

A word in the spec has more than one meaning, and the AI picks the wrong one. This is perhaps the most common and most invisible failure because it doesn't look like a failure — the output is coherent and well-formed, it just addresses the wrong interpretation.

**Example from requirements engineering research:** "The admin can delete any user account or data activities." Does this mean the admin can delete accounts AND data activities, or delete accounts OR (separately) manage data activities? Two plausible readings, neither of which is obviously wrong. ([Research on Requirements Ambiguity, ResearchGate](https://www.researchgate.net/figure/Examples-of-ambiguous-software-requirements-that-lead-to-incorrect-development_tbl2_372483994))

**In AI prompting:** "Summarize the recent changes." "Recent" could mean the last day, week, sprint, quarter, or year. The model picks one and proceeds.

**The fix:** Operationalize every relative term. Replace "recent" with "from the last 7 days."

### Failure Mode 2: Semantic Underspecification

The specification is syntactically clear but semantically incomplete — the words are unambiguous, but the concept they refer to hasn't been fully defined.

**Example:** "The system should support large files." "Large" is semantically vague. Large for this domain might mean anything from 1MB to 1GB depending on context. The spec reads as complete, but it contains a definitional gap.

In AI prompting, semantic underspecification often manifests as unspecified edge cases. The main case is described but the boundaries aren't. The model handles the main case fine and produces unpredictable behavior at the edges.

**The fix:** Add explicit boundary definitions. "Large files: files between 10MB and 500MB. Files above 500MB should produce an error message, not be processed."

### Failure Mode 3: Conflicting Constraints

Two requirements exist in the spec that cannot both be satisfied simultaneously, and the AI must silently choose one. The failure is invisible: the output satisfies one requirement and violates the other, but the violation may not be obvious unless you're looking for it.

**Example:** A spec that says "be comprehensive" and also "be concise" without defining the priority order. The model will optimize for one at the expense of the other, and you won't know which until you read the output.

**The fix:** Make constraints explicit and ordered. "Priority order: accuracy first, completeness second, conciseness third. In cases of conflict, prefer the higher-priority attribute."

### Failure Mode 4: Missing Preconditions

The spec assumes a starting state that may not always be true, but doesn't say so. The AI performs correctly when the precondition is met and fails confusingly when it isn't.

**Example:** A customer support agent spec that assumes the customer's account information is already in the context. When that information isn't present, the agent hallucinates it or fails to handle the missing data gracefully.

**The fix:** Explicitly list preconditions: "Before starting, verify that the following are present in context: customer ID, account tier, and last-interaction date. If any are missing, request them."

### Failure Mode 5: Underspecified Scope (Scope Creep)

The spec describes what to do but not where to stop. The AI extends its work beyond what was intended, making decisions that weren't authorized.

This is the analogue of scope creep in project management: "Scope creep often occurs because the project team started with vague requirements. When project goals are not clearly articulated, stakeholders may have different interpretations of what project success looks like, creating a vacuum that is quickly filled with new, often conflicting requirements." ([PMI: Scope Creep](https://www.pmi.org/learning/library/controlling-scope-creep-4614))

In AI agents, scope creep looks like an agent that decides to take additional actions it wasn't asked to take — sending emails when it was only asked to draft them, modifying files when it was only asked to read them, or making additional API calls when it was only asked for analysis.

**The fix:** Explicit no-gos. "Do not take any action beyond producing the output described. Do not call any external APIs. Do not modify any existing files."

### Failure Mode 6: Prompt Underspecification (The CMU Findings)

The CMU 2025 research paper "What Prompts Don't Say" systematically studied a subtler failure mode: prompts that *work* most of the time but contain implicit requirements that the model guesses at. The critical finding: "Underspecified prompts are 2x as likely to regress across model or prompt changes, sometimes with accuracy drops exceeding 20%."

What makes this especially dangerous is that the failure is latent. The spec works today. You update the model version, or add a sentence to the prompt, and suddenly it breaks — not because of the change you made, but because the change disrupted an implicit assumption the model was relying on.

The researchers also found that "simply adding more requirements to a prompt does not reliably improve performance, due to LLMs' limited instruction-following capabilities and competing constraints." There is a point of diminishing returns — and sometimes negative returns — from piling on specifications. ([CMU: What Prompts Don't Say](https://arxiv.org/abs/2505.13360))

**The fix:** Proactive requirements discovery. Before deploying a spec, explicitly enumerate the requirements you *haven't* stated and evaluate whether the model is reliably handling them. The researchers propose "requirements-aware prompt optimization" — systematic discovery, evaluation, and monitoring of implicit requirements.

### Failure Mode 7: The Telephone Game in Multi-Agent Pipelines

In multi-step AI pipelines, each agent receives the output of the previous one as its input. Context can degrade across these hand-off points: the 2025 "Agent Drift" paper quantified this as "progressive degradation of agent behavior, decision quality, and inter-agent coherence over extended interaction sequences." ([Agent Drift: arXiv 2601.04170](https://arxiv.org/abs/2601.04170))

What happens in practice: Agent A produces output with certain implicit assumptions baked in. Agent B receives that output and makes different implicit assumptions about what it means. By Agent C, the original intent has been garbled — not through any single failure, but through the accumulation of small interpretive divergences at each step.

**The fix:** Explicit hand-off specifications. At each step in a pipeline, explicitly restate the goal and relevant constraints, not just pass the previous output. Write mini-specs for each inter-agent interface that make the input assumptions and output requirements explicit. Never rely on implicit continuity across agent boundaries.

### Failure Mode 8: Specification-Evaluation Mismatch

The spec describes one thing, but the evaluation criterion used to assess the output measures something different. The AI optimizes for what it can read in the spec, not for what the human actually cares about. This is the AI version of Goodhart's Law: "When a measure becomes a target, it ceases to be a good measure."

**Example:** A spec says "write a comprehensive analysis." The implicit evaluation criterion is quality of insight. But the AI optimizes for visible comprehensiveness — length, number of points covered, breadth of sources cited. The output is comprehensive and shallow, which fails the actual goal while passing the stated criterion.

**The fix:** Write the evaluation criterion before writing the spec. Ask "how would I grade this output?" and then make the grading criterion explicit in the spec.

---

## 11. Writing Techniques — Concrete Moves for Clearer Specs

This section catalogs concrete, actionable techniques for writing clearer specifications. These draw from requirements engineering, BDD, prompt engineering research, and the writing cultures of high-quality engineering organizations.

### Technique 1: Operationalize Every Relative Term

Any adjective or adverb that implies a scale without specifying a point on that scale is a precision risk. Replace relative terms with measurable criteria.

| Weak | Strong |
|------|--------|
| "Be concise" | "Respond in under 150 words" |
| "Respond quickly" | "Response time under 3 seconds" |
| "Be thorough" | "Cover all 5 criteria listed below" |
| "Handle large inputs" | "Handle inputs up to 50,000 tokens" |
| "Recent data" | "Data from the last 30 calendar days" |
| "Professional tone" | "Match the tone of the examples provided" |

### Technique 2: Lead with Examples, Not Just Instructions

Abstract instructions are inherently ambiguous because they leave interpretation to the model. Concrete examples constrain interpretation by showing the intended output directly. This is the core insight of Gojko Adzic's *Specification by Example*: "The traditional approach of documenting requirements in lengthy, static documents is not effective. Instead, stakeholders use concrete examples to illustrate and validate the desired behavior."

In prompt engineering, this maps to few-shot prompting — but the deeper principle is that *any* concrete example you can provide alongside an instruction narrows the interpretation space toward your intent.

**Before:** "Format the output as a structured report."

**After:** "Format the output as a structured report. Example: [provide one actual example of a correctly formatted report]."

### Technique 3: Define Your Domain Glossary Inline

Borrowed from DDD's ubiquitous language principle: at the top of any specification that uses domain-specific or ambiguous terms, include an explicit definition section.

```
Definitions for this spec:
- "Customer": a user who has completed at least one purchase
- "Active": a customer who has logged in within the last 90 days
- "At-risk": an active customer who has not purchased in the last 60 days
- "Churned": a customer who was active 6 months ago but has not purchased in the last 6 months
```

This technique collapses the most common class of lexical and semantic ambiguity before it can propagate into the output.

### Technique 4: Write the No-Gos First

Before finalizing a spec, ask: "What would a reasonable AI do with this that I don't want?" and "What would a reasonable human think is in scope that isn't?" Write explicit no-gos for every answer.

The act of writing no-gos forces you to think about the boundaries of your specification from the outside in. Most specification failures are boundary failures — the spec handles the main case but fails at the edges because the edges were never defined.

Format: "This task does NOT include: [explicit list]."

### Technique 5: Use the Pre-Mortem to Discover Unstated Assumptions

Before shipping a specification, run a brief pre-mortem: imagine the AI has produced a completely wrong or embarrassing output. What assumption did it make that caused that failure? Each answer to this question is a specification gap. Go add the explicit constraint that would prevent that failure.

This is especially valuable for finding *implicit assumptions* — the things you know but didn't say because they seemed obvious. They are only obvious to you.

### Technique 6: Write Acceptance Criteria Before the Spec

Write what "done" looks like before writing the instructions for how to get there. This mirrors test-driven development: the test (evaluation criterion) comes before the code (specification). This technique consistently catches underspecification because it forces you to think about output before you think about process.

Format: "This task is complete when: [bulleted list of testable criteria]."

### Technique 7: State the Rationale for Key Constraints

For every significant constraint in your specification, add a one-line rationale. This serves two purposes: it prevents the AI from "helpfully" violating the constraint when it seems counterproductive, and it helps future maintainers of the spec understand what they'd be changing if they modified the constraint.

"Respond in under 150 words **because** users read on mobile and drop off for longer messages."

"Do not include pricing **because** pricing requires Sales team approval and varies by customer tier."

### Technique 8: Use XML or Structural Tagging for Long Specs

For complex, multi-part specifications, structural tagging helps the AI distinguish between different elements of the spec. Anthropic's prompt engineering documentation explicitly recommends XML tags for structuring prompts with multiple components. ([Anthropic: Use XML Tags](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags))

```xml
<role>You are a senior financial analyst specializing in SaaS metrics.</role>

<task>Analyze the provided ARR cohort data and produce a retention curve.</task>

<context>The data is monthly, from 2022-2025. All values are in USD thousands.</context>

<output_format>A markdown table followed by 3-5 bullet point observations. No prose introduction.</output_format>

<constraints>
- Do not extrapolate beyond the data provided
- Flag any anomalous cohorts with a [NOTE] tag
- Do not include revenue projections
</constraints>
```

Structure makes the spec scannable for humans and more reliably parsed by the model.

### Technique 9: Write at the Right Level of Abstraction

Too abstract: the AI doesn't know what to do. Too granular: you've micromanaged every decision and the AI has no room to apply judgment where it should. Using Cockburn's sea level analogy, aim for the level where a competent human expert would understand the goal and have the judgment to handle edge cases, but wouldn't be second-guessing your intent.

A useful test: could a smart, experienced colleague execute this task correctly from only this spec, without asking any questions? If yes, it's probably at the right level. If they'd need clarification, you're too abstract. If they'd feel over-directed in ways that don't serve the goal, you're too granular.

### Technique 10: The Stripe Writing Test

Stripe's engineering culture mandates that before key decisions, the organizer must circulate a written document explaining the problem, proposed solution, and open questions. This creates a forcing function: writing disciplines thinking. Before any AI task spec is executed, write it down as if you're explaining it to a colleague. If you can't write a clear, self-contained explanation, the specification isn't ready. ([Slab: Stripe Writing Culture](https://slab.com/blog/stripe-writing-culture/))

---

## 12. Decision Frameworks — Scoping and Granularity Decisions

### When to Decompose a Task

Use this decision tree for decomposition decisions:

```
Is the task too large to execute reliably in a single pass?
├── Yes → Decompose
└── No  → Consider keeping holistic

Does the task require fundamentally different reasoning modes at different stages?
├── Yes → Decompose (research | analysis | synthesis are often separable)
└── No  → Consider keeping holistic

Do the sub-parts depend heavily on each other's outputs for quality?
├── Yes → Keep holistic (creative writing, strategic analysis)
└── No  → Decompose

Do different parts require different tools, models, or data sources?
├── Yes → Decompose
└── No  → Consider keeping holistic

Is a human or automated checkpoint required between stages?
├── Yes → Decompose
└── No  → Consider keeping holistic
```

### How to Set Appetite (Scope Constraints)

Before scoping a specification, answer four questions:

1. **What is the maximum investment this is worth?** (Time, tokens, API calls, human review cycles)
2. **What is the minimum viable output that would be useful?** (This defines the floor)
3. **What would "good enough" look like?** (This is often the right target, not "perfect")
4. **What specifically is this NOT trying to do?** (Write the no-gos before you write the spec)

The appetite should constrain the solution design. If the most elegant solution exceeds the appetite, design a different solution that fits within it.

### The PRD Structure for AI Feature Specs

When writing a Product Requirements Document for an AI feature, the structure that has emerged from best practice at companies like Google and Linear includes:

1. **Problem statement** (What user problem is this solving? With evidence.)
2. **Proposed solution** (High-level approach, not implementation details)
3. **Success metrics** (How will you measure whether this worked?)
4. **Scope** (What's included AND what's explicitly excluded)
5. **Acceptance criteria** (Specific, testable conditions for "done")
6. **Known risks and rabbit holes** (What could go wrong? How will you detect it?)
7. **Dependencies** (What other systems, teams, or data does this depend on?)

The key addition relative to traditional PRDs: the "known risks and rabbit holes" section. This is directly borrowed from Shape Up and addresses the most common failure mode in AI feature development — discovering mid-build that a core assumption was wrong.

---

## 13. Evaluation Design — Specifying What "Done" Looks Like

The evaluation criterion is the specification for the spec. If you know exactly how you would evaluate whether a task was completed correctly, you know enough to write a specification that makes correct completion achievable.

### The Evaluation First Principle

Write your evaluation criterion before writing your prompt or task specification. Ask: "If the AI produces exactly the right output, what would I see?" Then write a specification that makes that output the most natural result.

This is the AI equivalent of test-driven development. The test comes first; the implementation comes second. The advantage is the same: writing the test first forces you to be precise about what "correct" means, which catches underspecification at the cheapest possible moment.

### Types of Evaluation Criteria

**Binary criteria:** Either the output has a property or it doesn't. "The summary must not exceed 200 words." "The JSON must be valid." "Every claim must be accompanied by a source." These are the easiest to specify and test.

**Scalar criteria:** The output is rated on a scale. "The tone should be professional (1-5 scale, target: 4+)." Harder to test mechanically, but can be evaluated by an LLM-as-judge system.

**Reference criteria:** The output is compared against a reference example. "The analysis should match the structure and depth of the attached example." Powerful but requires a high-quality reference.

**Coverage criteria:** The output must include specific items. "The summary must address: [list of required points]." Useful when you know exactly what content the output must cover.

### LLM-as-Judge for Automated Evaluation

For AI-powered systems, a powerful evaluation pattern is LLM-as-judge: a second LLM call that evaluates the output of the first against the specification. This requires that the specification be precise enough to evaluate programmatically — which in turn means the specification must be precise.

The criterion for whether your evaluation design is good: could you hand this evaluation rubric to a capable LLM and have it produce consistent, reliable scores? If yes, your spec is probably precise enough. If not, the spec needs more work.

### The Definition of Done

From agile software development: the "Definition of Done" is a checklist that every piece of work must satisfy to be considered complete. It applies universally, across all work items, and creates a quality floor.

For AI systems, a Definition of Done for any output might include:
- Factual accuracy (no hallucinated facts verifiable by source checking)
- Format compliance (output matches specified format)
- Coverage (all required topics are addressed)
- Constraint satisfaction (all negative constraints are obeyed)
- Length compliance (output is within specified length bounds)

Making this checklist explicit transforms evaluation from subjective to systematic.

---

## 14. Key Takeaways for the AI Practitioner and AI PM

These are the distilled principles from across the entire body of research. They represent the highest-leverage insights for improving specification quality.

**1. Specification quality is a stability property, not a quality property.** Unclear specs don't just produce worse outputs — they produce outputs that break when anything changes. The CMU research shows underspecified prompts regress 2x as often as specified ones. Build for stability first.

**2. Completeness means self-contained. A spec that requires the reader to infer any important context is incomplete.** Before finalizing, ask: could a smart, uninformed person act correctly on this spec alone? The answer must be yes.

**3. Negative specifications are as important as positive ones.** Defining what you don't want, what's out of scope, and what behaviors are prohibited is essential for preventing well-intentioned overreach. Shape Up's no-gos are a first-class spec element, not an afterthought.

**4. Examples do more work than instructions.** A concrete example constrains interpretation space in a way that an abstract instruction cannot. When in doubt, show, don't just tell.

**5. Write the evaluation criterion first.** If you don't know exactly how you'd grade the output, you're not ready to write the spec. Evaluation-first forces precision and catches underspecification early.

**6. Shared vocabulary is a prerequisite for precision.** Borrowed from DDD: if you and the AI don't share exact definitions of your key terms, every ambiguous term is a specification failure waiting to happen. Define your domain glossary inline.

**7. The right granularity for decomposition is task-specific, but the guiding principle is: each sub-task should be completable in one focused LLM call without losing critical global context.** Don't over-decompose — holistic context produces holistic quality for holistic tasks.

**8. Identify rabbit holes before you hand off the task.** Every known risk that you don't address explicitly in the spec will be addressed implicitly by the AI, in whatever way its training suggests. Address risk upfront.

**9. Appetite is a constraint, not an estimate.** Decide upfront how much this is worth (tokens, calls, steps, time). The solution must fit the appetite. This is the forcing function that prevents scope creep.

**10. Spec quality is the highest-leverage intervention available.** You can't improve a model's intelligence by writing a better spec, but you can radically change how that intelligence is directed. A well-specified task extracts far more value from the same model than a vague one.

---

## 15. Anti-Patterns

The following are the most common specification mistakes and what to do instead.

**Anti-pattern: Solution-first specification.** Writing a spec that describes implementation steps rather than desired outcomes. The problem: it locks in one approach, prevents the AI from using better approaches, and often reflects an incomplete understanding of the goal.
*Instead:* Describe the outcome. Let the AI determine how to get there.

**Anti-pattern: "I'll know it when I see it" specifications.** Specs that describe tone, quality, or style without examples or reference points. "Make it professional" or "write something compelling" are not specifications — they're requests for the AI to guess.
*Instead:* Provide reference examples or operationalized criteria.

**Anti-pattern: Spec drift.** Updating a spec over multiple iterations without tracking which version is authoritative. Happens constantly with iterative prompting.
*Instead:* Treat specs as versioned artifacts. When you change a spec, document what changed and why.

**Anti-pattern: No-scope specification.** A spec that describes what to do but not when to stop. Results in agents that do more than asked, make unauthorized decisions, or spiral.
*Instead:* Explicit scope boundaries and no-gos are mandatory.

**Anti-pattern: Weasel words.** Using subjective descriptors ("reasonable," "appropriate," "user-friendly," "comprehensive") as if they are precise. They are not.
*Instead:* Replace every weasel word with a measurable criterion.

**Anti-pattern: Conflicting constraints without priority.** Including multiple requirements that cannot all be satisfied simultaneously, without specifying which wins when they conflict.
*Instead:* Explicit priority ordering for all constraint sets.

**Anti-pattern: Context without constraint.** Providing extensive background context without using that context to constrain the output. Context tells the AI what it's working with; constraints tell it what to do with that. Both are necessary.
*Instead:* For every piece of context you include, ask "how does this constrain the output?" and make that constraint explicit.

**Anti-pattern: Decomposing holistic tasks.** Breaking a task into atomic sub-tasks when the quality of the output depends on coherence across the whole — creative writing, strategic synthesis, nuanced judgment.
*Instead:* Keep holistic tasks holistic. Decompose only when sub-tasks are genuinely independent.

**Anti-pattern: Implicit hand-offs in multi-agent pipelines.** Passing outputs from one agent to the next without restating goal context, assuming the next agent will correctly infer the original intent from the output alone.
*Instead:* Write explicit mini-specs for every inter-agent interface. Never rely on implicit continuity.

---

## Sources

- [What Prompts Don't Say: Understanding and Managing Underspecification in LLM Prompts — CMU / arXiv 2025](https://arxiv.org/abs/2505.13360)
- [A Taxonomy of Prompt Defects in LLM Systems — arXiv 2024](https://arxiv.org/html/2509.14404v1)
- [Karl Wiegers: Software Requirements (3rd ed.) — via Bookey Summary](https://www.bookey.app/book/software-requirements)
- [IEEE 830 Software Requirements Specification Standard — IEEE Xplore](https://ieeexplore.ieee.org/document/720574)
- [Alistair Cockburn: Writing Effective Use Cases — Use Case Template](https://cis.bentley.edu/lwaguespack/CS360_Site/Downloads_files/Use%20Case%20Template%20(Cockburn).pdf)
- [Gojko Adzic: Specification by Example — gojko.net](https://gojko.net/books/specification-by-example/)
- [Eric Evans: Domain-Driven Design / Ubiquitous Language — Martin Fowler Bliki](https://martinfowler.com/bliki/UbiquitousLanguage.html)
- [Martin Fowler: Specification By Example — martinfowler.com](https://martinfowler.com/bliki/SpecificationByExample.html)
- [Ryan Singer / Basecamp: Shape Up — Write the Pitch](https://basecamp.com/shapeup/1.5-chapter-06)
- [Ryan Singer / Basecamp: Shape Up — Risks and Rabbit Holes](https://basecamp.com/shapeup/1.4-chapter-05)
- [Cucumber / BDD: Gherkin Reference](https://cucumber.io/docs/gherkin/reference/)
- [Writing Better Gherkin — Cucumber](https://cucumber.io/docs/bdd/better-gherkin/)
- [Agile Alliance: INVEST Criteria](https://agilealliance.org/glossary/invest/)
- [Anthropic: Prompting Best Practices (Claude 4)](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Anthropic: Use XML Tags to Structure Prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags)
- [Anthropic: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Google: ML Problem Framing Guide](https://developers.google.com/machine-learning/problem-framing)
- [TDAG: Multi-Agent Task Decomposition — arXiv 2024](https://arxiv.org/abs/2402.10178)
- [Amazon Science: Task Decomposition and Smaller LLMs](https://www.amazon.science/blog/how-task-decomposition-and-smaller-llms-can-make-ai-more-affordable)
- [Agent Drift: Behavioral Degradation in Multi-Agent LLM Systems — arXiv 2025](https://arxiv.org/abs/2601.04170)
- [Stripe Writing Culture — Slab](https://slab.com/blog/stripe-writing-culture/)
- [How Linear Builds Product — Lenny Rachitsky](https://www.lennysnewsletter.com/p/how-linear-builds-product)
- [PMI: Controlling Scope Creep](https://www.pmi.org/learning/library/controlling-scope-creep-4614)
- [Jama Software: Guide to Poor Requirements](https://www.jamasoftware.com/requirements-management-guide/requirements-management/guide-to-poor-requirements-identify-causes-repercussions-and-how-to-fix-them/)
- [Requirements Ambiguity Research — NumberAnalytics](https://www.numberanalytics.com/blog/ultimate-guide-requirements-ambiguity-software-engineering)
- [12-Factor Agents — DZone / MLOps Community](https://dzone.com/articles/understanding-twelve-factor-agents)
