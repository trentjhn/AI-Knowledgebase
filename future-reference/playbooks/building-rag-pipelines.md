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
- **Instruct the model to use only the retrieved content.** Add to your system prompt: "Answer based only on the provided documents. If the documents don't contain the answer, say so — do not use outside knowledge." This reduces hallucination but is **not a reliable guardrail on its own** — frontier models frequently override such instructions when they have relevant training knowledge. Treat this as one layer, not the only layer. Pair with output validation: check that claims in the response are grounded in the retrieved documents (Chain-of-Verification below, or automated NLI-based grounding checks).
- **Cap the number of chunks — but tune to your model.** More retrieved chunks is not always better, and the right ceiling is model-dependent. Smaller models (< 13B parameters) tend to lose coherence past 5–8 chunks. Frontier models (GPT-4o, Claude 3.5+, Gemini 1.5+) can effectively use 15–20+ high-quality chunks. The universal principle: a smaller number of highly relevant chunks outperforms a larger number of loosely relevant ones. Start conservative, then increase K while monitoring answer quality.

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

**Advanced indexing strategies.** Beyond standard semantic chunking, two indexing variations improve retrieval quality for specific document types. *Question-based indexing* generates a set of representative questions that each chunk would answer, then indexes those question embeddings rather than the chunk's raw text. Since retrieval query embeddings are structurally closer to question embeddings than to document passage embeddings, this closes the semantic gap between how users ask and how documents are written — at the cost of an LLM call per chunk during ingestion. *Chunk-summary indexing* generates a concise summary of each chunk and indexes the summary embedding rather than the raw text. Summaries strip domain jargon and structural noise that harm embedding quality, resulting in more semantically accurate similarity scores. Both approaches trade ingestion-time LLM cost for retrieval-time accuracy improvement.

**Retrieval component fine-tuning.** When off-the-shelf embedding models perform poorly on your domain vocabulary, you have three fine-tuning options at different cost levels. *Encoder fine-tuning* retrains the embedding model itself on domain-specific (query, relevant-chunk) pairs, improving how the embedding model represents domain concepts. *Ranker fine-tuning* trains a cross-encoder reranking model on domain (query, passage, relevance-score) triples, improving the reranking step without touching the retrieval embeddings. *RA-DIT* (Retrieval-Augmented Dual Instruction Tuning) goes further by jointly fine-tuning both the LLM generator and the retriever using (query, context, answer) triplets from your domain — the generator learns to use retrieved context better, and the retriever learns to surface context the generator can actually use. RA-DIT produces the largest quality gains but requires labeled (query, context, answer) training data and the infrastructure to train both components.

---

## Hybrid Search — BM25 + Semantic with RRF

Most production RAG systems use hybrid retrieval — not semantic-only. Understanding why, and how to implement it, is the difference between a system that works in demos and one that works on real user queries.

> **2025 meta note:** Two-channel hybrid (BM25 + semantic) is now the baseline for production RAG systems, not the ceiling. The current competitive architecture is a **4-channel parallel approach** that adds knowledge graph traversal and temporal reasoning as first-class retrieval systems — see the dedicated section below after this one. Start here to understand the foundation; move to the 4-channel section to understand where the field has moved.

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

## The 4-Channel Parallel Retrieval Architecture (2025 Meta)

The two-channel hybrid (BM25 + semantic) introduced above is the correct starting point — but it's now the floor, not the ceiling. The field has converged on a **four-channel parallel retrieval architecture** that adds knowledge graph traversal and temporal reasoning as first-class retrieval systems, fused via RRF into a single ranked list. This section explains each new channel in depth: what problem it solves, why the other channels can't compensate for its absence, and how to implement it.

### Why Two Channels Are No Longer Enough

BM25 handles exact and near-exact keyword matches. Semantic search handles paraphrase and conceptual similarity. Together, they cover most queries well. But there are two distinct classes of queries they both fail on — and these failures are systematic, not edge cases.

**Class 1: Relational queries.** "What security policies apply to systems owned by the payments team?" or "Which vendors have supplied both pumps and valves to our facilities?" or "What regulations affect all the jurisdictions where our highest-revenue customers are located?" These queries require following *relationships between entities*, not matching text. A user didn't ask "security policies" — they asked about policies that apply through a chain of ownership relationships. No embedding distance captures that traversal. BM25 will find documents containing "payments team" and "security policies" but won't assemble the correct answer because the relationship is implicit across multiple documents, not explicit in any single chunk.

**Class 2: Temporal queries.** "What is the current cancellation policy?" or "What changed in the compliance requirements since last year?" or "Show me the most recent specification for this component." These queries have recency semantics that are invisible to embeddings. The word "current" has no embedding signal that selects the 2025 version of a document over the 2022 version — both contain the same entities, similar language, and similar structure. Temporal reasoning requires treating time as a first-class retrieval dimension, not an afterthought filter.

Knowledge graph traversal solves Class 1. Temporal reasoning solves Class 2. Adding them to BM25 + semantic produces a system that handles the full space of query types, not just the majority of them.

---

### Channel 3: Knowledge Graph Traversal

#### What a Knowledge Graph Is

A knowledge graph is a structured representation of entities and the relationships between them. Unlike a vector database (which stores chunks of text as points in embedding space) or an inverted index (which stores term-document associations), a knowledge graph stores **named entities** (people, products, systems, locations, regulations, organizations) and **typed relationships** between them (owns, applies-to, built-by, located-in, governs, supersedes).

