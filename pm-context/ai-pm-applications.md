# AI PM Applications — The PM Integration Layer

> **Purpose:** For every major AI concept in this knowledge base, this file answers: what does an AI PM need to know about this, what decisions do they own, and what does owning it actually look like?
>
> **How this file is used:** Zenkai combines the technical AI explanation (from the main KB files) with this file to generate PM-contextualized learning. Read this alongside the primary domain file, not instead of it.

---

## How to Use This File

Each section maps to a KB domain. For each domain you're learning, read the technical file first, then come back here to translate that knowledge into PM decisions and actions. The structure is consistent across all 8 domains:

- **What this means for your role** — how it shows up day-to-day
- **Decisions you'd own** — the specific calls that require understanding this
- **Questions to ask your engineering team** — how to engage technically without writing code
- **How to evaluate it** — what good looks like vs. red flags
- **Specification angle** — how to write a clear spec for a system that uses this concept

---

## 1. Prompt Engineering

**Primary KB file:** `prompt-engineering/prompt-engineering.md`

### What this means for your role

You are not writing prompts. But you are the person deciding what outcome a prompt needs to produce, what constraints it must respect, and what "good" looks like when the prompt executes. The actual prompt text is an implementation detail — your job is to specify the behavior precisely enough that any competent prompt engineer (or AI) can build something that works.

Prompt engineering shows up for you in a specific, recurring scenario: you're reviewing a demo or a draft of an AI feature, and the output isn't right. You need to be able to say *why* it isn't right in a way that's actionable — not just "this doesn't feel right" but "the model is hallucinating because it has no grounding data" or "the tone is wrong because the system prompt doesn't constrain formality." That diagnosis requires knowing what the levers are.

The other scenario is tradeoff conversations. Your engineering team will tell you that adding more examples makes the prompt more reliable but increases token costs by 40%. You need to understand what they're actually saying well enough to make that call.

### Decisions you'd own

**Tone and persona constraints.** If your AI feature has a voice — a customer service agent, an in-app assistant, a copilot — you define that voice and translate it into constraints that go into the system prompt. "Friendly but not casual. Professional but not stiff. Never more than 3 sentences per response." These constraints are yours to define; engineering implements them.

**Temperature and reliability tradeoffs.** A high-temperature setting produces creative, varied outputs. A low-temperature setting produces consistent, predictable ones. For a customer-facing feature that needs to be reliable, you'll push for low temperature. For a brainstorming tool, higher temperature serves the user better. You make this call based on what the user actually needs.

**Whether to use few-shot examples.** Few-shot prompting (giving the model 3-5 examples of good input/output pairs) significantly improves output quality and consistency, but it increases token costs and requires maintaining an example library. You decide whether the quality lift is worth the cost. This is a business decision disguised as a technical one.

**When to invest in prompt iteration vs. architectural change.** If a prompt keeps producing bad outputs, the team has two paths: iterate on the prompt (cheap, fast) or change the architecture (expensive, slow). You own the prioritization call. Knowing that CoT (Chain of Thought) prompting alone can eliminate whole categories of reasoning errors tells you when prompt iteration still has runway.

**Prompt version control and documentation policy.** Prompts are code. If your team treats them like ephemeral config — no versioning, no documentation, no rollback path — you'll have no idea what changed when outputs degrade. You set the standard for how prompts are managed in your product.

### Questions to ask your engineering team

- "Walk me through what's in our system prompt right now. What role, what constraints, what output format?"
- "Have we tested this with zero-shot vs. few-shot? What did we see?"
- "What temperature are we running at? What happened when you tried higher or lower?"
- "If the model starts giving bad answers after a model update, how do we know which prompt version was in place?"
- "How are we documenting prompt changes over time? Is there a changelog?"

### How to evaluate it

**Good:** The prompt has a clear persona, a constrained output format, explicit instructions for edge cases ("if the user asks about X, respond with Y"), and a version history. The team can tell you what happens when inputs are ambiguous. Outputs are consistent across runs.

**Red flags:** Nobody can tell you exactly what's in the production system prompt. The team is iterating prompts in a shared doc with no version control. Output quality varies dramatically between runs with identical inputs. The model sometimes produces completely off-topic responses with no fallback handler.

### Specification angle

When writing a spec for a feature that uses prompting, include:

- The persona: who is the AI pretending to be, and what are the behavioral constraints on that persona?
- The output contract: exact format the response must follow (JSON schema, max length, specific fields)
- Edge case handling: what happens when the user asks something the AI shouldn't answer? What's the refusal behavior?
- Quality bar: example of a great response and example of an unacceptable response, both for the same input
- Token budget: is there a cost constraint that limits prompt length or response length?

---

## 2. Context Engineering

**Primary KB file:** `context-engineering/context-engineering.md`

### What this means for your role

