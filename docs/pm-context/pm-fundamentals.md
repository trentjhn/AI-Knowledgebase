# PM Fundamentals — Core Frameworks for AI Product Work

> **Note:** This file is staged here temporarily. It moves to `zenkai/pm-context/pm-fundamentals.md` when the Zenkai repo is created.
>
> Source: Synthesized from pm-frameworks-refresher.md (interview-prep repo) + applied to AI product context.

---

## What These Frameworks Are For

PM frameworks are thinking tools, not scripts. Their value is that they give you a structured way to approach a problem under pressure — in a meeting, in an interview, in a production incident. You internalize the structure so you can think clearly when stakes are high, not so you can recite steps mechanically.

For AI product work specifically, many classic PM frameworks apply directly — but some require adaptation because AI products are probabilistic, non-deterministic, and require ongoing management after launch in ways traditional software doesn't.

---

## 1. Discovery — Understanding the Problem Before Building

### The Core Principle: Learn, Don't Validate
Your job in discovery is to uncover truth, not to confirm your hypothesis. The most common mistake is designing research that seeks agreement with an idea you already have.

**Ask diagnostic questions that make the user tell a story:**
- "Walk me through the last time you tried to do X."
- "What was hard about it?"
- "What did you try before that didn't work?"

**Avoid:** "Would you use X?" (hypothetical), "Do you think this is valuable?" (leading).

### Jobs to Be Done (JTBD)
Every user is trying to accomplish something. The product is a means to that end, not the end itself.

**Format:** "When [situation], I want to [motivation], so I can [outcome]."

**Why it matters for AI products:** AI features often solve a latent job — something users couldn't do before, not just a faster version of what they already did. Understanding the underlying job helps you spec the AI's behavior around the actual need rather than the surface request.

**Example:** Users don't want "an AI summarizer." They want to get through their document backlog so they can make a decision by end of day. That changes what the summary needs to contain, how long it should be, and what the fallback is when the AI can't confidently summarize.

### Metrics That Prove Discovery Is Working
- You're hearing things you didn't expect
- Your hypothesis has changed at least once
- You can articulate the user's problem in their words, not yours

---

## 2. Prioritization — Deciding What to Build

### RICE Scoring
Quantitative prioritization for comparing features or projects.

**Formula:** (Reach × Impact × Confidence) / Effort

| Factor | What It Means | How to Estimate |
|---|---|---|
| Reach | How many users affected per quarter | 1,000 users, 10% of DAU |
| Impact | How much does it move the needle per user | 0.25 (minimal) → 3 (massive) |
| Confidence | How sure are you of the estimates | 100% / 80% / 50% |
| Effort | Person-months to build | 0.5 / 1 / 2 / 3+ |

**For AI products:** Effort estimates are harder because AI development is less predictable than traditional engineering. Build in uncertainty buffers. Confidence ratings matter more — be honest about what you don't know.

### Impact/Effort Matrix
Fast, visual prioritization when you need alignment quickly.

```
              HIGH IMPACT
                   │
   Quick Wins      │      Big Bets
   (Do First)      │      (Plan Carefully)
                   │
LOW EFFORT ────────┼──────── HIGH EFFORT
                   │
   Fill-ins        │      Money Pits
   (Do If Time)    │      (Avoid/Cut)
                   │
              LOW IMPACT
```

### MoSCoW — When Stakeholders Want Everything
Force prioritization by categorizing everything:
- **Must** — Cannot launch without it
- **Should** — Important, include if possible
- **Could** — Nice to have
- **Won't** — Explicitly out of scope for this release

**For AI products:** "Must" should include evaluation infrastructure and monitoring — not just the AI feature itself. Shipping an AI feature without monitoring is not a complete launch.

### Kano Model — What Customers Expect vs. What Delights Them
| Type | Description |
|---|---|
| Basic | Expected — dissatisfying if absent, not noticed if present |
| Performance | More is better — linear satisfaction |
| Delighter | Unexpected — disproportionate joy when present |

**For AI products:** Accuracy is usually a basic expectation — users don't celebrate when the AI is right, they're frustrated when it's wrong. Speed and quality improvements are performance factors. Surprising capability demonstrations are delighters — but only when the basics are solid.

---

## 3. Metrics — Measuring What Matters

### The North Star Metric
One metric that captures the core value the product delivers to users. It should:
- Reflect actual customer value (not a proxy)
- Correlate with long-term revenue
- Be actionable by the product team

**For AI products:** Standard engagement metrics often mislead. High usage of an AI feature doesn't mean it's working — users might be re-running queries because the first answer was wrong. Define a north star that reflects genuine value delivery, not just activity.

**Example:** For an AI-powered document Q&A feature, "questions answered without follow-up clarification needed" is a better north star than "questions asked."