```
Concrete example:
PaymentsTeam --[owns]--> PaymentsService
PaymentsService --[runs-on]--> AWSInfrastructure
SecurityPolicy_SOC2 --[applies-to]--> AWSInfrastructure
DataRetentionPolicy_2024 --[supersedes]--> DataRetentionPolicy_2021
```

A query like "what policies apply to systems the payments team owns?" becomes a graph traversal: start at `PaymentsTeam`, follow `owns` edges to get services, follow `runs-on` edges to get infrastructure, follow `applies-to` edges inbound to get policies. The answer emerges from traversal — no semantic matching required.

#### How Knowledge Graphs Enable Multi-Hop Retrieval

**Multi-hop retrieval** is the ability to answer questions that require following a chain of relationships across multiple documents or entities. It's where BM25 and semantic retrieval fundamentally break down: they retrieve documents, but they don't *connect* information across documents.

Single-hop example (both BM25 and semantic can handle this): "What is the warranty policy for the Model X pump?" — the answer likely exists in a single document.

Multi-hop example (requires graph traversal): "What warranty terms apply to the components supplied by vendors who have had compliance failures in the last 12 months?" This requires: (1) find vendors with compliance failures in the time window → (2) find components they supplied → (3) find the warranty policies for those components → (4) synthesize. No single document contains this answer. A knowledge graph with the right entity relationships makes this traversable. Without it, you'd need a human analyst to manually cross-reference multiple data sources.

#### Microsoft GraphRAG — The Production Architecture

Microsoft's **GraphRAG** paper (2024) formalized the knowledge-graph-augmented RAG approach and is now the most referenced architecture for production knowledge graph retrieval. The approach has two phases:

**Phase 1: Graph Construction (done at ingestion time)**

1. **Entity extraction:** Run LLM calls over all source documents to extract named entities and relationships. The prompt asks the model to identify entities (with type and description) and relationships (with type, directionality, and confidence) from each chunk.

2. **Community detection:** Run graph clustering algorithms (Leiden algorithm is standard) to group related entities into hierarchical "communities" — clusters of closely connected entities. A community might be "all entities related to the Q4 regulatory filing" or "all entities in the payments infrastructure."

3. **Community summarization:** Generate a natural-language summary of each community — what it's about, which entities it contains, what their relationships are. These summaries become retrieval targets.

4. **Store the graph:** Entity nodes and typed relationship edges go into a graph database (Neo4j, Amazon Neptune, or a lighter option like NetworkX for small graphs). Community summaries go into the vector database alongside regular document chunks.

**Phase 2: Query-Time Retrieval**

When a query arrives, the system runs two parallel retrieval paths:

- **Local search:** Traditional retrieval for specific entity-centric questions. Find the most relevant entities in the query, retrieve their immediate neighbors from the graph, pull the associated document chunks. Good for: "Tell me about entity X."

- **Global search:** Community-summary retrieval for broad, cross-cutting questions. Map the query to relevant communities (using embedding similarity on the community summaries), retrieve the community summaries, let the LLM synthesize across them. Good for: "What are the major themes in our regulatory exposure?" — a question that requires synthesis across many entities and documents.

The key architectural insight from GraphRAG: **community summarizations are retrieved in the global search path, not raw document chunks.** The summaries are purpose-built for the LLM to synthesize from — they're already at the right granularity. This is why GraphRAG significantly outperforms standard RAG on questions that require broad understanding of a corpus, not just retrieval of specific facts.

#### Building Your Own Knowledge Graph for RAG

If you're not using GraphRAG, you can construct a simpler knowledge graph inline with your document ingestion pipeline:

**Entity extraction prompt pattern:**
```
Given the following document chunk, extract all named entities and their relationships.

For each entity: identify its name, type (person/organization/system/policy/location/date),
and a one-sentence description.

For each relationship: identify the source entity, target entity, relationship type
(owns/governs/applies-to/built-by/supersedes/located-in/etc.), and directionality.

Return as JSON.

Document: {chunk}
```

**Storage:** For small to medium knowledge bases (< 1M entities), NetworkX (Python graph library) is sufficient. For larger production systems, Neo4j's vector and graph integration (called Vector + Graph Hybrid Search) provides both graph traversal and vector similarity in a single database. For cloud-native, Amazon Neptune + Neptune Analytics supports both graph queries and semantic retrieval.

**Retrieval at query time:**

```python
def knowledge_graph_retrieve(query, graph, top_k=10):
    # 1. Extract query entities
    query_entities = extract_entities_from_query(query)  # LLM call

    # 2. Find matching entities in graph
    matched_nodes = [graph.find_node(entity) for entity in query_entities]

    # 3. Traverse n-hop neighborhood
    neighborhood = []
    for node in matched_nodes:
        neighborhood.extend(graph.get_neighbors(node, max_hops=2))

    # 4. Retrieve document chunks associated with neighborhood nodes
    associated_chunks = [node.source_chunk for node in neighborhood]

    # 5. Score by graph centrality (more connected nodes are more relevant)
    scored_chunks = score_by_centrality(associated_chunks, graph)

    return scored_chunks[:top_k]
```

#### When Knowledge Graph Traversal Is Worth the Investment

Knowledge graph construction requires significant upfront work: entity extraction LLM calls over your entire corpus (expensive at ingestion), graph DB infrastructure, and query-time entity resolution. It pays off when:

