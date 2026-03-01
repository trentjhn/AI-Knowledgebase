# PM Fundamentals for AI Products

**Table of Contents**
1. [Product Discovery for AI Features](#1-product-discovery-for-ai-features)
2. [Roadmap Prioritization When the Technology is Probabilistic](#2-roadmap-prioritization-when-the-technology-is-probabilistic)
3. [Success Metrics for AI Systems](#3-success-metrics-for-ai-systems)
4. [PRD Structure for AI Features](#4-prd-structure-for-ai-features)
5. [Writing Briefs an Engineering Team Can Actually Build From](#5-writing-briefs-an-engineering-team-can-actually-build-from)
6. [Stakeholder Communication for AI Products](#6-stakeholder-communication-for-ai-products)

---

## 1. Product Discovery for AI Features

### How AI Feature Discovery Differs

Standard feature discovery assumes you're translating a user problem into a deterministic solution: if X happens, do Y. AI feature discovery has a prior question you must answer first: is this problem even well-suited for a probabilistic system?

That question doesn't come up in normal discovery. You don't ask "is a button the right technology for submitting this form?" But with AI, the technology choice shapes what's possible, what can fail, and what success even means. Discovery for AI features needs to resolve this before anything else.

The second difference: users can't tell you what they want from AI because they usually haven't thought in terms of AI. They can tell you their problem. They cannot tell you which parts of that problem should be automated, which should surface a suggestion, and which should stay under human control. That's your job to figure out during discovery — not theirs.

### What Problems Are Actually Solvable With AI

A useful heuristic: AI is a good fit when the task is pattern-recognition-heavy, the cost of being wrong is recoverable, and human judgment time is genuinely the bottleneck.

**Good fit:**
- Classifying inbound customer messages by intent (wrong classification → wrong routing, correctable)
- Generating a first draft the user edits (bad draft → user revises, not catastrophic)
- Surfacing anomalies in a dataset for a human to review (false positive → reviewed and dismissed, low cost)
- Ranking or reordering items based on user behavior signals (bad ranking → user scrolls, slightly annoying)

**Poor fit — keep it deterministic:**
- Applying a discount exactly as specified in a contract (wrong discount → billing dispute, compliance risk)
- Verifying that a payment amount matches an invoice (arithmetic errors → financial error, high cost)
- Displaying a regulatory disclosure at the correct moment (missing disclosure → legal violation)
- Sending a notification at a time the user explicitly set (missed time → user trust violation)

The test: if being wrong 5% of the time is acceptable because users can recover easily, AI is a candidate. If a 0.1% error rate causes real harm (financial, legal, safety), keep it rule-based.

### User Research for AI Features

The challenge: users describe their problems in task terms, not capability terms. "I want to know when something is wrong" is useful problem framing. "I want AI to detect anomalies" is not user research — that's you projecting a solution.

Techniques that work:

**Wizard of Oz testing.** Fake the AI. Have a human manually perform what the AI would do — surface the same suggestions, generate the same outputs — and observe how users react. This tells you if the output format, timing, and level of control match user expectations before you build anything. Uber used this for surge pricing UX; Airbnb used it for smart pricing suggestions.

**Shadow mode observation.** For features that augment an existing human workflow, sit with users doing the current task manually. Watch where they pause, what they look up, what they get wrong. That's where AI actually helps — not where they think AI would help.

**Explicit/implicit preference separation.** Ask users what they want explicitly, then build a prototype that gives it to them. Often they say they want full automation but use the override constantly. The gap between stated preference and actual behavior tells you where to put the human-in-the-loop.

**The "what would you do if this was wrong" question.** Underused in AI discovery. For every candidate AI output, ask users: if this was wrong, how would you know? How bad is it? How would you fix it? The answers define your fallback behavior, confidence threshold, and error UX before engineering starts.

### Scoping an AI Feature That Hasn't Been Built Before

The core problem: you can't do standard estimation because nobody knows how well the model will perform at your specific task until you run experiments.

The answer is to scope in tiers, not in one shot.

**Tier 1 — Feasibility (1-2 weeks, research + data science).**
Can the model do this task at all? Run a prototype with real data. Don't tune, don't optimize, just get a baseline number. If baseline performance is below your minimum threshold by more than 30%, either the problem is wrong or the approach is wrong. Stop before building.

**Tier 2 — MVP quality bar (2-4 weeks, small-scale build).**
With reasonable effort, can the model hit a quality bar users would accept? This is where you define the minimum acceptable quality metric (covered in Section 3) and test whether you can reach it before committing to a full build.

**Tier 3 — Productionizable scope.**
Given what we learned about model performance, what scope makes sense? This often means narrowing the initial feature: instead of AI that handles all inbound support queries, AI that handles the top 5 most common query types where performance is reliably above threshold.

The scoping decision you always have to make: do you launch a narrow feature that works well, or a broad feature that works inconsistently? Consistent > broad, almost always. Users form mental models based on their first few interactions. An AI feature that's right 95% of the time in a narrow domain is better than one that's right 70% of the time across a broad domain.

---

## 2. Roadmap Prioritization When the Technology is Probabilistic

### Why RICE and ICE Break Down

RICE (Reach, Impact, Confidence, Effort) and ICE (Impact, Confidence, Ease) assume that if you build the feature correctly, you get the impact you estimated. With AI features, you can build it "correctly" and still not get the impact — because model performance on your actual production data may be worse than lab performance, or users may not interact with the output the way you expected.

The Confidence score in RICE is meant to capture this uncertainty, but it's calibrated for engineering complexity uncertainty, not model performance uncertainty. "How confident are we this will work?" means something different when the output is probabilistic.

Specific failure modes:
- Lab accuracy ≠ production accuracy. Your eval set is never perfectly representative of real user inputs.
- Model performance degrades on long-tail cases that are common in production but rare in your eval set.
- User behavior toward AI outputs is harder to predict than behavior toward UI changes.

### How to Estimate Impact When Model Performance is Uncertain

Use ranges, not point estimates. And be explicit about which range dimension comes from model performance vs. demand.

**Example.** You're prioritizing an AI feature that auto-categorizes expense reports. Estimated reach: 50,000 reports/month. If model precision is 95%, time saved per report is 2 minutes; if precision is 80%, users spend more time correcting than they save and the feature creates negative value.

Write the impact estimate as a range tied to model performance scenarios:
- Model precision ≥ 92%: positive impact, estimated $X/month saved
- Model precision 85-92%: neutral to marginal, likely not worth shipping
- Model precision < 85%: net negative, need to gate behind a review flow

Now your prioritization decision includes a clear dependency: fund enough research time to validate which scenario you're in before committing to the full build.

**Expected value with scenarios.** When forced to rank AI features against deterministic features for the same sprint, use expected value:

EV = (P(model hits bar) × impact if good) + (P(model misses bar) × impact if bad)

This makes the model performance uncertainty explicit in the prioritization math instead of hiding it in the Confidence score.

### Managing AI Features in a Roadmap Alongside Deterministic Features

The biggest structural issue: AI features take longer to get "done" because done has a quality dimension that deterministic features don't. A button either submits the form or it doesn't. An AI categorization feature works at 73% accuracy in week 2, 81% in week 4, 89% in week 6. When do you ship?

Tactics that help:

**Define the quality bar before the sprint starts.** If you can't answer "what quality level constitutes shippable?" before engineering starts, you cannot manage an AI feature against a roadmap. Decide this in discovery (see Section 1, Tier 2). Not deciding is a choice that will cost you sprint extensions.

**Use a gated model.** Ship the AI feature to 5% of users first. Measure. If quality metrics hold at scale, expand. This de-risks committing to a full launch date before you know production performance.

**Decouple model improvement from feature improvement.** Track model quality work (collecting better training data, tuning prompts, improving retrieval) separately from product work (UI, integrations, downstream workflows). Mixing them makes the roadmap unreadable and makes it hard to know what's actually blocking quality.

### When to Cut Scope vs. Improve Model Quality

This is one of the harder PM judgment calls. Two factors drive the decision:

**Cut scope when:** the long-tail cases driving down quality are genuinely rare or low-value, and shipping for the common cases creates immediate user value. Don't spend weeks improving performance on 2% of cases when 98% already works. Ship the 98%, document the limitation, monitor the 2%.

**Improve model quality when:** the failing cases are high-stakes or high-frequency. If the 20% of cases where the model fails represent your highest-value users or your most common query type, shipping is counterproductive. You'll get adoption and then churn when the failures hit the cases that matter.

A useful forcing question: if the model performs exactly as it does in the lab today and never improves, would we ship this? If yes, scope it down and ship. If no, identify the specific improvement needed and timebox it.

---

## 3. Success Metrics for AI Systems

### Why Standard Conversion/Engagement Metrics Often Fail

Conversion and engagement metrics measure whether users do something. They don't measure whether the AI did the right thing. This gap creates a misleading picture of AI feature health.

**Examples of the failure:**

An AI email subject line generator has 70% adoption rate (users click "use suggested subject line" frequently) — but deliverability and open rates are flat. The metric says success; the actual outcome says the model is generating plausible-sounding subject lines that don't actually perform better than what users would have written.

An AI support chatbot deflects 60% of tickets (strong by industry standards) — but CSAT for those deflected tickets is 2.1/5 (terrible). The deflection metric says success; the customer experience metric says users are bouncing off an unhelpful bot and not reaching humans who could actually help them.

The fix: for every AI feature, define a metric that captures output quality, not just output volume.

### How to Define Success When Outputs Are Non-Deterministic

Three-layer metric structure:

**Layer 1: Business outcome.** The thing the feature is supposed to move. Revenue, retention, support costs, time-to-complete. This is your north star. AI is the mechanism; the business outcome is what you're actually optimizing for.

**Layer 2: Proxy quality metric.** Something measurable that correlates with output quality. Can be implicit (users accepting suggestions without editing heavily) or explicit (thumbs up/down feedback, annotation by human raters). This is your leading indicator.

**Layer 3: Model performance metric.** Precision, recall, NDCG, BLEU, whatever's appropriate for the task. This tells you if the model is performing well before that shows up in business outcomes. Lagging by days to weeks.

You need all three. Layer 3 without Layer 1 means you don't know if good model performance translates to business value. Layer 1 without Layer 3 means you can't diagnose problems or anticipate regressions.

### Quality Metrics Explained in Product Terms

**Precision.** Of the things the AI flagged/returned/generated as relevant, what fraction actually was? High precision means low false positive rate. A fraud detection model with 99% precision flags 100 transactions as fraud and is right about 99 of them. Users care about precision when false positives are costly — if your AI recommends items to remove from a cart, false positives are items removed that the customer actually wanted.

**Recall.** Of everything that should have been flagged/returned/generated, what fraction did the AI actually get? High recall means low false negative rate. A fraud detection model with 99% recall catches 99 out of every 100 actual fraud cases. Users (and the business) care about recall when misses are costly — if your AI is supposed to surface all compliance issues in a document, missed issues are liability.

The precision/recall tradeoff: raising one typically lowers the other. Setting the threshold between them is a product decision, not a model decision. Where you set it depends on the cost of false positives vs. false negatives in your specific context.

**NDCG (Normalized Discounted Cumulative Gain).** Used for ranked lists and recommendations. Measures whether the most relevant results appear at the top. Useful when you're surfacing a list of options (recommendations, search results, similar items) and the order matters. Product translation: an NDCG of 0.8 means your ranking is capturing most of the value a perfect ranking would deliver.

**F1 Score.** Harmonic mean of precision and recall — useful when you need a single number that balances both. Good for internal model evaluation; less useful for communicating to stakeholders.

### Leading vs. Lagging Indicators for AI Feature Health

**Leading indicators (move first, signal model issues early):**
- Edit rate on AI-generated content. If users are heavily editing outputs, quality is declining before they stop using the feature entirely.
- Override rate on AI suggestions. If users are rejecting suggestions more frequently, the model is drifting from their preferences.
- Confidence score distribution. If the model's own confidence scores are shifting down, a quality problem is forming before it shows in outcomes.
- Latency. Increasing response time is often the first signal of upstream model or retrieval issues.

**Lagging indicators (confirm what already happened):**
- Task completion rate
- Feature adoption/retention
- Business outcome metrics (revenue, deflection, savings)
- User satisfaction scores

Healthy AI feature monitoring watches leading indicators daily and lagging indicators weekly. Waiting for lagging indicators to catch problems means you're reacting to what already happened.

### How to Know If Your AI Feature Is Actually Working

Simple test: run a holdout group that doesn't get the AI feature. Compare outcomes between groups. If the AI feature group doesn't outperform the holdout on your Layer 1 business metric, the feature isn't adding value — regardless of what your Layer 3 model metrics say.

If you can't run a holdout, use pre/post with careful attribution. But be rigorous: many AI features get credit for improvement that would have happened anyway due to other changes or natural trends.

---

## 4. PRD Structure for AI Features

### How an AI PRD Differs From a Standard PRD

A standard PRD describes what a system should do and how users interact with it. An AI PRD has to do all of that plus describe what the model should output, how good is good enough, what happens when it's not good enough, and how you'll know the difference.

Missing any of those sections means engineering and data science will make judgment calls on your behalf — and those calls will reflect their priorities (technical elegance, model metrics) rather than yours (user experience, business outcomes).

### Sections Required in an AI PRD That Standard PRDs Don't Have

**Model behavior specification.**
What the model should do in the normal case, stated with enough specificity that a data scientist could write an eval for it. Not "the model should understand user intent" — that's not a spec, it's a hope. Instead: "Given a support message, the model should classify it into one of [5 defined categories] with ≥90% agreement with human annotation on a held-out test set of 500 labeled examples."

**Quality bar.**
The minimum acceptable model performance level, stated as a specific metric threshold, before the feature ships to users. Example: "Precision ≥ 88% and recall ≥ 80% on the internal eval set. If either is below these thresholds, the feature does not ship — not even to a limited cohort."

This section forces the conversation about what "good enough" means before the feature is built, not after engineering has already invested weeks.

**Eval criteria.**
How you'll measure whether the model meets the quality bar. What is the eval set? How was it constructed? Who labeled it? How often will it be refreshed? A quality bar without a corresponding eval methodology is not enforceable.

**Fallback behavior.**
What happens when the model produces output below the confidence threshold, fails to produce output, or produces an output flagged as unacceptable? Options typically include: show nothing (silent failure), show a deterministic fallback, show the output with a disclaimer, or escalate to a human. Each option has UX and product implications that need to be decided in the PRD, not by an engineer at 11pm before launch.

**Data requirements.**
What training data, fine-tuning data, or retrieval data does the model need? Where does it come from? Who owns it? Are there privacy or compliance constraints on its use? This section is often missing from AI PRDs and causes mid-sprint delays when legal or privacy review surfaces issues.

**Monitoring and regression plan.**
How will the feature be monitored in production? What metric thresholds trigger an alert? What constitutes a regression that requires an incident response vs. a routine model refresh?

### How to Write the Model Behavior Section

This is the hardest part and the part most PMs skip or write poorly.

The model behavior section answers: what should the model do, in concrete terms, across the cases that matter?

**Structure it as a decision table.** Input condition → expected output → acceptable variance.

| Input type | Expected output | Acceptable variance | Not acceptable |
|---|---|---|---|
| Clear, single-intent message | Classified to correct category, confidence ≥ 0.8 | Any category with confidence ≥ 0.8 | Multiple categories returned; confidence < 0.6 |
| Ambiguous message (multiple intents) | Top-ranked intent returned, confidence 0.5-0.7 | Either plausible intent, flagged as ambiguous | High confidence classification of wrong intent |
| Off-topic / gibberish | Return null / "unable to classify" | N/A | Any classification returned |

**Write at least 5 concrete examples.** Each example should include: the exact input, the correct output, why it's correct, and at least one common wrong answer the model might produce.

**State what the model should not do.** Constraint architecture (from specification-clarity.md) applies here directly. "The model should not classify compliance-related messages as billing issues, even if the user mentions payment." Negative constraints are as important as positive ones.

### Defining Acceptable vs. Unacceptable Outputs Concretely

Vague: "The model should not produce harmful content."

Concrete: "The model should not produce outputs that: (1) contain personally identifiable information not present in the input, (2) make specific financial or legal recommendations in first person, (3) reference competitors by name in a comparison context, (4) produce content that would fail our existing legal review checklist [link]."

The test for concreteness: could a junior annotator, given this definition, reliably tell whether a specific model output is acceptable or not? If yes, it's concrete enough. If they'd have to make judgment calls, it's still too vague.

---

## 5. Writing Briefs an Engineering Team Can Actually Build From

### The Gap Between "We Want AI to Do X" and a Buildable Spec

The most common PM failure mode on AI features: writing a brief that describes the desired outcome without specifying the approach, the constraints, the data, or the quality bar.

"We want AI to automatically route customer support tickets to the right team" is not a brief. It's a problem statement. A brief answers:
- What data does the model have access to at inference time?
- What are the possible output categories and how are they defined?
- What quality bar must be hit before we ship?
- What's the fallback when the model is uncertain?
- What's in scope and out of scope for this sprint?

Without these, engineering starts building based on their own assumptions. Those assumptions accumulate, and by the time the feature is in review, the team has built something that solves a subtly different problem than you specified.

### How to Write Acceptance Criteria for Probabilistic Systems

Standard acceptance criteria follow Given/When/Then format and assume deterministic behavior: Given X happens, When Y is done, Then Z occurs exactly. This breaks for probabilistic outputs because "Then Z occurs exactly" is never true for an AI system.

Modify the format:

**Given/When/Then/At-Quality:**
- Given: [input condition]
- When: [model processes input]
- Then: [expected output behavior]
- At quality: [minimum acceptable performance rate across a defined test set]

Example: "Given a support email, when the model classifies its intent, then it should return one of [5 defined categories] within 3 seconds. At quality: ≥88% precision and ≥82% recall on the internal eval set of 600 annotated examples."

This adds the quality dimension that probabilistic systems require without abandoning the structured format.

**Write acceptance criteria for the unhappy path.** Standard ACs focus on the happy path. For AI features, the unhappy path ACs are equally important:
- Given a message in a language the model hasn't been trained on, when the model processes it, then it should return null rather than a low-confidence classification.
- Given an API timeout from the model provider, when the timeout occurs within the user's request, then the UI should surface a manual routing option within 2 seconds.

### How to Specify Edge Cases and Failure Modes

Use a taxonomy rather than trying to enumerate every edge case.

**Four categories of AI failures to specify:**

1. **Low-confidence correct.** Model gets the right answer but reports low confidence. Define how the UX should handle this — surface as-is with a caveat, or suppress until confidence improves?

2. **High-confidence incorrect.** Model is wrong and doesn't know it. This is the dangerous one. What safeguards exist? What's the UX after a user catches the error? Does this surface in monitoring?

3. **Refusal / null output.** Model declines or fails to produce output. What's the trigger? What's the fallback?

4. **Out-of-distribution input.** Input is structurally or semantically outside what the model was trained on. How is this detected? What happens?

For each category, the brief should specify: detection method, UX behavior, and logging/monitoring approach.

### What Engineers and Data Scientists Actually Need From PM to Start Work

**Data scientists need:**
- A labeled eval set or a plan for creating one (who labels, how many examples, what the labeling criteria are)
- The quality threshold that constitutes "done" — stated as a specific metric
- The priority order between precision and recall when you can't have both
- Access to representative production data or a sampling plan

**Engineers need:**
- The API contract: what goes in, what comes out, in what format, within what latency
- The fallback behavior at each failure mode (don't leave this for them to decide)
- The monitoring requirements: what gets logged, what triggers alerts
- The definition of a regression for purposes of rollback decisions

**Both need:**
- A clear description of the task, not the technology. "Classify support emails into 5 categories" is clearer than "use an LLM to understand user intent."
- The acceptance criteria before they start, not after they finish building.
- A PM who will look at examples with them early — during model development, not at review.

---

## 6. Stakeholder Communication for AI Products

### Managing Expectations When AI Outputs Are Variable

The first conversation to have with stakeholders is about what probabilistic means. Most non-technical stakeholders have a mental model of software as deterministic: if you put X in, you get Y out, every time. AI systems violate this assumption. The same input can produce different outputs. Performance varies across user segments and input types. "It worked in the demo" does not guarantee "it works in production."

Set the frame early: "This feature will be right 90% of the time. That's better than the manual process we have today, which is right 75% of the time. But it means we need to design the user experience to handle the 10% case, and we need to monitor the 10% rate, because it will change over time."

The 90% number makes the value concrete. The explicit acknowledgment of the 10% prevents stakeholders from being surprised when it happens. Both are necessary.

**Anchor to relative performance, not absolute.**
"The model is 87% accurate" sounds uncertain. "The model handles this 87% of the time vs. our current manual process handling it 65% of the time" sounds like a clear win. Frame AI performance against the current baseline wherever possible.

### How to Explain Model Limitations Without Undermining Confidence

The instinct when a model has limitations is to either hide them or over-disclose them. Neither works. Hiding limitations means stakeholders discover them at bad moments — in a demo, in a board meeting, in a customer call. Over-disclosing means stakeholders walk away thinking the feature is fragile when it isn't.

The approach: be specific about limitations, not vague.

Vague: "The model isn't perfect and will make some mistakes."

Specific: "The model performs well on English-language messages from our US customer segment, where we have the most training data. Performance on Spanish-language messages is 15 points lower — that's on the roadmap for Q3. If a Spanish-language customer writes in, they get the manual routing flow."

The specific version tells stakeholders exactly where the limitation is, how large it is, and when it will be addressed. They can factor that into their planning. The vague version just makes them uneasy without giving them anything to work with.

### When to Say "AI Can't Do This Reliably" vs. "This Needs More Data/Time"

These are different statements with different implications for roadmap and resourcing, and stakeholders will conflate them if you don't distinguish clearly.

**"AI can't do this reliably"** means the task is either beyond current model capabilities, requires data that doesn't exist or is inaccessible, or has error costs that make the realistic performance level insufficient for the use case. Examples: generating legally binding contract language, making individual medical dosage recommendations, predicting individual user behavior with high certainty.

**"This needs more data/time"** means the task is tractable, you have a credible path to the required quality level, and what's blocking you is data volume, compute time, or iteration cycles. Examples: improving classification accuracy from 76% to 88% with more labeled examples, reducing hallucination rate by improving retrieval quality in a RAG system, improving personalization with more behavioral signal.

The test for which frame applies: has anyone built something similar that works? If yes, it's probably "more data/time." If the task is genuinely novel or structurally beyond what models do well, it might be "can't do reliably." Be careful about calling things "impossible" — the field moves fast. But be equally careful about promising "more data/time" when the fundamental task is wrong for AI.

### How to Communicate AI Incidents

AI incidents are different from software bugs. A software bug is a defect in code that has a root cause and a fix. An AI incident is often a systemic performance shift — the model started behaving differently at scale, or a new class of inputs exposed a gap in training. The cause is fuzzier and the fix is less obvious.

**Incident communication template:**

1. **What happened.** "Starting at [time], the model began returning [description of bad output] for [description of affected input class]. Approximately [X]% of requests in the past [time period] were affected."

2. **What we did immediately.** Rollback, fallback to deterministic behavior, traffic reduction, human escalation. Always have one of these available. An AI feature with no fallback behavior is a production risk.

3. **Why it happened (best current understanding).** "Our eval set didn't contain examples of [edge case]. In production, [X]% of traffic is [edge case]." Or: "The model provider pushed an update that changed output behavior in ways we didn't anticipate." Be honest about what you don't know yet.

4. **What we're doing to prevent recurrence.** New eval examples, monitoring for the specific failure pattern, human review gate for low-confidence outputs in the affected input class.

**The trust principle for AI incidents:** stakeholders lose trust not when AI fails — they expect imperfection — but when the failure was predictable and unmonitored, or when the communication is vague or defensive. Speed + honesty + a clear remediation plan protects trust. Silence and deflection destroy it.

**Regression communication.** Regressions are particularly tricky because they're often gradual — model performance slowly drifts over weeks as production data distributions shift, and there's no single "the bug was introduced" moment. Build monitoring that catches gradual drift before stakeholders experience it. If you're explaining a regression after a stakeholder noticed it, you're already behind.

---

## Cross-References

| Concept | See Also |
|---|---|
| Writing specs for AI systems | specification-clarity/specification-clarity.md L22–81 (7-property framework), L131–187 (acceptance criteria) |
| Model selection and tradeoffs | agentic-engineering/agentic-engineering.md L344–506 |
| AI system architecture patterns | ai-system-design/ai-system-design.md L23–92 (AI vs. deterministic decision framework) |
| Observability and metrics tooling | ai-system-design/ai-system-design.md L383–435 |
| PRD evaluation design | specification-clarity/specification-clarity.md L533–685 |
| Failure mode catalog | specification-clarity/specification-clarity.md L354–428 |
| Production prompt documentation | playbooks/writing-production-prompts.md L97 |
