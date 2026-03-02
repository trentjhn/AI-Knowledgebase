# AI System Design and Architectural Patterns

> **Distilled from:** Chip Huyen (*AI Engineering*, 2025; *Designing Machine Learning Systems*, 2022) · Eugene Yan (*Patterns for Building LLM-based Systems*, 2023; *What We've Learned From A Year of Building with LLMs*, 2024) · Martin Fowler (*Emerging Patterns in Building GenAI Products*, Feb 2025) · Uber Engineering (*Michelangelo* platform case study) · Netflix Engineering (*Supporting Diverse ML Systems*, 2024) · Airbnb Engineering (*Bighead* ML platform) · Meta Engineering (*Building Meta's GenAI Infrastructure*, 2024) · LinkedIn Engineering (*AI/ML Data Platform*, 2024) · Applied LLMs collaborative guide (Yan, Bischof, Frye, Husain, Liu, Shankar, 2024) · 12-Factor Agents (HumanLayer, 2025) · Google Cloud Well-Architected Framework AI/ML Perspective (2024) · Lilian Weng, *LLM Powered Autonomous Agents* (2023) · MLSys 2024 Conference papers · Stanford CS329S (Machine Learning Systems Design) · GokuMohandas, *Made With ML* (2023–2025)

---

## Table of Contents

