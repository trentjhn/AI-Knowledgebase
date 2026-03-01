# Playbook: Building RAG Pipelines

> **Use this when:** You need an AI to answer questions based on specific, up-to-date, or proprietary information — documentation, internal knowledge bases, support articles, research papers, legal documents, product databases — that either doesn't exist in the model's training data or can't be stuffed entirely into a system prompt.

---

## What RAG Is and Why It Matters

Every language model has a knowledge cutoff — it knows what it was trained on and nothing more. Beyond that, even within its training data, it can confabulate: generate plausible-sounding but wrong answers for specific facts, names, dates, and figures.

RAG (Retrieval-Augmented Generation) is the standard solution to both problems. Rather than asking the model to recall facts from memory, RAG retrieves the relevant information from an external source at query time and injects it into the prompt. The model then *reads* the retrieved content and synthesizes an answer from it.

The mental model: instead of a model that "knows things," you have a model that "reads things and explains them." This is a more reliable and more maintainable approach to factual accuracy than relying on training data alone.

---

## How RAG Works (The Pipeline)

A RAG pipeline has three stages, each of which has design choices that significantly affect quality:

**1. Ingestion** — Getting your documents into a searchable form
Your documents are split into chunks, converted into embeddings (numerical representations of meaning), and stored in a vector database. When a query comes in, the query is also converted to an embedding and compared against stored embeddings to find the most semantically similar chunks.

**2. Retrieval** — Finding the relevant content
Given a user query, the system retrieves the top-K most relevant chunks from the vector database. The quality of retrieval determines the ceiling on answer quality — if the right information isn't retrieved, the model can't use it.

**3. Generation** — Producing the answer
The retrieved chunks are injected into the prompt alongside the user's question. The model reads the chunks and generates an answer grounded in what it just read, not what it remembered.

---

## Core Technique Stack

### 1. Chunking Strategy — The Most Underrated Decision

How you split your documents into chunks has an outsized effect on retrieval quality. Get this wrong and you'll retrieve chunks that contain half of an answer — or chunks that happen to match the query keywords but don't actually answer the question.

**Key chunking principles:**
- **Chunk by semantic unit, not by character count.** A chunk should contain one complete idea, not 500 arbitrary characters. Paragraphs or sections are better boundaries than fixed-length splits.
- **Include overlap.** When you split documents, have consecutive chunks share some content (e.g., 10–15% overlap). This prevents answers that span a chunk boundary from being split across two non-adjacent retrievals.
- **Keep metadata with chunks.** Store the source document, section title, and page number alongside each chunk. This lets you cite sources in answers and helps users verify information.
- **Different document types need different strategies.** A legal contract has very different structure from a support article. Tune your chunking approach per document type rather than applying one strategy everywhere.

### 2. Query Understanding Before Retrieval

Users rarely phrase their questions in the same language as your documents. Someone asking "how do I cancel?" might be looking for content titled "Subscription Management" or "Account Settings." If you retrieve purely based on the literal query, you'll miss relevant content.

**Techniques:**
- **Query rewriting.** Before retrieval, use an LLM call to rephrase the user's query into a more complete, precise form likely to match your document language. "how do I cancel?" becomes "What is the process for canceling a subscription or account?"
- **HyDE (Hypothetical Document Embedding).** Generate a hypothetical answer to the query, then retrieve based on that hypothetical answer's embedding rather than the raw query. Since your hypothetical answer is in the same style as your documents, it retrieves more relevant chunks.
- **Multi-query retrieval.** Generate 2–3 variations of the query and retrieve for each. Take the union of results. This catches relevant content that a single query phrasing might miss.

### 3. Context Injection — What Goes Into the Prompt

Once you've retrieved relevant chunks, you need to inject them into the prompt in a way the model can use effectively.

**Best practices:**
- **Put retrieved content before the question.** The model attends more reliably to content that comes before the question than after it. Structure your prompt as: system instructions → retrieved chunks → user question.
- **Label the sources clearly.** Wrap each chunk with its metadata: `[Source: Product FAQ, Section: Billing, Last updated: 2025-01]`. This helps the model cite sources accurately and helps you audit answers.
- **Instruct the model to use only the retrieved content.** Add to your system prompt: "Answer based only on the provided documents. If the documents don't contain the answer, say so — do not use outside knowledge." This prevents the model from mixing retrieved facts with hallucinated ones.
- **Cap the number of chunks.** More retrieved chunks is not always better. Past 5–8 chunks, the model starts to lose track of the earlier ones. A smaller number of highly relevant chunks usually outperforms a large number of loosely relevant ones.

