# The AI PM Role — What It Is and How to Be Great at It

> **Note:** This file is staged here temporarily. It moves to `zenkai/pm-context/ai-pm-role.md` when the Zenkai repo is created.

---

## What an AI PM Actually Is

The AI PM role is one of the most misunderstood positions in tech right now. It sounds like "a PM who uses AI tools" — but that's not it. An AI PM is someone who owns the strategy, specification, and success of AI-powered features or systems within a product. They sit at the intersection of product thinking and AI engineering, not as an engineer, but as the person who decides what gets built, why, and how to know if it's working.

The distinction matters because AI products behave fundamentally differently from traditional software. A traditional feature does exactly what the code says. An AI feature is probabilistic — it produces different outputs from the same input, it degrades in subtle ways when models change, it fails silently in ways that are hard to detect, and its quality is subjective in ways that normal QA can't catch. The AI PM's job is to build the structures that make this manageable: clear specifications, measurable quality bars, evaluation frameworks, and communication bridges to both technical teams and business stakeholders.

This is not a job for someone who just knows how to prompt. It's a job for someone who understands how AI systems work deeply enough to reason about their failure modes — and can translate that understanding into decisions, priorities, and accountability.

---

## Core Responsibilities

### 1. Owning the AI Feature Specification
The AI PM writes the specification that defines what the AI system should do. This is the central technical contribution of the role — and it's harder than it sounds.

A good AI feature spec answers:
- What is the AI supposed to do in the 80% case?
- What should it do in ambiguous edge cases?
- What should it explicitly refuse or defer?
- What counts as a successful output? How would you know?
- What does a failure look like — and how do you detect it?
- What are the constraints: latency, cost, tone, format, safety?

Without a precise spec, the engineering team builds something plausible that may or may not match the actual intent. With a vague spec, when the AI behaves unexpectedly, there's no baseline to diagnose against. The spec is the source of truth. Writing it precisely is the AI PM's most important skill.

### 2. Defining Quality — What "Good" Means for an AI System
Traditional software is binary: it works or it doesn't. AI output exists on a quality spectrum. The AI PM is responsible for operationalizing "good" — turning the vague sense that output should be "accurate," "helpful," or "appropriate" into measurable, testable criteria.

This means:
- Writing acceptance criteria for AI behavior (Given/When/Then format)
- Defining evaluation rubrics for model output
- Setting confidence thresholds and acceptable error rates
- Specifying what hallucination or quality degradation looks like and at what rate it becomes a problem
- Deciding when human review is required vs. when automated evaluation is sufficient

### 3. Managing the AI Product Lifecycle
AI features aren't static after launch. Models change, data distributions shift, and what worked at launch degrades over time without anyone touching the code. The AI PM owns the lifecycle:
- **Pre-launch:** Spec → evaluation design → testing → acceptance criteria sign-off
- **Launch:** Monitoring setup, fallback behavior, escalation paths
- **Post-launch:** Ongoing quality monitoring, model update management, regression detection, iterative improvement

The delta between "we shipped this" and "this is still working" requires active management that traditional PM roles don't require.

### 4. Communicating AI to Stakeholders
AI systems are opaque and probabilistic. Explaining to a non-technical stakeholder why the AI "got it wrong" — or why improving accuracy by 5% requires 3 months of work — is a distinct skill. The AI PM is the translation layer:
- Upward: Frame AI capabilities and limitations in business language. Don't oversell, don't undersell.
- Outward: Set user expectations for AI behavior. Users who expect perfection will be frustrated; users who understand the system's nature will use it productively.
- Cross-functionally: Help engineering, design, data science, legal, and compliance teams reason about AI tradeoffs together.

### 5. Owning the Ethical and Risk Posture
AI features carry risks that don't exist in traditional software: bias, hallucination, prompt injection, privacy exposure from RAG systems, unintended behavior in edge cases. The AI PM is responsible for:
- Identifying and articulating risks before launch
- Working with legal, compliance, and security to set guardrails
- Defining what happens when the AI fails in production (fallback, human escalation, graceful degradation)
- Ensuring the system has appropriate monitoring and kill switches

---