Context engineering is the discipline of deciding what information the AI gets access to, in what order, and in what format. Every AI feature you build is really an information architecture problem — the model is only as useful as the context you put in front of it.

This shows up constantly. You're building a customer support AI: what customer history does it need? What product documentation? What prior conversation turns? How much fits in the window before you start degrading? These are your decisions. Engineering can implement the retrieval pipeline, but you have to define what information matters and why.

The PM-specific framing: context is user data that creates value. Your instinct is to give the AI more — more history, more documents, more customer signals. Context engineering tells you that "more" doesn't linearly improve output and can actually hurt it. There's an optimal information density, and you're responsible for defining it.

### Decisions you'd own

**What user data surfaces in the AI's context.** In a fintech app, does the AI see transaction history? Account balance? Past support interactions? You own the data policy for the AI layer, not just as a privacy/legal question but as a product design question. What context does the AI need to be genuinely useful vs. what context adds noise?

**Memory architecture.** You define whether the AI "remembers" across sessions (long-term memory) or starts fresh every time. This is a product decision with engineering implications: long-term memory requires a storage layer, retrieval logic, and a data retention policy. Do users expect the AI to remember them? Does remembering make the product better or creepier?

**Context window budget allocation.** In a complex AI feature, context is finite. If you're putting documentation in, you're taking space away from conversation history. If you're putting detailed system instructions in, you're reducing space for tool outputs. You decide the priority order. This is a product requirements conversation: "We need the last 10 conversation turns plus the user's account summary, and the system prompt must fit in 2,000 tokens. What has to give?"

**RAG scope.** If your AI pulls from a document corpus (product docs, knowledge base, prior tickets), you decide what's in that corpus. An outdated knowledge base that includes deprecated features produces confident wrong answers. You own the corpus maintenance policy.

**Context freshness requirements.** Real-time data vs. cached data is a cost-latency-accuracy tradeoff. Do users need the AI to know their account status as of this second, or is data from 5 minutes ago acceptable? You make this call.

### Questions to ask your engineering team

- "What's currently in the context window when a user sends their first message? Walk me through every component."
- "What happens when the context gets too large? Does it truncate? What gets dropped first?"
- "If we add customer transaction history, how much does that grow the context? What's the cost impact per query?"
- "Are we using RAG? If so, what's in the retrieval corpus and who maintains it?"
- "How do we handle context poisoning — what if the user deliberately puts misleading information into the conversation to manipulate the AI?"

### How to evaluate it

**Good:** The team can describe exactly what's in the context for any given user interaction. There's a documented priority order for what gets dropped when context is full. The retrieval corpus is versioned and has a maintenance process. The product has a documented data policy for what user data surfaces in AI context.

**Red flags:** Nobody knows exactly what's in the context window. Increasing context size is being proposed as a fix for quality issues without analysis of why outputs are bad. The knowledge base was seeded once and never updated. Long conversations produce significantly worse responses than short ones, with no mitigation plan.

### Specification angle

When writing a spec for a feature with context requirements:

- Define the full context composition: system prompt + user data + conversation history + retrieved documents + tool outputs. Each component, its source, and its size constraint.
- Specify the fallback behavior when retrieval fails or data is unavailable. Does the AI respond from training knowledge? Does it say "I don't know"?
- State the recency requirement for retrieved data explicitly: "Account data must be no older than 5 minutes. Documentation may be cached for 24 hours."
- Define what user data the AI is allowed to surface back to the user. A common failure mode: the AI reveals system context it should not expose.

---

## 3. Reasoning LLMs

**Primary KB file:** `reasoning-llms/reasoning-llms.md`

### What this means for your role

Reasoning models (OpenAI o3, Claude 3.7 Sonnet, Gemini 2.5 Pro) are a different category of model. They work through problems step-by-step before producing an answer, which makes them significantly more accurate on complex tasks — but also slower and more expensive. As the PM, you decide when to use one.

This is a recurring architectural decision. Every time you're evaluating a new AI feature or reviewing a model selection recommendation from your team, you need a framework for this call. The cost of getting it wrong in either direction is real: using a standard model on a task that needs reasoning means bad outputs; using a reasoning model on a simple task means unnecessary latency and spend.

### Decisions you'd own

**Use reasoning model vs. standard model.** The framework for this decision: Is the task multi-step with long logic chains? Are there high-stakes consequences if the answer is wrong? Is speed the primary UX constraint? Complex tasks with high stakes justify reasoning models. Fast, simple tasks (sentiment classification, short summarization, formatting) do not.

**Latency tolerance for the feature.** Reasoning models can take 15-60 seconds. Some user interactions tolerate this (a PM writing a complex product brief, an analyst running a research query). Others don't (a customer support chat, a real-time recommendation). You set the latency budget; the model choice follows from it.

