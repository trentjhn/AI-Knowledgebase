# AI PM Applications — How Each AI Concept Maps to PM Decisions

> **Note:** This file is staged here temporarily. It moves to `zenkai/pm-context/ai-pm-applications.md` when the Zenkai repo is created.
>
> This is the core PM integration file for Zenkai. For every AI concept in the knowledge base, it answers: what decisions does an AI PM make that require understanding this? What does owning this look like in practice?

---

## Prompt Engineering

**The PM's Relationship to Prompts**

Most PMs treat prompts as an engineering detail — something the team writes and the PM approves. This is wrong. The system prompt is the product specification for an AI feature's behavior. It defines persona, constraints, tone, output format, what the AI should refuse, and how it should handle ambiguity. If you don't understand how prompts work, you can't write a good spec for your AI feature, you can't evaluate whether the engineering team's prompt is correct, and you can't diagnose why the AI is behaving unexpectedly.

**PM Decisions That Require Prompt Engineering Knowledge**

- **Writing AI feature specs.** Your spec must be specific enough that it can be translated into a prompt. Vague requirements ("make the AI sound helpful") cannot be prompted. Specific requirements ("respond in 2–3 sentences, never use the first person, always cite sources") can be.
- **Reviewing prompt drafts.** You need to be able to read a system prompt and evaluate whether it matches the product intent. Is the persona correct? Are the constraints right? Are there gaps where the AI will do something you didn't anticipate?
- **Deciding on few-shot examples.** Few-shot prompting (providing examples in the prompt) is one of the most effective techniques. As the PM, you decide what behavior you want to demonstrate — the examples embody your product decisions.
- **Temperature and output format decisions.** Temperature (how creative vs. predictable the AI is) is a product decision, not just a technical one. A customer service bot should have low temperature — consistent, predictable. A creative writing assistant should have higher temperature. You need to understand this to make the call.
- **Versioning and change management.** When the prompt changes, the product behavior changes. You need prompt version control and a process for testing prompt changes before they go to production.

**Questions to Ask Your Engineering Team**
- What does the system prompt say? Can I review it?
- How are we testing prompt changes before deploying them?
- Are we version-controlling the prompts? What's the rollback process?
- What happens if the model ignores the prompt constraints?

**Red Flags to Watch For**
- "The prompt is just a few lines" — complex AI features need complex, precise prompts
- "We'll tune the prompt after launch" — prompt quality should be evaluated pre-launch
- No version history for the prompt — you've lost auditability

---

## Context Engineering

**The PM's Relationship to Context**

Context engineering is about what information goes into the model's context window — and what gets left out. This is a product decision as much as a technical one. The PM decides: what does the AI need to know to do its job? What should it remember? What background information does it need? What conversation history matters?

**PM Decisions That Require Context Engineering Knowledge**

- **Defining the AI's information scope.** What information should the AI have access to? User history? Company documentation? Real-time data? The PM defines the information architecture — what's in context, what's retrieved, what's excluded.
- **CLAUDE.md and system-level instructions.** If your team uses Claude Code or similar tools, the CLAUDE.md defines the AI's operating context. As a PM, understanding that this file shapes every AI interaction helps you think about what instructions and context are worth including.
- **Deciding what to remember across sessions.** Long-term memory for AI features is a product decision. Does the AI remember this user's preferences? Their past queries? Their role? These decisions have privacy, cost, and UX implications — all PM territory.
- **RAG scope decisions.** When building a RAG system, you decide what documents go into the retrieval index. This is information architecture: what knowledge should the AI have access to? What's out of scope? What's too sensitive to include?
- **Context compression tradeoffs.** Long conversations get expensive and degrade in quality as context fills up. The PM defines how context is managed over time — what gets summarized, what gets dropped, what's preserved.

**Questions to Ask Your Engineering Team**
- What's currently in the context window for this feature? Show me the full prompt including system instructions and retrieved content.
- How do we handle conversations that exceed the context limit?
- What user data is being included in context, and is privacy review complete?
- How does the AI's response quality change over a long conversation?

**Red Flags to Watch For**
- No clear definition of what goes in context and why
- User PII being included in context without privacy review
- Quality degradation in long sessions that nobody is measuring

---

## Reasoning LLMs

**The PM's Relationship to Reasoning Models**

Reasoning models (Claude Opus, o3, Gemini 2.5 Pro) are more capable but slower and more expensive than standard models. Choosing between them is a product tradeoff, not just a technical preference. The PM decides when the quality difference justifies the cost and latency difference.

**PM Decisions That Require Reasoning Model Knowledge**