### 4. Grounding and Hallucination Prevention

Even with retrieved content in the prompt, models can still drift — paraphrasing retrieved content in ways that change its meaning, or filling in gaps with confabulated details. Prevent this with explicit grounding instructions.

**In your system prompt:**
- "Quote directly from the documents when accuracy is critical."
- "If the documents partially address the question but don't fully answer it, say what the documents do say and acknowledge what's missing."
- "Do not infer or extrapolate beyond what the documents state."

**Chain-of-Verification:** For high-stakes answers, have the model verify its own response against the retrieved documents after generating it. Prompt: "Review your answer against the provided documents. Does every claim you made appear in the documents? Correct anything that doesn't."

See `prompt-engineering/prompt-patterns.md` for the Fact Check List and Reflection patterns, which apply directly here.

### 5. Fallback Behavior

The system needs a principled response when it can't find an answer — not a hallucinated one. Design this explicitly:

- **"I don't know" is a valid answer.** Prompt the model: "If the retrieved documents don't contain enough information to answer the question, say so clearly. Provide what information you do have and suggest where else the user might look."
- **Escalation path.** For chatbot contexts, define what happens when RAG fails: link to documentation, connect to a human, or surface a search interface.

---

## Recommended Workflow

**Step 1: Understand your documents before building anything**
Before writing any code, read through a representative sample of your source documents. What kinds of questions will users ask? Do your documents actually contain the answers? How are they structured? This shapes every subsequent decision.

**Step 2: Choose your chunk size experimentally**
Start with semantic chunking (paragraph-level) and evaluate retrieval quality on a set of test queries. Are the retrieved chunks actually answering the questions? Adjust chunk size, overlap, and splitting strategy based on what you observe.

**Step 3: Build and test retrieval in isolation**
Before connecting the LLM, test your retrieval layer alone. Given a test query, do the top-K retrieved chunks actually contain the answer? If retrieval fails, the model can't compensate. Fix retrieval problems here, not in the prompt.

**Step 4: Design the generation prompt**
Once retrieval is working, write the system prompt for the generation step. Be explicit about grounding, citation, and fallback behavior. Test it on cases where the answer is in the documents and cases where it isn't — both should behave correctly.

**Step 5: Add query enhancement**
Once the basic pipeline works, add query rewriting or multi-query retrieval. Measure whether retrieval quality improves. This step often produces the biggest quality jump after the initial build.

**Step 6: Evaluate end-to-end**
Build a test set of question-answer pairs from your actual documents. Run the full pipeline on every test case. Measure: did it retrieve the right content? Did it answer correctly? Did it hallucinate anything? Use this as your baseline and regression suite.

---

## Common Pitfalls

**Retrieval returns irrelevant chunks.** The semantic similarity of the query doesn't match the semantic content of the answer. Fix: try query rewriting, HyDE, or hybrid retrieval (combining semantic similarity with keyword matching). Also check your chunking — very short chunks often lose context.

**The model ignores retrieved content and uses training data instead.** Fix: make the grounding instruction more explicit. Add: "Your knowledge is limited to the documents provided below. Do not use any other information." Also ensure retrieved content is prominently placed in the prompt — content buried deep is attended to less reliably.

**Retrieved content is stale.** The vector database contains an old version of a document. Fix: implement document versioning and timestamp checking. Re-ingest updated documents promptly. Add last-updated metadata to chunks so the model can note when information may be outdated.

**Too many chunks dilute the answer.** The model retrieves 10 chunks, most loosely related, and synthesizes a generic response. Fix: reduce K (the number of retrieved chunks), add a reranking step to select the most relevant subset, or implement a "minimum relevance score" threshold below which chunks are discarded.

**Chunks cut through important context.** The retrieved chunk starts mid-sentence or mid-explanation. Fix: increase chunk overlap, use semantic splitting rather than character-based splitting, or include surrounding sentences as context padding around each chunk.

---

## Scaling Up

**Reranking.** After initial retrieval, add a second pass that reranks the retrieved chunks by relevance to the specific query. Cross-encoder reranking models can significantly improve which chunks the model ultimately sees.

**Hybrid search.** Combine semantic (vector) search with keyword (BM25) search and merge the results. Keyword search catches exact matches that semantic search misses; semantic search catches paraphrases that keyword search misses. The combination outperforms either alone. See the full section below.