**Thinking effort tier allocation.** Reasoning models let you set how hard they think — low, medium, or maximum effort, which maps to cost and latency. Low thinking effort is fast and cheap; maximum thinking effort is slow and expensive but approaches human expert quality on hard problems. You define which tier a use case needs based on task complexity and cost sensitivity.

**Where in the pipeline reasoning belongs.** A practical pattern: use a standard model for quick, cheap operations at scale (classifying incoming items, drafting initial responses) and route only the complex, high-stakes cases to a reasoning model for final evaluation. This is the "cascade" pattern. You own the routing logic specification — what makes a case "complex enough" to escalate?

**Model evaluation criteria.** When your team runs A/B tests between a standard and reasoning model for a specific task, what metrics matter? Accuracy? User satisfaction? Task completion rate? You define the evaluation criteria before the test, not after.

### Questions to ask your engineering team

- "We're using a reasoning model here — what's the p95 latency? Have we profiled this with production-scale traffic?"
- "What was the quality difference between o3 and Sonnet on our actual test cases? Can I see the failure cases for each?"
- "What's the cost per query at scale? If we 10x the user base, is this model still viable?"
- "Are we using the thinking effort controls? What tier are we at, and have we evaluated whether a lower tier is sufficient?"
- "Is there a fallback if the reasoning model times out or errors? Does the user see a failure or does something else handle it?"

### How to evaluate it

**Good:** The team can articulate why a reasoning model is needed for this specific task (not just "it's better"). There's latency data from actual testing. The cost/query at projected scale has been calculated and is within the budget. There's a clear fallback pattern for model failures.

**Red flags:** The team defaulted to a reasoning model because it "seems more capable." Nobody has measured the actual quality difference on your specific task. Latency is handwaved as acceptable without user research. The reasoning model is used for every step in a multi-step pipeline regardless of task complexity.

### Specification angle

When writing a spec for a feature requiring a model recommendation:

- Define the task class explicitly: "This is a single-step extraction task (low complexity)" or "This requires evaluating competing business constraints across 5 dimensions (high complexity)."
- State the latency requirement: "User-facing response must complete in under 3 seconds."
- State the accuracy bar: "Error rate below 2% on the test set of 500 labeled examples."
- State the cost constraint: "Maximum $0.02 per user query at steady state."
- These four parameters together determine the model choice — not intuition.

---

## 4. Agentic Engineering

**Primary KB file:** `agentic-engineering/agentic-engineering.md`

### What this means for your role

An agent is an AI that takes actions, not just answers questions. It can search the web, write files, call APIs, send messages, spawn sub-agents, and chain multi-step operations toward a goal — autonomously. As the PM, you own the product spec for what the agent does, what it's allowed to do, when it stops to ask for human input, and what happens when it fails.

This is a fundamentally different product design challenge than traditional software. Traditional software does exactly what you programmed. An agent makes decisions. You can't enumerate every state the agent might encounter. Instead, you design its decision-making constraints: its goal, its tools, its boundaries, and its escalation paths.

The core PM responsibility in agentic products: every capability you give an agent is a product decision, not just a technical one. Adding a "send email" tool means the agent can now send emails on behalf of users. That has UX implications, legal implications, and trust implications. You own all of them.

### Decisions you'd own

**Agent scope.** One agent, one purpose. You define the scope. An agent that does "everything" fails in unpredictable ways. An agent scoped to "classify incoming support tickets and draft response suggestions" can be built, tested, and improved reliably. Scope creep in agents is a product failure, not just a technical one.

**Tool set.** Every tool you give an agent is a decision. What external systems can it call? What data can it read? What can it write or modify? Each tool adds capability and adds failure surface. You prioritize: what minimum tool set does this agent need to accomplish its goal? Start there. Don't add tools because they might be useful.

**Human-in-the-loop thresholds.** This is the most important agentic product decision. Where does the agent stop and ask a human to confirm before proceeding? Irreversible actions (deleting records, sending customer communications, processing payments) require human approval. Reversible drafting actions (creating a draft, flagging a ticket, suggesting a response) can proceed autonomously. You draw this line explicitly in the spec.

**Multi-agent architecture.** Some tasks benefit from multiple specialized agents working together — an orchestrator that plans, specialist agents that execute, a reviewer agent that checks output quality. You decide when this complexity is warranted vs. when a single agent is sufficient. More agents = more coordination cost = more failure modes.

**Error handling and recovery.** What does the agent do when a tool call fails? When it's stuck in a loop? When it encounters a case outside its spec? You define the failure taxonomy and what happens in each case. "If a tool call fails three times, surface the error to the user and stop" is a product requirement, not just an engineering detail.

### Questions to ask your engineering team

- "What's the full list of tools this agent has access to? Can it take any irreversible actions?"
- "Walk me through the HITL (human-in-the-loop) gates. What triggers a pause for human approval?"
- "What happens when the agent is halfway through a task and encounters something outside its spec?"
- "How do we trace what the agent actually did on a given run? If something goes wrong, how do we debug it?"
- "What's the maximum number of steps an agent takes in a single run? Is there a hard limit?"