- Your questions frequently span multiple documents or entities ("what does X impact?")
- You have well-defined entity types in your domain (organizations, systems, policies, regulations — as opposed to free-form narrative content)
- Users ask relational questions, not just factual lookups
- Your corpus has explicit relationships worth encoding (ownership, governance, version history)

It's overkill when your queries are primarily factual lookups in self-contained documents (most customer support RAG systems don't need it), or when your corpus is mostly narrative text without clear entity structure.

---

### Channel 4: Temporal Reasoning

#### The Problem: Embeddings Are Semantically Blind to Recency

This is the most underappreciated failure mode in production RAG systems. When a user asks "what is the current refund policy?", the word "current" carries semantic weight — but **embedding models don't encode temporal recency as a retrievable dimension.** A document from 2019 describing the refund policy has almost identical embedding similarity to a 2024 document describing the updated refund policy, because both are about the same topic using similar terminology.

The result: RAG systems routinely surface outdated information with high confidence. Worse, when the same topic is covered in documents from multiple time periods, the system may retrieve a mix of old and new, and the generation model synthesizes them into an answer that's neither fully accurate to any version.

This failure mode is invisible in development (when your test corpus is usually small and freshly ingested) but consistently surfaces in production (where document sets accumulate over months and years, and users often specifically want the most recent answer).

#### Temporal Reasoning as a Retrieval Channel

Treating temporal reasoning as its own retrieval channel means going beyond "filter by date" to actually understanding *what makes a document temporally relevant to this query*. There are three distinct mechanisms, applied in combination:

**Mechanism 1: Temporal Query Parsing**

Before retrieval, parse the query for temporal references — explicit ("what changed in Q3 2024?") and implicit ("current policy," "latest version," "after the update"). Use an LLM or lightweight NER to:
- Identify temporal expressions ("this year," "since the merger," "after 2022")
- Convert relative expressions to absolute date ranges (as of query time)
- Classify the temporal intent: point-in-time ("what was the policy on 2023-06-01?"), recency ("current/latest"), change-detection ("what changed since X?")

```python
def parse_temporal_intent(query):
    # Returns structured temporal intent
    return {
        "has_temporal_signal": True,
        "intent": "recency",          # recency | point-in-time | change-detection
        "start_date": "2024-01-01",
        "end_date": None,              # None = no upper bound (present)
        "signal_phrase": "current"    # the phrase that triggered this
    }
```

**Mechanism 2: Date-Weighted Scoring**