- **Model selection for features.** For a customer service chatbot answering simple FAQs, a standard model is fine and much cheaper. For an AI feature that evaluates contract language or reasons through complex diagnoses, a reasoning model may be necessary. The PM makes this call — not because they pick the model, but because they define the quality bar that determines which model is needed.
- **Thinking effort tiers.** Reasoning models can be prompted to think more or less (low/medium/high thinking budget). More thinking = better quality but slower and more expensive. The PM defines the acceptable latency and cost envelope, which determines the thinking budget.
- **When to use reasoning models as judges.** Reasoning models are excellent at evaluating other AI outputs — "does this summary accurately reflect the source document?" Using a reasoning model as a judge in your evaluation pipeline is a product decision about evaluation quality vs. evaluation cost.
- **Communicating capability differences to stakeholders.** If you're replacing a standard model with a reasoning model, you're changing the product's cost structure and response time. Stakeholders need to understand this tradeoff.

**Questions to Ask Your Engineering Team**
- Which model are we using and why? Have we tested alternatives?
- What's the cost per query for this feature at expected scale?
- What's the P95 latency? Is that acceptable for the user experience?
- Are we using reasoning models anywhere in the evaluation pipeline?

**Red Flags to Watch For**
- Using reasoning models everywhere by default (cost will be prohibitive at scale)
- Never using reasoning models for complex tasks (false economy — quality suffers)
- No latency monitoring for model response times

---

## Agentic Engineering

**The PM's Relationship to Agents**

An AI agent is a system where the model can take actions — calling tools, browsing the web, writing and running code, sending messages — in a multi-step loop to accomplish a goal. Agents are powerful and risky. The PM's job is to define what the agent is allowed to do, what it must ask permission for, and what it must never do — then build the evaluation and monitoring to ensure those boundaries hold.

**PM Decisions That Require Agentic Engineering Knowledge**

- **Defining the agent's scope.** What tools does the agent have access to? What data? What systems? The PM draws the boundary. An agent with access to email, calendar, and CRM simultaneously has a very different risk profile than one that can only read documents. Every tool is an expansion of what can go wrong.
- **Human-in-the-Loop (HITL) design.** The PM decides which agent actions are auto-approved and which require human confirmation. This is not a binary choice — it's a graduated policy based on reversibility and impact. The agent can auto-send a draft; it must get approval before sending a final email to a customer.
- **Failure mode planning.** Agents fail in ways traditional software doesn't — they get stuck in loops, take unintended actions, misinterpret goals. The PM writes the failure mode catalog: what can go wrong, how do we detect it, what's the recovery path?
- **Cost and latency expectations.** Multi-step agent workflows are expensive. Each tool call, each model invocation costs tokens and time. The PM sets the acceptable cost per workflow and latency budget — which constrains how many steps the agent can take.
- **The orchestration vs. execution boundary.** In well-designed agent systems, there's a separation between the model (which reasons and decides) and the application layer (which validates and executes). The PM needs to understand this architecture to write specs that correctly assign responsibility.

**Questions to Ask Your Engineering Team**
- What tools does the agent have access to? What's the permission model for each?
- What happens when the agent takes an unintended action? What's the rollback?
- Are there rate limits and spend limits on agent workflows?
- What's the maximum number of steps an agent can take before requiring human review?
- How do we detect when an agent is stuck in a loop?

**Red Flags to Watch For**
- Agent has write access to production systems without approval gates
- No maximum step limit — agents can run indefinitely
- No monitoring on agent actions — you only know something went wrong after the fact
- "The agent will figure it out" — agents need precise specs, not vague goals

---

## Skills

**The PM's Relationship to Skills**

Skills are reusable instruction sets that give AI systems specialized capabilities. As an AI PM, you'll encounter skills as a way to package specific behaviors — either skills your team builds for internal workflows, or skills that shape how AI tools behave during your team's work (like Claude Code skills).

**PM Decisions That Require Skills Knowledge**

- **When to build a skill vs. a prompt.** A skill is worth building when you're doing the same thing repeatedly and re-explaining context each time. The PM decides which repeated workflows are worth formalizing into skills vs. which are one-offs.
- **Skill scope and YAML frontmatter.** The description field of a skill determines when it triggers. If it triggers too broadly, it interferes with unintended tasks. If it triggers too narrowly, it never gets used. The PM is responsible for defining the trigger criteria precisely — this is specification work.
- **Skills vs. MCP servers.** Skills encode knowledge and instructions. MCP servers provide tool access and data connectivity. When your team needs the AI to do something new, the PM decides: is this a knowledge/behavior problem (skill) or a connectivity problem (MCP)?
- **Evaluating skill quality.** How do you know if a skill is working? The PM defines the success criteria: does it trigger when it should? Does it not trigger when it shouldn't? Does following the skill produce the intended output?

**Questions to Ask Your Engineering Team**
- What skills are currently active in our AI tooling? What do they do?
- How are skills being tested before deployment?
- Is there a registry of skills being used across the team?

---

## AI Security

**The PM's Relationship to AI Security**

AI features introduce security and safety risks that don't exist in traditional software. The AI PM is the person responsible for ensuring these risks are identified, scoped, and mitigated before launch — not as an afterthought, but as part of the spec.

**PM Decisions That Require AI Security Knowledge**