### How to evaluate it

**Good:** The agent has a clearly defined scope document. Every tool is explicitly listed with a rationale for its inclusion. HITL gates are defined for all irreversible actions. There are trace logs for every agent run. The team has run red-team tests on what happens with adversarial inputs.

**Red flags:** The agent has access to tools "just in case." HITL behavior is undefined or left to the agent's discretion. Nobody has tested what happens when the agent encounters an unexpected state. Agent runs have no trace/audit trail. The agent's behavior on edge cases was discovered in production.

### Specification angle

An agent spec is more than a product brief. It needs to function as the agent's operational handbook. A well-formed agent spec includes:

- **Goal statement:** One sentence. What the agent is trying to achieve.
- **Tool inventory:** Every tool, with a one-sentence description of when it should be used.
- **HITL gates:** Explicit list of action types that require human confirmation before execution.
- **Out-of-scope handling:** What the agent does when it encounters a task outside its spec. Does it escalate? Refuse? Stop?
- **Failure protocol:** What happens when tools fail, when the agent loops, when confidence is low.
- **Evaluation criteria:** How you'll know the agent is performing correctly. Specific metrics, not vibes.

---

## 5. Skills (Agent Skills)

**Primary KB file:** `skills/skills.md`

### What this means for your role

A skill is a portable, reusable package of agent behavior. It solves a specific problem: AI agents have no memory. Without skills, every user interaction starts from scratch — the agent doesn't know your team's naming conventions, your approval process, your brand voice, or how to use a specific tool correctly. Skills codify that institutional knowledge and make it persistent.

From a product perspective, skills are features. When you decide to package a workflow as a skill, you're deciding to make that workflow consistent, portable, and maintainable as a product artifact. This is a product decision, not just a developer convenience.

### Decisions you'd own

**What gets packaged as a skill vs. inline instructions.** Not every workflow needs a skill. One-off tasks, highly dynamic processes, and tasks that vary significantly by user context are poor skill candidates. Repeatable, consistent workflows with stable steps are excellent skill candidates. You make the call on what to standardize.

**Skill scope and granularity.** A skill scoped too broadly does everything poorly. A skill scoped too narrowly requires users to chain too many skills together. The right granularity: one skill handles one coherent workflow. "Draft a customer support response" is a skill. "Do all customer support tasks" is not.

**Skill ownership and maintenance.** Skills are living product artifacts. When a workflow changes, the skill must change. When a tool it depends on gets updated, the skill must be tested and potentially updated. You define who owns each skill and what the update process looks like. Without this, skills become outdated and start producing wrong behavior silently.

**Skill distribution policy.** Who gets access to which skills? A skill with access to sensitive customer data should not be broadly distributed. A skill for internal team productivity can be shared across the org. You define the distribution and access policy.

**When a skill becomes a product feature.** Sometimes a skill that started as an internal tool has product potential. It works reliably enough and solves a real user problem that it could be offered to customers. You identify these opportunities and own the decision to productize.

### Questions to ask your engineering team

- "What skills are currently in production? What workflows do they cover?"
- "What triggers a skill to load? How does the agent know when to use which skill?"
- "If a skill is outdated, what happens? Does it fail silently or surface an error?"
- "How do we test a skill before shipping it? What does the QA process look like?"
- "Is there a skills catalog that documents all available skills and their current state?"

### How to evaluate it

**Good:** There's a maintained skills catalog with owner, version, and last-validated date for each skill. Skills have explicit test cases that run on every update. The YAML frontmatter accurately describes when the skill should be invoked. Users can reliably predict what the skill will do.

**Red flags:** Skills were created but nobody maintains them. The team doesn't know which skills are currently deployed. Skills load based on vague keyword matching with no clear invocation criteria. Users encounter inconsistent behavior because the skill conflicts with other loaded context.

### Specification angle

When specifying a new skill:

- **Invocation trigger:** Exactly what user intent or context should activate this skill? Be specific enough to avoid false positives.
- **Workflow steps:** Every step the skill executes, in order, with decision points marked.
- **Tool dependencies:** Every external tool or MCP integration the skill requires.
- **Output contract:** What does a successful skill execution produce? What format? What must it include?
- **Failure behavior:** If the skill cannot complete (missing tool, insufficient data), what does it communicate to the user?
- **Owner and review cadence:** Who maintains this skill and how often is it reviewed for accuracy?

---

## 6. AI Security

**Primary KB file:** `ai-security/ai-security.md`

### What this means for your role

You own the risk posture of your AI feature. Not security engineering — they implement the controls. But you define the threat model, you decide which risks are acceptable vs. which require mitigation, and you sign off on the feature before it ships. If your AI feature gets exploited and causes harm to users or the business, the spec you approved is part of the chain of accountability.