**Parent/Child hierarchical indexing.** Store documents at two granularities — small child chunks and large parent chunks — but only index the child chunks for search. When retrieval finds a relevant child chunk, return its parent chunk to the model instead. This gives you the best of both sizes: child chunks are precise enough to match a specific query accurately, while parent chunks carry enough surrounding context for the model to generate a complete, well-grounded answer. A child chunk that perfectly matches "cancellation policy" might be three sentences — not enough context to explain the full policy. Its parent section might be three paragraphs, which is what you actually want to generate from.

**Query clarification vs. query rewriting.** These are related but distinct and should be handled separately. *Rewriting* is automatic — resolve pronoun references ("How do I update it?" → "How do I update the SQL schema?"), split compound questions into focused sub-queries, and rephrase for better embedding similarity. This happens every time, algorithmically. *Clarification* is different: it pauses the pipeline and asks the user when the query is genuinely too ambiguous to resolve without their input. The split matters because rewriting everything automatically creates noise (you change the user's meaning), while never clarifying means you silently retrieve for the wrong thing. Use rewriting by default; use clarification sparingly, only when retrieval would be meaningless without more context.

**Agentic RAG with multi-agent map-reduce.** For complex questions that require multiple lookups, the basic agentic pattern is: retrieve, evaluate whether results are sufficient, re-query with a refined query if not, synthesize when confident. For questions that are actually multiple questions in one ("Compare X and Y across A, B, and C"), go further: decompose the question into independent sub-queries, spawn a parallel agent per sub-query, let each agent run its own retrieval and self-correction loop independently, then aggregate all agent responses into a single answer. This is slower and more expensive but handles multi-hop and multi-part questions that sequential single-shot retrieval simply cannot answer well. Each sub-agent can also compress its own retrieved context before returning results, keeping the aggregation step from drowning in tokens. See the full Agentic RAG section below.

**Evaluation pipeline.** Track retrieval quality (did the right chunk get retrieved?), faithfulness (is the answer grounded in retrieved content?), and answer quality (is the answer correct?) as separate metrics. They fail independently and require different fixes.

---

## Hybrid Search — BM25 + Semantic with RRF

Most production RAG systems use hybrid retrieval — not semantic-only. Understanding why, and how to implement it, is the difference between a system that works in demos and one that works on real user queries.

### Why Keyword Search First

The counterintuitive professional approach is to implement BM25 keyword search *before* semantic search, not after. The reason: semantic search fails on exact matches. When a user asks about a specific product name, error code, API endpoint, or person's name, the semantic embedding of "TypeError: cannot read property of undefined" may not retrieve the document that contains that exact string — because semantically similar documents might discuss a completely different error. BM25 finds it immediately.

BM25 (Best Match 25) is a probabilistic keyword ranking function. It scores documents based on how often query terms appear in the document, adjusted for document length and term frequency saturation — so adding the same keyword 50 times doesn't keep increasing the score. It's fast, predictable, and excellent at exact and near-exact matches.

The correct mental model: **BM25 handles precision (did we find the right document?), semantic handles recall (did we find documents that are relevant but phrased differently?).** You need both.

### Reciprocal Rank Fusion (RRF)

RRF is the standard algorithm for combining ranked results from multiple retrieval systems into a single merged list. It's simple, parameter-light, and works well in practice.

The formula for each document's RRF score:

```
RRF_score(doc) = Σ 1 / (k + rank_in_system_i)
```

Where `k` is a constant (typically 60) and `rank_in_system_i` is the document's rank in retrieval system `i` (BM25 rank, semantic rank, etc.).

What this does: a document that ranks 1st in BM25 and 5th in semantic gets a high combined score. A document that ranks 50th in BM25 and 51st in semantic gets a low combined score even though it appeared in both lists. Documents that only appear in one list get partial credit. The `k` constant prevents the top-ranked document from having an outsized influence.

In practice, for a hybrid system:
1. Run BM25 retrieval → get ranked list A
2. Run semantic retrieval → get ranked list B
3. For every document in the union of A and B, compute its RRF score
4. Sort by RRF score descending — this is your merged ranked list
5. Take top-K documents for the model

### Hybrid Search Architecture

A production hybrid search layer typically looks like this:

```
User query
    ↓
[Parallel retrieval]
    ├── BM25 search → top-20 by keyword rank
    └── Semantic search → top-20 by embedding similarity
    ↓
[RRF fusion]
    → merge and re-rank by combined score
    ↓
[Top-K selection]
    → take top 5-8 for the model
    ↓
[Optional: reranking]
    → cross-encoder reranking on the merged set
```

Expose a single unified search API that accepts a `mode` parameter: `keyword_only`, `semantic_only`, or `hybrid`. This lets you A/B test retrieval modes and fall back cleanly if one system degrades.

### Section-Based Chunking for Hybrid Search

For hybrid retrieval to work well, chunks need to preserve logical document boundaries rather than split arbitrarily. Section-based chunking uses document structure (headings, sections, paragraphs) as natural chunk boundaries. This keeps complete ideas within a single chunk, which improves both BM25 precision (the relevant term appears alongside its context) and semantic accuracy (the embedding represents a complete thought, not half a sentence).

---

## Agentic RAG — The Decision Graph

Standard RAG is a fixed pipeline: retrieve → inject → generate. Agentic RAG adds decision nodes that let the system evaluate its own retrieval quality and adapt before generating an answer. The result is a system that handles difficult queries gracefully instead of generating a confident but wrong answer based on irrelevant chunks.

### The Core Decision Graph

```
User query
    ↓
[Retrieval]
    → BM25 + semantic hybrid search
    ↓
[Document Grading]
    → Is each retrieved chunk relevant to the query?
    ↓
    ├── All/most chunks relevant → [Generation]
    │                                   → Final answer
    └── Insufficient relevant chunks → [Query Rewriting]
                                            ↓
                                       [Re-retrieval]
                                            ↓
                                       [Document Grading]
                                            ↓
                                       [Generation] (with what we have)
```

This loop has a maximum iteration count — typically 2–3 rewrites before generating with whatever was retrieved, or returning a "I couldn't find sufficient information" response.

### Document Grading

Document grading is an LLM call that evaluates each retrieved chunk independently: "Given this query, is this document relevant enough to include in the answer?" The grader returns a binary yes/no (or a relevance score), and low-scoring chunks are filtered out before generation.

This prevents the main generation step from receiving noise chunks that would dilute or contradict the answer. A grader catches retrieval failures that RRF scores don't — a document can rank highly in both BM25 and semantic search while being completely unhelpful for the specific query.

Grader prompt pattern:
```
You are a relevance assessor. Given a question and a retrieved document chunk,
determine if the chunk contains information relevant to answering the question.

Question: {query}
Document: {chunk}

Return JSON: {"relevant": true/false, "reason": "brief explanation"}
```

Important: the grader must be fast and cheap (use a smaller model). Grading every chunk with an expensive model defeats the purpose — you're adding latency to save latency.

### Query Rewriting for Re-Retrieval

When grading reveals that retrieved chunks are insufficient, the system rewrites the query before retrying. The rewriter has access to: the original query, the failed retrieval results (so it knows what didn't work), and optionally the grading reasons (so it understands *why* the retrieval failed).

Rewriting patterns that work:
- **Decomposition.** "Explain the difference between RAG and fine-tuning for customer support" → two separate queries: "RAG for customer support use cases" and "fine-tuning for customer support use cases."
- **Specificity increase.** "How does it work?" → "How does the BM25 ranking algorithm score documents?"
- **Terminology shift.** If the initial query used informal language, rewrite with technical terminology likely to match document vocabulary.
- **Scope narrowing.** If retrieval returned too many loosely relevant documents, rewrite to target a specific subtopic.

### Guardrails — Out-of-Domain Detection

Before retrieval even starts, an agentic system can detect when a query is outside the domain of its knowledge base and respond appropriately rather than attempting retrieval on a hopeless query.

The guardrail is a lightweight classifier (a small model or embedding similarity check against domain-representative examples): "Is this query about the domain this system covers?" If not, skip retrieval entirely and return a polite rejection: "This system covers X. Your question appears to be about Y, which is outside what I can help with."

This prevents the system from hallucinating answers to questions it has no data for — a common failure mode when RAG pipelines are deployed on out-of-domain queries.

### Reasoning Step Tracking

In a LangGraph-style implementation, each node in the decision graph logs its reasoning: what it retrieved, what it graded, why it rewrote the query, what it decided. This trace is essential for debugging — without it, when the system gives a wrong answer you can't tell whether retrieval failed, grading was too aggressive, rewriting made things worse, or generation drifted from the retrieved content.

Expose this trace in your monitoring system (see Production Observability below). In development, log it verbosely. In production, store it for debugging but don't expose it to users.

---

## Production Operations

Getting a RAG pipeline to work in a demo is one problem. Keeping it working reliably in production is another. These are the operational patterns that matter at scale.

### Ingestion Pipeline Architecture

Documents don't ingest themselves. A production ingestion pipeline is automated, idempotent, and observable.

**Orchestration with Airflow.** For systems that continuously ingest new documents (research papers, support tickets, news articles), Apache Airflow or a similar DAG orchestrator handles scheduled ingestion. A DAG runs on a defined schedule (daily, hourly), fetches new documents from the source, parses them, chunks them, generates embeddings, and indexes them. Idempotency is critical: running the same DAG twice should not create duplicate documents in the index.

**Document parsing for complex formats.** PDFs, especially scientific papers, are not plain text. Libraries like Docling handle scientific PDF parsing — extracting structured content from multi-column layouts, tables, figures, and equations. Raw PDF text extraction (PyPDF2, pdfplumber) fails on complex layouts. Use a dedicated scientific parser for academic or technical documents.

**Rate limiting and retry logic.** External APIs (arXiv, PubMed, news feeds) enforce rate limits. Build exponential backoff with jitter into your fetcher: on a 429 response, wait 2^n seconds plus random jitter before retrying. Cap total retries at 5. Log every rate limit event — sustained rate limiting means you need to slow your ingestion schedule or request higher limits.

**Metadata alongside content.** Every chunk should be stored with: source document identifier, section title, ingestion timestamp, document version or hash, and any domain-specific metadata (author, date, category). This metadata powers filtering ("only retrieve from documents updated in the last 6 months"), citation, and debugging.

### Observability with Langfuse

Langfuse is the standard open-source observability tool for LLM pipelines. It traces every request end-to-end — retrieval call, document grading calls, rewrite call, generation call — and gives you:

- **Token usage per call and per pipeline run.** Immediately reveals if your prompt is inflating with unnecessary content.
- **Latency breakdown.** Which step is slow? Retrieval? Grading? Generation? Streaming?
- **Cost tracking.** Every API call has a cost; aggregate cost per query type to understand your unit economics.
- **Trace inspection.** For any specific failed query, replay the full trace: what was retrieved, what was graded out, what was sent to the model, what the model produced.

Instrument your pipeline by wrapping each logical step in a Langfuse span. The trace structure should mirror your decision graph: `retrieval → grading → (optional: rewrite → re-retrieval → grading) → generation`.

### Caching with Redis

Identical or near-identical queries are common in production RAG systems. Caching retrieved results for repeated queries eliminates redundant retrieval and LLM calls.

**What to cache:** The full pipeline result (query → final answer) for exact query matches. Optionally, cache retrieved chunks for query embeddings within a cosine similarity threshold (near-duplicate queries get the same cached retrieval).

**Cache invalidation:** When source documents are updated or re-ingested, the cache for queries that used those documents must be invalidated. Store document IDs alongside cached results; invalidate cache entries when a document ID is re-ingested.

**TTL strategy:** Set cache TTL based on how frequently your source documents change. For a static knowledge base, long TTLs (days) are fine. For frequently updated sources, short TTLs (hours) or event-driven invalidation.

### Streaming Responses

For user-facing RAG systems, streaming the generation output dramatically improves perceived latency. Instead of waiting for the entire answer to generate before displaying anything, the UI starts rendering the response as tokens arrive.

The standard pattern is Server-Sent Events (SSE) for HTTP streaming:
- Backend: stream tokens from the LLM as they arrive, forward each token as an SSE event
- Frontend: `EventSource` API receives tokens, appends them to the displayed response in real-time

Design your API with two endpoints: `/ask` for standard synchronous responses (useful for integrations, batch processing) and `/stream` for SSE streaming (useful for user-facing chat interfaces). The underlying pipeline is the same — only the response delivery mechanism differs.

One important constraint: if your agentic pipeline includes multiple retrieval and grading passes before generation, all of that processing happens before streaming begins. Streaming only applies to the final generation step. The user sees a spinner during the retrieval/grading phase and streaming text once generation starts. Design your UI to communicate this clearly — a "Searching..." indicator during retrieval, then streaming text once generation begins.

---

*Draw from: `prompt-engineering/prompt-engineering.md` (system prompting, grounding, CoT) · `prompt-engineering/prompt-patterns.md` (Fact Check List, Reflection, Context Manager) · `context-engineering/context-engineering.md` (context selection and compression strategies)*