For recency queries, apply a temporal decay function that scores documents higher when they're more recent. The decay function should be:
- Continuous (not a binary cutoff)
- Domain-tuned (policies and regulations decay slowly, news decays fast)
- Combined multiplicatively with semantic/BM25 score, not additively (a highly irrelevant but recent document shouldn't beat a very relevant older one)

```python
import math
from datetime import datetime

def temporal_decay_score(doc_date, query_date, half_life_days=365):
    """
    Exponential decay: documents lose half their temporal score every half_life_days.
    half_life_days=365 for policy/compliance docs (slow decay)
    half_life_days=30 for news/events (fast decay)
    half_life_days=90 for technical documentation
    """
    days_elapsed = (query_date - doc_date).days
    if days_elapsed < 0:
        return 1.0  # future-dated doc (ingestion edge case) gets full score
    decay = math.exp(-0.693 * days_elapsed / half_life_days)  # 0.693 = ln(2)
    return decay

def combine_scores(semantic_score, temporal_score, temporal_weight=0.3):
    """
    Multiplicative combination: temporal score modulates, not replaces, relevance.
    A temporal_weight of 0.0 = pure relevance. 1.0 = pure recency.
    0.3 is a reasonable default for most knowledge base RAG.
    """
    return semantic_score * (1 + temporal_weight * (temporal_score - 1))
```

**Mechanism 3: Version-Aware Retrieval**

For domains where documents have explicit version relationships (technical specs, regulatory filings, policy versions), extend the knowledge graph to encode supersession relationships, and use those to filter retrieval results:

```
Policy_v3 --[supersedes]--> Policy_v2 --[supersedes]--> Policy_v1
```

At query time: if a document is superseded by a more recent version that's also in the corpus, down-rank or exclude the older version. This requires the knowledge graph to encode `supersedes` edges — which is why temporal reasoning and knowledge graph traversal are complementary: the graph encodes *which* documents are outdated, temporal scoring determines *how much* to penalize them.

#### Temporal Retrieval as a Parallel Channel

Rather than post-processing semantic results with temporal filters, implement temporal reasoning as a parallel retrieval channel that runs concurrently with BM25, semantic, and knowledge graph retrieval:

```python
def temporal_channel_retrieve(query, temporal_intent, doc_store, top_k=20):
    if not temporal_intent["has_temporal_signal"]:
        return []  # no temporal signal → this channel contributes nothing

    if temporal_intent["intent"] == "recency":
        # Sort all documents with relevant entities by date descending
        # Score by (relevance * temporal_decay)
        candidates = doc_store.query_by_entity(query, limit=100)
        scored = [(doc, semantic_score(query, doc) * temporal_decay_score(
            doc.date, datetime.now(), half_life_days=doc.domain_half_life
        )) for doc in candidates]
        return sorted(scored, key=lambda x: x[1], reverse=True)[:top_k]

    elif temporal_intent["intent"] == "point-in-time":
        # Filter to docs that were current on the specified date
        target_date = temporal_intent["start_date"]
        return doc_store.query_valid_at_date(query, date=target_date, limit=top_k)

    elif temporal_intent["intent"] == "change-detection":
        # Retrieve documents from before and after the specified date
        # Surface differences as the retrieval result
        before = doc_store.query_before_date(query, date=temporal_intent["start_date"])
        after = doc_store.query_after_date(query, date=temporal_intent["start_date"])
        return before + after  # let the model identify changes
```

#### When to Add Temporal Reasoning

Add it when:
- Your corpus contains documents from multiple time periods on the same topics
- Users frequently ask about "current," "latest," or "updated" state
- Regulatory, policy, or specification documents are a primary use case
- Document versions accumulate over time (not a static one-time corpus)

You can skip explicit temporal reasoning (and rely on simple date-filter pre-processing) when:
- Your corpus is ingested once and rarely updated
- All documents are approximately the same age
- Users don't ask recency-dependent questions

---

### Full 4-Channel Architecture

With all four channels, the retrieval layer looks like this:

```
User query
    ↓
[Pre-retrieval processing — parallel]
    ├── Temporal parsing → extract temporal intent + date range
    └── Entity extraction → identify named entities for graph traversal
    ↓
[4-channel parallel retrieval]
    ├── BM25 search               → top-N by keyword rank
    ├── Semantic search           → top-N by embedding similarity
    ├── Knowledge graph traversal → relevant entity neighborhood + document chunks
    └── Temporal channel          → date-weighted or version-filtered results
    ↓
[RRF fusion across all 4 channels]
    → each document gets: Σ 1 / (k + rank_in_channel_i) for each channel it appeared in
    → channels that don't fire (no graph entities found, no temporal signal) contribute 0
    ↓
[Cross-encoder reranking on merged top-N]
    → select top 5-10 for the model
    ↓
[Generation with grounding instructions]
```

**Key implementation note:** Channels that don't apply to a given query contribute nothing — they don't penalize results by injecting noise. If a query has no temporal signal, the temporal channel returns an empty list and contributes 0 to RRF scores. If a query has no recognizable entities for graph traversal, the knowledge graph channel returns nothing. RRF handles this gracefully: a document that only appears in BM25 and semantic results still gets a combined score from those two systems.

#### RRF With 4 Systems: The Math

The RRF formula extends naturally to any number of retrieval systems:

```
RRF_score(doc) = Σ_i [ 1 / (k + rank_i(doc)) ]
```

Where the sum is over all channels in which the document appears, and `rank_i(doc)` is the document's rank in channel `i`. Documents not appearing in a channel are simply excluded from that channel's term in the sum (equivalent to infinite rank → 0 contribution).

With 4 channels, a document that ranks well in multiple channels accumulates contributions from all of them — this is exactly the desired behavior. A document about "current refund policy" that ranks 1st in temporal (very recent), 3rd in semantic (topic match), 10th in BM25 (keyword match), and doesn't appear in knowledge graph (no entity traversal) gets:
```
RRF_score = 1/(60+1) + 1/(60+3) + 1/(60+10) + 0
          = 0.0164 + 0.0157 + 0.0143 + 0
          = 0.0464
```

A competitor that only appears in semantic at rank 1 gets:
```
RRF_score = 1/(60+1) = 0.0164
```

The multi-channel document wins decisively, which is the correct behavior — it's reinforced across multiple retrieval signals.

#### Tuning Channel Weights

Standard RRF weights all channels equally. If you have reason to trust some channels more than others for your domain, you can weight them:

```
Weighted_RRF_score(doc) = Σ_i [ w_i / (k + rank_i(doc)) ]
```

Where `w_i` is the weight for channel `i`. Reasonable starting weights:

| Query type | BM25 | Semantic | Knowledge Graph | Temporal |
|---|---|---|---|---|
| General knowledge base | 1.0 | 1.0 | 0.5 | 0.5 |
| Technical/legal documents | 1.0 | 0.8 | 0.8 | 1.0 |
| Relational/organizational | 0.5 | 1.0 | 1.5 | 0.3 |
| News/events | 0.8 | 1.0 | 0.3 | 1.5 |

Tune these empirically on your actual query distribution. Don't weight the knowledge graph highly if your graph construction is sparse — a sparse graph produces noisy retrieval that hurts more than it helps.

#### Sequencing Your Build

You don't need all four channels before you launch. The right build order:

1. **Semantic only** — prove the core use case works before adding complexity
2. **+ BM25 + RRF** — this should be the state before you call anything "production"
3. **+ Reranking** — often produces the largest quality jump after the initial hybrid
4. **+ Temporal reasoning** — add when users are asking about current/latest state
5. **+ Knowledge graph** — add when users are asking relational/multi-hop questions

Don't skip to 4 or 5 before nailing 1-3. Knowledge graph construction is expensive and produces no value if your basic retrieval pipeline isn't tuned.

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

## LangGraph — Implementing the Decision Graph

LangGraph is a library for building agentic workflows as directed graphs with explicit state. It's the standard tool for implementing the agentic RAG decision loop because it makes the control flow visible, debuggable, and modifiable — instead of a tangle of conditionals buried in a single function.

### The Core Concept: State + Nodes + Edges

A LangGraph workflow has three building blocks:

**State** is a typed dictionary that flows through every node in the graph. Every node reads from state and writes back to it. For an agentic RAG system, state carries: the original query, retrieved documents, grading results, rewrite count, and final answer.

```python
class RAGState(TypedDict):
    query: str
    rewritten_query: str | None
    retrieved_docs: list[Document]
    graded_docs: list[Document]
    rewrite_count: int
    answer: str | None
```

**Nodes** are functions that take state, do one thing, and return updated state. Each step in your decision graph is a node: retriever, grader, rewriter, generator, guardrail.

**Edges** define the flow between nodes. Normal edges always go from A to B. Conditional edges route based on state — this is where the "should I rewrite or generate?" decision lives.

### Building the Agentic RAG Graph

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(RAGState)

# Add nodes — one function per decision step
workflow.add_node("guardrail",  check_domain)        # is this query in-domain?
workflow.add_node("retrieve",   retrieve_documents)   # hybrid BM25 + semantic
workflow.add_node("grade",      grade_documents)      # are chunks relevant?
workflow.add_node("rewrite",    rewrite_query)        # refine if grading fails
workflow.add_node("generate",   generate_answer)      # LLM call

# Entry point
workflow.set_entry_point("guardrail")

# Fixed edges
workflow.add_edge("retrieve", "grade")
workflow.add_edge("rewrite",  "retrieve")  # after rewriting, retrieve again
workflow.add_edge("generate", END)

# Conditional edges — where the intelligence lives
workflow.add_conditional_edges(
    "guardrail",
    route_after_guardrail,          # function returns "retrieve" or "reject"
    {"retrieve": "retrieve", "reject": END}
)

workflow.add_conditional_edges(
    "grade",
    route_after_grading,            # function returns "generate" or "rewrite"
    {"generate": "generate", "rewrite": "rewrite"}
)

app = workflow.compile()
```

The routing functions are the decision logic — they inspect state and return the name of the next node:

```python
def route_after_grading(state: RAGState) -> str:
    sufficient_docs = [d for d in state["graded_docs"] if d.relevant]
    if len(sufficient_docs) >= 2:
        return "generate"
    if state["rewrite_count"] >= 2:
        return "generate"   # give up rewriting, generate with what we have
    return "rewrite"
```

### Why Graph Structure Over If/Else

The graph isn't just aesthetic. It gives you:

- **Visualization.** LangGraph can render the workflow as a diagram. You can see exactly what path a query took through the system — invaluable for debugging unexpected behavior.
- **State transparency.** Because all intermediate state is explicit and typed, you can inspect it at any point. After a failed query, you can see exactly what was retrieved, what was graded out, how many rewrites happened.
- **Modular testing.** Each node is a plain function — test it in isolation without running the full pipeline.
- **Easy iteration.** Adding a new step (a reranker, a second grader, a different generator) is adding a node and rewiring an edge, not refactoring a monolithic function.

### Max Iteration Guard

Always cap the rewrite loop. Without a maximum, a query that consistently fails retrieval will loop indefinitely. A rewrite count of 2–3 is the standard ceiling — after that, generate with whatever was retrieved and express appropriate uncertainty.

---

## Evaluating Agentic RAG

Evaluating a basic RAG pipeline is already covered in `evaluation/evaluation.md`. Agentic RAG introduces new failure modes that require additional evaluation dimensions — because you're now not just asking "was the answer correct?" but "did the agent make the right decisions along the way?"

### The Four Layers of Agentic RAG Evaluation

**Layer 1 — Retrieval quality** (same as basic RAG)
Did the retrieval step surface relevant documents? Measure recall@K: of the K documents retrieved, how many were actually relevant to the query? This is your baseline — if retrieval is broken everything else is irrelevant.

**Layer 2 — Grader accuracy**
Is the document grader making correct relevance calls? Evaluate this independently with a labeled dataset of (query, document, relevant: true/false) triples. Measure:
- Precision: of documents it marked relevant, how many actually were?
- Recall: of actually relevant documents, how many did it catch?

A grader with low recall (misses relevant documents) will over-trigger rewrites, adding latency for no reason. A grader with low precision (marks irrelevant documents as relevant) lets noise into the generation step, degrading answer quality. Both failure modes are invisible if you only measure final answer quality.

**Layer 3 — Rewrite effectiveness**
When the system rewrites a query and retries, does the rewrite actually improve retrieval? Measure whether rewritten queries retrieve better documents than the original query did. If rewrites don't reliably improve retrieval, the rewrite node is adding latency without benefit.

Track: for queries that triggered a rewrite, what was the grading score before and after? If rewritten queries pass grading at similar rates to original queries, your rewriter isn't working.

**Layer 4 — Guardrail precision and recall**
Is the guardrail correctly classifying in-domain vs. out-of-domain queries? False positives (rejecting valid domain questions) frustrate users. False negatives (allowing out-of-domain queries through) lead to hallucinations.

Build a labeled test set with:
- Clearly in-domain queries that should pass
- Clearly out-of-domain queries that should be rejected
- Edge cases — in-domain but out-of-scope (the hardest category)

Measure precision and recall on each category separately. Track the edge case category closely — that's where user frustration lives.

### Tracing Every Decision

The evaluation pipeline for agentic RAG requires per-query traces, not just aggregate metrics. You need to know, for each query: which path through the graph it took, what was retrieved, what was graded, whether it rewrote and how many times, and what the final answer was.

Langfuse handles this automatically when instrumented correctly — each node emits a span with its inputs and outputs. Your evaluation pipeline queries Langfuse for traces, samples them, and runs your evaluation metrics against the trace data.

Without traces, all you can measure is final answer quality. With traces, you can pinpoint exactly where in the decision graph failures originate.

### The Compound Failure Problem

Agentic RAG has a compounding failure mode that basic RAG doesn't: each decision node can fail in a way that makes downstream failures more likely. A grader that's too aggressive (grades most documents as irrelevant) forces excessive rewrites, which may produce worse queries, which retrieves worse documents, which grades even worse.

This means aggregate metrics can look deceptively stable while individual components are degrading. Track each layer's metrics independently and watch for correlated degradation — if rewrite rate is climbing while final answer quality holds steady, your grader has quietly become more aggressive and you haven't noticed yet because users haven't complained.

---

## ASMR — Agentic Search and Memory Retrieval

> **Research context:** Supermemory (2025). Achieved ~99% on LongMemEval using agentic reasoning to replace vector search entirely. The headline accuracy requires careful interpretation — see the scoring note below before drawing conclusions.

ASMR is a fundamentally different approach to RAG for memory-intensive applications. It does not improve retrieval. It abandons retrieval. Instead of embedding documents and finding nearest neighbors in a vector space, ASMR deploys parallel agents that actively read through stored knowledge and reason about relevance. The gap this fills is precise: **semantic similarity matching cannot reliably distinguish between an old fact and its correction, or between a primary statement and an exception buried elsewhere in a document.** An agent doing active reasoning can make those distinctions. Cosine distance cannot.

### Why Vector Search Fails on Memory-Intensive Data

The failures are systematic, not edge cases. They emerge from two properties of memory-heavy applications that vector retrieval cannot handle:

**Temporal failure.** A user says in session 1: "I'm vegetarian." In session 47: "I've started eating fish again." Both statements embed into similar vector regions — they're both about dietary preferences. When queried "what does this user eat?", vector search may retrieve the older statement (higher frequency, more recency-neutral), the newer one, or both simultaneously. If both are retrieved and injected into context, the model must reason about which supersedes the other — but it has no way to know the chronological order of the sessions it's reading. The retrieval system surfaced both because they're both relevant; their temporal relationship is invisible in embedding space.

**Nuance failure.** A document states a general rule in paragraph 1 and a specific exception in paragraph 8. Vector retrieval chunks them. The general rule chunk is a strong match for the query about the rule; the exception chunk may have low similarity to the query if it's phrased differently. The model sees the rule without the exception. The semantics of the exception don't require proximity to the rule — it could live anywhere in the document, in any phrasing, and still apply.

ASMR's claim is that a dedicated reasoning agent, reading the full stored knowledge with the query in hand, can resolve both problems. The agent reads all the sessions chronologically, understands that session 47 overrides session 1, and synthesizes accordingly. The agent reads the full document, encounters the exception, and includes it in its answer.

### The Two-Phase Architecture

#### Phase 1 — Parallel Ingestion (Observer Agents)

Ingestion in ASMR is not chunking. It is **semantic extraction with category typing.**

Instead of splitting sessions into overlapping fixed-length chunks and embedding them, ASMR deploys parallel observer agents that read assigned sessions concurrently and extract **structured findings** categorized into six typed knowledge classes:

| Category | What It Captures |
|---|---|
| **Personal Information** | Identity facts that persist — name, location, relationships, occupation |
| **Preferences** | Stated or inferred preferences — diet, communication style, working hours |
| **Events** | What happened and when — past interactions, reported experiences, history |
| **Temporal Data** | Time-sensitive facts, conditions, durations — "currently on a project until March" |
| **Updates** | Corrections or changes to previously stated facts — the most critical category |
| **Assistant Information** | What the system knows about its own capabilities and prior commitments |

The **Updates** category is the architectural insight. Traditional RAG has no category for "this supersedes something said earlier." ASMR explicitly types corrections and overrides as their own class of finding, so when the retrieval phase runs, it knows to weight Updates over the Personal Information or Preferences entries they replace.

**Why parallel readers?**

For a user with 100 conversation sessions, sequential reading saturates a single agent's context window and takes proportionally long. ASMR distributes across multiple observer agents with interleaved session assignment:

```
Observer Agent 1: sessions 1, 4, 7, 10, 13 ...
Observer Agent 2: sessions 2, 5, 8, 11, 14 ...
Observer Agent 3: sessions 3, 6, 9, 12, 15 ...
```

Interleaving (rather than consecutive blocks) distributes temporal coverage across all agents, so no single agent is reading only early sessions or only recent ones. Each observer produces structured findings — typed, timestamped, and mapped back to their source session ID for verification later.

The ingestion output is not a vector database. It is a structured finding store — a collection of typed knowledge entries associated with session metadata. In the Supermemory implementation, this lives in-memory or in simple key-value storage.

#### Phase 2 — Active Retrieval (Search Agents)

When a query arrives, the system does not query a vector database. It deploys **3 parallel search agents**, each with a specialized focus, to read the structured finding store and reason about what's relevant:

- **Search Agent 1 — Direct facts:** Searches for explicit statements and direct answers
- **Search Agent 2 — Context and implications:** Searches for related context, social cues, and inferred meaning
- **Search Agent 3 — Temporal timeline:** Reconstructs chronological sequences and resolves temporal relationships

Each agent reads independently, evaluates the findings in its domain, and returns its most relevant results with reasoning. The orchestrator then compiles all three sets of findings and cross-references them against the original source session excerpts — a verification step that confirms each finding is actually present in the stored knowledge, not hallucinated by the search agent.

This produces both **breadth** (three different search angles, each finding something the others might miss) and **depth** (verbatim source verification as a grounding check).

```
Query arrives
    ↓
[3 parallel search agents — concurrent]
    ├── Agent 1: direct facts + explicit statements
    ├── Agent 2: context, implications, social cues
    └── Agent 3: temporal reconstruction + relationship mapping
    ↓
[Orchestrator compiles findings]
    → cross-references findings against source session excerpts
    → resolves conflicts between agents (Updates supersede older Preferences/Personal Info)
    ↓
[Verified context package]
    → passed to answering ensemble
```

### The Answering Ensemble

After retrieval, the verified context is routed through a set of specialized answering agents rather than a single generation prompt. Two variants were tested:

#### 8-Variant Ensemble (pass@8 accuracy: 98.60%)

Context is routed in parallel to 8 specialized prompt variants simultaneously. Each variant is tuned for a different answer type:
- A precise counter (for "how many times did X happen?")
- A time specialist (for temporal questions)
- A context deep-dive expert (for questions about nuanced state)
- General knowledge synthesizers with varying instruction emphasis
- Others tuned to specific question categories in LongMemEval

Each variant independently evaluates the context and generates an answer. The system is scored as **pass@8**: the question is marked correct if **any** of the 8 variants produces the correct answer.

**CRITICAL accuracy note:** Pass@8 is not the production metric. It measures whether the right answer exists somewhere in the system's output — not whether the system reliably surfaces it as its answer. If 7 variants give the wrong answer and 1 gives the right answer, the question scores as correct. For a system that will provide a single response to a user, this overstates practical accuracy. The 98.60% figure is the upper bound on what's achievable; it does not represent what a user experiences.

#### 12-Variant Decision Forest (single-output accuracy: 97.20%)

The production-realistic variant: 12 specialized answering agents run independently, then an aggregator LLM synthesizes a single authoritative answer from all 12 responses using:
- **Majority voting** — what did most agents conclude?
- **Domain trust weighting** — for time questions, weight the time specialist's answer more heavily
- **Conflict resolution** — when agents disagree, the aggregator reasons about which answer is better supported by the context

The 97.20% accuracy figure uses pass@1 scoring — one answer out, it's either right or wrong. This is the honest production metric. Both figures are genuinely impressive on LongMemEval, but practitioners should reference the 97.20% when evaluating whether ASMR is worth deploying.

### What LongMemEval Actually Tests

LongMemEval is a rigorous benchmark designed to simulate exactly the failure modes ASMR targets. It is not a standard QA benchmark. Its properties:

- **Conversation histories exceeding 115,000 tokens** — well beyond what fits in a single context window
- **Contradictory information across sessions** — old facts explicitly overridden by newer ones
- **Events spread across multiple time periods** — requiring temporal reconstruction to answer correctly
- **Questions requiring temporal reasoning** — "what does the user currently believe about X?", "how many times did X happen?", "what changed since session Y?"

Most memory systems score poorly on LongMemEval because **retrieval, not reasoning, is the bottleneck**: the challenge is not generating a correct answer from good context, it's getting only the right, temporally-ordered information into context in the first place. ASMR's architectural response is to replace the retrieval step entirely with a reasoning step that reads everything and selects contextually.

For reference: baseline vector RAG systems typically score in the 50–65% range on LongMemEval, and the best specialized memory systems before ASMR were in the 70–80% range. The jump to ~97–98% represents a material change in what the architecture can handle.

### Key Engineering Insights

**1. Agentic retrieval beats vector search specifically for temporal and multi-session data.**

This is a precise claim, not a general one. ASMR's advantage is specifically on data where old facts get corrected by new ones, and where the system must know which version of a fact is current. For a static document corpus where no document supersedes another, vector search is faster, cheaper, and comparably accurate.

**2. The Updates category is the structural key.**

The six-category knowledge typing exists primarily to make Updates a first-class concept. Everything else (Personal Information, Preferences, Events, Temporal Data, Assistant Information) could be typed differently without changing the fundamental approach. But without an explicit Updates category — a dedicated slot for "this corrects something previously known" — the architecture has no way to reason about supersession during retrieval. This is the single design decision that most directly explains why ASMR outperforms vector retrieval on temporal benchmarks.

**3. Parallel processing improves granularity without sacrificing speed.**

Both ingestion (parallel observer agents) and retrieval (parallel search agents) are parallelized. Without parallel ingestion, a 100-session conversation history would overflow a single agent's context window. Without parallel retrieval, three serial search passes would triple latency. The parallelism is not an optimization — it is load-bearing for the architecture to function at realistic scale.

**4. Specialization beats generalization at the answering stage.**

Routing context to specialist agents (counter, time specialist, context deep-diver) outperforms any single general-purpose prompt on LongMemEval's diverse question types. The aggregation step — whether pass@8 or a decision forest — works because specialists are genuinely better at their narrow domains than a generalist is across all of them.

### The Cost Reality

ASMR involves many LLM calls per query. At minimum:

| Phase | Calls |
|---|---|
| Ingestion (per session batch) | 3 observer agents |
| Retrieval (per query) | 3 search agents |
| Answering (per query) | 8–12 specialist agents + 1 aggregator |
| **Total per answered question** | **~14–18 LLM calls** |

The Supermemory research used smaller models — Gemini 2.0 Flash, GPT-4o-mini — to keep this affordable at research scale. Even with smaller models, the unit economics require careful analysis before production deployment.

**Rough cost framing:** At $0.15/1M input tokens (GPT-4o-mini), a 115k-token history processed by 3 observer agents is roughly $0.05 in ingestion costs per user. Per query, 3 search agents + 12 answering agents reading a compressed context package might total $0.02–0.08 depending on context size. At low volume (thousands of queries/day), this is manageable. At high volume (millions of queries/day), the economics require dedicated analysis and likely model optimization.

**Where ASMR is currently suited:**
- Medical records retrieval and longitudinal patient history queries
- Legal document analysis across large, interconnected document sets
- Enterprise knowledge management for high-value, complex queries
- Personal memory systems for premium applications where accuracy is paramount

**Where it is not yet suited:**
- Mass-market consumer applications at billions of queries per day
- Cost-sensitive applications where $0.05/query is too expensive
- Any use case where latency < 1 second is a hard requirement

### "No Vector Database Required" — What This Actually Means

Eliminating the vector database is not just infrastructure simplification — it changes the cost model and the deployment profile.

**What's eliminated:**
- Embedding model inference at ingestion (generating and storing vectors)
- Vector database infrastructure (Pinecone, Weaviate, pgvector — their hosting, maintenance, and query costs)
- Index maintenance and re-embedding when documents change

**What replaces it:**
- LLM compute at ingestion (observer agents reading and extracting findings)
- Simple key-value or in-memory storage for structured findings (trivially cheap)
- LLM compute at retrieval (search agents reading findings and reasoning)

The trade-off: **vector infrastructure cost → LLM compute cost.** For many use cases, LLM compute per query is more expensive than vector search per query, but the operational simplicity is significant — no vector DB to provision, no embedding model to maintain, no index to synchronize when knowledge changes.

The practical implication: ASMR can be embedded in systems and environments where vector database infrastructure doesn't exist. Edge devices, embedded systems, and applications running on constrained infrastructure can implement ASMR with only an LLM API endpoint and local key-value storage. This is not true of any vector-search-based RAG approach.

### When to Consider ASMR Over Traditional RAG

**ASMR is the better choice when:**
- Your data has a **temporal update pattern** — users correct past statements, preferences change, facts are overridden. This is the primary condition. Without it, ASMR's advantage over vector search is marginal.
- You have **multi-session user data** where old preferences or facts are superseded by new ones and the system must know which version is current
- You are handling **long conversation histories** (thousands of tokens of prior context) that can't fit in a single context window and where the chronological ordering of facts matters
- Query accuracy is **high-value and lower-frequency** — the compute cost per query is acceptable relative to the value of getting the right answer
- Your deployment environment has **no existing vector DB infrastructure** and adding it is a significant burden
- The load-bearing accuracy requirement is **"latest fact supersedes older fact"** — this is exactly what ASMR's Updates category and temporal search agent are built for

**Traditional RAG is still the right choice when:**
- You need **low latency** — ASMR's 14–18 LLM calls per query create meaningful latency overhead, especially at P99. Vector search retrieval is typically sub-100ms; ASMR retrieval is measured in seconds.
- Your corpus is **large, static, and non-temporal** — a documentation library, a product catalog, a legal code base where documents don't supersede each other. Vector search excels here.
- You need **cost efficiency at scale** — 15–18 LLM calls per query is expensive at millions of queries per day. Embedding + vector search at that scale is a small fraction of the LLM compute cost.
- **Retrieval errors are acceptable and roughly uniform** across query types — if your use case tolerates some errors and doesn't specifically suffer from temporal failures, vector search with hybrid retrieval handles most cases well
- Your data doesn't have meaningful **correction and override patterns** — ASMR's primary edge disappears without them

### Connection to the 4-Channel Architecture

ASMR's temporal timeline reconstruction (Search Agent 3) addresses the same underlying problem as the temporal reasoning channel described in the 4-channel architecture section above: **semantic embeddings are blind to recency.** The solutions differ in implementation:

| | 4-Channel Temporal Channel | ASMR Search Agent 3 |
|---|---|---|
| Mechanism | Date-weighted scoring applied to vector search results | Agent actively reads knowledge and reasons about temporal sequences |
| Infrastructure | Vector DB + temporal metadata + decay function | Structured finding store + LLM reasoning |
| Latency | Low (parallel with other channels, fast scoring) | Higher (LLM call, sequential reasoning) |
| Accuracy on complex temporal chains | Moderate — scoring resolves obvious recency, misses multi-step chains | Higher — can follow "A was updated by B which was itself revised by C" |
| Cost | Low per query | High per query |

The 4-channel temporal channel is the right choice when you want to improve recency handling within an existing vector RAG system incrementally. ASMR is the right choice when temporal accuracy is the primary correctness requirement and you're willing to replace the retrieval architecture entirely.

Both solve the same root problem. ASMR solves it more thoroughly. The 4-channel architecture solves it more cheaply.

---

*Draw from: `prompt-engineering/prompt-engineering.md` (system prompting, grounding, CoT) · `prompt-engineering/prompt-patterns.md` (Fact Check List, Reflection, Context Manager) · `context-engineering/context-engineering.md` (context selection and compression strategies) · `evaluation/evaluation.md` (Ragas metrics, LLM-as-judge, production monitoring)*