AI security is different from traditional software security in one critical way: the attack surface includes the model's behavior, not just system access controls. An attacker can manipulate an AI feature by crafting adversarial inputs — they don't need to breach a server. This means security review is part of every AI feature spec, not something that happens after the feature is built.

### Decisions you'd own

**Risk tier classification.** Every AI feature has a risk profile. A low-stakes feature (suggest a tweet) has different requirements than a high-stakes feature (approve a loan, send a customer refund, access patient records). You classify the risk tier explicitly, because that classification drives security requirements. Tier 1: low risk, no irreversible actions, no sensitive data access. Tier 3: high risk, irreversible actions possible, sensitive PII in context. The tier determines the security control checklist.

**What actions require human approval before execution.** Irreversible actions executed by an AI without human confirmation are the primary risk in agentic features. You define the human-in-the-loop gate policy as a product requirement. This is both a security decision and a UX decision.

**Data exposure policy.** What user data is the AI allowed to access? What can it surface back in responses? Can it include one user's data when responding to another? You define the data exposure boundaries in the spec, explicitly. Engineering implements them.

**Prompt injection threat model.** If your AI feature processes user-submitted content (support tickets, user messages, uploaded documents), that content can contain adversarial instructions designed to manipulate the AI. You decide: does this feature process untrusted content? If yes, you require the engineering team to implement defenses (input sanitization, content markers, sandboxing) and you verify they exist before shipping.

**Incident response protocol.** When your AI feature does something wrong at scale — generates harmful content, leaks data, takes an unintended action — what is the response? Who gets notified? Can the feature be disabled quickly? Do you have audit logs to understand what happened? You define the incident response requirements before shipping, not after an incident.

### Questions to ask your engineering team

- "Is this feature exposed to untrusted user content? Have we evaluated prompt injection risk?"
- "What are the irreversible actions this feature can take? What prevents those from being triggered by a malicious input?"
- "What user data is in the context window? Can that data be leaked back to other users through the AI?"
- "Do we have audit logs for every AI action? Can we reconstruct what happened on any given run?"
- "What's the kill switch? If this feature starts producing harmful outputs at scale, how fast can we disable it?"

### How to evaluate it

**Good:** The feature has a documented threat model. Irreversible actions require explicit human confirmation. Prompt injection testing was done before launch. There are audit logs for all AI actions. The team can describe the kill switch and has tested it.

**Red flags:** Security review was treated as a post-launch checklist item. The feature processes untrusted user content with no injection defenses. No audit logging exists. The team cannot articulate what the worst-case failure mode is. The AI can take irreversible actions without human confirmation.

### Specification angle

Every AI feature spec should include a security section with:

- **Risk tier:** Low / Medium / High, with rationale
- **Sensitive data inventory:** What data the AI accesses and what it can surface in responses
- **Irreversible action list:** Every action the AI can take that cannot be undone, with the required confirmation gate
- **Untrusted content handling:** Whether the feature processes user-submitted content and what defenses are in place
- **Audit requirements:** What gets logged, retention period, who can access logs
- **Failure mode playbook:** Top 3 failure scenarios and the response protocol for each

---

## 7. AI System Design

**Primary KB file:** `ai-system-design/ai-system-design.md`

### What this means for your role

AI system design is about choosing the architecture pattern for your AI feature. The main choice: how does the AI get the knowledge it needs to do its job? The three primary patterns are prompt engineering (put the knowledge in the system prompt), RAG (retrieve relevant knowledge at query time), and fine-tuning (bake the knowledge into the model through training). These are fundamentally different approaches with very different cost, accuracy, maintenance, and latency profiles.

You don't design the architecture — but you make the product requirements decisions that determine which architecture is appropriate. Speed? Cost? Accuracy? How often the underlying knowledge changes? What the failure modes should look like? These are your inputs. The architecture follows from them.

### Decisions you'd own

**Prompt engineering vs. RAG vs. fine-tuning.** This is the central architectural decision for most AI features, and it's a product decision more than a technical one. Prompt engineering works when knowledge fits in the system prompt and doesn't change often. RAG works when you have a large, dynamic knowledge corpus that needs to stay current. Fine-tuning works when you need the model to have deeply internalized domain behavior and the knowledge is stable. You frame the requirements; engineering selects and validates the pattern.

**Where AI belongs in the product vs. where deterministic code is better.** Not every feature benefits from AI. A discount percentage calculation doesn't need a model — it needs arithmetic. A nuanced customer complaint response does. You distinguish these clearly in specs. Using AI where a rule would do is waste; using rules where judgment is required is failure.

