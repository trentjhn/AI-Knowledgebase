# Inference Optimization

**What this covers:** How LLMs actually run in production — where compute goes, why serving is expensive, and the full toolkit for making it faster, cheaper, and more scalable. Every section includes concrete numbers and a "when to use" judgment call.

**Prerequisites:** Familiarity with transformer architecture basics (attention heads, layers, weights). You don't need to implement anything, but you should know what forward passes and attention matrices are conceptually.

---

## Table of Contents

1. [What Inference Optimization Actually Is](#1-what-inference-optimization-actually-is)
2. [Quantization](#2-quantization)
3. [Speculative Decoding](#3-speculative-decoding)
4. [KV Cache Optimization](#4-kv-cache-optimization)
5. [Continuous Batching](#5-continuous-batching)
6. [Model Serving Frameworks](#6-model-serving-frameworks)
7. [Parallelism Strategies](#7-parallelism-strategies)
8. [Flash Attention](#8-flash-attention)
9. [Production Optimization Workflow](#9-production-optimization-workflow)
10. [Cost Mental Model](#10-cost-mental-model)

---

## 1. What Inference Optimization Actually Is

### Training vs. Inference Compute

**Training** is a one-time cost. You run a massive GPU cluster for weeks or months, compute gradients, update weights, repeat. The result: a frozen set of weights saved to disk. This is expensive once.

**Inference** is the ongoing cost. Every time a user sends a message, you load those frozen weights and do a forward pass to generate tokens. You do this millions of times per day, in real time, with latency requirements. This is where money actually goes in production.

The distinction matters because training optimizations (gradient checkpointing, mixed precision training, etc.) are irrelevant post-deployment. You need a completely different toolkit.

### Why Inference Is the Bottleneck

Three separate problems converge at inference time, and they pull in different directions:

**Latency:** Users expect responses in under a second for simple queries, a few seconds for complex ones. LLMs are autoregressive — they generate one token at a time, and each token requires a full forward pass through all model layers. A 70B parameter model doing a forward pass takes meaningful wall-clock time. Generate 500 tokens, and you've done 500 sequential forward passes. You cannot parallelize across output tokens (each token depends on the previous ones).

**Throughput:** A single GPU serving one request at a time is massively wasteful. The GPU has thousands of CUDA cores; a single forward pass doesn't saturate them. You want to batch many requests together to amortize the fixed cost per pass. But batching increases latency for individual requests. This is the core tension.

**Memory:** Modern LLMs require enormous amounts of GPU VRAM just to hold their weights. Llama 3 70B in FP16 (standard half-precision) requires ~140GB VRAM — that's 8 A100 80GB GPUs just to load the model, with no room for the requests themselves. VRAM limits how much batching you can do, how long the sequences can be, and how many requests you can serve concurrently.

### The Fundamental Tradeoffs

| Dimension | Optimize for speed | Optimize for quality | Middle ground |
|-----------|-------------------|---------------------|---------------|
| Precision | INT4 quantization | FP16/BF16 full precision | INT8 |
| Memory | Smaller KV cache, sliding window | Full KV cache | GQA, prefix caching |
| Throughput | Large batches | Small batches (lower latency) | Continuous batching |
| Model size | Smaller/distilled model | Full model | Speculative decoding |

Every inference optimization is a tradeoff negotiation. The goal is finding the efficient frontier for your specific use case — knowing which corner you're in determines which tools apply.

### Key Metrics You Must Know

**Tokens per second (TPS):** How many output tokens the system generates per second, total. A throughput metric — matters for batch jobs, cost efficiency, capacity planning.

**Time to First Token (TTFT):** How long from request submission until the first output token arrives. Drives perceived responsiveness. For streaming interfaces, this is the "time until something appears on screen." TTFT is primarily a function of prompt processing speed (prefill phase).

**Time Per Output Token (TPOT):** Average time between successive output tokens after the first. Drives streaming smoothness. TPOT is primarily a function of the decode phase — the autoregressive bottleneck.

**P50 / P95 / P99 latency:** Median, 95th percentile, 99th percentile end-to-end latency. P50 tells you the typical user experience. P95 and P99 tell you the tail — the worst 5% and 1% of requests. Tail latency matters: if P99 is 10 seconds, roughly 1 in 100 requests feels broken to the user. SLAs are usually defined at P95 or P99, not P50.

**GPU utilization:** What percentage of GPU compute is being used. In naive serving setups, GPU utilization can be 30-50% because the GPU is idle waiting for sequential token generation. Good serving frameworks push this above 80%.

**Memory bandwidth utilization:** LLM inference is often memory bandwidth-bound (reading weights from HBM into SRAM for computation), not compute-bound. This is why certain optimizations (Flash Attention, quantization) are so impactful — they reduce memory traffic.

---

## 2. Quantization

### What Quantization Is

Neural network weights are stored as floating-point numbers. By default, a trained model uses 32-bit floats (FP32) or 16-bit floats (FP16/BF16). Quantization means converting those weights to a lower-precision format — fewer bits per number.

The payoff: a weight that used to take 16 bits now takes 8 bits (INT8) or 4 bits (INT4). This halves or quarters the memory footprint, which means:
- Larger models fit on fewer GPUs
- More room for batching and KV cache
- Faster weight loading from memory (memory bandwidth-bound workloads get faster)
- Reduced cost

The risk: information loss. Fewer bits means less representational precision. The question is whether that precision loss degrades model quality in a way that matters for your use case.

### Precision Formats Explained

**FP32 (32-bit floating point):**
- 1 sign bit, 8 exponent bits, 23 mantissa bits
- The format GPUs were designed for decades ago; used for training because gradients need high precision
- 4 bytes per weight
- Not used for inference in 2024+ (too slow, too much memory)

**FP16 (16-bit floating point):**
- 1 sign bit, 5 exponent bits, 10 mantissa bits
- 2 bytes per weight
- More mantissa precision than BF16, but narrower exponent range (max representable value: ~65,504)
- Vulnerable to overflow on activation outliers in LLMs (large activations can exceed the representable range)

**BF16 (Brain Float 16):**
- 1 sign bit, 8 exponent bits (same as FP32), 7 mantissa bits
- 2 bytes per weight
- Same dynamic range as FP32 — handles large outlier values without overflow
- Less mantissa precision than FP16, but LLMs don't need it
- **Preferred over FP16 for LLM inference** because LLM activations have significant outliers that would overflow FP16
- Requires hardware support: A100, H100, TPUv3+ support BF16 natively; older GPUs may not

**INT8 (8-bit integer):**
- 1 byte per weight
- Not a floating-point format — values are integers in a fixed range (e.g., -128 to 127)
- Requires a "dequantization" step to convert back to float for computation (or quantized GEMM kernels)
- Accuracy degradation: typically less than 1% on standard benchmarks

**INT4 (4-bit integer):**
- 0.5 bytes per weight (two weights packed per byte)
- Requires group quantization (see GPTQ below) to maintain quality
- Accuracy degradation: typically 1-3%, model-dependent
- The standard for VRAM-constrained production serving

**FP8 (8-bit floating point):**
- Emerging format (H100 supports it natively)
- Better than INT8 for activations because it preserves dynamic range
- Flash Attention 3 leverages FP8; increasingly common in 2024-2025

### Why Quantization Works (The Surprising Reason)

LLM weights don't use their full numerical range uniformly. In practice, most weights cluster in a small range; extreme values are rare. The information content of the full precision format is largely redundant — you're paying 16 bits of storage for what's effectively a few bits of useful information in most weights.

More concretely: when researchers analyze weight distributions in trained LLMs, they find that ~99% of weights fall within a narrow range, with a small tail of outliers. Quantizing those 99% to lower precision loses almost nothing. The challenge is handling the outliers — which is exactly what AWQ and GPTQ address differently.

### Post-Training Quantization (PTQ)

PTQ quantizes an already-trained model without any retraining. You take the FP16 weights and convert them to INT8 or INT4. No GPU cluster required, no training data needed (or just a small calibration set). This is the practical approach for most teams.

**GPTQ (Generative Pre-trained Transformer Quantization):**
- Published by Frantar et al. (2022), now the dominant INT4 quantization method
- Core idea: minimize the quantization error layer by layer using second-order information (Hessian of the layer's outputs)
- **Group-wise quantization:** instead of using one scale factor for the entire weight matrix, use a separate scale factor per group of ~128 weights; this dramatically reduces quantization error on weights with non-uniform distributions
- Requires a small calibration dataset (~512 samples) to compute the Hessian
- Process takes hours on a GPU, but you only do it once; the output is a quantized model file
- Quality: very close to FP16 at INT4, especially with group size 128
- Widely supported: vLLM, llama.cpp, AutoGPTQ library

**AWQ (Activation-aware Weight Quantization):**
- Published by Lin et al. (2023)
- Different insight: instead of minimizing reconstruction error uniformly, identify the ~1% of weights that are most important based on activation magnitudes (how often large activations flow through each weight channel), and protect them
- Protection mechanism: scale important channels before quantization (not actually storing them at higher precision, but mathematically equivalent) — these channels dominate the output, so preserving their effective precision matters most
- Often better quality than GPTQ at INT4, particularly on instruction-following tasks and at lower group sizes
- Supported by vLLM, AutoAWQ library

**Which to use:** AWQ is often preferred for quality-sensitive applications; GPTQ has broader tooling support and is fine for most cases. Both are dramatically better than naive round-to-nearest quantization.

### Quantization-Aware Training (QAT)

Instead of quantizing after training, simulate quantization during training — use "fake quantization" operators that round weights as if they were quantized but still compute in full precision. The model learns to be robust to the quantization error.

Result: significantly better quality than PTQ at the same bit-width, sometimes matching FP16 quality at INT4. But requires the original training pipeline, training data, and GPU compute. Not feasible for most practitioners unless you control the training process. Used by model providers when releasing optimized versions (e.g., Google's Gemma has QAT variants).

### The Accuracy Cliff

Empirical benchmarks across many models and datasets:

| Precision | Memory vs. FP16 | Accuracy degradation | Notes |
|-----------|----------------|---------------------|-------|
| BF16 | 1× (baseline) | ~0% | Reference quality |
| INT8 | 0.5× | <1% | Safe default; nearly lossless |
| INT4 (GPTQ/AWQ) | 0.25× | 1–3% | Noticeable on some tasks; fine for most |
| INT4 (naive) | 0.25× | 5–15% | Avoid; use GPTQ or AWQ |
| INT3 | 0.19× | 10–30% | Significant degradation; use carefully |
| INT2 | 0.13× | Very high | Research territory; not production-ready |

The cliff is real at INT3 and below. INT8 is almost always safe. INT4 with a good method (GPTQ/AWQ) is the practical sweet spot when VRAM is the constraint.

### Concrete VRAM Numbers

| Model | BF16/FP16 | INT8 | INT4 |
|-------|-----------|------|------|
| 7B | 14GB | 7GB | 4GB |
| 13B | 26GB | 13GB | 7GB |
| 34B | 68GB | 34GB | 17GB |
| 70B | 140GB | 70GB | 35GB |
| 405B | ~810GB | ~405GB | ~200GB |

What this means practically: Llama 3 70B at FP16 requires 8× A100 80GB GPUs just to hold the model weights (140GB / 80GB = 1.75, so you need at least 2 GPUs, but with overhead you need more). At INT4, it fits comfortably on 2× A100 80GB GPUs (35GB weights + room for KV cache and batch).

### When to Use Quantization

**Use INT8:** When serving a model that fits in your VRAM at BF16, but you want headroom for larger batch sizes or KV cache. Near-zero quality cost. Should be the default for production serving.

**Use INT4 (GPTQ or AWQ):** When you're VRAM-constrained — the model you need doesn't fit at BF16 or INT8. Evaluate quality on your actual use case before deploying; some tasks are more sensitive than others.

**Avoid quantization when:** Quality is paramount and VRAM is not a constraint (e.g., high-value medical/legal applications where 1-3% degradation is unacceptable). Use BF16.

---

## 3. Speculative Decoding

### The Autoregressive Bottleneck

Standard LLM generation is inherently sequential. To generate the next token, you must complete the forward pass for the current token, sample from the output distribution, append the sampled token to the sequence, and repeat. You cannot generate token N+1 until token N is finalized.

This means generating 200 tokens requires 200 sequential forward passes through the full model. Each forward pass through a 70B model takes meaningful time even on fast hardware. Speculative decoding is the main technique for breaking this sequential constraint.

### Core Mechanism

The insight: **verifying k tokens is no slower than generating 1 token.**

When the target model does a forward pass over a sequence of length n, it computes the probability distribution at every position in parallel — that's just how transformer attention works. So if you show the target model a candidate sequence of k new tokens, it can check whether it would have generated each of those tokens in a single forward pass. The cost is the same as a forward pass for generating 1 token.

The algorithm:
1. A small, fast "draft" model generates k tokens speculatively (e.g., k=4)
2. The large "target" model performs a single forward pass over the prompt + those k draft tokens
3. Compare the draft model's chosen tokens against the target model's probability distributions at each position
4. Accept draft tokens that match the target model's distribution (within a threshold); reject the first mismatch
5. From the rejection point onward, use the target model's output (which you already computed in step 2)
6. Net result: you've generated some number of verified tokens (1 to k+1) at the cost of approximately 1 target model forward pass

The acceptance rate varies by task. Easy/predictable text (code boilerplate, formulaic writing, short completions) accepts more draft tokens. Creative/diverse generation accepts fewer.

### Speed Gains

Empirical results vary by task type:

| Task type | Typical speedup | Notes |
|-----------|----------------|-------|
| Code generation | 2.5–3.5× | High acceptance rate; predictable structure |
| Summarization | 2–2.5× | Moderate predictability |
| Short factual Q&A | 1.5–2× | Often too short to benefit much |
| Creative writing | 1.2–1.8× | Low acceptance; diverse outputs |
| Very short outputs (<20 tokens) | ~1× | Overhead outweighs benefit |

The gains are in latency (TTFT stays the same; TPOT improves), not throughput. Speculative decoding doesn't help if you're trying to maximize tokens/second for a batch workload — it actually slightly reduces throughput due to draft model overhead.

### Draft Model Requirements

The draft model must:
- Share the exact same tokenizer as the target model (non-negotiable — you're comparing token distributions)
- Be substantially smaller, so speculative generation is fast: 7B draft for a 70B target is typical (10:1 ratio)
- Be somewhat aligned with the target model's output distribution (ideally fine-tuned from the same base)

Example pairings: Llama 3 8B (draft) → Llama 3 70B (target). The 8B model runs ~10× faster, generating k=4 draft tokens in the time the 70B model would take to generate 1, then the 70B verifies all 4 in one pass.

### Self-Speculative Decoding / Medusa Heads

Maintaining a separate draft model has operational overhead (two models to load, serve, and update). Medusa (Cai et al., 2024) takes a different approach: add multiple extra "speculation heads" to the target model itself.

Each head predicts a future token in parallel with the main head. The main head predicts token t+1; head 2 predicts t+2; head 3 predicts t+3, etc. These heads are small (a single linear layer) and trained to match the main model's output. During generation, all heads run simultaneously, and you accept the longest consistent prefix.

Tradeoffs vs. separate draft model:
- Speedup: typically 1.5–2× vs. 2–3× with separate draft model
- No tokenizer constraint (same model)
- No separate model to manage
- Requires modifying and fine-tuning the target model (adding the heads)
- Not available for arbitrary off-the-shelf models unless someone has released a Medusa version

### When to Use Speculative Decoding

**Use it when:** Latency is the primary concern; you're streaming responses to users; your workload has predictable outputs (code, templates, structured data). The draft model overhead is worth the TPOT improvement.

**Don't use it when:** Throughput is more important than latency; you're running large offline batch jobs; outputs are highly creative/diverse (acceptance rate too low to be worth it); you don't have a compatible draft model available.

---

## 4. KV Cache Optimization

### What the KV Cache Is

Transformer attention works by computing Query (Q), Key (K), and Value (V) matrices for each token at each layer. When generating token N, the model needs K and V from all previous tokens (tokens 1 through N-1) to compute attention. Without caching, you'd recompute K and V for every previous token on every generation step — O(n²) total compute.

The KV cache solves this: after computing K and V for each token, store them in GPU memory. On the next generation step, read from cache instead of recomputing. This reduces per-token generation from O(n) compute to O(1) compute for the cached portion.

Cost: the cache occupies GPU VRAM, and it grows with every token generated.

### Memory Formula

KV cache size = 2 × num_layers × num_heads × head_dim × sequence_length × batch_size × bytes_per_element

For Llama 3 70B with GQA (Grouped Query Attention):
- 80 layers, 8 KV heads (after GQA), head_dim = 128
- 2 (K and V) × 80 × 8 × 128 = 163,840 floats per token per batch element
- At BF16 (2 bytes): 327,680 bytes ≈ 320 KB per token per batch element

For a batch of 32 requests at sequence_length=8,192:
- 320 KB × 8,192 tokens × 32 requests = ~83GB just for KV cache

This is why VRAM management for the KV cache is a first-class problem, not an afterthought.

### PagedAttention (vLLM's Core Innovation)

Before PagedAttention, serving frameworks pre-allocated a contiguous block of GPU memory per request for the full maximum sequence length. A 4,096-token max sequence reserved 4,096 slots even if the actual request was 200 tokens. This caused two problems: fragmentation (lots of wasted reserved space) and inability to share memory across requests.

PagedAttention (Kwon et al., 2023, the vLLM paper) borrows virtual memory paging from operating system design:

1. KV cache is divided into fixed-size "pages" (blocks), typically 16 or 32 tokens per block
2. Pages are allocated on demand as sequences grow — no pre-allocation
3. Logical pages (the sequence's view of contiguous memory) are mapped to physical pages (actual GPU memory) via a page table, just like OS virtual memory
4. Physical pages can be non-contiguous
5. Pages can be shared across requests with identical prefixes (same system prompt = same first N pages)

Results from the original paper: 24× throughput improvement over naive serving. In practice, memory utilization goes from ~40% (naive) to >95% (PagedAttention), enabling far more concurrent requests on the same hardware.

PagedAttention also enables copy-on-write sharing for beam search (multiple candidate beams share the same prefix pages until they diverge) and across requests (shared system prompts).

### Prefix Caching

When many requests share the same prefix — a long system prompt, a document being analyzed, a few-shot example set — you're recomputing the same KV cache values for that prefix on every request. Prefix caching stores the KV cache for common prefixes and reuses them.

Effect: TTFT drops dramatically for cached prefixes. If your system prompt is 2,000 tokens and it's cached, the effective prefill work for each new request is reduced by those 2,000 tokens. For a 2,500-token total context, that's an 80% prefill savings.

This is what Anthropic calls "prompt caching" in their API — when you cache a system prompt, subsequent requests with that same prefix are charged less and return faster because the KV cache was precomputed and stored. The economics: cached tokens cost ~10% of normal input tokens. See `cost-optimized-llm-workflows.md` for the full pricing model.

In self-hosted vLLM: enable with `--enable-prefix-caching` flag. Works best when your system prompt is long and consistent across requests.

### Sliding Window Attention (Mistral Approach)

Rather than attending to all previous tokens (KV cache grows unboundedly), only attend to the most recent W tokens. Mistral 7B uses W=4,096.

Effect: KV cache size is bounded by W regardless of sequence length. You can serve arbitrarily long sequences without running out of VRAM for KV cache.

Tradeoff: you lose attention to tokens outside the window. Information from earlier in the context can only influence current generation indirectly (via tokens that were themselves influenced by earlier tokens — recency gradient). For many tasks this is fine; for tasks requiring explicit reference to information from thousands of tokens ago, it's a real capability loss.

### Grouped Query Attention (GQA) and Multi-Query Attention (MQA)

In standard Multi-Head Attention (MHA), each attention head has its own separate K and V matrices. For a model with 64 attention heads, you store 64 sets of K and V in the cache.

**Multi-Query Attention (MQA):** All Q heads share a single K head and a single V head. KV cache size reduced to 1/64 of MHA. Small quality degradation; used in some early models.

**Grouped Query Attention (GQA):** Q heads are divided into groups; each group shares one K head and one V head. Middle ground between MHA and MQA. Example: 64 Q heads, 8 KV groups → KV cache is 8/64 = 1/8 of MHA.

GQA is now the standard in modern LLMs: Llama 3 (all sizes), Mistral 7B, Gemma 2, Phi-3, etc. Minimal quality impact, substantial memory savings. When you see "GQA" in a model card, the KV cache is significantly smaller than you'd compute with the raw num_heads figure — use the num_kv_heads value instead.

### When to Focus on KV Cache

KV cache is always relevant for long-context workloads. Key decisions:
- Enable prefix caching whenever requests share system prompts (almost always free wins)
- Use GQA models when available (already baked in for modern LLMs)
- Configure appropriate max batch size based on VRAM budget for KV cache (don't just maximize — OOM kills throughput)
- For truly long-context serving (100K+ tokens), consider sliding window or other bounded-cache architectures

---

## 5. Continuous Batching

### The Problem with Static Batching

Naive LLM serving uses static (synchronous) batching: collect N requests into a batch, run them together until all N complete, then collect the next batch. This seems efficient but has a fundamental flaw.

Requests have wildly different completion lengths. One request might finish in 50 tokens; another in 500. With static batching, the 50-token request finishes early but its GPU slot sits idle for the remaining 450 tokens of the 500-token request. The batch doesn't release until the last request finishes. GPU utilization: 30-60%.

For a visual: imagine a 4-lane highway where all cars must travel at the speed of the slowest car, and fast cars sit at the destination waiting for the others before the next group can leave. Extremely wasteful.

### Continuous Batching (Iteration-Level Scheduling)

Continuous batching (also called dynamic batching or in-flight batching) operates at the token level rather than the request level. After every single token generation step:

1. Check if any sequence in the batch generated an EOS (end-of-sequence) token
2. If yes, immediately remove that sequence from the batch
3. Pull in a waiting request from the queue to fill the slot
4. Continue to the next token generation step

The batch composition changes every single token step. No request ever waits for another request to finish before its slot is freed. GPU utilization approaches 90%+.

This is not a minor optimization. The difference:

| Serving approach | GPU utilization | Throughput at scale |
|-----------------|----------------|---------------------|
| Static batching (naive) | 30–60% | 1× (baseline) |
| Continuous batching | 85–95% | 5–30× |

The 5-30× range is real — the multiplier depends on how variable your request lengths are. If all requests are exactly the same length, static batching is fine. In practice, request lengths are extremely variable, so continuous batching wins enormously.

### Implementation

You don't implement this yourself. Every serious serving framework uses continuous batching:
- vLLM: yes, core feature
- TGI: yes, core feature
- SGLang: yes
- Triton Inference Server: supported with TensorRT-LLM backend

If you're rolling your own serving code without a framework, you're almost certainly leaving 80% of your GPU throughput on the table.

### Interaction with PagedAttention

Continuous batching and PagedAttention work together. PagedAttention handles the memory management for variable-length KV caches; continuous batching handles the scheduling. Together they're why vLLM can achieve near-100% GPU utilization with arbitrary-length requests.

---

## 6. Model Serving Frameworks

### vLLM

- **Origin:** UC Berkeley, 2023. Open source (Apache 2.0).
- **Core innovation:** PagedAttention (the original implementation)
- **Language:** Python + CUDA kernels
- **Best at:** High-throughput multi-user serving. The default choice for self-hosted LLM serving.
- **Key features:**
  - PagedAttention + continuous batching
  - OpenAI-compatible REST API (drop-in replacement for many use cases)
  - Tensor parallelism (`--tensor-parallel-size N`)
  - Pipeline parallelism for very large models
  - Prefix caching (enable with `--enable-prefix-caching`)
  - Quantization support: GPTQ, AWQ, INT8, FP8
  - Speculative decoding support
  - Streaming support
- **Limitations:** Setup can be involved; not the easiest for containerized deployment compared to TGI
- **Recommended when:** Self-hosting a model for multi-user serving, batch inference jobs, need high throughput

### TGI (Text Generation Inference)

- **Origin:** Hugging Face, 2023. Open source.
- **Language:** Rust + Python; ships as a Docker container
- **Best at:** Ease of deployment, especially for models from the HuggingFace Hub
- **Key features:**
  - Continuous batching
  - Flash Attention 2 (default)
  - Streaming via SSE
  - HuggingFace Hub integration (just specify the model ID)
  - Tensor parallelism
  - Quantization (GPTQ, AWQ, BNB)
- **Limitations:** Raw throughput at scale is slightly below vLLM for equivalent hardware; less flexible than vLLM for advanced configurations
- **Recommended when:** Quick containerized deployment; Hugging Face ecosystem; simpler operational requirements

### Triton Inference Server (NVIDIA)

- **Origin:** NVIDIA, production-grade, battle-tested over many years. Open source.
- **Language:** C++ core; Python/Java/Go client SDKs
- **Best at:** Enterprise deployments on NVIDIA hardware; multi-model serving (not just LLMs); framework-agnostic (PyTorch, TensorRT, ONNX, TF)
- **Key features:**
  - TensorRT backend provides maximum performance on NVIDIA GPUs (graph optimization, kernel fusion, INT8/FP8)
  - Multi-model serving (serve classification + LLM + embedding model from one server)
  - Dynamic batching
  - CUDA MPS (Multi-Process Service) for sharing GPUs across models
  - Kubernetes integration; production-grade monitoring (Prometheus, Grafana)
- **Limitations:** Highest setup complexity; requires TensorRT engine compilation (hours per model); steep learning curve; overkill for simple use cases
- **Recommended when:** Enterprise with dedicated infra team; need to optimize specifically for NVIDIA hardware; serving multiple model types; strict latency SLAs

### SGLang

- **Origin:** Stanford, 2024. Open source.
- **Language:** Python
- **Best at:** Agent workloads with structured outputs; complex multi-turn LLM programs
- **Core innovation:** RadixAttention — a prefix caching system that automatically identifies and caches shared prefixes across requests using a radix tree structure; more sophisticated than vLLM's prefix caching for dynamic patterns
- **Key features:**
  - RadixAttention (superior prefix reuse for agent patterns)
  - Structured output generation (JSON schema enforcement, faster than constrained decoding in other frameworks)
  - OpenAI-compatible API
  - Continuous batching
  - Designed for multi-call LLM programs (not just single request/response)
- **Limitations:** Newer, smaller community than vLLM; less battle-tested at scale
- **Recommended when:** Agent architectures with repeated system prompts and structured outputs; complex multi-turn programs; when prefix reuse is critical to your workload

### Ollama

- **Best at:** Local development, personal use, experimentation
- **Not for:** Production serving of multi-user applications
- **Features:** Clean CLI and API; automatic model download; quantized model support; local OpenAI-compatible API
- **Why not production:** Single-user, no serious batching, no horizontal scaling, not optimized for throughput

### Framework Selection Guide

| Use case | Recommended | Reasoning |
|----------|-------------|-----------|
| Self-hosted multi-user serving | vLLM | Best throughput/feature balance |
| Quick containerized deployment | TGI | Docker-first; HuggingFace integration |
| Enterprise, NVIDIA hardware | Triton + TensorRT | Max performance on NVIDIA; enterprise features |
| Agent workloads, structured outputs | SGLang | RadixAttention; structured output efficiency |
| Local dev / experimentation | Ollama | Best DX for local use |
| Managed inference (no infra) | Provider API | Anthropic, OpenAI, Together AI, Groq |
| High-volume batch jobs (cost-sensitive) | vLLM on spot instances | Self-hosted; Together AI or Groq for managed |

---

## 7. Parallelism Strategies

Single GPU too slow? Model doesn't fit? The answer is parallelism — spreading work across multiple GPUs. There are four distinct strategies, each solving a different constraint.

### Tensor Parallelism

**What it does:** Splits individual weight matrices across GPUs. Each GPU holds a column-slice (or row-slice) of each weight matrix. Every forward pass, each GPU computes on its slice, then an all-reduce operation combines results.

**Example:** A weight matrix of shape [4096, 16384] split across 4 GPUs → each GPU holds [4096, 4096]. All 4 GPUs process every layer in parallel, then sync after each layer.

**Communication requirement:** Frequent all-reduce operations between every layer. Requires high-bandwidth interconnect — NVLink (within-node GPU interconnect) provides 600 GB/s+ bandwidth. Ethernet or PCIe is too slow.

**Best for:** Single large models that don't fit on one GPU; within-node (same physical machine) setups where NVLink is available.

**Practical limit:** Typically 8 GPUs on one node (8× A100 is a standard setup). Beyond that, you hit diminishing returns as communication overhead grows.

### Pipeline Parallelism

**What it does:** Splits the model by layers. GPU 1 handles layers 1-20, GPU 2 handles layers 21-40, etc. Data flows sequentially through GPUs in a pipeline.

**Example:** Llama 3 70B has 80 transformer layers. Across 4 GPUs: GPU 1 (layers 1-20) → GPU 2 (layers 21-40) → GPU 3 (layers 41-60) → GPU 4 (layers 61-80).

**Communication requirement:** Low — only activations at layer boundaries need to transfer between GPUs. Works over lower-bandwidth connections (ethernet between nodes).

**Limitation — pipeline bubbles:** Between micro-batches, some GPUs sit idle waiting for data from the upstream GPU. Efficiency degrades with small batch sizes. With large batches and micro-batch pipelining (GPipe schedule), you can reduce bubble size to ~1/n_stages.

**Best for:** Very large models spread across multiple nodes; inter-node parallelism where NVLink isn't available.

### Data Parallelism

**What it does:** Run complete copies of the model across GPUs; each GPU processes a different subset of the batch. Gradients are aggregated (during training) or outputs collected (during inference).

**At inference time:** Multiple replicas of the same model serve different requests. A load balancer distributes requests across replicas.

**Best for:** High-throughput batch processing where you want to process many requests in parallel; horizontal scaling of serving infrastructure.

**Limitation:** Each GPU must hold the complete model. Only works when the model fits on a single GPU (or within a single node with tensor parallelism).

### Expert Parallelism (MoE Models)

**What it does:** For Mixture-of-Experts models (Mixtral 8×7B, DeepSeek-V2, GPT-4 reportedly), different "expert" layers live on different GPUs. The routing network sends each token to a subset of experts (e.g., top-2 of 8), and those experts may live on different GPUs.

**Why it matters:** MoE models have large total parameter counts but small "active" parameter counts per token. Mixtral 8×7B has 56B total parameters but only activates ~14B per token. With expert parallelism, you can serve a 56B parameter model with the per-token compute cost of a 14B model.

**Best for:** Serving MoE architectures; DeepSeek V2/V3 and similar models benefit heavily from this.

### Combining Strategies

In practice, large-scale serving uses combinations:

- **Tensor parallelism within a node** (NVLink-connected GPUs): splits matrices across the 8 GPUs in one server
- **Pipeline parallelism across nodes** (InfiniBand or ethernet): chains multiple servers
- **Data parallelism across clusters**: multiple copies of the (tensor+pipeline parallelized) model for horizontal scale

For a 405B model: 4× tensor parallelism within each 8-GPU node, 2× pipeline parallelism across 2 nodes = 8 GPUs total per model replica, then data parallelism across replica count for throughput.

### Decision Guide

| Constraint | Strategy |
|-----------|---------|
| Model fits on 1 GPU; want more throughput | Data parallelism (more replicas) |
| Model doesn't fit on 1 GPU (same node) | Tensor parallelism |
| Model doesn't fit across 1 node | Pipeline parallelism (cross-node) |
| Model is MoE architecture | Expert parallelism |
| Need max scale | Combine: tensor within node + pipeline across nodes + data for throughput |

---

## 8. Flash Attention

### The Standard Attention Memory Problem

The transformer attention mechanism computes Q, K, V matrices and then the attention matrix as softmax(QK^T / sqrt(d_k)) × V. The intermediate result QK^T is a matrix of size [sequence_length × sequence_length]. For a sequence of 8,192 tokens, this is 8,192² = 67 million values. At FP16, that's ~134MB per attention head per layer, materialized in GPU High Bandwidth Memory (HBM).

Standard attention is O(n²) in memory. For long sequences (32K, 64K, 128K tokens), this is prohibitive — the attention matrices alone would exhaust VRAM.

Beyond memory: reading and writing this large matrix from/to HBM is slow. HBM bandwidth is fast (~2 TB/s on H100) but not infinite; repeatedly moving 134MB matrices for every attention head for every layer dominates runtime.

### Flash Attention: IO-Aware Attention

Flash Attention (Dao et al., 2022) reorders the attention computation to be "IO-aware" — it processes attention in tiles that fit in the GPU's on-chip SRAM (which is small but extremely fast: 20-50 MB, ~80 TB/s bandwidth), never materializing the full attention matrix in slow HBM.

The technique: compute softmax in a numerically stable way across tiles, accumulating results as you go. The full attention output is computed correctly without ever writing the full n×n matrix to HBM. This is a mathematical rearrangement of the same computation — the result is bit-for-bit identical to standard attention.

Impact:
- Memory: O(n) instead of O(n²) — enables very long sequences
- Speed: 3–7× faster than standard attention on A100 (less HBM traffic)
- Enables contexts that were previously infeasible (128K+ tokens)

**Flash Attention 2 (2023):** Additional parallelization across sequence length dimension; better work partitioning; now the standard in all serious frameworks.

**Flash Attention 3 (2024):** Exploits H100-specific features: FP8 support, asynchronous memory operations, tensor core overlapping. 1.5–2× improvement over FA2 specifically on H100 GPUs.

### Practitioner Notes

You almost certainly don't implement Flash Attention yourself. It's a CUDA kernel — extremely complex low-level code. What you do:

1. Ensure your serving framework has it enabled (vLLM and TGI both use FA2 by default)
2. Verify your GPU is supported (FA3 requires H100; FA2 requires A100 or newer; older V100s have limited support)
3. When comparing frameworks or benchmarks, check whether FA2 is enabled — benchmarks without FA2 are not representative of production performance

The practical checklist: run `vllm serve --flash-attn` (or check that flash_attn is installed and recognized). If it's not running, you're leaving significant performance on the table for any sequence longer than a few hundred tokens.

---

## 9. Production Optimization Workflow

A practical sequence for taking a model from "it runs" to "it's production-ready." Don't skip to step 6; the order matters because each step informs the next.

### Step 1: Profile First

Before optimizing anything, establish a baseline with measurements:
- What is your baseline TTFT at p50 and p99?
- What is your TPOT?
- What is GPU utilization (nvidia-smi; should show compute utilization, not just memory)?
- What is your throughput in tokens/second at your expected concurrent request count?
- What does your request length distribution look like? (p50, p95 prompt length; p50, p95 completion length)

Without this baseline, you cannot tell if your optimizations are working. Every subsequent step should be validated against this baseline.

Tools: `vllm bench`, `locust` for load testing, `nvidia-smi dmon` for GPU metrics, built-in logging in vLLM.

### Step 2: Choose Your Serving Framework

Based on the framework selection guide above. The typical default: vLLM. If you're doing agent workloads with many shared system prompts: SGLang.

### Step 3: Enable Flash Attention

Should be on by default in vLLM and TGI. Verify it's actually running — check startup logs for confirmation. If using a custom or older framework, this may require explicit configuration.

Impact: especially significant for sequences >1,000 tokens. If your use case has long contexts and this wasn't enabled, you may see 3-5× latency improvement from this step alone.

### Step 4: Configure Quantization

Start with INT8 unless you have a specific reason not to. Near-zero quality degradation, halves VRAM usage.

If VRAM is still the constraint after INT8, evaluate INT4 (GPTQ or AWQ):
1. Obtain or generate a quantized model (AutoGPTQ or AutoAWQ libraries)
2. Run quality benchmarks on a sample of your actual prompts/expected outputs — not generic benchmarks like MMLU, which may not predict quality on your specific task
3. Compare to your INT8 or BF16 baseline; if degradation is acceptable, proceed

Don't over-quantize. If INT8 fits in VRAM comfortably and leaves room for your expected KV cache size, there's no reason to use INT4.

### Step 5: Set Batch Size

The right batch size is not "as large as possible." The tradeoff:
- Too small: GPU underutilized; low throughput; wasted capacity
- Too large: OOM from KV cache; high latency; requests queue up waiting for GPU slots

Approach: benchmark throughput at batch sizes of 8, 16, 32, 64, 128 (or whatever your VRAM allows). Plot throughput (tokens/second) vs. latency (TPOT p95). The inflection point — where throughput stops increasing significantly but latency starts climbing — is your working batch size.

In vLLM: `--max-num-seqs` controls the maximum concurrent sequences; `--max-num-batched-tokens` controls the token budget per step.

### Step 6: Enable Prefix Caching

If your system prompt is longer than ~100 tokens and is consistent across requests (it almost always is), prefix caching gives you free throughput improvement.

In vLLM: `--enable-prefix-caching`

Measure TTFT before and after on requests that share the prefix. You should see significant reduction. On long system prompts (1,000+ tokens), TTFT improvement can be 50%+ for cached requests.

If using Anthropic's API, enable prompt caching by marking your system prompt with the `cache_control` header. The economics: first request pays full input token price; subsequent requests within 5 minutes pay ~10% of that price.

### Step 7: Configure Tensor Parallelism

If the model doesn't fit on a single GPU at your chosen quantization level:
- `--tensor-parallel-size N` in vLLM, where N is the number of GPUs to split across
- Must be within a single node (NVLink) for acceptable performance
- Powers of 2 work best: 2, 4, 8

If the model doesn't fit across a single 8-GPU node, add pipeline parallelism (`--pipeline-parallel-size N`). This is uncommon except for very large models (70B+ at FP16 or INT8, 405B at any precision).

### Step 8: Add Speculative Decoding (If Latency Is the Constraint)

Only worth doing if:
- Your primary concern is latency (TPOT specifically), not throughput
- You have a compatible draft model available (same tokenizer, substantially smaller)
- Your workload generates predictable outputs (code, templates, structured data)

In vLLM: `--speculative-model <draft_model_name> --num-speculative-tokens 5`

Benchmark TPOT p50 and p95 before and after on your actual workload. If speedup is <1.3×, the draft model isn't well-matched to your workload. If >2×, this is likely a significant improvement worth the operational complexity.

### Step 9: Continuous Profiling

Production traffic differs from benchmarks:
- Prompt length distribution changes with feature launches
- Concurrent request volume varies throughout the day
- Model updates may change output length distribution

Keep monitoring:
- TTFT, TPOT at p50/p95 in production (not just benchmarks)
- GPU utilization (target: >80%; if <60%, something is wrong)
- Queue depth (if requests queue consistently, you need more capacity or a smaller model)
- Memory pressure (OOM errors indicate batch size or sequence length limits need adjustment)

Set up automated alerts on p99 latency and GPU OOM events.

---

## 10. Cost Mental Model

### The Two Cost Regimes

**Provider API (Anthropic, OpenAI, Together AI, Groq):**
- Pay per token (input tokens cheaper than output tokens)
- No infrastructure to manage
- Variable cost: $0 at zero usage, scales linearly with usage
- Fixed overhead: low (just API keys and integration code)
- Pros: zero upfront cost, no ops burden, automatic scaling
- Cons: at high volume, token prices add up fast; limited control over model/performance

**Self-hosted (vLLM on cloud GPUs or on-prem):**
- Pay for GPU compute (by the hour, whether or not you're generating tokens)
- High fixed cost (GPU instances are expensive)
- Low marginal cost per token (you're paying for the GPU regardless)
- Pros: cost-efficient at high volume; control over model, performance, data privacy
- Cons: significant ops burden; requires inference engineering expertise; cold start problem for variable traffic

### Break-Even Analysis

The break-even point: when does self-hosting become cheaper than provider API?

Rough calculation framework:

**Provider API cost/month** = (input_tokens/month × input_price) + (output_tokens/month × output_price)

**Self-hosting cost/month** = GPU_instance_cost/month + engineering_hours/month × engineer_hourly_cost + storage + networking

For a rough rule of thumb with GPT-4-class models (as of 2025 pricing):
- An A100 80GB instance runs ~$3-5/hour → ~$2,200-3,600/month for one GPU
- One A100 serving Llama 3 70B INT4 might generate 50-100K tokens/minute at peak
- At average 50% utilization: 50K tokens/min × 60 min × 24h × 30d × 0.5 ≈ 1 billion tokens/month per GPU
- GPT-4-class output tokens at $15/M = $15,000/month for 1B tokens at provider API
- GPU cost: ~$3,600/month

**At >10M tokens/day consistently, self-hosting vLLM usually beats provider API cost.** Below that threshold, provider API wins on total cost of ownership once you factor in engineering time.

The threshold shifts depending on:
- Which model (Llama 3 8B is much cheaper to host than 70B; Claude is expensive at API)
- How efficient your serving is (bad serving = higher effective cost per token)
- GPU type and cost (H100 is faster but more expensive per hour)
- Traffic pattern (steady-state vs. spiky — spot instances can reduce cost for batch workloads)

### VRAM Requirements Table

Weights only — add KV cache on top of this:

| Model | BF16/FP16 | INT8 | INT4 |
|-------|-----------|------|------|
| 7B | 14GB | 7GB | 4GB |
| 13B | 26GB | 13GB | 7GB |
| 34B | 68GB | 34GB | 17GB |
| 70B | 140GB | 70GB | 35GB |
| 405B | ~810GB | ~405GB | ~200GB |

What you actually need = weights + KV cache + overhead (typically 10-15% of total VRAM).

At BF16: 70B fits on 2× H100 80GB with room for KV cache. At INT4: fits on a single H100 80GB.

At INT4: Llama 3 7B fits on a single 3090 consumer GPU (24GB). This is why INT4 quantization enabled the consumer-local-model ecosystem (llama.cpp, Ollama).

### GPU Reference (2024-2025)

| GPU | VRAM | HBM Bandwidth | Use case |
|-----|------|---------------|----------|
| RTX 3090/4090 | 24GB | 936 GB/s | Local dev, small model inference |
| A10G | 24GB | 600 GB/s | Cloud inference, cost-optimized |
| A100 40GB | 40GB | 1,555 GB/s | Mid-scale serving |
| A100 80GB | 80GB | 2,000 GB/s | Standard production serving |
| H100 80GB | 80GB | 3,350 GB/s | High-performance production |
| H200 141GB | 141GB | 4,800 GB/s | Large model serving without quantization |

The H100 is ~1.7× the memory bandwidth of the A100 at similar VRAM capacity. For memory-bandwidth-bound inference (which most LLM serving is), H100 delivers ~1.5-2× throughput improvement over A100, justifying its higher cost at scale.

---

## 11. The Architectural Horizon — Beyond Token-by-Token

Everything covered in this document assumes the standard transformer + discrete token paradigm. All current production LLMs operate this way. But the field is actively exploring architectural alternatives that attack the same bottlenecks from a more fundamental level.

This section is a monitoring snapshot — not techniques to use today, but what to understand and watch.

### Why Token-by-Token Is the Core Bottleneck

Every optimization in this document — speculative decoding, continuous batching, Flash Attention — is a workaround for a single constraint: **autoregressive generation is inherently sequential**. Token N depends on token N-1. You cannot parallelize across output length. No matter how well you engineer the serving stack, a 1000-token response requires 1000 sequential forward passes.

This is why inference latency scales linearly with output length. It's a property of the architecture, not the implementation.

### Speculative Decoding vs. Architectural Solutions

The techniques in this document are **implementation-level optimizations** — they make the current architecture faster without changing its fundamental nature.

Architectural alternatives try to change the nature itself:

| Approach | How it reduces steps | Current status |
|----------|----------------------|----------------|
| Speculative decoding | Draft model predicts K tokens; target verifies in 1 pass | Production-ready, 2-3× speedup |
| Multi-token prediction | Model predicts multiple tokens per step via additional heads | Meta research (2024), early production |
| **Continuous latent space (CALM)** | Predict a compressed vector representing K tokens per step | Research, 1.82B params max, unproven at scale |
| SSM/Mamba | Replace attention with linear-scaling state space model | Early production in hybrid form |
| Byte-level models | Process bytes not tokens; hierarchical compression eliminates vocabulary bottleneck | Research, competitive at ~7B |

### Continuous Latent Space (CALM) — The Token vs. Vector Trade

The most radical near-term research direction: instead of predicting which discrete token comes next (choosing from a vocabulary of 32,000+ options), predict a **continuous vector** that represents an entire chunk of K tokens.

**How it works:**
1. An autoencoder is trained to compress K tokens → 1 continuous vector (128 floating-point numbers), then reconstruct the original tokens back from that vector
2. A language model is trained to predict sequences of these vectors — not token probabilities
3. At generation: predict vector → decode via autoencoder → get K tokens. K× fewer autoregressive steps.

**What "continuous" means:** discrete tokens are like piano keys — fixed positions, 32K options. A continuous vector is a point in 128-dimensional space — infinite possible values, no fixed vocabulary. Similar chunks (4 tokens that share 3 words) end up as nearby points in this space naturally, because the encoder processes shared structure identically.

**The genuine open questions:**
- Single-token swaps that change meaning entirely ("sat **down**" vs. "sat **alone**") require the vector space to encode fine-grained distinctions at scale. This works at K=4 but degrades at higher K.
- Energy-based training (required because standard cross-entropy doesn't apply to continuous space) is harder to scale than standard LM training. Infrastructure is immature.
- All results use a custom metric (BrierLM) not comparable to MMLU, HumanEval, or other standard benchmarks. Real-task quality is uncharacterized.
- Largest model tested: 1.82B parameters (DeepSeek researcher, 2025 arXiv). Production LLMs are 70B-700B+.

**The honest assessment:** Directionally interesting, genuinely novel in its training approach, but the path from 1.82B-parameter research to production is long. The efficiency gains are theoretical until demonstrated at scale with real hardware benchmarks.

### SSMs / Mamba — The Attention Alternative

Standard attention is O(n²) — every token attends to every other token. Flash Attention reduces the memory cost but not the compute complexity. State space models (SSMs) achieve O(n) linear scaling by maintaining a fixed-size hidden state that compresses history, rather than attending to all past tokens.

**Mamba (2023)** is the most prominent SSM — input-dependent state transitions (unlike earlier fixed-transition SSMs) give it flexibility comparable to attention on most tasks. The limitation: can't precisely retrieve specific information from far back in context (transformers do this trivially with attention; Mamba must have compressed that information into its fixed-size state).

**The practical bet is hybrids:** Jamba (AI21 Labs, 2024) alternates Mamba layers with attention layers. Most of the sequence gets linear-scaling Mamba processing; occasional attention layers handle precise retrieval. This is likely the near-term production architecture for long-context applications where KV cache cost is prohibitive.

### What to Watch

- **Benchmark results at 7B+** on standard tasks (MMLU, HumanEval, GSM8K) for CALM and similar continuous-space models — small-scale results frequently don't transfer
- **Hybrid SSM/Transformer** adoption in production serving stacks — this is the most likely near-term architectural shift
- **Byte Latent Transformer (BLT, Meta 2024)** scaling — byte-level models that eliminate tokenization are competitive at 7B; whether this holds at 70B+ is the open question
- **Wall-clock speedup benchmarks** for any architecture claiming K× efficiency gains — theoretical step reduction ≠ actual latency reduction when per-step compute increases

For the full landscape: see `LEARNING/FOUNDATIONS/emerging-architectures/emerging-architectures.md`

---

## Quick Reference: Technique Selection

| Problem | Technique | Expected gain |
|---------|-----------|--------------|
| Model doesn't fit in VRAM | INT4 quantization (GPTQ/AWQ) | 4× VRAM reduction |
| Minimal quality risk quantization | INT8 PTQ | 2× VRAM reduction, <1% quality loss |
| Latency too high (TPOT) | Speculative decoding | 2–3× TPOT improvement |
| GPU underutilized | Continuous batching (use vLLM/TGI) | 5–30× throughput improvement |
| KV cache running out at long contexts | GQA model + prefix caching | 4–8× KV cache reduction |
| Repeated long system prompts slowing TTFT | Prefix caching | 50%+ TTFT reduction for cached requests |
| Standard attention too slow/memory-heavy | Flash Attention 2 (framework default) | 3–7× attention speedup |
| Multi-GPU required | Tensor parallelism (same node) | Linear with GPU count |
| Model spread across nodes | Pipeline parallelism | Linear with node count |
| Agent workloads with shared prefixes | SGLang + RadixAttention | Better than vLLM prefix cache for dynamic patterns |

---

*Last updated: 2026-03-22. Sources: vLLM paper (Kwon et al., 2023), Flash Attention (Dao et al., 2022, 2023, 2024), AWQ (Lin et al., 2023), GPTQ (Frantar et al., 2022), Medusa (Cai et al., 2024), SGLang (Zheng et al., 2024).*