- **Prompt injection risk assessment.** Any AI feature that processes user-provided text or external content (web pages, documents, emails) is vulnerable to prompt injection — where malicious content hijacks the AI's behavior. The PM decides: what content can the AI process, from what sources, and what guardrails are in place?
- **Defining what the AI should never do.** The system prompt must include explicit constraints on harmful behavior. The PM defines these constraints based on the risk profile of the feature. A coding assistant needs different constraints than a customer service bot.
- **Least privilege for agents.** Agent features should have the minimum permissions necessary to accomplish their task. The PM defines the scope of permissions needed — not the maximum possible, the minimum necessary. This is a product decision that has direct security implications.
- **Communicating AI risk to stakeholders.** Legal, compliance, and leadership need to understand the security posture of AI features in business terms. The PM translates: "this feature is vulnerable to prompt injection if a user uploads a malicious document" becomes "we need to add document sanitization before launch to prevent the AI from taking unauthorized actions."
- **Monitoring and kill switches.** Every AI feature needs a kill switch — the ability to disable it immediately if something goes wrong. The PM defines the conditions under which the kill switch should be triggered and ensures monitoring exists to detect those conditions.

**Questions to Ask Your Engineering Team**
- Has a security review been done on the AI feature? Who did it?
- What external content can the AI process? How is it sanitized?
- What's the kill switch process for this feature?
- Are agent permissions scoped to the minimum needed?
- Is there an audit log of AI actions?

**Red Flags to Watch For**
- "Security will review after launch" — AI security review must happen pre-launch
- Agent has permissions that aren't needed for its stated purpose
- No audit log — you can't investigate incidents without one
- No monitoring on AI output — you only know about harmful outputs when users report them

---

## AI System Design

**The PM's Relationship to System Architecture**

You don't design the system, but you make decisions that determine the system's architecture. Knowing the major patterns helps you understand what your team is proposing, evaluate tradeoffs, and communicate decisions upward.

**PM Decisions That Require System Design Knowledge**

- **Choosing the right architecture pattern.** Should this feature be a simple API call? A RAG system? An agent? A model cascade? Each choice has different cost, latency, quality, and complexity tradeoffs. The PM defines the quality bar and constraints — the engineering team proposes the architecture — but you need to understand the options to evaluate the proposal.
- **Deciding when AI is the right tool.** Not every feature should be AI-powered. If a rule-based system does the job reliably and cheaply, use it. The PM applies the AI vs. deterministic decision framework: is the input space too varied for rules? Does the task require judgment? Is expected quality good enough? Only if yes to these should you use AI.
- **Setting latency and cost requirements.** System architecture decisions are heavily influenced by latency and cost constraints. If you require sub-100ms responses, that rules out reasoning models and multi-step agents. These constraints belong in the spec.
- **Fallback architecture.** What happens when the AI fails? A caching layer, a simpler model fallback, a human escalation path — these are product decisions that shape system architecture.
- **Observability requirements.** The PM defines what needs to be monitored. Latency, error rate, quality scores, cost per query — these go into the launch spec, not the post-launch wishlist.

**Questions to Ask Your Engineering Team**
- Why this architecture over alternatives? What are the tradeoffs?
- What does fallback behavior look like when the AI fails?
- What are we monitoring in production?
- What's the cost per query at current scale? At 10x scale?

---

## Specification Clarity

**The PM's Relationship to Specification**

This is the AI PM's core skill. Everything else in this document requires good specification to be effective. A PM who can write precise, unambiguous, executable specifications for AI systems is more valuable than one who can't — because the quality of the spec determines the quality of everything built from it.

**PM Decisions That Require Specification Knowledge**

- **Writing AI feature specs.** The seven properties of a good spec: unambiguous, complete, verifiable, consistent, prioritized, feasible, traceable. Every AI feature spec should be evaluated against these.
- **Acceptance criteria as the quality bar.** "The AI should be helpful" is not acceptance criteria. "Given a user question about a product feature, when the question matches content in the knowledge base, then the AI responds with an answer that: (a) directly addresses the question, (b) cites the source document, (c) is under 200 words" — that is acceptance criteria.
- **Failure mode catalog.** Before building, enumerate how the AI can fail. What happens when it hallucinates? When it refuses a valid request? When the user's query doesn't match the knowledge base? Specifying failure modes forces you to think through edge cases and design explicit fallback behaviors.
- **Constraint architecture.** Specify not just what the AI should do but what it must never do. Negative specifications are as important as positive ones. "The AI must not speculate about competitor pricing" is a constraint that must be in the spec.
- **Decomposition.** Break complex AI tasks into atomic, independently evaluable steps. "Summarize, then extract key entities, then check for accuracy" is better than "intelligently process the document" — because each step can be tested and improved independently.

**How Good Specification Prevents Common AI Failures**
- Vague spec → ambiguous prompt → inconsistent behavior → hard to debug
- No acceptance criteria → no quality bar → no way to know if it's working
- No failure modes → no fallback → users see raw AI errors
- No constraints → AI does something unexpected → stakeholder incident
- Good spec → precise prompt → testable behavior → debuggable failures → maintained quality over time