**Data freshness requirements.** RAG requires a retrieval corpus. Fine-tuned models require training data. Both go stale. You define how often knowledge must be updated and how quickly updates must be reflected in the model's responses. This drives architectural decisions: real-time indexing vs. nightly pipeline vs. weekly training runs.

**Fallback behavior when the AI fails or is uncertain.** AI systems fail, hallucinate, time out, and produce low-confidence outputs. You specify the graceful degradation path: deterministic fallback, human escalation, or explicit "I don't know" response. Without this, engineering defaults to the easiest answer (usually crashing or returning garbage), not the right product behavior.

**Evaluation strategy.** You cannot know if your AI system is performing correctly without evaluation. You define the evaluation criteria (accuracy, precision, recall, user satisfaction, task completion rate) and require an evaluation pipeline before the feature ships. "We'll evaluate based on user feedback" is not a spec — it's a hope.

### Questions to ask your engineering team

- "Are we using RAG, fine-tuning, or prompt engineering? What drove that choice?"
- "If we use RAG, how often is the retrieval corpus updated? What happens if it's stale?"
- "What's the eval pipeline? What metric tells us the AI is performing well? What's the current baseline?"
- "What does the user see when the AI times out or returns a low-confidence response?"
- "We said we need 95% accuracy — have we measured our baseline? What are we actually at today?"

### How to evaluate it

**Good:** The architecture choice was driven by documented requirements (knowledge size, update frequency, latency budget, accuracy bar). There's an eval pipeline with a baseline metric. The fallback path is specified and tested. The team distinguishes clearly between what AI handles and what deterministic code handles.

**Red flags:** The team chose fine-tuning before validating with prompt engineering. Nobody has defined "accuracy" for this feature. The fallback is "the AI will just try again." Evaluation is planned for after launch. The architecture was copied from a blog post without matching to actual requirements.

### Specification angle

When writing a spec for an AI feature, include:

- **Knowledge source:** Where does the AI's domain knowledge come from? Static training, system prompt, retrieval corpus, or fine-tuning?
- **Update frequency:** How often does that knowledge need to refresh? What's the staleness tolerance?
- **Accuracy requirement:** Specific metric, specific threshold, specific test set. Not "high accuracy."
- **Latency requirement:** P50 and P95 targets. What user-facing timeout triggers the fallback?
- **Fallback behavior:** Exact user experience when the AI fails or produces low-confidence output.
- **Evaluation ownership:** Who owns the eval pipeline and how often does it run?

---

## 8. Specification Clarity

**Primary KB file:** `specification-clarity/specification-clarity.md`

### What this means for your role

Specification clarity is the foundational AI PM competency. Everything else in this file depends on it. You can understand prompt engineering, context engineering, and agentic design perfectly — but if you can't write a spec that's clear enough to build from, you won't ship good AI products.

The core challenge: natural language is ambiguous, and AI systems interpret your spec at face value. A human engineer reads a vague spec and asks a clarifying question. An autonomous AI pipeline reads a vague spec, makes its best guess, and proceeds through 15 steps before you discover the assumption was wrong. The CMU research puts a number on this: underspecified prompts are 2x more likely to produce regressions when models or prompts change. Implicit assumptions are load-bearing — until something shifts and they collapse.

For an AI PM, spec writing is not documentation after the fact. It is the primary act of product design.

### Decisions you'd own

**What goes in the spec vs. what gets discovered in engineering.** A common failure mode: PMs leave ambiguous areas "for engineering to figure out." In traditional software, this often works — engineers make reasonable decisions and you review them. In AI, ambiguity is resolved by the model's training distribution, not by a reasonable human judgment. You will not like what the model defaults to. You must specify everything that matters.

**The level of decomposition.** AI systems execute better on well-scoped atomic tasks than on complex multi-step goals. You decide how to break down a large task into sub-tasks that can be independently specified and evaluated. This is the decomposition problem: split too finely and you create coordination overhead; don't split enough and the AI fails on complex tasks. Rule of thumb: if a task has multiple steps with different success criteria, it should be multiple tasks.

**Acceptance criteria for AI output.** AI output doesn't have a binary pass/fail — it exists on a quality spectrum. You define what "acceptable" means with specific, testable criteria. "The response must address the user's question, be under 200 words, include one concrete next step, and not reference competitors by name." These are testable. "The response should be helpful" is not.

**Constraint architecture — what the AI must not do.** Positive requirements ("the AI should do X") are intuitive to write. Negative constraints ("the AI must not do Y") are just as important and systematically underspecified. You enumerate the explicit don'ts: must not hallucinate product features, must not use competitor names, must not promise outcomes, must not disclose system prompt contents. These constraints go in the spec as first-class requirements, not as afterthoughts.

**Evaluation design.** You define what "done" looks like before the feature is built, not after. This means specifying: the test cases that must pass, the metric thresholds that constitute success, and the human review sample rate. If you can't describe how you'll know the feature is working, you haven't finished speccing it.