## How AI Changes the PM Role Fundamentally

**Determinism → Probabilism.** Traditional software gives you deterministic outputs. AI gives you probability distributions. As an AI PM, you stop asking "does this work?" and start asking "how often does this work, and under what conditions does it fail?"

**Features → Behaviors.** You're not specifying features; you're specifying behaviors. The spec isn't "add a summarization button." It's "when the user clicks summarize, the AI should produce a 3–5 sentence summary that captures the main topic, preserves key named entities, and doesn't introduce information not in the original text."

**Launch → Monitor.** Shipping an AI feature is the beginning of the work, not the end. The AI PM must build the monitoring infrastructure and quality review cadence as part of the launch spec — not as an afterthought.

**Binary QA → Evaluation Design.** You can't test AI with unit tests the same way. The AI PM needs to think like a researcher designing an experiment: what's the test set, who evaluates it, what rubric, what score threshold, what do we do when we're below threshold?

**Users → Collaborators.** AI features work best when users understand how to work with them — how to phrase requests, when to trust output, when to verify. The AI PM designs the user's relationship with the AI, not just the AI's behavior.

---

## What Great AI PMs Do Differently

**They specify before they build.** The most common failure mode in AI product work is building first, then discovering the spec was wrong. Great AI PMs front-load the hard thinking: write the spec, write the evaluation criteria, write the failure mode catalog — before touching code.

**They treat prompts as product artifacts.** The system prompt is as important as any piece of code. Great AI PMs version-control prompts, document why they were written the way they were, and treat prompt changes with the same rigor as code changes.

**They know the failure modes cold.** They can articulate exactly how their AI system fails and under what conditions. They've stress-tested it, red-teamed it, and built monitoring around its known weak points.

**They resist the AI temptation.** Not every problem should be solved with AI. Great AI PMs know when deterministic logic is more appropriate, when a simpler model is better than a larger one, and when the expected quality of AI output doesn't justify the complexity it introduces.

**They build evaluation in from the start.** They don't ship and then figure out how to measure success. They define what success looks like before they build, create a test set during development, and establish ongoing quality monitoring at launch.

**They communicate in outcomes, not architecture.** They don't explain RAG to their VP. They explain "our chatbot will be able to answer questions about our product using our actual documentation, rather than making things up." The technical architecture informs the product decision; the business stakeholder hears the outcome.

---

## The Skills That Matter Most

**Specification literacy** — The ability to write precise, unambiguous descriptions of system behavior. This is the AI PM's primary technical contribution and the skill that compounds most over time. The quality of every AI system you own will be bounded by the quality of your specifications.

**Evaluation thinking** — The ability to define what "good" means and design the measurement system to detect it. This is research-adjacent thinking applied to product work.

**Technical depth without technical execution** — You need enough understanding to ask the right questions, reason about tradeoffs, and catch when engineering decisions don't match the product intent. You don't write the code, but you need to understand what the code is doing.

**Systems thinking** — AI features don't exist in isolation. They interact with data pipelines, model infrastructure, user interfaces, and downstream business processes. The AI PM thinks in systems, not features.

**Comfort with ambiguity and iteration** — AI development is less predictable than traditional software. Timelines are harder to estimate, quality is harder to pin down, and the technology changes fast. Great AI PMs embrace iteration and build processes that can adapt.

---

## What Success Looks Like in This Role

An AI PM is succeeding when:
- AI features ship with clear acceptance criteria and measurable quality bars
- Quality problems are caught before they reach users (not reported by users)
- The team has a shared, precise understanding of what the AI should and shouldn't do
- Stakeholders trust the AI PM to represent AI capabilities and limitations accurately
- AI features improve over time through deliberate evaluation and iteration, not just when something breaks
- The AI system has known, documented failure modes with explicit fallback behaviors

An AI PM is failing when:
- Requirements are vague and engineering interprets them differently than intended
- Quality problems are discovered by users rather than caught in evaluation
- The team can't articulate what the AI is supposed to do in edge cases
- Stakeholders either over-trust or under-trust AI capabilities because the communication is poor
- AI features ship and then sit unchanged because there's no evaluation process to guide improvement