### Pirate Metrics (AARRR) — The Funnel
| Stage | Metric | Question |
|---|---|---|
| Acquisition | Signups, traffic | How do users find the feature? |
| Activation | First value moment | Do they have a good first experience? |
| Retention | Return usage | Do they come back? |
| Revenue | ARPU, conversion | Does it drive business value? |
| Referral | NPS, sharing | Do they tell others? |

**For AI products:** Activation is the hardest stage. Users often try an AI feature once, get a mediocre result, and never return. Activation for an AI feature means the user got a response that was actually useful — not just any response. Define your activation event precisely.

### Leading vs. Lagging Indicators
| Type | Definition | Example |
|---|---|---|
| Leading | Predicts future outcome | Feature adoption rate, query success rate |
| Lagging | Confirms outcome after the fact | Churn rate, revenue |

**For AI products:** This distinction is critical. Churn from a bad AI feature happens slowly — users tolerate it for a while before leaving. Leading indicators like "user accepts AI suggestion without editing" or "user re-queries within 30 seconds" (indicating the first answer failed) give you early warning.

### How to Measure Goals That Seem Qualitative
Every qualitative goal has a quantitative proxy:
| If your goal is... | Measure it with... |
|---|---|
| "Helpful" AI responses | Acceptance rate, re-query rate, edit distance |
| "Trustworthy" AI | Fact-check accuracy, citation quality, user correction frequency |
| "Fast" experience | P50/P95 latency, time-to-first-token |
| "Good user experience" | Task completion rate, session abandonment, SUS score |

---

## 4. Roadmapping — Sequencing the Work

### Vision → Strategy → Roadmap → Backlog

```
VISION (3-5 years) — The world we're trying to create
        ↓
STRATEGY (1 year) — The bets we're making to get there
        ↓
ROADMAP (Quarters) — The sequence of work
        ↓
BACKLOG (Sprints) — The specific tasks
```

**For AI products:** Strategy must account for model capability curves. AI capabilities are advancing fast — features that are impossible today may be cheap commodity features in 18 months. Strategy should distinguish between "build because only we can" vs. "build now because timing matters" vs. "wait for the capability to mature."

### Build vs. Buy vs. Partner
| Option | When to Choose It |
|---|---|
| Build | Core to your differentiation, need full control, long-term cost matters |
| Buy | Table stakes, someone else does it better, speed matters |
| Partner | Accelerates go-to-market, access to distribution, neither alone could do it |

**For AI products:** Most teams should start with buy/API for AI capabilities. Building your own models is extremely expensive and rarely the right choice unless the capability is truly core and differentiating. The question is usually "which foundation model provider" and "how much customization (fine-tuning, RAG, prompt engineering)" — not "should we train from scratch."

---

## 5. Execution — Getting Work Shipped

### OKRs — Setting Clear Goals
- **Objective:** Qualitative, inspirational goal
- **Key Results:** 2–4 quantitative measures of success

**For AI products:** Key results should include quality metrics, not just output metrics. "Ship the AI feature" is not a key result. "AI feature achieves 85% user satisfaction rating with <2% hallucination rate on test set" is.

### Stakeholder Management
Map stakeholders on influence (ability to affect decisions) and interest (degree to which this affects them):

```
                  HIGH INTEREST
                       │
   Keep Satisfied      │      Manage Closely
   (High influence,    │      (Key players)
    low interest)      │
                       │
LOW INFLUENCE ─────────┼──────── HIGH INFLUENCE
                       │
   Monitor             │      Keep Informed
   (Minimal effort)    │
                       │
                  LOW INTEREST
```

**For AI products:** Legal and compliance are often high-influence, variable-interest stakeholders who can block AI features late in the process. Engage them early. The question "have legal and compliance signed off on AI behavior?" should be asked at the spec stage, not the week before launch.

### Root Cause Analysis — 5 Whys
When something goes wrong, ask "why" five times to find the actual root cause instead of fixing the symptom.

**For AI products:** When an AI feature fails, the root cause is almost never "the model was wrong." It's usually: the spec was ambiguous, the evaluation didn't catch the failure mode, the prompt didn't constrain the behavior adequately, or the monitoring didn't surface the problem early enough. Trace it back.

---

## 6. Key Mental Models for AI PMs

### First Principles Thinking
Break the problem down to fundamental truths, then build back up. Especially useful when AI hype leads to overcomplicated solutions.

> "Instead of assuming we need a multi-agent RAG pipeline, let me ask: what's the actual user problem? What's the simplest architecture that reliably solves it?"

### Inversion
Ask "how do we fail?" instead of "how do we succeed?" Build your risk mitigation from the failure modes.

> "If this AI feature caused a major incident in production, what would have caused it? That's our security and reliability checklist."

### Second-Order Thinking
AI features have second-order effects that traditional features don't. If users learn to rely on an AI assistant for decisions, what happens when the AI is wrong and they don't notice? If the AI becomes very good, does it reduce users' own skill development? Think past the first effect.

### The 80/20 Principle
20% of the AI's capability covers 80% of the valuable use cases. Ship the 80% that works reliably before trying to cover the long tail of edge cases.
