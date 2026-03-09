# Project Planning Template — FILLED EXAMPLE

Support Ticket AI Classifier — real example of a completed project plan using the template.

**Project Name:** Support Ticket Auto-Classifier
**Owner:** Support Engineering Team
**Date Started:** 2026-03-01

---

## Phase 0: High-Level Ideation

### Problem Statement (1 sentence)
We need to auto-classify support tickets so that our support team can prioritize and respond faster.

### Ideation Canvas

**1. Problem Statement** (The real pain point)
We manually review 500 support tickets per day. Our keyword-based classifier is 60% accurate, causing tickets to go to the wrong team, delaying responses by 2-3 hours on average. We lose ~$50k/month in support efficiency.

**2. Users Affected** (Who specifically?)
12 support agents processing 500 tickets/day. Also: customers (slower responses) and support leadership (can't track team workload accurately).

**3. Current State** (How is it done today?)
Regex-based classifier runs, routes 60% of tickets correctly to [Logistics, Billing, Technical, Account, Fraud]. Agents manually override ~100 tickets/day (~20%) because classification is wrong. Takes 1 minute per ticket to review and correct.

**4. Desired State** (What does success look like?)
- Auto-classifier achieves 95%+ accuracy
- Agents spend <30 seconds per ticket (just review, not reclassify)
- Manual override rate drops to <5%
- Response time to customers drops from 4 hours to 1 hour average

**5. Key Constraint** (What matters most? Speed? Accuracy? Cost?)
Accuracy > Speed > Cost. We'd rather spend $2k/month on a good solution than save $200/month with a bad one. Accuracy is customer-facing.

**6. Scope Boundary** (What are we NOT solving?)
- NOT: response generation (Phase 2 can add this)
- NOT: sentiment analysis (future iteration)
- NOT: multi-language (Phase 1 constraint: English only)
- NOT: custom category training (fixed 12 categories for now)

**7. Success Metrics** (Measurable outcomes)
- Accuracy: 95%+ on validation set (measured weekly via human spot-check)
- Agent time per ticket: 4.2m → 3m (weekly average)
- Override rate: 20% → <5% (daily tracking)
- Cost: ≤ $500/month (daily tracking)

**8. Non-Negotiables** (Must-haves)
- GDPR-compliant (customer data in EU)
- Works offline for 15 min if API down (graceful degradation)
- Supports 3 languages by Phase 2 (currently hardcoded for English-only in Phase 1)
- Explains why it chose a category (confidence % at minimum)

### Gate: Phase 0 Done?
- [x] Problem is stated clearly (not solution-focused)
- [x] 3+ people agree on real problem (Support Lead, 2 agents, CTO)
- [x] Success metrics are measurable (95%+, <3m, <5%, ≤$500)
- [x] Constraints are explicit (accuracy primary, non-negotiables listed)
- [x] Scope is bounded (categories fixed, languages deferred)

**Status:** ✅ APPROVED by support leadership

---

## Phase 1: Specification

### Pre-Phase Brainstorm
**Who defines "done"?** Support Lead has final sign-off. Agents validate accuracy.
**What detail matters most?** Confidence scores (agents need to trust the model). Category definitions (must be unambiguous — what's "Logistics" vs. "Account"?).
**What could we drop if pressured?** Offline mode (nice-to-have). Confidence scores (must-have). Multi-language (defer to Phase 2).
**What might change?** Categories might expand. Confidence threshold might be tuned based on real data.

### Acceptance Criteria (BDD Format)

**Feature:** Auto-classify support tickets into 12 categories with ≥95% accuracy

```
- [ ] Given ticket: "My order hasn't arrived after 2 weeks", When classification runs, Then output: {"category": "Logistics", "confidence": 0.94}
- [ ] Given ambiguous ticket: "Can't login or reset password", When classification runs, Then output: {"category": "UNCLASSIFIED", "confidence": 0.45}
- [ ] Given ticket with profanity: "[angry customer]", When classification runs, Then confidence is not penalized (only category matters)
- [ ] Given empty or null ticket, When classification runs, Then return error: {"error": "invalid_input", "message": "ticket body required"}
```

**Performance:**
- Latency p50: ≤ 200ms
- Latency p95: ≤ 500ms
- Cost per classification: ≤ 1¢

**Out of Scope:**
- NOT implementing: response generation, sentiment analysis, priority scoring
- NOT supporting: multi-language (Phase 1), custom categories (Phase 1), fine-tuned model (Phase 2+)

### Spec Properties Checklist (7 Properties)
- [x] **Complete:** Any engineer reading this knows: input format (ticket text), output format (JSON with category + confidence), all 12 categories defined
- [x] **Unambiguous:** Defined each category with 2-3 examples (e.g., "Logistics: order status, delivery, tracking | Account: profile, settings, preferences")
- [x] **Consistent:** "Always return confidence ≤ 1.0" + "UNCLASSIFIED for confidence < 0.6" + no contradictions
- [x] **Verifiable:** "95%+ accuracy on validation set" is measurable. "Fast" is not (we specified ms thresholds).
- [x] **Bounded:** 12 fixed categories, English only, ≤2000 chars per ticket
- [x] **Prioritized:** "Accuracy > speed > cost"
- [x] **Grounded:** Concrete examples for each category, acceptance criteria with real ticket examples

### Playbook Selection

**Decision Tree Result:**
- "Does it make independent decisions?" YES → Use Building AI Agents? NO, it's single-pass classification.
- "Does it search external knowledge?" NO → RAG not needed (categories are fixed, in-memory).
- "Is it conversational?" NO → Chatbots not applicable.
- "Multiple agents?" NO → Multi-Agent Orchestration not needed.
- "Cost is primary concern?" NO → Cost-Optimized not primary, but worth considering.
- **Result:** Simple Classifier (single-pass). Use "Writing Production Prompts" playbook.

**Playbook(s) Selected:**
- [x] Writing Production Prompts (primary: prompt engineering for classifier)
- [ ] Building AI Agents (not needed: no tool use, no loops)
- [ ] Building RAG Pipelines (not needed: no retrieval)
- [ ] Cost-Optimized LLM Workflows (secondary: will optimize model routing in Phase 2)
- [x] (Consider) Cost-Optimized if volume is high (routing to Haiku for easy cases)

**Why these?**
- Writing Production Prompts: We're building a classifier with a prompt. Need format enforcement, confidence calibration, error handling.
- Cost-Optimized (secondary): If 500 tickets/day, cost matters. Will explore model routing (Haiku for < 200 tokens + high confidence, Sonnet for complex).

### Gate: Spec Done?
- [x] All 7 properties present (reviewed with Support Lead)
- [x] Acceptance criteria testable (examples provided, validation plan defined)
- [x] Playbook(s) selected (Writing Production Prompts + Cost-Optimized)
- [x] Team agrees on scope (categories locked, languages deferred)

**Status:** ✅ SPEC APPROVED

---

## Phase 2: Architecture & Design

### Pre-Phase Brainstorm
**Dominant constraint?** Accuracy (95%+). Cost and latency are secondary.
**Which pattern fits?** Simple classifier. No loops, no tool use. Input → prompt → model → parse output → return.
**Where does context go?** System prompt (instructions for classification) + category definitions (in-prompt examples) + ticket text (user input).
**What could break?** Hallucinations (model invents a category not in the list). Confidence miscalibration (model says 0.9 confident but wrong). Context overflow (very long tickets).

### Four Pillars

**Pillar 1: Prompt**
```
You are a support ticket classifier. Your job is to classify each support ticket
into one of these 12 categories:

1. Logistics: order tracking, delivery, shipping, address changes
2. Billing: charges, refunds, invoices, payment methods
3. Technical: bugs, errors, crashes, connectivity
4. Account: login, password, profile, settings
5. Fraud: suspicious activity, unauthorized access, chargebacks
6. Returns: return requests, refund status, product exchanges
7. Warranty: warranty claims, defects, repairs
8. General: general inquiries, feedback, surveys
9. Escalation: complaint, executive escalation
10. Product: questions about product features, specs
11. Pricing: price questions, discounts, promotions
12. Other: doesn't fit above

Rules:
- Respond ONLY with JSON: {"category": "...", "confidence": 0.0-1.0}
- If you're not confident (< 60%), respond: {"category": "UNCLASSIFIED", "confidence": <value>}
- Never invent categories. Only use the 12 above.
- Confidence: 0.9-1.0 = very sure, 0.7-0.9 = fairly sure, 0.5-0.7 = unsure, < 0.5 = guessing

Classify this ticket:
```

**Pillar 2: Model**
- Choice: Claude Sonnet (good balance of accuracy for reasoning + cost)
- Reasoning: Haiku is cheaper but less accurate at classification edge cases. Opus is overkill for single-pass task.
- Cost ceiling: $500/month (at 500 tickets/day, ~250k tokens/month → ~$1.50/month actually, so plenty of headroom)

**Pillar 3: Context**
- What goes in: System prompt (300 tokens) + category definitions (500 tokens) + ticket text (variable, avg 400 tokens) = ~1200 tokens avg
- What's omitted: No conversation history. No retrieval. No state.
- Memory strategy: Stateless (each ticket classified independently)

**Pillar 4: Tools**
- Available: None (pure classification, no API calls needed)
- Restricted: N/A
- Fallback: On parsing error, mark as UNCLASSIFIED

### Decision Matrix (Cost vs. Complexity vs. Speed vs. Reliability)

**Constraint from Phase 0:** Accuracy is PRIMARY. Cost is secondary.

| Option | Cost/month | Complexity | Speed (latency) | Reliability | Notes |
|--------|-----------|-----------|-----------------|-------------|-------|
| A: Simple Sonnet classifier | $2 | Low (prompt only) | 200ms | 95% (hallucination risk on edge cases) | Cheapest, simplest. But hallucinations on ambiguous tickets. |
| B: RAG + fewshot (retrieve examples) | $50 | Medium (needs vector DB + caching) | 400ms | 97% (grounded in examples) | More reliable but slower, more expensive infrastructure. |
| C: Fine-tuned Sonnet | $200 + $1k infra | High (data pipeline, training) | 50ms | 98% (custom to domain) | Slowest to build. Fastest at inference. Overkill for first phase. |

**Winner:** Option A (Simple Sonnet) because:
- Meets 95% accuracy target with good prompt engineering
- Fastest to deploy (2 weeks vs 6 weeks for RAG)
- Cheapest ($2/month vs $50+)
- If accuracy drifts, we can iterate to Option B (RAG) in Phase 2 without re-architecting
- Risk is acceptable: hallucinations are rare, we have UNCLASSIFIED fallback

**Cost Optimization:** If volume grows 5x, will revisit model routing (Haiku for easy cases, Sonnet for hard).

### Pattern Selected
Simple Classifier (stateless, single-pass, no loops).

**Why?**
- No iteration needed (ticket → classification → done)
- No tool use (pure text classification)
- No multi-agent (one model makes decision)
- Perfect fit for the problem

### Gate: Architecture Done?
- [x] Four Pillars filled (prompt, model, context, tools)
- [x] Decision matrix completed (Option A winner: simple Sonnet)
- [x] Pattern selected (Simple Classifier)
- [x] Trade-offs acknowledged (accuracy over speed/cost)
- [x] Risks identified (hallucinations on edge cases → mitigated by UNCLASSIFIED fallback)

**Status:** ✅ ARCHITECTURE APPROVED

---

## Phase 3: Development & Prototyping

### Pre-Phase Brainstorm
**Minimal feature set?** Classify a single ticket end-to-end. No UI, no database, no scaling. Just: prompt → Claude API → parse response.
**What can we mock?** Everything except the core: model, prompt, response parsing.
**How will we test?** Happy-path: 5 real tickets from support team, confirm accuracy by hand.
**Where will we discover problems?** Edge cases (very long tickets, special characters, ambiguous categories).

### Minimal Implementation Checklist

- [x] Core pipeline works (input ticket → Sonnet → JSON response → parsed)
- [x] One happy-path example runs end-to-end (ticket: "Order not arriving" → Logistics, 0.94)
- [x] Error handling for 3 failure modes:
  - [x] API timeout: retry 3x with exponential backoff, then mark UNCLASSIFIED
  - [x] Invalid JSON response: fallback to regex-based classification, log error
  - [x] Hallucinated category: validate category is in list, mark UNCLASSIFIED if not
- [x] Logging in place (request_id, input, output, latency, cost, error)
- [x] Basic test passes (happy-path accuracy 95/100 on sample tickets)
- [x] Performance measured: avg latency 180ms, cost 0.8¢ per call

### Testing Strategy

**Unit Testing:**
```python
def test_parse_response():
    response = '{"category": "Logistics", "confidence": 0.94}'
    result = parse_response(response)
    assert result['category'] == 'Logistics'
    assert result['confidence'] == 0.94
```

**Functional Testing:**
```python
def test_classify_ticket():
    ticket = "My order hasn't arrived"
    result = classify(ticket)
    assert result['category'] in ['Logistics', 'Returns']
    assert result['confidence'] >= 0.7
```

**Behavioral Testing:**
```python
# Test on 100 real support tickets, 95/100 correct (95% accuracy)
# Measure latency: p50=180ms, p95=320ms
# Measure cost: 0.8¢ per call
```

### Gate: Prototype Done?
- [x] Minimal feature set works end-to-end
- [x] Happy-path test passes (95% accuracy on sample)
- [x] Performance measured (180ms latency, 0.8¢ cost)
- [x] 3 failure modes handled (timeout, invalid JSON, hallucination)
- [x] Code is reviewable (straightforward, well-commented)

**Status:** ✅ PROTOTYPE WORKS

---

## Phase 4: Scale & Harden

### Pre-Phase Brainstorm
**What breaks first at scale?** Cost (500 tickets/day = 250k tokens/day). API rate limits (Claude API allows 50k tokens/min per account, we're at ~170 tokens/min, safe). Accuracy drift (model might behave differently on real data than test set).
**What do we need to see?** Cost per day, accuracy on real tickets (weekly spot-check), timeout/error rates.
**How do we recover from failures?** Timeout: circuit breaker (if >50 errors in 5min, fall back to regex classifier). Accuracy drift: re-run Phase 3 testing, potentially revisit prompt.

### Context Management

- [x] Define what goes in context (System prompt 300T + categories 500T + ticket avg 400T = 1200T avg, max 1500T)
- [x] Define what's omitted (No history, no retrieval)
- [x] Handle overflow (If ticket > 2000 chars: truncate to first 1500 + last 200 chars)
- [x] Test with realistic volumes (Ran on 100 real tickets, performance stable)

### Observability (Logging)

```json
{
  "timestamp": "2026-03-01T14:23:45Z",
  "request_id": "ticket_12345",
  "input_length": 420,
  "model": "claude-sonnet",
  "output_category": "Logistics",
  "output_confidence": 0.94,
  "latency_ms": 245,
  "cost_cents": 0.8,
  "error": null,
  "fallback_triggered": false
}
```

### Cost Optimization

**Current cost:** $0.8 × 500/day × 30 days = ~$12/month (way under $500 budget)
**Budget:** $500/month
**Headroom:** 40x (can grow to 20k tickets/day before exceeding budget)
**Optimization strategy:** If volume exceeds 2000 tickets/day, implement model routing:
- If ticket < 200 tokens AND confidence_score > 0.8 from Haiku first pass → use Haiku (0.3¢)
- Otherwise → use Sonnet (0.8¢)
- Estimated 30% cost reduction, no accuracy loss

### Failure Recovery (Failure Taxonomy)

| Symptom | Root Cause | Recovery |
|---------|-----------|----------|
| Accuracy drops from 95% to 85% | Model behavior changed OR data distribution changed (new ticket types) | 1. Spot-check 20 misclassified tickets. 2. Update prompt with new examples. 3. Re-test on validation set. |
| Classification returns category not in 12 | Hallucination (model invented category) | Validate category against allowed list. Mark UNCLASSIFIED if invalid. Log the hallucination for prompt tuning. |
| Timeout rate spikes to 30% | API overloaded OR network issues | Implement circuit breaker: if >10 timeouts in 5min, fall back to regex classifier (60% accurate). Notify on-call. |
| Cost doubles | Unexpected volume spike | Check if tokens/request increased (very long tickets?). If so, implement truncation. Monitor daily. |

### Gate: Hardened & Ready?
- [x] Context management tested (truncation works, tested on long tickets)
- [x] Logging in place (every request logged)
- [x] Cost tracked and under budget ($12/month, $500 budget)
- [x] 5+ failure modes handled (timeout, hallucination, invalid JSON, accuracy drift, volume spike)
- [x] Accuracy ≥ 95% target (measured on 100 real tickets)
- [x] Latency within tolerance (p95 < 500ms)

**Status:** ✅ PRODUCTION-READY

---

## Phase 5: Production Deployment

### Pre-Phase Brainstorm
**Rollout strategy?** Gradual: 10% of tickets day 1, 50% day 2, 100% day 3. Circuit breaker: if accuracy drops below 90%, fall back to regex.
**Success metrics in prod?** Same as Phase 0: accuracy 95%+, agent time <3m, override rate <5%.
**Failure response?** If accuracy < 90%, fall back to regex (old system). Alert support lead within 5 min.
**Access control?** All agents can see classifications. Only support lead can toggle on/off.

### Safety Rules Applied

- [x] Rule 1: Database migrations immutable + versioned (NA for this project, stateless)
- [x] Rule 2: Schema changes auto-generate migrations (NA, no DB)
- [x] Rule 3: Features fully tested before prod (Feature flag: ENABLE_AI_CLASSIFIER=false by default)
- [x] Rule 4: Infrastructure as code (CI/CD: deploy via GitHub Actions, no manual setup)
- [x] Rule 5: Dependencies pinned exactly (anthropic-sdk==1.2.3, not >=1.0)
- [x] Rule 6: Code follows established patterns (All handlers follow: input validation → API call → response parsing → logging → error handling)

### Agentic Pattern Considerations

**Pattern:** Simple Classifier
**Safety level:** HIGH (stateless, no loops, no tool use, deterministic)
**Key monitoring:**
- Request success rate (target: >99%)
- Accuracy (target: >95%)
- Latency p95 (target: <500ms)
- Cost per request (target: <1¢)
- Fallback rate (target: <5%)

### Deployment Checklist

- [x] Code reviewed (2 engineers, CTO)
- [x] All tests pass (unit, functional, behavioral)
- [x] Feature flag ready (ENABLE_AI_CLASSIFIER=false, can toggle at runtime)
- [x] Staging tested (staging env identical to prod: same API keys, same model)
- [x] Monitoring dashboards live (cost, latency, accuracy, error rate)
- [x] Alerts configured (accuracy < 90%, error rate > 5%, cost > $100/day)
- [x] Rollback plan documented (disable feature flag, fall back to regex)
- [x] Documentation updated (API docs, runbook: "classifier is down", how to roll back)

### Gate: Production-Ready?
- [x] Safety rules applied
- [x] Monitoring in place
- [x] Rollback plan tested (toggling flag works instantly)
- [x] Team trained (support lead knows how to disable, on-call engineer has runbook)
- [x] Go/No-go decision: **GO** ✅

**Deployment Date:** 2026-03-15
**Rollout:** Day 1 (10%), Day 2 (50%), Day 3 (100%)

---

## Phase 6: Production Operation & Evolution

### Pre-Phase Brainstorm
**What metrics matter?** Accuracy, agent time per ticket, override rate, cost (from Phase 0).
**What will we do with data?** Weekly review: support lead reviews 20 misclassified tickets, updates prompt if pattern found.
**When do we iterate?** If accuracy drops below 92% OR override rate > 8% → re-run Phase 3 (prompt tuning).
**When do we stop?** When accuracy stable at 95%+ for 4 weeks AND no actionable improvements found.

### Metric Templates

**Metric 1: Accuracy**
- Current (baseline): 60% (regex classifier) | Target: 95% | Alarm: < 92%
- Measured: Weekly spot-check (support lead reviews 20 classifications)
- Week 1 result: 96% ✅
- Week 2 result: 95% ✅

**Metric 2: Agent Time per Ticket**
- Current (baseline): 4.2m | Target: 3m | Alarm: > 3.5m
- Measured: Daily average from time tracking
- Week 1 result: 3.8m (15% improvement) ✅

**Metric 3: Override Rate**
- Current (baseline): 20% | Target: <5% | Alarm: > 8%
- Measured: % of tickets reclassified by agent
- Week 1 result: 6% ✅

**Metric 4: Cost**
- Current: $12/month | Budget: $500/month | Alarm: > $200/month
- Measured: Daily tracking
- Week 1 result: $3 ($21 projected/month) ✅

### Iteration Triggers

| Trigger | Go Back To | Recovery |
|---------|-----------|----------|
| Accuracy drops < 92% for 2 days | Phase 3 (Prompt Engineering) | Review misclassified tickets, update prompt examples, re-test |
| Override rate > 8% | Phase 1 (Spec Review) | Did categories change? Are definitions ambiguous? Update spec + prompt. |
| Cost > $100/month | Phase 4 (Optimization) | Volume increased? Implement model routing (Haiku for easy cases). |
| Latency p95 > 1s | Phase 4 (Optimization) | API degraded? Implement caching? Check Claude API status. |

### Stopping Criteria

- [x] All success metrics met for 2+ weeks (accuracy 95%+, time <3m, override <5%, cost <$25/month)
- [x] Cost ≤ budget ($3/month vs $500)
- [x] Accuracy ≥ spec target (96% > 95%)
- [x] Team satisfied (support lead: "This is working great")
- [x] No actionable improvements left (confidence calibration is good, hallucinations < 0.1%, edge cases handled)

### 4-Week Reflection Checklist

- [x] Metrics still valid? YES (accuracy, speed, override still matter)
- [x] Are we hitting targets? YES (all 4 metrics green)
- [x] What's the biggest blocker? NONE (system is stable)
- [x] Which phase should we revisit? NONE
- [x] Loop or stop? STOP iteration. Maintain and monitor.

---

## Summary

**Project Status:** ✅ LIVE IN PRODUCTION (deployed 2026-03-15)

**Key Decisions:**
- Model: Claude Sonnet (best accuracy/cost ratio)
- Pattern: Simple Classifier (stateless, no loops)
- Primary Constraint: Accuracy (95%+ > speed/cost)
- Playbook(s): Writing Production Prompts + Cost-Optimized

**Results (vs. Phase 0 goals):**
- Accuracy: 60% → 96% ✅
- Agent time: 4.2m → 3.8m ✅
- Override rate: 20% → 6% ✅
- Cost: $50k/month savings in agent time vs $12/month spend ✅

**Next Steps (Phase 2+ features):**
1. Multi-language support (currently English-only)
2. Sentiment analysis (escalate angry customers)
3. Response generation (draft responses, not just classification)

**Last Updated:** 2026-03-22
**Next Review:** 2026-04-22 (monthly check-in)

---

## How This Worked

1. **Kickoff (Phase 0-1):** Filled problem + spec in one meeting. 2 hours total.
2. **Design (Phase 2):** Evaluated 3 options, chose simple classifier. 1 hour.
3. **Build (Phase 3):** Implemented prompt + API call + error handling. 4 days.
4. **Harden (Phase 4):** Added logging, tested edge cases, optimized. 3 days.
5. **Deploy (Phase 5):** Feature flag, gradual rollout, monitoring. 1 day.
6. **Operate (Phase 6):** Weekly metrics review, stable at 95%+ after week 2.

**Total time to production:** 2 weeks (spec + design + build + deploy)
**Team involved:** 1 engineer (build), 1 support lead (spec/validation), CTO (design review)

This is what a successful project looks like when you follow the meta-workflow.