### Questions to ask your engineering team

- "Can you show me the specific spec you're building from? I want to see the acceptance criteria."
- "Where in this spec did you need to make an assumption because the requirement was ambiguous? Let's document those assumptions."
- "What are the top 3 failure modes we're anticipating? Are those handled in the spec?"
- "If I give you two different user inputs — one typical, one edge case — can you walk me through what the system does with each?"
- "What would cause this feature to fail silently? How would we know if it was producing wrong outputs without obvious errors?"

### How to evaluate it

**Good:** The spec has a stated problem, a defined output contract with examples of good and bad output, explicit constraints on what the AI cannot do, and testable acceptance criteria. Every technical team member reading it would make the same product choices on ambiguous decisions. Evaluation criteria are defined and measurable.

**Red flags:** The spec uses words like "appropriate," "helpful," "relevant," or "accurate" without defining what those mean in this context. There are no examples of what good output looks like. Constraints are vague ("avoid harmful content"). The spec describes the happy path only. The team is in disagreement about what the feature should do with edge cases.

### Specification angle

The seven properties of an executable AI spec (from IEEE 830, adapted for AI systems):

1. **Specific** — Every requirement has a single, unambiguous interpretation. "Fast" → "P95 latency under 2 seconds."
2. **Testable** — Every requirement can be verified with a concrete test case. "Helpful" → "Addresses the user's specific question as stated, includes a concrete action."
3. **Complete** — The spec covers all relevant behaviors including edge cases and failure modes. Not just the happy path.
4. **Consistent** — No requirement contradicts another. "Be concise" does not conflict with "always include all relevant context" without a resolution rule.
5. **Bounded** — The scope is explicit. The spec states what the AI will not do as clearly as what it will do.
6. **Exemplified** — At least one worked example of the expected input and the acceptable output range. For AI systems, include a "good output" example AND a "bad output" example for the same input.
7. **Evaluable** — The spec defines how success will be measured. What metric, what threshold, what test set, who evaluates.

When writing an AI feature spec, run it through this checklist before handing off. Any property that fails is a gap that will become a production bug.

---

## Cross-Domain: The PM Decision Hierarchy

When you encounter an AI feature decision, the decision hierarchy is:

1. **What does the user need?** (Product, not AI)
2. **Does AI earn its place here, or does a rule work?** (AI system design)
3. **What information does the AI need?** (Context engineering)
4. **What should the AI produce?** (Specification clarity + prompt engineering)
5. **Does the task require deep reasoning or standard generation?** (Reasoning LLMs)
6. **Does the AI take actions beyond generating text?** (Agentic engineering + skills)
7. **What are the failure modes and who could exploit them?** (AI security)
8. **How will you know it's working?** (Evaluation — lives in spec clarity and system design)

These are not sequential steps. They're a checklist you run against every significant AI product decision. If you can answer all eight with specificity, you have a complete picture of the problem and are ready to write a spec.

---

## Real-World Scenario Mappings

These scenarios show how multiple domains activate together in practice. For each scenario, the relevant PM decisions are listed.

### Scenario A: You're building a customer-facing AI support chat

**Prompt engineering:** You spec the persona ("empathetic, clear, no jargon, responds in under 4 sentences"). You define temperature (low — consistency over creativity). You require the team to maintain a few-shot example library of the top 20 support scenarios.

**Context engineering:** You decide the AI gets: last 5 conversation turns, user's account tier and plan, last 3 support ticket titles (no full text). You decide it does NOT get payment history (unnecessary, privacy risk). You require real-time account status (freshness requirement).

**Specification clarity:** You write acceptance criteria: "The AI must correctly identify the issue category in 90% of test cases. It must never reference internal system names or raw database IDs. It must offer a concrete next step in every response."

**AI security:** The AI processes user-written messages (untrusted content). You require prompt injection defenses. You flag that users might try to manipulate the AI into revealing other users' data, and specify that account data retrieval is always scoped to the authenticated user.

**AI system design:** You start with RAG + prompt engineering before fine-tuning. The knowledge corpus is the support documentation, updated nightly. Fallback: if AI confidence is low (no relevant doc retrieved), escalate to human agent.

---

### Scenario B: You're shipping an internal AI analyst copilot

**Reasoning LLMs:** The copilot is used for complex data analysis and scenario modeling — multi-step logic, competing constraints. You specify a reasoning model (Claude 3.7 or equivalent) for the core analysis task. For quick lookups and formatting, you route to a standard model to cut cost and latency.

**Agentic engineering:** The copilot can query internal databases, pull from data warehouses, and generate charts. You define HITL gates: querying a database is autonomous, but modifying any data requires explicit human confirmation. You limit tool access to read-only by default with a write-access upgrade path that requires manager approval.