1. [Executive Summary — 10 Principles of AI System Design](#1-executive-summary)
2. [Where Does AI Belong? The AI vs. Deterministic Decision Framework](#2-where-does-ai-belong)
3. [Core Architectural Patterns](#3-core-architectural-patterns)
4. [System Design Trade-offs Specific to AI](#4-system-design-trade-offs)
5. [Data Architecture for AI Systems](#5-data-architecture)
6. [Observability and Monitoring](#6-observability-and-monitoring)
7. [Scalability Patterns at Production Scale](#7-scalability-patterns)
8. [AI-Native vs. AI-Augmented Architecture](#8-ai-native-vs-ai-augmented)
9. [Anti-Patterns — What to Avoid and Why](#9-anti-patterns)
10. [The 12-Factor Agent Standard](#10-the-12-factor-agent-standard)
11. [Key Takeaways for Practitioners](#11-key-takeaways)
12. [MLOps Engineering Patterns](#12-mlops-engineering-patterns)

---

## 1. Executive Summary

Ten principles that distill everything below. Read this section once, then use the rest as the reference.

**Principle 1 — AI is a component, not an architecture.** AI belongs in specific, well-bounded places inside a larger system. The surrounding system — data pipelines, APIs, caches, fallback logic, evaluation loops — is what makes AI reliable. Most teams underinvest in the system and overinvest in the model.

**Principle 2 — Use deterministic code by default; reach for AI when variation is the point.** If a function can be expressed as a rule, write the rule. AI earns its place only when the task is too variable, too unstructured, or too context-dependent to encode explicitly.

**Principle 3 — Start simple, layer complexity only when the pain is clear.** The right progression is: single prompt → RAG → routing → fine-tuning → agents. Every jump adds failure surface area. Eugene Yan and the Applied LLMs team found that prompt engineering + RAG + evals gets you 80–90% of the way there for most use cases.

**Principle 4 — Evaluation is an architectural component, not an afterthought.** You cannot run, improve, or trust an AI system without evals. In 2025, Google observed that evaluation evolved from a passive metric into an active architectural component — integrated directly into pipelines as a feedback loop.

**Principle 5 — The data layer is harder than the model layer.** Uber learned this at scale with Michelangelo: data is "generally the hardest part of ML." Feature stores, training-serving consistency, embedding pipelines, and vector database choice all matter more than the model in most production situations.

**Principle 6 — Design for graceful degradation from day one.** AI components will fail, hallucinate, time out, or return low-confidence outputs. The architecture must handle these as expected cases — not exceptions — with tiered fallbacks, confidence thresholds, and human-in-the-loop escalation paths.

**Principle 7 — Observability for AI is different from observability for traditional software.** Logging requests/responses is not enough. You need semantic drift detection, hallucination rate tracking, output quality metrics, and prompt version auditing. Traditional APM tools are blind to the dimensions that matter most for AI.

**Principle 8 — Caching, routing, and model cascades are primary cost controls.** At scale, 60–70% of queries can be handled by smaller, faster, cheaper models. Semantic caching eliminates repeat computation. These are not optimizations — they are core architectural decisions that determine whether a system is economically viable.

**Principle 9 — No GPU before PMF.** The Applied LLMs guide's most important strategic principle: validate your use case with API-hosted models first. Custom infrastructure, fine-tuning, and self-hosting come after you have proven product-market fit. Inverting this order is an expensive mistake.

**Principle 10 — Treat AI agents as well-engineered software, not magic.** The most successful production agents aren't autonomous beings — they are well-structured software systems that use LLMs for specific, controlled transformations at the right points. Own your control flow; don't outsource it to a framework.

---

## 2. Where Does AI Belong? The AI vs. Deterministic Decision Framework

### The core question

When you are designing a system and someone says "we should use AI for this," the right response is to ask a specific question: *Is the desired behavior too variable or unstructured to express as explicit logic?* If the answer is no — write the logic. If yes, AI earns its place.

This is not an AI-skeptical position. It is an engineering discipline position. AI has real, irreplaceable strengths. Those strengths apply to a specific class of problems. Applying them elsewhere adds cost, latency, and unpredictability without return.

### Decision criteria: when deterministic code wins

Use deterministic code when:

- The rule can be written explicitly without significant loss of accuracy (validation logic, date math, pricing formulas, compliance checks, permission checks, status transitions)
- The output must be auditable or explainable in a regulatory context
- The operation must be perfectly reproducible — same input, same output, every time
- Latency requirements are in single-digit milliseconds (deterministic logic runs in microseconds; model inference takes hundreds of milliseconds at minimum)
- Failures are not acceptable — financial transaction processing, authentication, access control

In healthcare, for example, clinical decision support systems use rule-based deterministic logic to apply standardized medical guidelines. A wrong output from a probabilistic model is not acceptable when the cost is a patient outcome. Banks use rule-based engines to validate loan applications against regulatory criteria for the same reason. (Source: Deterministic vs Non-Deterministic AI, Augment Code/Kubiya research, 2024–2025)

### Decision criteria: when AI wins

Use AI when:

- The input space is open-ended: natural language, images, audio, unstructured documents
- The output requires judgment that is context-dependent and cannot be fully specified in advance
- The goal is similarity, relevance, or meaning — not exact match
- Human behavior must be predicted or modeled
- The content needs to be generated, transformed, or summarized in ways that require natural language fluency
- Patterns must be found in high-dimensional data that are not enumerable as rules

Classic examples: semantic search (can't enumerate every synonym), content recommendation (can't enumerate every user preference permutation), document Q&A (can't enumerate every question), code completion, anomaly detection in logs.

### The hybrid architecture: AI interprets, deterministic code executes

The emerging consensus from 2024–2025 research is that the strongest production systems separate these roles cleanly. The AI interprets ambiguous or unstructured inputs and converts them into structured signals. Deterministic code then acts on those signals — enforcing business rules, executing transactions, updating state. This is sometimes called the "Rule Maker Pattern."

Think of it like this: the AI is the interpreter who translates what the user actually wants into a structured specification. The deterministic system then executes that specification faithfully. Neither component tries to do the other's job.

A concrete example from Stack Overflow's 2025 Developer Survey: developer trust in AI-generated code accuracy dropped from ~43% to ~33% between 2024 and 2025, even as adoption of AI coding tools continued rising. The lesson is that AI-generated code needs a deterministic validation layer (tests, linting, static analysis) on top — not because AI is bad, but because mixing AI generation with deterministic enforcement is the right architecture. The trust gap also signals that developers are becoming more calibrated about AI limitations, not necessarily that model quality dropped.

---

## 3. Core Architectural Patterns

### Pattern 1: Direct Prompting / API Integration

**What it is.** The simplest AI architecture: your application calls a foundation model API, passes a prompt, and uses the response. No infrastructure, no fine-tuning, no RAG.

**When to use it.** Prototyping, low-volume use cases, tasks where a general model is already good enough, situations where iteration speed matters more than cost efficiency.

**Trade-offs.** Cheap and fast to build. Not controllable at scale — you are dependent on the provider's model versions, pricing, and uptime. No customization to your domain. No context from your data. Output quality is ceiling-bounded by what the general model knows.

**Real-world example.** Martin Fowler's GenAI patterns article (Feb 2025, Thoughtworks) identifies direct prompting as the correct starting point for any GenAI system: "Direct Prompting gets you started." He and co-author Bharani Subramaniam describe it as a necessary first step before adding any other layer.

---

### Pattern 2: RAG — Retrieval-Augmented Generation

**What it is.** Instead of relying on what a model memorized during training, you retrieve relevant documents or records from an external store at query time and inject them into the model's context. The model then generates a response grounded in that retrieved content.

The pipeline has four stages: (1) documents are chunked and embedded into vectors, (2) vectors are stored in a vector database indexed for similarity search, (3) at query time, the user's query is embedded and compared against stored vectors to find relevant chunks, (4) those chunks are injected into the prompt as context, and (5) the model generates a response grounded in the retrieved material.

**When to use it.** When your application needs to answer questions about your proprietary data. When the model's training knowledge is outdated. When you need to reduce hallucinations by grounding the model in actual documents. When the data changes frequently and you can't retrain constantly.

**Trade-offs.** Reduces hallucinations dramatically. Enables use of proprietary data without fine-tuning. Adds pipeline complexity (ingestion, chunking, embedding, indexing, retrieval). Introduces retrieval failure modes — bad chunks produce bad answers even with a good model. Retrieval latency adds 50–200ms to response time at baseline.

**Real-world example.** Eugene Yan's *Patterns for Building LLM-based Systems* (2023): "RAG fetches relevant data from outside the foundation model and enhances the input with this data, providing richer context to improve output. RAG helps reduce hallucination by grounding the model on the retrieved context, thus increasing factuality." Martin Fowler's GenAI patterns identify hybrid retrieval (combining vector similarity with BM25 keyword matching) and query rewriting as key extensions of basic RAG for production use.

**Advanced RAG patterns.** At production scale, basic RAG gets extended with: query rewriting (the user's question is expanded or clarified before retrieval), reranking (a cross-encoder model reorders retrieved chunks for relevance), hybrid retrieval (combining dense vector search with sparse keyword search), and agentic RAG (the agent decides when to retrieve and what to retrieve rather than always retrieving).

---

### Pattern 3: Model Router and Gateway

**What it is.** A layer that sits between your application and your models, routing each request to the right model based on cost, latency, capability, or task type. A gateway adds API key management, rate limiting, logging, and policy enforcement at this same layer.

**When to use it.** When you have multiple models (different providers, different sizes, specialized vs. general). When cost optimization matters. When you need centralized control over which prompts go where.

**Trade-offs.** Adds a network hop. Requires routing logic that correctly classifies queries. Enables massive cost reduction (routing simple queries to small cheap models, complex queries to large expensive models) and resilience (fallback when one provider is down).

**Chip Huyen's architecture progression** (from *AI Engineering*, 2025) treats this as Step 3 in a 5-step layering approach: Enhance Context → Put in Guardrails → Add Model Router and Gateway → Reduce Latency with Caches → Add Agent Patterns.

**Real-world example.** Model cascade systems (HybridServe, Google's Speculative Cascades, Not-Diamond routing) route 60–70% of queries to small efficient models with 40–85% cost reduction and 2–10x faster responses, with zero quality loss on those queries. The key insight is that most queries are simple enough that a smaller model handles them correctly — only the complex tail needs the expensive model.

---

### Pattern 4: Model Cascade

**What it is.** A specific routing pattern where you try a small, fast, cheap model first. If its output meets a confidence threshold, you return it. If not, you escalate to a larger, slower, more expensive model. You only pay the cost of the large model for the queries that actually need it.

**When to use it.** High-volume inference workloads. Cost-sensitive applications. When task difficulty varies significantly across your query distribution.

**Trade-offs.** The confidence threshold is a hyperparameter that requires tuning. Adds latency when escalation happens (you've paid for two inference calls). Requires a confidence signal that is actually calibrated (not all models give reliable confidence scores).

**Research backing.** MLSys 2024 papers include several cascade architectures. Google's Speculative Cascades blog (Research) describes combining cascades with speculative decoding for better output quality at lower cost. The academic paper "A Unified Approach to Routing and Cascading for LLMs" (OpenReview, 2024) shows that a theoretically optimal cascade strategy outperforms existing strategies by up to 14%.

---

### Pattern 5: Context Augmentation Pipeline

**What it is.** A preprocessing layer that enriches every request before it reaches the model, injecting relevant context: user history, session state, retrieved documents, business rules, dynamic instructions. This is the formal architecture behind context engineering — building the right information packet for the model at every call.

**When to use it.** Always, in some form. Even simple applications benefit from structured context injection. Critical for personalized applications and for applications that need to stay current with changing business rules.

**Trade-offs.** Context has a hard ceiling — the model's context window. More context is not always better; irrelevant context degrades performance (the "lost in the middle" problem where models fail to use information in the middle of long contexts). Requires careful context selection and prioritization.

---

### Pattern 6: Guardrails — Input and Output Validation Layer

**What it is.** Validation logic that wraps the model call on both sides. Input guardrails filter or reject prompts before they reach the model (blocking prompt injections, out-of-domain requests, PII, policy violations). Output guardrails validate or block the model's response before returning it to the user (checking for hallucinations, harmful content, format violations, domain violations).

**When to use it.** Any production system. This is not optional. Martin Fowler's GenAI patterns (Feb 2025) describe guardrails as a non-negotiable layer: "Gen AI systems can be tricked into responding contrary to enterprise policies or leak confidential information, with guardrails added at the boundaries of the request/response flow."

**Architecture.** Think of guardrails as a middleware interception layer. The pattern is: Request → Input Guardrail → Model → Output Guardrail → Response. AWS Bedrock Guardrails, LlamaGuard, and NeMo Guardrails are managed implementations of this pattern.

**Three guardrail layers** (from production architecture guidance, 2026):
- Input guardrails: domain enforcement, PII detection, adversarial prompt detection, topic filtering
- Processing guardrails: tool access controls, RAG source restrictions, data access policies
- Output guardrails: factual grounding checks (NLI-based), format validation, content policy checks, confidence thresholds

---

### Pattern 7: Caching Layer

**What it is.** Storing model responses so repeated or similar queries don't require a new inference call. There are three tiers of caching: exact match (hash the prompt, return the cached response if the hash matches), semantic caching (embed the query, find cached responses within similarity threshold), and KV-cache / prefix caching (cache partial computation within the model itself for shared prompt prefixes).

**When to use it.** High-volume applications. Applications with system prompts that are long and shared across all calls. Chat applications where conversation history is re-sent with each turn.

**Impact.** Research shows 31% of LLM queries exhibit semantic similarity to previous requests. Anthropic's prompt caching reduces costs by up to 90% and latency by up to 85% for long prompts. OpenAI's automatic prefix caching achieves 50% cost reduction. At scale, this is arguably the single highest-ROI optimization available. (Source: LMCache technical report, 2024; Anthropic/OpenAI documentation)

---

### Pattern 8: Agent Pattern with Tool Use

**What it is.** Rather than a single prompt-and-response call, the model is embedded in a loop where it can use tools (APIs, databases, code interpreters, search engines), observe the results, and take further actions. The model acts as a reasoning engine that breaks down a task, executes steps, observes results, and adapts. Lilian Weng's foundational formulation (2023): Agent = LLM + memory + planning skills + tool use.

**When to use it.** Multi-step tasks that require information lookup, computation, or external side effects. Tasks where the path to the solution is not known in advance. Automation of complex workflows.

**Trade-offs.** Dramatically more capable than single-prompt systems for complex tasks. Also dramatically harder to debug, monitor, and control. Failures compound across steps. Costs multiply. Latency multiplies. Unpredictable behavior becomes a larger surface area. Use only when simpler patterns genuinely cannot solve the problem.

**Lilian Weng's taxonomy of agent components:**
- Planning: subgoal decomposition, reflection and self-correction (ReAct, Tree of Thoughts)
- Memory: in-context (short-term), external stores (long-term), embedding stores (semantic retrieval)
- Tool use: APIs, databases, code execution, search

---

### Pattern 9: Online vs. Offline Inference

**What it is.** Online inference (also called real-time inference) serves predictions synchronously as requests come in — the user waits for the result. Offline inference (batch inference) runs predictions on a dataset asynchronously, often on a schedule, and stores results for later lookup.

**When to use each:**

Online inference: user-facing features where low latency matters (chat, search re-ranking, real-time personalization), actions that depend on the current user context

Offline inference: generating embeddings for a document corpus, pre-computing recommendations for all users nightly, processing logs, any workload where freshness requirements can tolerate minutes-to-hours of delay

**The critical insight** (from Chip Huyen's *Designing Machine Learning Systems*, 2022, where she devotes ten pages to this decision): the choice is not about model capability — it is about freshness requirements and latency tolerance. A model running offline can be larger, more expensive, and higher accuracy because you are not blocking a user. An online model must be fast, which means smaller or more constrained.

**Real-world example.** Airbnb's Bighead platform and Netflix's Metaflow both support both modes. Netflix uses offline inference for generating recommendation scores that are stored and served at display time; it uses online inference for personalizing search results in real time.

---

### Pattern 10: Event-Driven AI Architecture

**What it is.** Instead of request-response interactions, AI components consume and produce events on a streaming bus (Kafka, Flink). Model inference is triggered by events rather than user requests. Results are published as events that other services consume.

**When to use it.** Real-time anomaly detection, fraud detection, continuous feature computation, AI systems that must react to business events (inventory changes, sensor readings, transaction patterns) rather than user queries.

**Trade-offs.** Decouples AI inference from the upstream trigger, enabling high throughput and resilience. Harder to debug because causality is non-linear. Latency is higher than synchronous calls for individual events.

**Real-world example.** Kai Waehner's 2024 research shows that Kafka + Flink is the standard architecture for event-driven AI. Apache Flink embeds model inference directly in the stream processing application. The Apache Flink Agents project (2025) bridges agentic AI with streaming, enabling event-driven agents that react to live data at scale.

---

### Pattern 11: Multi-Agent Architecture

**What it is.** Multiple specialized AI agents collaborating on a task. A lead (orchestrator) agent breaks down tasks and delegates to specialized subagents that work in parallel or sequence. The AI equivalent of a microservices architecture.

**When to use it.** Tasks that decompose naturally into independent subtasks. Tasks that require different kinds of expertise (research agent, writing agent, code agent, verification agent). Tasks where parallelism reduces total wall-clock time.

**Anthropic's production multi-agent research system** (Engineering blog, June 2025): A lead Claude agent plans and decomposes queries, delegates to specialized subagents that work in parallel, with each subagent needing "an objective, output format, guidance on tools and sources, and clear task boundaries — without which agents duplicate work, leave gaps, or fail to find necessary information." Google's Agent Development Kit (ADK) formalizes 8 design patterns for multi-agent systems.

**Trade-offs.** Each agent interaction is an LLM call that adds cost and latency. Coordination overhead grows superlinearly with agent count. Debugging requires tracing across agent boundaries. Handoff failures are common if task boundaries are unclear.

---

## 4. System Design Trade-offs Specific to AI

### Latency vs. accuracy

This is the defining tension of AI system design, and it does not have a universal answer — it has a context-specific answer. The right framework is to work backwards from your user's latency tolerance, then find the highest-accuracy model that fits inside that budget.

Practical rules:
- Interactive user-facing features (chat, search, autocomplete): target <500ms end-to-end. This usually means smaller models, caching, streaming tokens to the UI to make latency feel lower.
- Background processing (document analysis, report generation): latency tolerance is minutes to hours. Use the best model available.
- Real-time classification (fraud, content moderation): target <50ms. This usually means dedicated smaller models or offline scoring with online lookup.

The tiered cascade architecture (Pattern 4) is the most mature solution: route the cheap fast path for most queries, escalate the expensive slow path for hard ones.

### Cost vs. quality

The three primary cost drivers in AI systems are model size (larger models cost more per token), context length (cost scales with tokens in and out), and call frequency (every call costs money).

Cost controls, in order of impact:
1. Semantic and prefix caching — eliminate repeated computation (up to 90% savings per Anthropic's prompt caching data)
2. Model routing / cascade — use small models for easy queries (40–85% savings, per HybridServe and related research)
3. Context compression — summarize conversation history rather than re-sending it verbatim
4. Batching — combine multiple inference requests into a single GPU pass
5. Quantization — run models at lower numerical precision (int8, int4) with modest accuracy tradeoff

The Applied LLMs guide's strategic principle: "No GPUs before PMF." API-hosted models are expensive but require zero infrastructure. Invest in self-hosting only after proving the product works and after you understand your actual load patterns.

### Reliability and fallback architecture

AI components have a fundamentally different failure profile than traditional software. They can: time out (provider downtime), return with low confidence (uncertain outputs), hallucinate (confident but wrong), degrade gradually (model drift over time), or be injected (adversarial inputs that hijack behavior). None of these failure modes are visible to a standard health check.

The most resilient systems use a multi-tier fallback:

```
Tier 1: Primary large model (high quality, higher cost)
Tier 2: Smaller/faster model (lower quality, reliable)
Tier 3: Cached/pre-computed response (static, always available)
Tier 4: Rule-based fallback (deterministic, lowest quality)
Tier 5: Graceful failure message with human escalation
```

The key principle from production reliability research (ilovedevops.substack, ItSoli AI research, 2024): "You cannot degrade gracefully if you cannot detect failure. Every response should carry measurable indicators like model confidence and retrieval alignment, and when scores fall below defined thresholds, the system should degrade gracefully."

### Nondeterminism as a first-class property

Traditional software testing assumes determinism — same input, same output, every time. AI systems violate this assumption at the model level. This has cascading implications for architecture:

- Testing must be statistical, not exact (you test the distribution of outputs, not individual outputs)
- Evals replace unit tests as the primary quality signal
- Canary deployments require longer measurement windows
- Pin model versions in production (use `gpt-4o-2024-11-20`, not `gpt-4o`, per Applied LLMs operational guidance)
- A/B testing must account for user experience effects, not just model metrics

Martin Fowler (2025): "As software products using generative AI move from proof-of-concepts into production systems, evals play a central role in ensuring that non-deterministic systems operate within sensible boundaries."

---

## 5. Data Architecture for AI Systems

### The data stack for AI

A production AI system typically needs four kinds of data infrastructure, each serving a different purpose:

**Feature store.** A centralized repository for ML features — the input variables to models. A feature store has two halves: the offline store (historical features for training, usually backed by a data lake like Iceberg or Parquet in S3) and the online store (current features for inference, usually backed by a low-latency key-value store like Redis or DynamoDB). LinkedIn's Frame system and Uber's Palette are canonical examples. The feature store solves the single most damaging silent failure in ML production: training-serving skew.

**Training-serving skew** is what happens when the features computed during training are computed differently than the features computed during serving. The model learns from one distribution and is deployed into another. This causes degraded performance that is extremely hard to diagnose because the model looks correct in isolation. Tecton's research on this problem (2024) identifies it as "one of the biggest challenges in machine learning." The solution is to use a single feature pipeline for both training and serving — even if this requires accepting slightly higher serving latency.

**Vector database.** Stores high-dimensional embeddings and supports approximate nearest neighbor (ANN) search for semantic similarity. The primary backing store for RAG systems. Examples: Pinecone (managed, enterprise), Milvus/Zilliz (open source, GPU-accelerated), pgvector (Postgres extension, simpler ops), Qdrant, Weaviate, Chroma.

**Relational database.** Still the right choice for structured transactional data — user records, business entities, events with known schemas. AI systems do not replace the relational database; they add a vector database alongside it. The relational database continues to store the source of truth; the vector database stores embeddings derived from that source.

**Graph database.** Optimized for highly interconnected data where relationships between entities are as important as the entities themselves. The right choice for fraud detection, social network analysis, knowledge graphs, recommendation systems that require multi-hop relationship traversal. Graph databases (Neo4j, Amazon Neptune) are increasingly used in GraphRAG patterns where the knowledge graph provides structured relational context that vector similarity alone cannot capture.

### When to use which database — the decision criteria

| Question | Answer | Database |
|---|---|---|
| Do you need to find semantically similar content? | Yes | Vector DB |
| Is your data highly connected and relationship-traversal is primary? | Yes | Graph DB |
| Do you need ACID transactions and structured queries? | Yes | Relational |
| Are you storing embeddings to complement existing structured data? | Yes | Vector DB alongside Relational |
| Do you need to combine semantic search with structured filters? | Yes | Hybrid (vector + relational, or multi-modal vector DB) |

The emerging consensus is that the answer is "and, not or." Production systems use relational databases for the source of truth, vector databases for similarity search, and often graph databases for relationship-heavy domains. The interesting engineering work is keeping them synchronized.

### Embedding pipeline architecture

An embedding pipeline converts raw content (documents, images, code, user behavior) into vector representations that can be stored and searched. The pipeline has four stages: chunking (breaking long documents into pieces the embedding model can process), embedding (running each chunk through an embedding model to produce a vector), indexing (loading vectors into the vector database with ANN indexing like HNSW or DiskANN), and refreshing (re-embedding when source content changes).

Key decisions in embedding pipeline design:
- Chunk size: smaller chunks (128–512 tokens) give more precise retrieval; larger chunks give more context per retrieved piece. Most production systems use 256–512 tokens with 10–20% overlap.
- Embedding model: OpenAI's `text-embedding-3-large`, Cohere Embed, or open source (`bge-large-en-v1.5`, `e5-large`). The model must match between indexing time and query time.
- Re-embedding trigger: source content changes, embedding model version changes, or periodic full re-index. Each is a different operational burden.

### RAG data architecture at scale

For high-scale RAG (millions of documents, thousands of queries per second), the architecture must separate write and read paths. The write path (ingestion, chunking, embedding, indexing) is typically asynchronous and can tolerate higher latency. The read path (query embedding, ANN search, context injection) must be synchronous and fast.

Production RAG systems (per 2025-2026 practitioner guides) isolate indexing, ingestion, and query services so they don't contend for the same resources. They tune ANN search parameters experimentally for the latency/recall tradeoff, and they plan for tail latency — users notice the slowest 1% of requests.

---

## 6. Observability and Monitoring

### Why AI observability is different

Traditional software monitoring asks: is the service up? Is latency within SLA? Are error rates acceptable? These questions are necessary but not sufficient for AI systems. A model can be up, fast, and not throwing errors while simultaneously hallucinating, drifting from its training distribution, or being successfully prompt-injected.

The unique failure modes of AI systems require new observability primitives:

**1. Output quality metrics.** You cannot tell if an AI response is good by looking at the HTTP status code. You need output quality signals: factual accuracy, groundedness to retrieved context, relevance to the user's question, toxicity, format compliance, instruction following. These require either LLM-as-judge evaluation, human evaluation, or user feedback (explicit ratings, implicit signals like re-queries and abandonment).

**2. Semantic drift detection.** The distribution of what users ask changes over time. If your user base was initially experts and is now beginners, query complexity shifts. If a news event happens, new topics flood in. Semantic drift monitoring embeds incoming queries over time and tracks whether the distribution shifts relative to your training or evaluation dataset. Standard statistical tests (Population Stability Index, KL divergence, Jensen-Shannon divergence) apply to the embedding distributions.

**3. Prompt version auditing.** Prompts are code. When a prompt changes — even slightly — behavior changes. Production systems must version-control prompts, log which prompt version produced which response, and be able to replay evaluation sets against old and new prompt versions to compare.

**4. Trace-level logging for agents.** Multi-step agent systems require trace logging that captures the full thought-action-observation cycle: what the model was thinking (chain of thought), what tool it called, what the tool returned, and what decision it made next. Without this, debugging a failed agent run is archaeologically difficult.

**5. Hallucination rate tracking.** For RAG systems, a practical proxy for hallucination is groundedness: does the response make claims that are not supported by the retrieved context? NLI (Natural Language Inference) models can score this automatically at scale. Tracking the groundedness score over time surfaces degradation.

**6. Model drift.** When the underlying model is updated by a provider, behavior can change without any change in your code. Pinning model versions (Applied LLMs operational lesson) is the preventive measure. Continuous evaluation against a held-out golden dataset is the detective measure.

### Key metrics dashboard for a production LLM system

| Metric | Why it matters | How to measure |
|---|---|---|
| Response latency (p50, p95, p99) | User experience | Time from request receipt to response complete |
| Time to first token | Streaming UX | Time from request to first token emitted |
| Token usage (input + output per request) | Cost tracking | Provider API response metadata |
| Cost per successful response | Economic viability | Token usage × token price |
| Cache hit rate | Cost efficiency | Semantic/exact cache hit count / total requests |
| Fallback rate | Model reliability | Count of requests escalating to fallback |
| Groundedness score | Hallucination proxy | NLI score of response vs. retrieved context |
| User satisfaction | Output quality | Thumbs up/down, re-query rate, abandonment rate |
| Prompt injection attempts | Security | Adversarial pattern classifier on inputs |
| Semantic drift | Distribution shift | Embedding distribution change over time |

### Observability tooling landscape (2024–2025)

Purpose-built LLM observability platforms have emerged: Arize AI (real-time performance monitoring and drift detection), Evidently AI (open source, strong on drift and data quality), Langfuse (open source, trace-level logging for LLM chains), LangSmith (LangChain's observability platform), Weights & Biases (strong on training metrics, extending to LLM evals), OpenTelemetry (the open standard, with OpenLLMetry extension for LLM-specific signals).

The OpenTelemetry blog (2024) recommends instrumenting LLM calls with spans that capture: model name, model version, prompt template version, input token count, output token count, latency, and output metadata (finish reason, etc.). This enables trace-level debugging across complex chains and agents.

---

## 7. Scalability Patterns at Production Scale

### What major companies have learned

**Uber — Michelangelo.** Uber's ML platform runs over 20,000 model training jobs monthly and serves 10 million real-time predictions per second at peak across 5,000+ production models. Key architectural decisions: (1) Modular plug-and-play architecture — each component can be independently upgraded without rebuilding the platform. (2) Deep learning only where its advantages apply — in several cases, XGBoost outperforms deep learning in both performance and cost. (3) Bring tools to developers, not developers to tools — early versions forced engineers to learn a new workflow; later versions embedded the platform into existing development environments. (4) The hybrid online/offline challenge is unsolved — "there are no great tools that address the hybrid online/offline capabilities (batch, streaming, and RPC) required by realtime ML systems." This remains a genuine open problem.

**Netflix — Metaflow + Maestro.** Netflix runs diverse ML workloads across recommendation, media processing, content demand modeling, and more. Architecture philosophy: provide a user-centric abstraction layer (Metaflow) while relying on battle-tested compute infrastructure (Titus, a Kubernetes-based compute platform). Metaflow handles the ML workflow definition; Maestro handles production scheduling, execution management, and SLO enforcement at massive scale. Netflix's lesson: "Supporting diverse ML systems requires a separation between the user-facing workflow layer and the infrastructure-level execution layer." The two should not be the same system.

**Airbnb — Bighead.** Before Bighead, deploying a model required each team to build a custom serving container — typical time from model idea to production was eight to twelve weeks. Bighead reduced this to days by providing end-to-end ML lifecycle management: Redspot (Jupyter-as-a-service), Zipline (feature platform), Deep Thought (real-time inference). The key lesson: most of the cost in ML isn't the model training — it's the surrounding plumbing. Build the plumbing once, reuse it everywhere.

**Meta — FBLearner to MWFS.** Meta evolved from a monolithic ML platform (FBLearner Flow) to a modular, SDK-based system (MWFS) providing abstractions that simplify interaction with complex underlying infrastructure. The lesson: monolithic ML platforms become bottlenecks as the variety of ML use cases grows. Modular SDK-based approaches allow teams to compose the infrastructure they need.

**LinkedIn — ProML + Frame + VeniceDB.** LinkedIn's ProML (Productive Machine Learning) program covers the full ML lifecycle. Frame is their feature platform — a "virtual feature store" that describes features both offline and online, with backends: Iceberg table (offline), Kafka topic (streaming), Venice store or Pinot table (online). VeniceDB provides the low-latency online serving layer. Key lesson: a unified feature definition that spans offline and online computation is the most effective way to eliminate training-serving skew.

### Inference infrastructure patterns at scale

**Batching.** Multiple inference requests combined into a single GPU pass, amortizing compute overhead. vLLM implements continuous batching (also called in-flight batching), where the GPU processes tokens from multiple requests simultaneously rather than waiting for one request to complete before starting the next. This dramatically improves GPU utilization for generative inference. (MLSys 2024 research; vLLM blog, 2025)

**KV-cache management.** The key-value (KV) cache stores intermediate computation from the attention mechanism so tokens don't need to be recomputed for shared prefixes. At enterprise scale, the KV cache requires 100GB to 1TB of cached content. LMCACHE (2024) combined with vLLM achieves up to 15x throughput improvement by moving KV cache data across memory hierarchy intelligently.

**Kubernetes for orchestration.** Kubernetes is the de facto standard for deploying AI inference workloads in 2025, providing horizontal scaling, load balancing, and resource management. Netflix (Titus), LinkedIn, and most cloud providers offer Kubernetes-based inference serving. The llm-d framework (Red Hat, 2025) provides KV-cache-aware routing within Kubernetes clusters, directing requests to GPU pods that already have relevant context cached.

**Speculative decoding.** A smaller "draft" model generates candidate tokens; the larger target model verifies them in parallel. When the draft model is right (which is often), multiple tokens are confirmed in a single forward pass, increasing throughput without changing output quality. Google Research's Speculative Cascades (2025) extends this pattern to multi-model cascade architectures.

---

## 8. AI-Native vs. AI-Augmented Architecture

### The conceptual distinction

AI-augmented architecture starts with a working traditional software system and adds AI on top as an enhancement. The core logic remains deterministic; AI provides a better interface, smarter defaults, or an accelerator for specific tasks. Examples: adding AI-powered search to an existing e-commerce platform, adding an AI writing assistant to an existing content management system, using AI to generate SQL from natural language for a BI dashboard.

AI-native architecture is built from the ground up with intelligence as the primary design principle. Business logic lives in model behavior rather than in code branches. The architecture assumes that models will evolve and data will change continuously. Decision-making is probabilistic rather than deterministic at core. Examples: an AI agent that autonomously manages a customer service workflow end-to-end, a system where product recommendations are generated fresh for each user rather than fetched from precomputed buckets.

### Architectural implications of the distinction

**Data architecture.** AI-augmented: data is stored in traditional relational systems; AI consumes it as input. AI-native: the data architecture itself is built around continuous model feedback loops — inference outputs become training data, user interactions are signals that continuously reshape behavior.

**Testing and validation.** AI-augmented: most behavior is still deterministic and testable with standard unit/integration tests. AI-native: the primary quality signal is evaluation (evals), not tests. The system is correct when its distribution of outputs meets quality thresholds, not when it produces exact expected outputs.

**Rollback.** AI-augmented: roll back a model update and the system returns to deterministic behavior. AI-native: model rollback requires data rollback too, because the model and data are co-dependent. This makes deployment risk management significantly more complex.

**Operational complexity.** AI-augmented: the operational burden is the sum of traditional ops plus AI monitoring. AI-native: the entire operational model changes — you need real-time quality monitoring, continuous evaluation, and active feedback loops as core infrastructure.

### Which to build when

AI-augmented is the right starting point for almost every enterprise system that exists today. It is lower risk, preserves working logic, and gets AI value quickly. Most organizations that think they want AI-native actually want AI-augmented.

AI-native is justified when: (a) the core problem cannot be solved at all without AI (you are building something genuinely new, not augmenting something existing), (b) the system's value compounds over time from learning (the competitive moat is the model getting better), or (c) the deterministic code alternative would require maintaining a combinatorially large rule set that becomes unmaintainable.

The IBM AI-native definition (2024): "AI-native systems are those where the intelligence itself is persistent and contextual, decisions are not isolated events but part of an ongoing feedback loop, and the architecture assumes that models will evolve and data will change continuously."

---

## 9. Anti-Patterns — What to Avoid and Why

### Anti-pattern 1: Jumping to agents for problems that don't require them

The pattern: a simple task that could be solved with a well-crafted prompt gets built as a multi-step agent with tool use, orchestration, and complex state management.

Why it's damaging: agents multiply every failure mode. A single-prompt solution that works 95% of the time becomes a two-step agent that works 90.25% of the time (95% × 95%), a five-step agent that works 77.4% of the time. Debugging is an order of magnitude harder. Cost is proportionally higher. The 12-Factor Agents project (2025): "Most 'AI agents' that actually succeed in production aren't magical autonomous beings at all — they're mostly well-engineered traditional software, with LLM capabilities carefully sprinkled in at key points."

The fix: start with the simplest possible architecture. Add complexity only when the simpler architecture demonstrably fails.

---

### Anti-pattern 2: Scattered AI calls throughout the codebase

The pattern: LLM calls are embedded throughout the application — in controllers, service layers, utility functions — wherever a developer thought AI would be useful.

Why it's damaging: with no clean AI layer, you have no single place to manage prompts, monitor AI behavior, optimize costs, apply guardrails, or test AI components independently. When the model changes behavior, you cannot trace which calls are affected. From architectural reviews of LLM systems (2024): "If your LLM code is scattered everywhere, you have no clean layer to manage prompts or fine-tune parameters, leaving no single place to monitor how changes in AI output affect the rest of your system."

The fix: implement AI as a dedicated service layer (pattern: AI Gateway + Service Abstraction). All model calls flow through this layer. Everything is centrally logged, versioned, and observable.

---

### Anti-pattern 3: Framework over-indexing

The pattern: building a system by stringing together framework components (LangChain chains, agent frameworks, etc.) without understanding what each component does or why.

Why it's damaging: frameworks add abstraction layers that make debugging harder. Errors surface as framework exceptions rather than model behavior. You cannot reason about what the model is actually seeing as its prompt. When the framework has a bug or limitation, you are stuck. The 12-Factor Agents principle on this: "Own Your Control Flow." Agents = prompt + switch + context + loop. You should be able to write this yourself.

The fix: understand the underlying mechanics before reaching for a framework. Use frameworks for convenience once you understand what they are doing. Be prepared to drop down to raw API calls when debugging.

---

### Anti-pattern 4: No evaluation strategy

The pattern: deploying an AI feature based on vibes — a few manual tests, demos that looked good, developer intuition.

Why it's damaging: you cannot improve what you cannot measure. A 51% of organizations using AI experienced at least one negative consequence from AI inaccuracy in 2025 (McKinsey Global AI Survey). Without evals, you discover quality problems when users complain, not before deployment. Martin Fowler (2025): "Evals play a central role in ensuring that non-deterministic systems operate within sensible boundaries."

The fix: build a golden evaluation dataset before deploying. It can be small (50–100 examples) initially. Run it on every prompt change. Track metrics over time. The Applied LLMs guide: "A representative set of evals takes us a step towards measuring system changes at scale."

---

### Anti-pattern 5: Treating prompts as volatile configuration

The pattern: prompts are strings hardcoded in application code, modified by developers on the fly, with no version control, no documentation of what changed, and no tracking of how changes affect output quality.

Why it's damaging: prompts are logic, not configuration. A one-sentence change in a system prompt can dramatically change model behavior across all users. Without version control and eval regression testing, prompt changes are untested deployments.

The fix: version control prompts as code. Name prompt versions explicitly (the same way you name model versions). Run your evaluation dataset against old and new prompt versions before deploying the new one.

---

### Anti-pattern 6: Ignoring training-serving skew

The pattern: the team builds a feature pipeline for offline training, then builds a separate implementation of the same logic for online serving. The two implementations diverge over time.

Why it's damaging: the model is trained on features computed one way and served with features computed differently. Performance degrades silently. The gap between offline eval metrics and production performance is one of the most common and frustrating phenomena in ML engineering. Tecton (2024): "This can cause catastrophic and hard-to-debug model performance problems."

The fix: define features once, compute them from a single codebase, deploy the same computation to both offline and online paths. This is what feature stores like Feast, Tecton, and LinkedIn's Frame are designed to enforce.

---

### Anti-pattern 7: Deploying without fallbacks

The pattern: the AI component has a single path — it calls the model, uses the response. If the model times out, returns low confidence, or hallucinates, the system either crashes or returns a bad response.

Why it's damaging: AI components fail in ways that are hard to predict and hard to detect from outside. Downtime, hallucinations, and confidence drops all require fallback paths.

The fix: design the fallback tiers first (see Section 4). Every AI call should have a plan for what happens when it fails or returns low confidence.

---

### Anti-pattern 8: Treating security as an afterthought

The pattern: the system is built and launched, then someone raises the question of prompt injection, data leakage, or adversarial inputs.

Why it's damaging: prompt injection is the new SQL injection. A malicious input can hijack an AI agent's behavior, exfiltrate data, or bypass guardrails. Unlike SQL injection, prompt injection is harder to sanitize because the boundary between instructions and data in a prompt is not syntactic — it is semantic.

The fix: add input guardrails at the architecture design stage. Apply the principle of least privilege to tool access (agents should not have access to tools they don't need). Sanitize user inputs before injection into prompts. Treat the output of any external data source as untrusted when it enters the model's context.

---

## 10. The 12-Factor Agent Standard

Inspired by the original 12-Factor App for web applications, the 12-Factor Agents framework (HumanLayer, Dex Horthy, 2025) provides a language-agnostic manifesto for building production-ready LLM-powered software. It emerged from analysis of 100+ production agent implementations.

The central thesis: the most successful production agents are well-engineered software systems that leverage LLMs for specific, controlled transformations. They are not magic — they are software.

### The 12 factors

**Factor 1: Natural language to tool calls.** Convert unstructured user requests into structured, schema-valid commands. Define a clear JSON schema or function signature that the LLM must use when it wants to take an action. This is the first boundary between probabilistic (AI) and deterministic (code) components.

**Factor 2: Own your prompts.** Prompts are first-class code artifacts. Version control them. Test them. Treat a prompt change as a code deployment requiring eval regression testing.

**Factor 3: Own your context window.** Explicitly manage what goes into the model's context at each turn. Do not rely on the framework to handle this. The context window is your most precious resource — curate it deliberately.

**Factor 4: Tools are just JSON and code.** A tool call is nothing more than structured JSON that your code interprets and executes. Demystify the abstraction. You can implement tool execution in a 20-line switch statement if needed.

**Factor 5: Separate business state from execution state.** Business state (what the user wants, what has been accomplished, what decisions have been made) lives in a persistent store. Execution state (what step are we on, what tool are we calling) lives in memory during a run. Confusing these creates unrecoverable failures.

**Factor 6: Own your control flow.** Do not outsource the loop logic to a framework. The core of an agent is: prompt → model response → action dispatch → observation injection → repeat. Write this yourself. Understand every branch.

**Factor 7: Pause and resume over long-running tasks.** Agents that run for minutes or hours must be able to save state and resume after interruption. Design for this from the start. Treat every agent run as potentially interrupted.

**Factor 8: Contact humans as a first-class operation.** Human escalation is a tool call, not a failure mode. When the agent reaches uncertainty or a decision boundary it cannot cross alone, it should request human input through a structured, observable channel.

**Factor 9: Small, focused agents over large general agents.** An agent that does one thing well is more reliable than an agent that tries to do everything. Compose small specialized agents into larger systems rather than building monolithic agents.

**Factor 10: Stateless agent design.** Each agent turn receives full context as input and produces a result as output — no implicit memory, no side effects outside the explicitly declared tools. Design agents as pure functions: (state, event) → (new state, actions).

**Factor 11: Observability as a first-class concern.** Log every prompt sent, every response received, every tool call made, and every observation injected. Trace IDs should span the full agent run. Without this, debugging is impossible.

**Factor 12: Treat AI as a component, not the system.** The agent is embedded in a larger software system. It interacts with databases, APIs, queues, and other services through defined interfaces. The system architecture matters as much as the model.

---

## 11. Key Takeaways for Practitioners

These are the principles a working AI engineer or AI PM should internalize:

**On architecture scope.** AI components live inside larger systems. The surrounding system — evals, fallbacks, data pipelines, caching, guardrails, monitoring — determines production reliability more than the model itself. Invest accordingly.

**On the build progression.** Start with direct prompting + evals. Add RAG when you need grounding in proprietary data. Add routing/caching when cost matters. Add agents only when the task genuinely requires multi-step reasoning and external actions. Fine-tune only after you have validated product-market fit with a general model. Self-host only after you understand your actual load patterns.

**On data.** The data layer is harder than the model layer, always. Training-serving skew is one of the most common silent killers of production ML performance. Feature stores exist for this reason. Take them seriously.

**On evaluation.** Evals are not a QA step — they are a continuous architectural component. Every AI system needs a golden eval set. Every prompt change should run against it. Every model version upgrade should run against it.

**On cost.** Caching and model routing are not optimizations — they are fundamental architecture decisions. At production scale, a system without a caching layer and routing strategy is not economically viable. Design these in from the start.

**On reliability.** AI components fail in ways traditional monitoring cannot detect. Build observability for the dimensions that matter: output quality, semantic drift, hallucination rate, confidence distributions, prompt injection attempts. Instrument from day one.

**On agents.** The most successful production agents are software first, AI second. Own your control flow. Keep agents small and focused. Human escalation is a feature, not a failure. Treat every LLM call as a latency/cost/reliability bet that requires justification.

**On strategy.** No GPU before PMF. Validate the use case with hosted APIs. Prove the product. Then optimize infrastructure. This sequence is counterintuitive but saves enormous amounts of money and time.

---

---

## 12. MLOps Engineering Patterns

> **Distilled from:** GokuMohandas, *Made With ML* (madewithml.com, 2023–2025) — a production MLOps course building a text classification system from notebook through distributed serving and CI/CD. Source code at github.com/GokuMohandas/Made-With-ML.

This section covers the engineering mechanics of taking an ML model into production — the practices that sit between "the model works in a notebook" and "the model is reliably serving production traffic." These patterns are distinct from the architectural patterns in Section 3: they are about the MLOps lifecycle, not the system topology.

---

### Experiment Tracking with MLflow

**The core problem.** ML experimentation is inherently exploratory — you try many combinations of hyperparameters, architectures, and preprocessing choices. Without systematic tracking, you lose the ability to reproduce the best result, compare runs objectively, or understand which variable changed between a good run and a bad one.

**MLflow as the tracking substrate.** MLflow provides four components that together solve this: the **Tracking Server** (logs experiments, runs, metrics, parameters, and artifacts), the **Model Registry** (versions trained models and manages their promotion lifecycle), the **Projects** format (reproducible packaging), and the **Models** format (standardized serialization for multi-framework serving).

Every training run should log at minimum: hyperparameter configuration, epoch-level metrics (train loss, validation loss, learning rate), final evaluation metrics, and the model checkpoint as an artifact. The Made-With-ML pattern uses `MLflowLoggerCallback` integrated into the Ray Train distributed trainer — metrics are emitted per epoch, artifacts are saved at run end. Runs are organized within named experiments for clean comparison.

**Best run retrieval.** The registry enables programmatic selection: `get_best_run_id()` queries an experiment, sorts runs by a specified metric (validation loss in ascending order, or F1 in descending), and returns the run ID. The model checkpoint is then fetched via `get_best_checkpoint()` which resolves the artifact URI from the run metadata. This pattern separates training from deployment — the deployment system asks "what is the best model?" and the registry answers, without requiring knowledge of how or when it was trained.

**Distributed training integration.** When training is distributed across workers (Ray Train, Horovod, etc.), MLflow integration must be configured at the trainer level, not in individual worker functions. Only the rank-0 worker should write to the registry; others report metrics through the distributed trainer's native reporting mechanism (`train.report()` in Ray). The tracking URI must be set identically on all workers, typically via a shared file system path or a hosted tracking server.

**Checkpoint retention policy.** Keep only the best N checkpoints during training (`num_to_keep=1` is common) to avoid filling storage with intermediate models. The scoring metric determines which checkpoint is "best" — validation loss for most tasks, task-specific metrics (F1, AUROC) for imbalanced classification.

---

### Three-Tier ML Testing

Testing ML systems requires three distinct test categories that complement each other. Most teams implement only one or two.

**Tier 1: Code tests.** Standard software tests applied to the ML codebase — unit tests for preprocessing functions, data transformation utilities, batch collation logic, and serialization. These use standard pytest patterns: parametrize for multiple input cases, temporary fixtures for I/O, numpy/torch equality assertions for array operations. Critical to include: seed reproducibility tests (verify that `set_seeds()` produces identical random sequences), and data format tests (verify tensor dtype, device placement, and shape after batching).

**Tier 2: Data tests.** Validation that the dataset used for training meets structural and distributional requirements before training begins. This includes: class distribution checks (each class must have sufficient representation after train/test split — `stratify_split()` enforces this), schema validation (required columns exist), and range checks on features. Running data tests in CI catches upstream data quality issues before they propagate to model performance silently.

**Tier 3: Model behavioral tests — slice-based evaluation.** This is the most underused tier and the most powerful for catching real-world failure modes. Rather than reporting only aggregate metrics (overall precision/recall/F1), slice-based evaluation computes metrics on **specific subsets** of the test data defined by domain-relevant attributes.

The Made-With-ML implementation uses Snorkel's `PandasSFApplier` to define **slicing functions** — predicates that label which rows belong to a slice:
- `nlp_llm` slice: projects mentioning transformers, LLMs, or BERT (the high-attention domain)
- `short_text` slice: projects with fewer than 8 words in combined title and description

Each slice is evaluated independently with its own precision, recall, and F1 (using micro averaging for slice-level metrics). Slices that underperform aggregate metrics reveal failure modes that aggregate metrics hide. A model with 88% overall F1 might have 61% F1 on short-text inputs — a critical bug for a production text classifier that would never surface in headline metrics.

**Implementing the three-tier testing structure:**
```
tests/
  code/     ← pytest unit tests for functions and utilities
  data/     ← dataset validation tests run before training
  model/    ← slice-based behavioral tests and performance thresholds
```

---

### Confidence-Based Output Filtering

A practical pattern for classification systems where low-confidence predictions are worse than no prediction at all. Instead of always returning the top predicted class, the serving layer applies a **confidence threshold**: if the maximum predicted probability across all classes is below the threshold, the prediction is reclassified as "other" (or an explicit abstention).

In the Made-With-ML implementation: the model predicts probability distributions across topic classes. If `max(probabilities) < 0.9`, the output is overridden to "other" rather than returning a low-confidence tag. This threshold is a configurable runtime parameter passed to the serving layer — it can be changed without redeploying the model.

The design implications: (1) the "other" class must be handled downstream by the consuming application, (2) the threshold is itself a hyperparameter that trades off coverage (predictions made) against precision (predictions that are correct), and (3) operating the threshold in production requires monitoring the distribution of "other" outputs — a spike in "other" rate is a signal of distribution shift.

This pattern applies beyond classification: confidence-based filtering in RAG systems (abstaining from answering when retrieval quality is low), in summarization (flagging outputs where the model's self-consistency score is below threshold), and in agentic systems (escalating to human review when the agent's confidence in a plan is low).

---

### Distributed Model Serving with Ray Serve

**The architecture.** Ray Serve is a scalable model serving library built on Ray. The `@serve.deployment` decorator converts a Python class into a distributed serving deployment with configurable replicas and resource allocation. The class receives HTTP requests, runs preprocessing and inference, and returns responses. A FastAPI `@serve.ingress` wrapper adds typed request/response schemas and automatic documentation.

**Resource specification.** Each deployment specifies CPU and GPU requirements at the actor level: `ray_actor_options={"num_cpus": 8, "num_gpus": 0}`. This enables the serving cluster to pack multiple model replicas onto available hardware. For GPU-intensive models, setting `num_gpus=1` pins each replica to a dedicated GPU. The number of replicas scales horizontally — Ray Serve handles request routing across replicas automatically.

**Endpoint design for ML serving.** Beyond the inference endpoint, production ML APIs should expose:
- `GET /` — health check returning service status and version
- `GET /run_id/` — the active model's registry identifier (enabling correlation between predictions and the model that made them)
- `POST /predict/` — inference endpoint with typed request schema
- `POST /evaluate/` — trigger evaluation on a labeled dataset (useful for online evaluation without redeployment)

**Model loading from registry at startup.** The serving class constructor calls `get_best_checkpoint()` from the model registry, initializing the predictor once at startup. All subsequent requests reuse the loaded model. This means updating the serving model requires redeploying the deployment (or implementing a more sophisticated hot-swap pattern). The `run_id` parameter makes the active model explicit and auditable.

---

### CI/CD for ML: Automated Training and Evaluation in Pull Requests

The most operationally mature pattern from Made-With-ML is treating model training and evaluation as a CI/CD artifact. When a developer opens a pull request, GitHub Actions automatically:

1. Submits a distributed training job (`anyscale jobs submit deploy/jobs/workloads.yaml --wait`)
2. Waits for completion and fetches results from S3
3. Converts JSON training and evaluation metrics to a markdown summary
4. **Posts the metrics as a PR comment**, making model performance visible to code reviewers

This pattern fundamentally changes the development feedback loop. Instead of asking "does the code run?", the CI pipeline asks "does the model perform acceptably?" Reviewers see training loss, validation metrics, and slice-level performance without needing to run anything locally. Performance regressions are visible before code merges to main.

**Two separate pipelines.** ML CI/CD separates training from serving:
- `workloads.yaml`: triggered on pull requests → runs training + evaluation → reports metrics to PR
- `serve.yaml`: triggered on push to main → deploys the new model to the serving cluster

The serving pipeline uses Anyscale's `rollout` command with a declarative `serve_model.yaml` configuration, authenticating via IAM role (not long-lived credentials). This separates the decision to merge code from the decision to deploy — code merges when metrics are acceptable; deployment is automatic after merge.

**Infrastructure setup per workflow run:**
- AWS IAM role assumption via OIDC (not access keys)
- Python pinned to a specific minor version (3.10.11)
- Dependencies pinned by version in requirements files
- Secrets (cluster tokens, API keys) stored in GitHub repository secrets, not in code

---

### Reproducibility Engineering

**Reproducibility is not automatic** in ML systems. The same code can produce different results across runs due to: non-deterministic GPU operations, random weight initialization, shuffled data loading, and probabilistic sampling during training. Production ML systems require explicit reproducibility controls.

**Seed management.** A `set_seeds()` utility must set seeds for every random number generator in the stack: Python's `random`, NumPy, PyTorch CPU, and PyTorch CUDA. Setting only one is insufficient — they are independent RNG streams. Unit tests for seed management verify that two runs with identical seeds produce identical outputs before and after seed reset.

**Dependency pinning.** All dependencies — ML frameworks, utility libraries, data processing — must be pinned to exact versions in `requirements.txt`. Major library updates (PyTorch, Transformers, Ray) regularly change numeric results for the same model configuration. Pre-commit hooks validate that pinned versions are used before code is committed.

**Experiment registry as the source of truth.** The MLflow model registry provides the authoritative record of what model is running in production: the exact run ID, the hyperparameter configuration, the training data version, the evaluation metrics, and the checkpoint artifact. Any production incident investigation starts here, not with code. The run ID exposed by the serving API's `/run_id/` endpoint makes this linkage operational.

**Configuration management.** A single `config.py` module is the canonical location for all paths, constants, external service URIs, and logging configuration. Domain-specific constraints (stopword lists, class definitions, confidence thresholds) live here rather than scattered across the codebase. This enables environment-specific overrides (local vs. cluster storage paths, local vs. hosted MLflow URI) without modifying application code.

---

### Hyperparameter Optimization

**HyperOpt with warm starting.** Rather than random search, production hyperparameter optimization uses Bayesian optimization: `HyperOptSearch` with initial points specified by the practitioner. This provides: (1) domain knowledge injection — if you know from prior experiments that learning rate of 1e-4 is a good starting point, you encode that as an initial point, (2) convergence acceleration — Bayesian methods find good configurations in fewer trials than random search.

**AsyncHyperBand for early stopping.** `AsyncHyperBandScheduler` terminates underperforming trials early based on intermediate metric values. Trials that diverge or stagnate are stopped before they consume their full compute budget, freeing resources for more promising configurations. The scheduler promotes trials that pass a grace period with acceptable metrics. This pattern makes hyperparameter search tractable at scale — you can explore a larger search space with the same compute budget by pruning bad trials aggressively.

**Search space design.** The Made-With-ML search space targets: dropout probability (0.3–0.9 uniform), learning rate (1e-5 to 5e-4 log-uniform), LR decay factor (0.1–0.9 uniform), and scheduler patience (1–10 integer). Log-uniform scaling for learning rate is critical — learning rates differ by orders of magnitude in impact, and linear sampling wastes budget on large-LR configurations that typically underperform.

**Concurrency limits.** Set explicit concurrency limits on parallel trials to avoid resource contention: too many parallel trials on a single cluster starves each trial of compute, producing noisy metrics that mislead the Bayesian optimizer. Two to four concurrent trials per GPU cluster is a reasonable default.

---

## Sources

- [AI Engineering (Chip Huyen, O'Reilly, 2025)](https://www.oreilly.com/library/view/ai-engineering/9781098166298/) — Architecture patterns, RAG, agents, evaluation, model routing
- [Designing Machine Learning Systems (Chip Huyen, O'Reilly, 2022)](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/) — Online vs. offline inference, data pipelines, feature engineering
- [Patterns for Building LLM-based Systems & Products (Eugene Yan, 2023)](https://eugeneyan.com/writing/llm-patterns/) — 7-pattern taxonomy including RAG, evals, guardrails, caching, user feedback
- [What We've Learned From A Year of Building with LLMs (Applied LLMs, 2024)](https://applied-llms.org/) — Tactical, operational, and strategic lessons; "no GPU before PMF"
- [Emerging Patterns in Building GenAI Products (Martin Fowler & Bharani Subramaniam, Feb 2025)](https://martinfowler.com/articles/gen-ai-patterns/) — 9 patterns for GenAI products, guardrails, RAG, evals
- [Meet Michelangelo: Uber's Machine Learning Platform (Uber Engineering)](https://www.uber.com/blog/michelangelo-machine-learning-platform/) — Feature stores, training-serving at scale, modular ML platform design
- [Supporting Diverse ML Systems at Netflix (Netflix Tech Blog / QCon SF 2024)](https://netflixtechblog.com/supporting-diverse-ml-systems-at-netflix-2d2e6b6d205d) — Metaflow, Maestro, diverse ML workloads, workflow orchestration
- [Bighead: Airbnb's End-to-End Machine Learning Platform](https://aicouncil.com/talks/bighead-airbnbs-end-to-end-machine-learning-platform) — Full ML lifecycle platform, reducing time-to-production
- [Building Meta's GenAI Infrastructure (Engineering at Meta, 2024)](https://engineering.fb.com/2024/03/12/data-center-engineering/building-metas-genai-infrastructure/) — Hardware and software ML infrastructure at Meta's scale
- [QCon London: Lessons Learned from LinkedIn's AI/ML Data Platform (InfoQ, 2024)](https://www.infoq.com/news/2024/04/linkedin-ai-platform-venicedb/) — VeniceDB, Frame feature store, ProML platform
- [LLM Powered Autonomous Agents (Lilian Weng, 2023)](https://lilianweng.github.io/posts/2023-06-23-agent/) — Agent architecture taxonomy: planning, memory, tool use
- [12-Factor Agents (HumanLayer / Dex Horthy, 2025)](https://github.com/humanlayer/12-factor-agents) — Principles for production-ready LLM applications
- [Well-Architected Framework: AI and ML Perspective (Google Cloud, 2024)](https://docs.cloud.google.com/architecture/framework/perspectives/ai-ml) — Reliability, performance, operational excellence for AI/ML on cloud
- [HybridServe: Efficient Serving with Confidence-Based Cascade Routing (arXiv, 2025)](https://arxiv.org/abs/2505.12566) — Model cascade architecture, cost/quality optimization
- [Speculative Cascades (Google Research, 2025)](https://research.google/blog/speculative-cascades-a-hybrid-approach-for-smarter-faster-llm-inference/) — Combining speculative decoding with cascade routing
- [MLSys 2024 Conference Proceedings](https://mlsys.org/Conferences/2024/AcceptedPapers) — SLoRA, VIDUR, SiDA, scalable serving research
- [How Apache Kafka and Flink Power Event-Driven Agentic AI (Kai Waehner, 2025)](https://www.kai-waehner.de/blog/2025/04/14/how-apache-kafka-and-flink-power-event-driven-agentic-ai-in-real-time/) — Event-driven AI architecture
- [Rethinking the Twelve-Factor App Framework for AI (Google Cloud Blog)](https://cloud.google.com/transform/from-the-twelve-to-sixteen-factor-app) — Extended 12-factor principles for AI systems
- [An Introduction to Observability for LLM-based Applications using OpenTelemetry (2024)](https://opentelemetry.io/blog/2024/llm-observability/) — LLM observability standards and instrumentation
- [Solving the Training-Serving Skew Problem with Feast Feature Store (Medium, 2025)](https://medium.com/@scoopnisker/solving-the-training-serving-skew-problem-with-feast-feature-store-3719b47e23a2) — Feature store patterns, skew prevention
- [Made With ML — GokuMohandas (madewithml.com, 2023–2025)](https://github.com/GokuMohandas/Made-With-ML) — MLOps engineering patterns: experiment tracking, three-tier ML testing, slice-based evaluation, distributed serving with Ray Serve, CI/CD for ML, confidence-based filtering, reproducibility engineering, hyperparameter optimization with HyperOpt + AsyncHyperBand
