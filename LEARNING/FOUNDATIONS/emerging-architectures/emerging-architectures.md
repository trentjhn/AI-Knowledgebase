# Emerging Architectures in LLMs — Frontier Monitoring Document

**Last updated: early 2026**
**Type: Frontier monitoring — not a practitioner how-to**

This document is different from the rest of the KB. The others tell you how to build things with AI today. This one tracks architectural research that challenges or extends the standard transformer + discrete tokenization paradigm — the foundation of essentially every production LLM you've used.

The goal is to give you a durable mental model for following the field as it evolves. "Here's where we are in early 2026, here's what's being explored, here's what to watch." Not "here's how to implement this."

Revisit this document in 6-12 month intervals. Things will have changed.

---

## Table of Contents

1. [The Current Dominant Paradigm (and its known limits)](#1-the-current-dominant-paradigm)
2. [State Space Models (SSMs) / Mamba](#2-state-space-models-ssms--mamba)
3. [Mixture of Experts (MoE)](#3-mixture-of-experts-moe)
4. [Byte-Level and Tokenization-Free Models](#4-byte-level-and-tokenization-free-models)
5. [Continuous / Latent Space Models](#5-continuous--latent-space-models)
6. [Linear Attention and Efficient Attention Variants](#6-linear-attention-and-efficient-attention-variants)
7. [Signal vs. Noise Framework — Evaluating Architecture Claims](#7-signal-vs-noise-framework)
8. [The Practical Implication for Builders](#8-the-practical-implication-for-builders)

---

## 1. The Current Dominant Paradigm

### What it is

The transformer architecture + discrete tokenization (BPE) is the foundation of essentially all production LLMs as of early 2026. GPT-4, Claude 3/3.5/3.7, Gemini 1.5/2.0, Llama 3, Mistral, DeepSeek — all of them. The architecture has remained surprisingly stable since the "Attention Is All You Need" paper (Vaswani et al., 2017). What has changed is scale, engineering infrastructure, training stability, and various incremental improvements layered on top.

Understanding the known bottlenecks of this architecture is the prerequisite for understanding why anything in the rest of this document is being explored at all.

### Known architectural bottlenecks

**Autoregressive generation — latency scales with output length**

Transformers generate one token per forward pass. To produce 1,000 tokens, the model runs 1,000 forward passes, each attending to all previous tokens. This is fundamental to the architecture, not a bug. It means generation latency is proportional to output length in a way that's hard to parallelize. Techniques like speculative decoding (see inference-optimization.md) help at the margins but don't change the underlying constraint.

**Quadratic attention complexity — O(n²) in sequence length**

Standard attention requires computing pairwise relationships between every token in the sequence. The computational cost scales quadratically with sequence length. A 1,000-token sequence requires O(1,000,000) operations. A 10,000-token sequence requires O(100,000,000).

FlashAttention (Dao et al., 2022) addresses the memory problem — it avoids materializing the full attention matrix by recomputing in tiles, reducing memory from O(n²) to O(n). This is why long-context models are practically feasible. But FlashAttention does not change the O(n²) compute complexity. The operations still happen — they're just memory-efficient now.

**Fixed vocabulary / tokenization**

BPE (Byte Pair Encoding) tokenization is a preprocessing decision made before training that cannot be changed afterward. This creates several friction points practitioners actually notice:

- Numbers tokenize inconsistently. "2024" might be 1 token or 4 tokens depending on training corpus frequency. Mathematical operations on tokenized numbers are inherently awkward.
- Non-English languages are penalized. BPE vocabularies are historically English-heavy. A sentence that costs 10 tokens in English might cost 20-30 tokens in Thai or Arabic — cutting effective context window in half.
- Code indentation is expensive. Each space is a token (or partial token), making heavily-indented code consume disproportionate context budget.
- Rare words and proper nouns get split into subword pieces that have no natural correspondence to the word's meaning.

**Context window limits — KV cache grows linearly**

The key-value (KV) cache stores intermediate attention computations so they don't need to be recomputed for each new token. It grows linearly with sequence length and batch size. At 128K token context, serving a single request requires gigabytes of GPU memory for the KV cache. This is currently one of the primary infrastructure bottlenecks for long-context deployment.

### Why the transformer has been hard to displace

The engineering infrastructure built around transformers is massive. Training stability is well-understood. Scaling laws (Chinchilla, etc.) tell practitioners how to allocate compute budget for predictable outcomes. The community understands how to debug transformer failures in ways that took years to develop.

New architectures need to be not just theoretically better — they need to outperform a heavily-optimized baseline that has had 7+ years of engineering investment. This is a recurring historical pattern in ML: better ideas lose to better-implemented ideas with more compute.

---

## 2. State Space Models (SSMs) / Mamba

### The core problem SSMs solve

Transformers attend to all previous tokens at every generation step. For a sequence of length n, each token attends to all n previous tokens — this is the O(n²) problem from Section 1.

State space models take a different approach: instead of attending to the full history, they maintain a fixed-size "hidden state" vector that compresses the entire sequence history. Processing a new token means updating this hidden state rather than attending to the full sequence. Computational cost is O(n) — linear in sequence length.

The tradeoff is explicit: you get linear scaling, but you give up the ability to precisely retrieve any arbitrary token from the past. Everything must be compressed into the hidden state, and information that doesn't survive the compression is gone.

### Mamba (Gu & Dao, 2023)

The key innovation in Mamba is **input-dependent state transitions**. Earlier SSMs (S4, H3, etc.) used fixed state transition matrices — the same compression function regardless of what the current input is. Mamba's state transitions change based on the current input. The model learns to selectively retain or discard information based on what it's currently processing.

Concretely: when reading "The Eiffel Tower is in Paris... [500 tokens later] ... where is the tower?", the model can learn to keep "Paris" in the state through the intervening text because the question-relevant tokens trigger retention. Fixed SSMs couldn't learn this kind of selective compression.

This "selective state space" mechanism is the core architectural contribution.

### Mamba-2 (2024)

Reformulated Mamba to establish a theoretical connection to linear attention — specifically, structured state space duality (SSD). This unified framing matters because it lets researchers borrow analysis tools from the attention literature and explains why Mamba works the way it does theoretically, not just empirically.

### Current competitive position

Mamba models perform competitively with transformers on standard language tasks at parameter counts up to roughly 3B. The performance gap opens at larger scales (7B+) and narrows again with careful engineering, but the gap is real.

The more honest limitation is task-specific: pure SSMs struggle on tasks requiring precise long-range retrieval. "Needle-in-a-haystack" style benchmarks — where you embed a specific fact in a long document and ask about it — reveal this weakness clearly. Attention handles this trivially by attending directly to the relevant token. SSMs must have retained the fact in their compressed state through all intervening text, which they often don't.

### Hybrid architectures — the practical near-term bet

The current most promising direction is not pure SSM replacing transformer, but hybrid architectures interleaving both.

**Jamba (AI21 Labs, 2024):** 52B parameter model alternating Mamba + Transformer blocks. The intuition: use Mamba layers for most of the sequence (linear scaling, cheap), use attention layers for key retrieval tasks (expensive but precise). Get most of the efficiency benefits without the retrieval weakness.

This hybrid framing is historically how architectural transitions tend to work in practice — not clean replacement but selective combination that exploits each approach's strengths.

---

## 3. Mixture of Experts (MoE)

### Current status

This is the least "emerging" entry in this document. MoE is already in production at scale. Mixtral 8x7B (Mistral, December 2023) is openly released and widely used. GPT-4 is widely believed (though not confirmed) to be a MoE model. DeepSeek-V3 (December 2024) is explicitly MoE and represents the current frontier of what the architecture can do.

Including it here because it's architecturally distinct from dense transformers in ways that matter for understanding the frontier.

### Core idea

Standard (dense) transformers activate all parameters for every token processed. MoE models have many "expert" feed-forward networks but only activate a subset of them per token. A router decides which experts handle which inputs.

This creates the key property: total parameter count can be much larger than active parameter count. You get the representational capacity of a large model at the inference cost of a small one.

### The routing problem

The router is typically a small MLP (a few hundred to few thousand parameters) that produces a probability distribution over all experts. The top-K experts by probability score are selected (K=2 is standard). The token is processed by those K experts, and their outputs are combined (usually weighted by the router probabilities).

Learning a good router is non-trivial. During training, the model must learn simultaneously which tokens should go to which experts, and what each expert should specialize in. These objectives interact.

### Expert collapse

The failure mode that makes MoE training harder than dense training: if the router learns that a few experts are generally good, it routes most tokens to them. The other experts receive little gradient signal and fail to develop useful specializations. Eventually, 90% of tokens go to 2-3 experts and the rest are wasted capacity.

**Auxiliary load-balancing losses** during training penalize imbalanced routing. This works but creates an objective conflict: the model is trying to minimize prediction loss AND minimize routing imbalance simultaneously. These can pull in opposite directions.

**DeepSeek-V3 innovation (December 2024):** Auxiliary-loss-free load balancing via learned bias terms added to the routing scores. Balance is achieved without a competing loss term. This is reported to improve model quality while maintaining load balance, suggesting the auxiliary loss was itself degrading model quality, not just adding an orthogonal objective. Worth watching as it becomes more widely tested.

### Current scaling frontier

DeepSeek-V3: 671B total parameters, 37B active per token (every token routes to 2 of 256 experts). This is the architecture enabling frontier-quality models at a fraction of inference cost — the 37B active parameters means inference cost is comparable to a dense 37B model despite having 671B total parameters.

### What to watch

Fine-grained MoE: many small experts rather than few large ones. Does expert specialization actually emerge (do experts learn domain-specific knowledge)? Current analysis suggests partial specialization — some syntactic/semantic patterns — but nothing approaching true domain expertise. MoE + SSM hybrids are a natural next step once both are sufficiently mature.

---

## 4. Byte-Level and Tokenization-Free Models

### The tokenization problem

BPE tokenization is, to be direct, a historical accident that became load-bearing infrastructure. It was designed for compression (word-frequency-based subword merges), not for linguistic or mathematical coherence. The production AI field has inherited this design choice because changing it requires retraining from scratch.

The practical consequences:

- "2024" → 1-4 tokens depending on training corpus. Arithmetic on numbers that aren't in the vocabulary requires the model to reason across token boundaries in ways that don't correspond to how arithmetic actually works.
- English has a vocabulary advantage that compounds with context window length. A non-English user with a 128K token window effectively has a shorter window.
- No ability to handle new character sets, new programming languages, or unusual formats without hitting out-of-vocabulary tokens that tokenize as individual bytes (the fallback).

### MegaByte (Yu et al., Meta, 2023)

Hierarchical byte-level model eliminating tokenization entirely. Two-level architecture:

- **Local model:** processes raw bytes grouped into fixed-size patches (e.g., 4 bytes per patch)
- **Global model:** operates on patch-level representations

The local model handles within-patch byte prediction; the global model handles cross-patch context. This avoids the quadratic attention problem by operating at patch granularity globally while remaining byte-exact locally.

Results: competitive with tokenized models at similar compute on standard benchmarks. Better performance on code and multilingual tasks — the domains where tokenization artifacts hurt most. Byte sequences are longer (~4x for English) so the context window math is harder, but the patch compression partially offsets this.

### Byte Latent Transformer (BLT, Meta, 2024)

More refined approach with a key architectural innovation: **entropy-based dynamic patching**. Instead of fixed-size patches, patch boundaries are placed based on the predictive uncertainty at each byte position.

High-entropy (unpredictable) regions — the beginning of words, code tokens, rare characters — get more compute. Low-entropy (predictable) regions — the middle of common words, repeated whitespace — are compressed aggressively into large patches. The model spends compute where it's actually needed.

Reported result: 50% of the FLOPs of a token-based model at equivalent quality on some benchmarks. If this holds at larger scales, it changes the efficiency calculus significantly.

### Why this matters beyond multilingual use cases

A byte-level model treats every input identically: any language, any script, any format. DNA sequences, chemical formulas, network logs, executable binaries — all are just bytes. There's no vocabulary decision, no out-of-vocabulary fallback, no tokenization artifacts. The model's generalization is constrained only by what it has seen, not by what tokens were included in the vocabulary.

### Current limitations

Byte sequences for English are roughly 4x longer than BPE token sequences, which means even with efficient patching the arithmetic for long-context inference is harder. More importantly: the entire inference infrastructure (CUDA kernels, serving frameworks, KV cache optimization) is built around token sequences of typical vocabulary sizes (~50K-100K). Byte-level models require infrastructure work that hasn't happened yet at scale.

This is the kind of gap that takes years to close — it's not about the architecture being wrong.

### What to watch

BLT scaling results at 7B+ parameters (current experiments are smaller). Whether entropy-based patching quality holds or degrades at scale. Adoption in multilingual production systems where the tokenization penalty is most economically painful.

---

## 5. Continuous / Latent Space Models

### The core idea

Every architecture discussed so far — transformer, SSM, MoE, byte-level — still predicts discrete outputs at inference time. Given a context, the model outputs a probability distribution over tokens (or bytes), samples one, then repeats.

Continuous / latent space models ask: what if the model predicted in a continuous vector space instead? Instead of "which discrete token comes next," the model learns to predict continuous representations of meaning, then decode those representations to text when output is needed.

This is inspired by the success of diffusion models in image generation, where the model learns to denoise continuous image representations rather than predicting discrete pixel values.

### CALM — Continuous Autoregressive Language Models (2025)

CALM (published by researchers including DeepSeek affiliates) predicts continuous vectors representing K-token chunks rather than individual tokens. The architecture is two-stage:

1. **Autoencoder:** learns to compress K tokens into 1 continuous vector and reconstruct them back
2. **Language model:** learns to predict these vectors autoregressively — predicting the next chunk's vector given previous chunk vectors

The theoretical efficiency gain: K× fewer autoregressive steps. If K=8, you need 1/8th as many forward passes to generate the same number of tokens.

**Current experimental status:** Experiments at up to 1.82B parameters. Custom evaluation metric (BrierLM) because standard perplexity doesn't apply to continuous predictions. Not yet benchmarked against standard tasks (MMLU, HumanEval, GSM8K) in a way comparable to existing literature.

This is important context for calibrating excitement: a 1.82B parameter model with a custom metric is very early research. The architecture is interesting; the validation against the field's shared benchmarks hasn't happened yet.

### Diffusion language models

Apply image diffusion (iterative denoising from noise toward data) to text generation. Generate all tokens in parallel across multiple denoising iterations rather than one token at a time.

**MDLM, SEDD (2024):** Most developed current approaches. Competitive with autoregressive models on some constrained generation tasks (infilling, editing — where you know something about the structure of what you're generating). Open-ended generation quality still lags autoregressive models.

The fundamental challenge: images are continuous (pixel values are real numbers, and nearby values are semantically similar). Text is discrete — "cat" and "bat" are one character apart but semantically distant. Diffusion in a continuous embedding space partially addresses this but introduces its own complications.

### Flow matching for text

Continuous normalizing flows applied to text generation. Theoretically cleaner than diffusion — one-step generation is theoretically possible (vs. many denoising steps in diffusion). Very early stage for language applications. Worth knowing it exists; not worth tracking closely until results at scale appear.

### The common thread and the key open question

All of these move away from "predict which discrete token comes next" toward "predict a distribution in a continuous space." The intuition is that the discretization step (forcing the model to commit to a specific token at each step) throws away useful information and imposes an artificial constraint.

The key open question is whether this translates from images to text. In image generation, there's no equivalent to "the name 'Smith' is either there or it isn't." Continuous spaces handle smooth transitions between values naturally; discrete facts are harder. Current evidence suggests continuous models are more useful for tasks with natural continuous structure (editing, constrained generation) than for open-ended generation where exact token identity often matters.

---

## 6. Linear Attention and Efficient Attention Variants

### Standard attention baseline

O(n²) time and O(n²) memory without optimization. FlashAttention brings memory to O(n) via tiled recomputation, but compute remains O(n²). This section covers approaches that actually change the computational complexity.

### Linear attention — the core idea

Standard attention computes a softmax over all pairwise token similarities:

```
Attention(Q, K, V) = softmax(QK^T / sqrt(d)) · V
```

The softmax forces global normalization across all n keys. Linear attention approximates this using a kernel function φ(·) that decomposes the computation:

```
LinearAttention(Q, K, V) = φ(Q) · (φ(K)^T · V)
```

Because matrix multiplication is associative, (φ(K)^T · V) can be computed first (O(n·d²)), then multiplied by φ(Q) (O(n·d²)). Total: O(n) rather than O(n²). The approximation quality depends on the kernel function — closer to softmax costs more; cheaper approximations diverge more.

### Current implementations worth tracking

**Performer (Choromanski et al., 2020):** Random feature approximation of softmax kernel. Unbiased estimator, but variance can be high. Doesn't match transformer quality in practice for most tasks.

**RetNet (Microsoft, 2023):** Recurrent formulation of linear attention. During training: parallel computation (efficient). During inference: recurrent computation (O(1) memory). Competitive with transformers on language tasks at up to ~3B parameters.

**RWKV-6 (2024):** Pure RNN architecture achieving transformer-competitive quality. O(1) memory at inference — truly constant regardless of sequence length, unlike attention's linearly growing KV cache. The cost is reduced precision retrieval. RWKV-6 is notable as a pure recurrent architecture that actually competes on language benchmarks rather than just efficiency metrics.

### The retrieval precision tradeoff

All linear attention variants sacrifice the ability to precisely retrieve specific tokens from the past. Standard attention can look at token 1 even when generating token 10,000, with no information loss. Linear attention variants must compress that context, and compression means some precision is lost.

For generation tasks (write me a story, summarize this), this is often fine. For retrieval tasks (what exactly did the document say about X), precision loss shows up in quality metrics. This is the same fundamental tradeoff as SSMs — they're related approaches to the same problem.

### GQA / MQA — the incremental path already in production

Grouped Query Attention (GQA) and Multi-Query Attention (MQA) reduce KV cache size by sharing K and V tensors across multiple attention heads. Standard attention has H heads, each with its own K,V. MQA has 1 shared K,V. GQA groups heads and shares within groups.

This is not linear attention — compute is still O(n²). But KV cache is reduced by 4-8x, enabling longer effective context windows without architectural overhaul.

Already deployed: Llama 3, Mistral, Gemini all use GQA. This is the incremental efficiency win that has shipped while linear attention remains in research.

---

## 7. Signal vs. Noise Framework

New "paradigm shift" architecture papers appear regularly. Most don't scale. Here's a practical framework for calibrating attention.

### Green flags — take seriously

**Results at 7B+ parameters.** Small-scale results frequently don't transfer. The history of efficient attention is littered with architectures that worked well at 1B and failed to match transformers at 7B+. If a paper only has <3B results, the verdict is genuinely unknown.

**Standard benchmark evaluation.** MMLU, HumanEval, GSM8K, HellaSwag, MMLU-Pro — these exist so researchers can make apples-to-apples comparisons. A paper that introduces a custom metric and doesn't report standard benchmarks is harder to assess. It may be a legitimate scaling issue (metric doesn't apply at scale yet) or it may be avoiding unfavorable comparisons.

**Hybrid approach.** Architectures that combine a new technique with proven transformer components are historically more likely to ship than "complete replacement" proposals. Jamba (Mamba + attention) is a cleaner bet than pure Mamba.

**Lab with production infrastructure.** Google, Meta, Mistral, DeepSeek, AI21 Labs — these organizations can actually scale and test. A compelling paper from a university group without access to 1,000+ GPU training runs is interesting but incompletely validated.

**Open weights.** Community reproduction is the best stress test. If the weights are available, the broader research community will find the failure modes quickly. Closed results are harder to assess.

### Red flags — wait and see

**Results only at <2B parameters.** See above. Small-scale results can be genuinely misleading.

**Custom evaluation metric not comparable to existing literature.** CALM's BrierLM is the recent example. Necessary because perplexity doesn't apply — but it means you can't compare to anything else.

**Speedup claims without wall-clock benchmarks on real hardware.** FLOPs reductions don't always translate to actual latency improvements due to memory bandwidth constraints, hardware utilization patterns, and software implementation maturity. "K× fewer operations" is not the same as "K× faster in production."

**"Completely replaces transformers" framing.** The likely near-term outcome for any competitive architecture is hybrid combination, not replacement. Claims of clean replacement are often overstated.

**No ablations.** Which specific component drives the improvement? Papers without ablations leave open the question of whether the architectural innovation is doing the work or whether it's confounded with training recipe changes, data quality, or compute differences.

### Current status table (early 2026)

| Architecture | Production-ready? | Maturity | Transformer threat level |
|---|---|---|---|
| MoE | Yes — in production | High | Complement, not replacement |
| Hybrid SSM/Transformer | Early production | Medium | Partial replacement for long-context use cases |
| Pure SSM (Mamba) | Research → early prod | Medium | Limited by retrieval precision weakness |
| Byte-level (BLT) | Research | Low-medium | Promising, 2-3 year horizon |
| Continuous/CALM | Research | Low | Long-horizon research direction |
| Diffusion LM | Research | Low | Niche use cases (infilling, constrained gen) |
| Linear attention | Research → early prod | Medium | Efficiency play, not quality play |

---

## 8. The Practical Implication for Builders

This section is the "so what" — how does knowing this change what you do?

### For the next 1-2 years (2026-2027)

Transformers remain the right default for everything. The engineering infrastructure (training frameworks, serving systems, optimization tools, scaling laws) is built around transformers. Switching away before alternatives are proven at scale is adopting infrastructure debt, not gaining advantage.

MoE is already the architecture of frontier models. If you're evaluating vendors or building on frontier APIs, the models you're using are almost certainly MoE under the hood. Understanding MoE helps you reason about expert routing, inference cost, and why some tasks might have inconsistent quality (routing variance can be non-trivial).

### For the next 2-4 years (2027-2029)

Hybrid SSM/transformer models will likely appear in production for specific long-context use cases. The economics are compelling: if you can process 500K tokens at SSM cost for most of the sequence and only pay attention costs for a small fraction, that changes the unit economics of long-context applications (legal document analysis, long video understanding, extended conversation history).

Watch Jamba-style models and similar hybrids. This is probably where you'll first encounter non-transformer architecture choices in vendor offerings.

### For the next 4+ years (2029+)

Byte-level and continuous-space models are the longer bets. If either achieves transformer parity at scale, the implications are significant:

- Byte-level parity: the tokenization stack (BPE vocabularies, tokenizer libraries, all the vocabulary-dependent infrastructure) becomes legacy. Multilingual and multi-format applications get dramatically simpler.
- Continuous-space parity: the discrete-token paradigm (the assumption underlying all current LLM APIs) changes. What "generating text" means architecturally shifts.

These are research directions, not near-term product decisions.

### PM / product implication

When evaluating AI vendors or making architecture decisions in 2026-2027, "transformer" vs. "hybrid SSM/transformer" will start mattering for specific use cases:

- **Long-context tasks (>100K tokens):** KV cache costs are the current bottleneck. Hybrid SSM models could offer substantially lower inference costs at long context. Worth asking vendors about architectural roadmap.
- **Multilingual products:** If your user base is non-English-heavy, tokenization inefficiency is a real cost. Byte-level models, if they reach production quality, would be a meaningful advantage. Worth watching BLT progress.
- **Real-time inference:** Latency-sensitive applications (voice assistants, interactive code completion) care about autoregressive generation speed. SSM and linear attention architectures promise faster inference. Currently not validated at quality parity for most tasks.

Knowing these tradeoffs lets you ask better procurement questions and recognize when a vendor's architectural choice is meaningful for your specific use case rather than marketing language.

---

## A Note on Uncertainty

This document reflects the state of a fast-moving research field as understood in early 2026. Several things are genuinely unknown:

- Whether any of the "research" architectures in the table above will reach production quality at scale
- Whether hybrid approaches (SSM + attention, byte-level + token) become the dominant path or whether cleaner replacements emerge
- Whether the continuous/latent space direction will translate from images to text in the ways researchers hope

The honest answer to "will transformers be replaced?" is: maybe, eventually, and probably not cleanly. The history of ML is that dominant architectures get augmented more often than replaced. The transformer will likely remain load-bearing long after better theoretical alternatives exist, because switching costs compound.

Track the green flags. Be skeptical of the red flags. Re-read this document in 12 months and see what changed.

---

*This document is part of the AI Knowledgebase — LEARNING/FOUNDATIONS/emerging-architectures/*
*Last updated: early 2026*
*Sources: Gu & Dao (Mamba, 2023), Gu & Dao (Mamba-2, 2024), Mistral (Mixtral 8x7B, 2023), AI21 Labs (Jamba, 2024), DeepSeek (DeepSeek-V3, 2024), Yu et al. Meta (MegaByte, 2023), Meta (BLT, 2024), DeepSeek researchers (CALM, 2025), Sahoo et al. (MDLM/SEDD, 2024), Choromanski et al. (Performer, 2020), Bo et al. (RWKV-6, 2024), Peng et al. (RetNet, 2023)*
