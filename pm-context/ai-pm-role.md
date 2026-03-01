# The AI PM Role — What It Actually Is

**Table of Contents**
1. [What the AI PM Role Is and How It Differs from Traditional PM](#1-what-the-ai-pm-role-is-and-how-it-differs-from-traditional-pm)
2. [Why AI PM Is an Undersupplied Role Right Now](#2-why-ai-pm-is-an-undersupplied-role-right-now)
3. [Core Responsibilities](#3-core-responsibilities)
4. [Specification as the Primary Technical Contribution](#4-specification-as-the-primary-technical-contribution)
5. [Day-to-Day Reality](#5-day-to-day-reality)
6. [What Good Looks Like vs. What Bad Looks Like](#6-what-good-looks-like-vs-what-bad-looks-like)
7. [Common Failure Modes for New AI PMs](#7-common-failure-modes-for-new-ai-pms)

---

## 1. What the AI PM Role Is and How It Differs from Traditional PM

### The Core Shift: Probabilistic vs. Deterministic Systems

Traditional PM owns features with deterministic behavior. If a button triggers a payment, it either processes or it doesn't. The behavior is binary. You write acceptance criteria, engineering builds it, QA runs the test cases, and either the system does what was specified or it doesn't.

AI PM owns features where behavior is probabilistic. The output of an AI feature isn't a fixed result — it's a distribution of possible outputs, shaped by training, context, prompts, temperature settings, and inputs the model has never seen before. A summarization feature that works correctly 94% of the time is still producing wrong summaries 6% of the time in production, for real users, right now.

This single shift — deterministic to probabilistic — changes almost everything about the job.

**Specific differences:**

| Traditional PM | AI PM |
|---|---|
| "Does the feature work?" is binary | "Does the feature work well enough?" is a threshold decision |
| Acceptance criteria are pass/fail | Acceptance criteria are pass/fail on a distribution |
| Bugs are reproducible | AI failures are often one-off or hard to reproduce |
| A fix to one thing doesn't break something else | Prompt changes can cause unexpected regressions |
| QA closes the loop | Eval is an ongoing process, never fully closed |
| Shipped means done | Shipped means monitored |

### Model Behavior vs. Feature Behavior

In traditional PM, the PM writes requirements and engineering implements them exactly. You specify a dropdown with options X, Y, Z — that's what ships.

In AI PM, the PM writes requirements and the model interprets them within a learned distribution shaped by its training data. You write a prompt instructing the model to "summarize in plain English for a non-technical user" — and the model produces something. Whether that output actually matches your intent depends on how precisely your spec collapsed the interpretation space.

You cannot test an AI feature by exhausting inputs the way you test a traditional feature. The input space is essentially infinite. What you can do is define a representative test set, specify quality bars on that set, and monitor for drift when things change.

### Specification as Technical Work

Traditional PMs write requirements and hand them off. If requirements are vague, an engineer asks a clarifying question.

AI PMs write specifications that function as executable instructions, directly shaping model behavior. There is no engineer in between who applies judgment to fill gaps. If your spec is vague, the model fills the gap with whatever its training distribution favors — which may or may not be what you wanted.

This is why spec writing is the AI PM's primary technical contribution, not an administrative artifact.

### The Core Tension

You don't write code. But you need to understand the systems deeply enough to direct the people who do.

This means understanding:
- What a language model can and cannot reliably do
- How prompt structure affects output quality
- Why a retrieval-augmented system fails on certain queries
- What temperature and sampling parameters do to output consistency
- Why model upgrades cause regressions even when nothing in your code changed
- How evaluation sets should be constructed and what they can and can't tell you

You don't need to implement any of these things. You need to understand them well enough to write specs that account for them, evaluate outputs against them, and communicate about them with stakeholders who know even less.

---

## 2. Why AI PM Is an Undersupplied Role Right Now

Three forces are colliding:

**The build rate outpaces the PM supply.** Every company with an engineering team is shipping AI features — copilots, summarizers, classifiers, routing systems, intelligent search. The number of AI features being built is growing faster than the number of PMs who know how to manage them well.

**Traditional PM skills are necessary but not sufficient.** A strong traditional PM with zero AI intuition will underestimate how hard eval is, over-promise on model capability, write specs that leave critical edge cases undefined, and be blindsided by regressions. Companies that need AI PMs can't just hire experienced PMs and assume they'll figure it out — the skill gap is real.

**The role is still being invented.** There's no settled career path, no standard job description, no agreed-upon benchmark for what "excellent AI PM" looks like. That's a risk, but it also means the bar for being distinctively good is low. Someone who can write a precise AI spec, define an eval framework, and communicate clearly about model limitations is already ahead of most candidates claiming AI PM experience.

### What the AI PM Role Looks Like in Different Company Contexts

The title and scope vary significantly depending on company stage.

**Early-stage startup (seed to Series B):** The AI PM is often the only PM, sometimes the founder. They write specs, build prototypes, prompt-engineer directly, and evaluate outputs themselves. The role bleeds into engineering. The advantage: direct control over the full stack. The risk: no eval discipline, no regression monitoring, shipping on vibes because there's no one to enforce rigor.

**Mid-stage company (Series B to D):** The AI PM has an engineering team and usually a data scientist. Specs become formal handoff artifacts. Eval becomes a shared responsibility with a defined process. The AI PM spends more time on stakeholder communication and roadmap prioritization, less time on direct hands-on model work. Friction: alignment between what executives expect from AI features and what models can reliably deliver.

**Enterprise / large company:** The AI PM owns a specific AI feature area within a larger product. There are dedicated ML engineers, data scientists, and a separate eval team. The AI PM's job is less about doing AI work and more about directing it — setting the requirements, validating the quality bar, and managing the feature through a formal launch process. Specs are longer, reviewed more formally, and subject to legal and compliance review (especially for consumer-facing AI). Red-teaming is often a required step before launch.

### The Skill Stack an AI PM Needs

This is not about knowing how to train models. It's about knowing enough to be dangerous in the right ways.

**Must understand:**
- How language models generate outputs (probability distributions, not lookup tables)
- What retrieval-augmented generation (RAG) is and where it fails (retrieval quality, context injection)
- What prompt engineering actually means and what it can and can't fix
- What an eval set is, how it's constructed, what it measures
- The difference between precision and recall and when each matters more
- What hallucination is and why it's hard to eliminate
- What a confidence threshold does (and what it costs the user experience)
- How fine-tuning differs from prompting, and when each is appropriate

**Does not need to know:**
- How to implement a transformer architecture
- How to write training code
- How to deploy model infrastructure
- How to design a vector database schema (but should know what a vector database is and why it exists)

---

## 3. Core Responsibilities

### Owning AI Feature Specifications

The spec is the AI PM's primary deliverable. For an AI feature, a good spec includes:
- What the AI is trying to do (the task definition)
- What inputs it receives and what format they're in
- What the output looks like and what format it's in
- What "good" looks like, with concrete examples
- What "bad" looks like, with concrete examples
- What edge cases matter and how they should be handled
- What the model should do when it doesn't know or can't complete the task
- What's explicitly out of scope

Bad spec: "Build an AI assistant that helps users draft support emails."
Good spec: "Given a user's description of their problem (free text, max 500 words) and their account tier (free/pro/enterprise), generate a draft support email that: (1) addresses the stated problem specifically, (2) maintains a professional but human tone — not corporate, not casual, (3) stays under 200 words, (4) does not make commitments about resolution timelines. If the user's problem is ambiguous, generate a clarifying question instead of a draft email. Do not include generic filler like 'I hope this message finds you well.'"

The second spec produces a measurably better system — not because the engineers are better, but because the AI has a much narrower interpretation space to work within.

The structural difference: the bad spec names a goal. The good spec defines a task, a set of constraints, a set of behaviors on edge cases, and an implicit quality bar you can check. Everything the model needs to do the right thing is present in the spec itself.

### Defining Quality Bars for Model Behavior

For every AI feature, the PM must answer: what does "good enough to ship" look like? This requires defining a quality bar before evaluating outputs, not after looking at them and deciding whether you like what you see.

Quality bars are typically specified along several axes:
- **Accuracy / correctness**: How often is the output factually correct? (e.g., "correct on at least 90% of the test set")
- **Format adherence**: How often does the output follow the required format? (e.g., "JSON output parses without error on 100% of valid inputs")
- **Tone / style**: Does the output match the intended register? (Requires human judgment or LLM-as-judge)
- **Failure handling**: How does the system behave on bad inputs? (e.g., "refuses to answer out-of-domain questions in 95%+ of test cases")
- **Latency**: Is the response fast enough for the use case? (e.g., "p95 under 3 seconds")

Quality bars should be set before seeing results. Setting them after is a rationalization exercise, not an evaluation.

### Writing Acceptance Criteria for AI Systems

AI acceptance criteria differ from traditional AC in one fundamental way: they apply to a distribution, not a single output.

Traditional AC: "When a user submits an empty form, the system displays an error message."
AI AC: "When a user query is outside the defined domain (as determined by a classifier with >90% precision on the held-out test set), the system responds with a declination message, not an attempt at an answer."

The second AC requires:
1. A definition of "outside the defined domain" (the edge case is specified)
2. An evaluation method (the classifier, the test set)
3. A threshold (>90% precision)
4. A specification of the correct behavior (declination, not an attempt)

When writing AI acceptance criteria, each criterion should be:
- Tied to a specific test or eval method
- Expressed with a measurable threshold
- Clear about what the correct behavior is, not just what the wrong behavior is

### Managing the Model/Feature Lifecycle

AI features are not static. They require ongoing management:

**Prompt changes:** Changing a prompt to improve one behavior can break another. Every prompt change needs a test against the existing eval set before shipping.

**Model upgrades:** When a provider updates a model (e.g., GPT-4o to GPT-4o-mini, Claude 3 to Claude 3.5), the AI PM needs to know: does our feature still perform? A model upgrade is a regression risk event that requires eval, not just a celebration of "better AI."

**Regression monitoring:** Production AI features need ongoing monitoring. You need to know when output quality drops — ideally before users notice. This means tracking output quality metrics over time, not just at ship time.

**Data drift:** The distribution of real-world inputs changes over time. A model tuned for one period's user questions may degrade as users ask different things. Regular eval refreshes are part of the PM's operational responsibility.

### Communicating AI Capabilities and Limitations

Executives want to know if the AI feature works. The correct answer is almost never "yes" or "no."

The AI PM's job is to translate model behavior into honest, useful language for non-technical stakeholders:
- "The feature performs well on the main use case (93% accuracy on our eval set) but has known gaps on edge cases involving X."
- "This feature reduces manual review volume by an estimated 40% for straightforward cases. Complex cases still require human review."
- "We're shipping with a confidence threshold that means the AI will decline to answer when it's uncertain. Users will see this for about 12% of queries based on current data."

The failure mode is overpromising — either because the PM doesn't understand the limitations well enough to communicate them, or because they're under pressure to hype the feature. Both lead to trust erosion when the feature underperforms against inflated expectations.

### Evaluating AI Outputs

This is different from traditional QA. Evaluating AI outputs requires:

**Human evaluation:** Structured review of a representative sample of outputs by people with domain expertise. Not just "does this look right" but scoring against specific dimensions defined in the spec.

**LLM-as-judge:** Using a separate, capable model to evaluate outputs at scale. Faster and cheaper than human eval, but introduces its own biases. Used for large-scale monitoring, not final quality gates.

**Regression testing:** Running an eval set every time something changes. The eval set is a set of fixed inputs with known correct outputs (or human-rated outputs as ground truth). If a change causes performance to drop on the eval set, it doesn't ship.

**Red-teaming:** Deliberately probing for failure modes — inputs designed to break the system, expose safety issues, or trigger unexpected behaviors.

### The Three Questions an AI PM Should Ask About Every Feature

Before any AI feature ships, the AI PM should be able to answer three questions:

1. **What exactly is this system supposed to do, in a way that is testable?** If you can't write it down such that a stranger could run a test and check whether it passed, the spec is not ready.

2. **What does failure look like, and is the failure rate acceptable?** Every AI feature fails. The question is whether the failure rate is below the threshold that the product can absorb. The PM should know the failure rate and have made an active decision about whether it's acceptable, not discovered it after launch.

3. **What happens when this feature breaks in production?** Is there a human fallback? Does the UI communicate uncertainty? Is monitoring in place to catch quality drops before they become user complaints?

Teams that can't answer all three before launch are flying blind.

---

## 4. Specification as the Primary Technical Contribution

### Why Specs Are the Leverage Point

An engineering team can take a vague spec and build something. But what they build will reflect their interpretation of what you meant, not necessarily what you meant. With traditional software, that gap closes through iteration and conversation. With AI systems, that gap is often baked into the system prompt or training instructions, producing consistent wrong behavior at scale.

The economic reality: if an AI feature has 1 million user interactions per month and the spec is imprecise enough to produce wrong behavior 5% of the time, that's 50,000 bad interactions per month. A better spec, written before the feature shipped, would have prevented most of them. No amount of post-launch patching is as cheap as getting the spec right.

### What a Bad AI Spec Looks Like

Bad specs share recognizable failure modes:

**Vague success criteria.** "The AI should give helpful responses to user questions." No definition of helpful. No threshold. No examples. No way to know if you've built the right thing.

**No failure modes defined.** The spec describes what the AI should do when things go right. It says nothing about what should happen when the user asks an out-of-scope question, when the retrieved context is irrelevant, when the user's intent is unclear, or when the model is likely to hallucinate.

**Implicit constraints.** "Respond professionally." What does professional mean for this brand? Does it mean formal? Friendly? Technical? Empathetic? The spec requires a shared understanding that may not exist.

**No quality bar.** "The summaries should be accurate." Accurate is not a threshold. What percentage of summaries need to be accurate? Measured how? By whom?

**Missing edge cases.** The spec describes the happy path and only the happy path. Edge cases — short inputs, ambiguous inputs, adversarial inputs, inputs in unexpected languages — aren't defined. The model does whatever it thinks is best, which varies.

### What a Good AI Spec Looks Like

**Task definition is specific.** "Given a customer support conversation transcript (5-50 messages), extract: (1) the customer's primary complaint in one sentence, (2) the resolution status (resolved/unresolved/escalated), (3) sentiment of the final customer message (positive/neutral/negative/frustrated). Output as JSON with keys: complaint, resolution_status, sentiment."

**Success is measurable.** "The extracted complaint must match a human reviewer's extraction in 88% of cases as measured on the 200-transcript eval set. Resolution status must be correct in 95% of cases. Sentiment must be correct in 90% of cases."

**Failure modes are specified.** "If the transcript has fewer than 3 messages, return `null` for all fields and include an `error` field with value `insufficient_context`. Do not attempt to extract from insufficient data."

**Constraints are explicit.** "Do not infer intent beyond what's stated in the transcript. Do not include PII (names, account numbers, email addresses) in the `complaint` field — describe the issue category, not the specific customer's information."

**Examples ground the intent.** Include at least one example input and expected output. Include one edge case. If possible, include one example of what the output should NOT look like.

### The Relationship Between Spec Quality and System Quality

Research from CMU (2025) found that underspecified prompts — specs that leave requirements implicit — are 2x more likely to regress when models or prompts change. The implicit assumptions were doing invisible load-bearing work. When something shifted, the system broke without anyone understanding why.

A precise spec creates a stable system. It also creates a debuggable system: when the output is wrong, you can trace back to which requirement wasn't met, rather than staring at outputs and guessing.

### The Spec as a Collaboration Tool

Good AI specs aren't just instructions to a model. They're shared contracts with the engineering team, data science, design, and legal/compliance. When an AI feature behaves unexpectedly in production, a well-written spec is the reference point that lets the team determine whether the model failed to follow the spec or whether the spec failed to anticipate the case. Without a good spec, that conversation devolves into opinion.

A spec written before the feature is built also prevents scope creep by making explicit what the feature is not doing. Stakeholders who later request behavior the spec explicitly excludes can be shown that the exclusion was intentional — not an oversight.

### The Spec Review Checklist

Before finalizing any AI feature spec, run through this checklist:

- [ ] Is the task definition specific enough that an outsider could understand what the model is doing?
- [ ] Are inputs defined (format, length constraints, example values)?
- [ ] Are outputs defined (format, length, structure)?
- [ ] Is there at least one concrete example of a good output?
- [ ] Is there at least one concrete example of a bad output?
- [ ] Are the three most likely edge cases defined and assigned a behavior?
- [ ] Is there a specified behavior when the model doesn't know or can't complete the task?
- [ ] Are quality thresholds stated (e.g., 90% accuracy on eval set)?
- [ ] Is the eval method specified (what test set, who judges, how)?
- [ ] Are explicit constraints listed (what the model should not do)?

A spec that passes this checklist produces measurably better AI features than one that doesn't. This checklist is not overhead — it's the work.

---

## 5. Day-to-Day Reality

### What an AI PM Actually Does Week to Week

**Spec writing and iteration (30-40% of time).** Drafting AI feature specs, reviewing them with engineering and data science, revising based on technical constraints, updating them when requirements shift. This is the core work, more than any other single activity.

**Eval review and quality work (20-30%).** Looking at AI outputs from production or test sets. Categorizing failures. Understanding whether a degradation is systemic or a one-off. Deciding whether something is ready to ship. Writing up eval results for stakeholders.

**Stakeholder communication (20-25%).** Translating what the model can and can't do into honest, useful information for product leadership, legal, customer success, and anyone else touching the feature. Setting expectations before launch. Post-launch reporting.

**Model/feature maintenance (10-20%).** Monitoring production metrics. Responding to quality regressions. Coordinating with engineering on prompt changes. Managing model upgrade assessments.

**Research and external monitoring (5-10%).** Keeping up with model capability improvements from providers. Understanding when a new model version changes what's possible. Evaluating whether a new technique (e.g., tool use, structured outputs, chain-of-thought prompting) could improve a specific feature.

### How AI PMs Work with Engineering, Data Science, and Design

**Engineering:** The AI PM provides the spec. Engineering translates it into a working system. The collaboration is dense at spec-writing time — engineers surface technical constraints that should be reflected in the spec, the PM surfaces user requirements that engineering needs to accommodate. After ship, the PM is the primary escalation point for quality issues.

**Data science / ML:** Data science owns the model selection, fine-tuning decisions, and eval infrastructure. The AI PM sets the quality targets (what accuracy, what threshold) and signs off on whether the system meets them. The PM does not design the eval methodology from scratch but needs to understand what the eval is testing and what it's not.

**Design:** AI features often have UX implications that traditional features don't — what happens when the model is uncertain? How does the UI communicate that an output is AI-generated? What does the user do when the AI is wrong? The PM drives these decisions in collaboration with design. Design often can't answer these questions without PM input on model behavior.

### Common Friction Points

**Stakeholder expectations vs. model reality.** Executives see AI demos and expect feature parity with the demo under all conditions. Real models perform well on rehearsed demos and less well on messy real-world inputs. The AI PM's job is to set honest expectations before this gap becomes a surprise.

**Eval gaps.** Building a representative eval set is hard. If the eval set doesn't cover an important slice of real-world inputs, you'll ship thinking quality is 92% when it's actually 65% on the inputs you forgot to test. The PM should push for eval sets built from real user data, not synthetic examples constructed to be easy.

**Regression surprise.** Model upgrades, prompt changes, and retrieved context changes all introduce regression risk. Teams that don't run regression evals before shipping changes accumulate invisible technical debt — the system works until it doesn't, and no one knows why.

**Latency vs. quality trade-offs.** More capable models are slower. More sophisticated prompting (chain-of-thought, multi-step reasoning) improves quality but adds latency. The PM must make explicit calls on these trade-offs and communicate them clearly — not leave them to engineering to decide by default.

### A Realistic Week as an AI PM

**Monday:** Review production quality dashboard — any metric drops over the weekend? One feature is showing a 4% increase in format errors since the model upgrade last Thursday. File a bug, schedule an eval run with the data science team for Wednesday.

**Tuesday:** Spec review with engineering for next quarter's AI search feature. Three hours total: one hour pre-work reading the draft, one hour in the room, one hour revising based on feedback. Engineering surfaced a constraint — the retrieval system has a 2-second hard cap. The PM needs to update the latency requirement in the spec to reflect reality.

**Wednesday:** Eval results from Monday's issue. The format errors trace to a prompt change that engineering made without running regression tests. PM documents the failure, updates the process to require PM sign-off on prompt changes. Writes update for product leadership.

**Thursday:** CEO asks if the new AI summarization feature is ready to ship. PM reviews the eval results: 91% accuracy on the core use case, 74% on the edge case set. Edge cases represent an estimated 18% of queries. The PM recommends a phased rollout with a confidence threshold — if the model's confidence score is below 0.7, fall back to a manual summary request. Communicates this recommendation with the rationale.

**Friday:** Research. Two hours reading about how a competitor handled context length limitations in their AI assistant. One hour reviewing a new technique for structured output extraction that engineering proposed. Writes a short doc on whether it's worth testing.

That's a representative week. It is not glamorous. It is primarily writing, reading outputs, making calls about quality thresholds, and managing the gap between what AI can do and what everyone assumes it can do.

### How AI PM Work Is Measured

**Output quality metrics:** The primary signal. Accuracy, format adherence, user satisfaction scores on AI-touched flows. These are measured before launch (eval) and continuously after (production monitoring). A PM who can't cite the current quality metrics on their features by memory is not paying enough attention.

**Regression rate:** How often do changes — to the prompt, the model, the retrieval logic, the context window — cause previously-correct behavior to break? A low regression rate is evidence of disciplined spec and eval practice. A high regression rate is evidence of shipping without adequate testing.

**Time-to-eval:** How quickly can the team evaluate a new build against the quality bar? Teams with mature eval infrastructure can turn this around in hours. Teams without it take weeks. The AI PM is responsible for pushing toward faster eval cycles because speed of eval = speed of iteration.

**Stakeholder trust:** Tracked informally, but real. Do product leadership, customer success, and legal trust this PM's assessments of AI feature readiness? Trust is built by being accurate — calling features ready when they are, calling out gaps when they exist, and never being surprised by a quality failure in production.

**Manual fallback reduction:** For AI features that augment or replace human review (content moderation, support triage, compliance checking), is the AI actually reducing the human workload? The PM owns this metric. If the AI feature isn't reducing human work, it isn't working.

---

## 6. What Good Looks Like vs. What Bad Looks Like

### Strong AI PM Behaviors

**Writes specs before looking at model outputs.** A strong AI PM defines what good looks like — in writing, with thresholds — before asking the model to produce anything. This is the discipline that prevents post-hoc rationalization ("I like this output, so the feature works").

**Treats eval as ongoing, not one-time.** Strong AI PMs build eval infrastructure early and maintain it. They know that eval is not a step in a launch checklist — it's a continuous practice that outlives any individual feature.

**Communicates in ranges, not absolutes.** "The feature performs well on X but has known gaps on Y" is how a strong AI PM talks about model behavior. Absolutes ("the AI gets this right") are almost always wrong and erode trust when the model fails.

**Escalates capability gaps before they become stakeholder surprises.** When a model can't reliably do what the feature requires, the strong AI PM surfaces that early, defines a workaround, and sets expectations. They don't ship and hope the failures are infrequent enough to not matter.

**Understands the distinction between model failure and spec failure.** When an AI output is wrong, the strong PM's first question is "did the model fail to execute a clear instruction, or did the instruction not specify the right thing?" These require different fixes.

**Maintains a regression eval set.** The strong AI PM insists on a test set that persists across changes. Before any prompt change, model upgrade, or retrieval logic change ships, it runs against this set. If something regresses, it doesn't ship until understood.

**Knows what they don't know.** Strong AI PMs know the limits of their own AI intuition. They ask data science to explain eval methodology before signing off. They don't claim the feature is ready when the eval coverage is incomplete.

### Weak AI PM Behaviors

**Ships by vibes.** Evaluates model outputs by reading a handful and deciding "this looks good." No structured eval. No threshold. No test set. This is how teams ship features that work fine in demo and fall apart in production.

**Conflates capability and reliability.** "The model can do X" is not the same as "the model reliably does X on our users' inputs." Weak AI PMs treat a successful demo as evidence of reliable production behavior.

**Writes specs after the fact.** Documents what the system does rather than specifying what it should do. This produces a spec that describes the current behavior but doesn't create a standard to check future changes against.

**Over-promises to stakeholders.** Describes AI features in terms of their best-case behavior, not their typical-case behavior. Leads to trust erosion when the feature underperforms against the stated bar.

**Ignores failure modes.** Specs happy paths only. When users hit edge cases — short inputs, ambiguous queries, adversarial prompts — the behavior is undefined and whatever the model does by default becomes the product behavior. This is almost always worse than intentional failure handling.

**Treats model upgrades as free wins.** Fails to run regression evals when a provider releases a new model version. Ships the upgrade because "it's better" without checking whether the existing features still perform.

**Doesn't own the eval set.** Delegates eval entirely to data science. Doesn't understand what the eval is measuring or what its blind spots are. Can't explain to stakeholders what the quality bar means in practice.

---

## 7. Common Failure Modes for New AI PMs

**The demo trap.** You see the model produce a great output once and assume that output is representative. It isn't. The model's distribution of outputs is wide, and cherry-picked demos tell you nothing about production quality.

**Treating AI as a black box they can't interrogate.** New AI PMs sometimes defer entirely to data science on questions about model behavior. This works until something goes wrong and they can't explain what happened. You need enough working knowledge to ask the right questions, read eval results, and understand what "precision/recall trade-off" means for your specific feature.

**Confusing output diversity with output quality.** AI outputs vary. Not all variation is bad — some variation reflects appropriate adaptation to different inputs. New AI PMs sometimes mistake variation for inconsistency or mistake consistency for correctness.

**Setting quality bars too late.** Starting eval work after the feature is mostly built means the quality bar gets shaped by what was built, not by what users actually need. Quality bars should be set during spec writing, before any model outputs are seen.

**Underestimating edge case volume.** The "happy path" in an AI feature is often a minority of actual production traffic. Real users are unpredictable. They write typos, change subjects mid-query, ask things the spec never anticipated, and push the system in directions that weren't tested. Edge cases are not edge cases in production — they're a substantial slice of the traffic.

**Treating the spec as a one-time artifact.** Writing a spec and calling it done. Not revisiting it when model behavior or user needs shift. The spec is a living document in AI product work. When something about the system changes, the spec should reflect the updated intention.

**Chasing accuracy without understanding the denominator.** "90% accurate" means different things depending on what's in the 10%. If the 10% failures are evenly distributed, that's a manageable quality issue. If the 10% are concentrated in one critical use case, that's a product failure. New AI PMs report overall accuracy; strong AI PMs ask about accuracy by slice.

**Conflating model improvement with feature improvement.** A better model does not automatically produce a better feature. The feature's performance depends on the prompt, the retrieved context, the output parsing, and the UX that wraps the model. An AI PM who relies on provider model upgrades to improve feature quality, without also improving the surrounding system, will be disappointed.

**Not building from real user data.** Eval sets built entirely from synthetic examples or internal brainstorming miss the actual distribution of real-world inputs. Real users ask weird things, write incomplete sentences, mix languages, and trigger behaviors that no synthetic set anticipated. Push to get real user query logs into your eval set as early as possible.

---

## Related KB Files

- `specification-clarity/specification-clarity.md` — Deep reference on spec writing, the 7-property framework, acceptance criteria, and constraint architecture
- `agentic-engineering/agentic-engineering.md` (L1270-1525) — Practices section: debugging, evaluation, intent engineering, spec engineering
- `ai-system-design/ai-system-design.md` (L383-435) — Observability and metrics: how to monitor AI systems in production
- `reasoning-llms/reasoning-llms.md` — When to use reasoning models, capability boundaries, design patterns