**Skills:** The team bundles the standard analysis workflow as a skill — specifying the sequence of steps for a standard business review (pull data, validate against last period, flag anomalies, draft commentary). The skill is owned by the analytics team lead and reviewed quarterly.

**Context engineering:** The copilot gets the analyst's current project context, the last 3 reports they ran, and the data schema for their assigned datasets. It does not get cross-team data without explicit access grants.

---

### Scenario C: You're evaluating whether to build a new AI feature at all

**AI system design principle:** Start by asking whether the task is truly variable and judgment-dependent. If a rule can solve it, write the rule. AI earns its place when variation is the point.

**Spec clarity principle:** If you cannot write a testable acceptance criterion for the feature, you cannot build it. "The AI should help users" is not a feature spec. "The AI should identify accounts at risk of churn within the top quartile (precision > 80%) using the last 90 days of activity signals" is.

**Reasoning LLMs principle:** Defaulting to the most capable model without evaluating the task complexity is waste. Validate with the simplest model first. Upgrade only when the simpler model demonstrably fails.

**Security principle:** Before shipping any AI feature, classify its risk tier. A feature that accesses no sensitive data, takes no irreversible actions, and processes only structured system-generated inputs is Tier 1. Build that feature differently than a Tier 3 feature that accesses PII, can send external communications, and processes user-generated content.

---

## The PM Anti-Pattern Catalog

Specific mistakes AI PMs make. These show up repeatedly across all domains.

**Shipping without evals.** Launching an AI feature with no automated evaluation pipeline means you are running a live experiment on your users. You will not know the feature degraded until users complain. Fix: define eval criteria in the spec, before a line of code is written.

**Treating prompts as ephemeral.** A prompt that took three weeks to optimize is a product asset. Changing it without version control is equivalent to modifying production code with no diff and no rollback. Fix: prompts live in version control with changelogs, same as code.

**Overcomplicating before validating.** Teams jump to fine-tuning, multi-agent architectures, and custom infrastructure before confirming the use case works with simple prompt engineering. Fix: enforce the progression — prompt first, then RAG, then fine-tuning, then agents. Each step requires evidence that the previous step was insufficient.

**Giving the agent too many tools.** Every additional tool increases attack surface and failure modes. An agent with 15 tools is harder to test, harder to audit, and harder to trust than an agent with 4 focused tools. Fix: justify each tool at spec time. If you can't state why the agent needs this tool for its specific goal, remove it.

**Underspecifying constraints.** The spec says what the AI should do, not what it must not do. Constraints are harder to think of than goals, but they are the primary source of production failures. Fix: every spec must have an explicit "must not" section alongside its "must" section.

**Conflating hallucination with feature requests.** When users say the AI "made something up," the root cause is usually a context engineering failure (the AI didn't have the right information) or a spec failure (the AI wasn't constrained from speculating). Hallucination is a symptom. The diagnosis requires checking context composition, retrieval quality, and constraint completeness. Fix: build a root cause taxonomy for quality failures before launch.

**Letting security be a post-launch audit.** AI security threats (prompt injection, data leakage, privilege escalation) exist at feature design time, not after deployment. Fix: threat model and HITL gates go in the spec. Security review happens before engineering starts, not after.

---

## Mental Models for AI PMs

These are the core intuitions to internalize. Each maps to one or more KB domains.

**"The spec is the product."** In AI, the spec is not a handoff document — it is the source of truth from which behavior is derived. A vague spec produces an AI that sometimes works and sometimes doesn't, with no clear theory of why. Write the spec as if it will be executed directly. (Specification clarity)

**"Context is the AI's entire world."** The model knows two things: what it learned in training, and what you put in the context window. If something important is not in the context, the model doesn't know it exists. Information architecture — deciding what goes in the window — is the primary design act for most AI features. (Context engineering)

**"Capabilities are liabilities."** Every tool you give an agent, every data source you connect, every action you enable — these are not just features. They are attack surfaces. They are things that can go wrong. Grant them deliberately, not generously. (AI security + agentic engineering)

**"Evals are the steering wheel."** You cannot improve what you cannot measure. AI systems degrade silently, drift over time, and behave differently on new inputs. Without a continuous evaluation pipeline, you are driving blind. Evals are not a QA step — they are an ongoing product investment. (AI system design + specification clarity)

**"Start with the simplest thing that could work."** The bias in AI product work is toward complexity. More models, more agents, more tools, more data sources. The correct bias is the opposite. Start with a single prompt and a standard model. Add complexity only when the simpler approach demonstrably fails on real user data. (AI system design)

**"The failure mode you didn't spec is the one that ships."** AI systems will encounter edge cases. The question is whether you defined the behavior in advance or left it to the model's defaults. Every undefined edge case is a product decision you made passively. (Specification clarity)

---

*Last updated: 2026-02-28*
*Paired with: KB-INDEX.md for navigation, each domain file for technical depth*
