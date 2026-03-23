# Multimodal AI — Practitioner Reference

**Scope:** Vision-language models, document understanding, multimodal RAG, audio/speech, video, agentic vision, evaluation, and practical build decisions. Designed for technical PMs making architecture and product decisions.

---

## Table of Contents

1. [What "Multimodal" Actually Means](#1-what-multimodal-actually-means)
2. [Vision-Language Models — Architecture Deep Dive](#2-vision-language-models--architecture-deep-dive)
3. [Major VLM Architectures](#3-major-vlm-architectures)
4. [Document Understanding](#4-document-understanding)
5. [Multimodal RAG](#5-multimodal-rag)
6. [Audio and Speech](#6-audio-and-speech)
7. [Video Understanding](#7-video-understanding)
8. [Multimodal in Agentic Systems](#8-multimodal-in-agentic-systems)
9. [Evaluation and Benchmarks](#9-evaluation-and-benchmarks)
10. [Building Multimodal Applications — Practical Guide](#10-building-multimodal-applications--practical-guide)

---

## 1. What "Multimodal" Actually Means

A **multimodal model** processes and reasons across more than one type of input signal. The word gets applied loosely, so it helps to be precise about what modalities are actually in play.

### The Modality Landscape

| Modality | What it is | Examples |
|---|---|---|
| Text | Token sequences | Natural language, code, markdown |
| Images | Pixel grids (raster) | Photos, screenshots, diagrams, charts |
| Audio | Waveform / spectrogram | Speech, music, ambient sound |
| Video | Temporal image sequences + optional audio | Recordings, screen captures |
| Code | Structured text with formal grammar | Python, SQL, HTML |
| Structured data | Tables, JSON, DataFrames | CSVs, database schemas |
| Documents | Mixed layout content | PDFs, invoices, forms, slides |

"Multimodal" in practice almost always means **vision-language** (image + text), because that's where the most capable commercial systems are. Audio-native LLMs are newer and less mature. True video understanding (temporal reasoning, not just frame sampling) is still an active frontier.

### Two Fusion Architectures

**Early fusion:** All modalities are processed together from the beginning. The model sees a unified token stream that mixes text tokens and visual tokens before any deep reasoning. Advantage: the model can learn cross-modal dependencies at every layer. Disadvantage: expensive to train from scratch; requires large paired datasets for all modality combinations.

**Late fusion:** Each modality is processed independently by a specialized encoder, then the outputs are combined at a later stage (often just before generation). Advantage: you can reuse powerful pre-trained encoders; easier to add new modalities. Disadvantage: the model can't learn fine-grained cross-modal interactions at early layers.

Most production VLMs today use a **late fusion** variant: a frozen (or lightly fine-tuned) vision encoder + a projection layer + a language model. Gemini is a notable exception — it uses a more integrated architecture.

### The Core Insight: Images as Token-Like Representations

VLMs do not "see" the way humans do. There is no holistic scene understanding or gestalt perception. What happens is:

1. An image is divided into a grid of **patches** (typically 14×14 or 16×16 pixel patches)
2. Each patch is encoded into a fixed-size vector by the vision encoder
3. These vectors are projected into the **same embedding space as text tokens**
4. The language model's attention mechanism processes the visual vectors and text tokens **identically** — it sees them all as just tokens with positions

The LM doesn't know a token came from a patch vs. a word. It just attends across all of them. This is why describing image content in text is so powerful — it's literally putting information into the same representational space the model reasons in.

This also explains the characteristic failure modes: VLMs are bad at precise spatial reasoning (left/right confusion, exact counting) because those require operations the attention mechanism doesn't naturally perform, and because patch-level representations lose the continuous spatial structure of the original image.

---

## 2. Vision-Language Models — Architecture Deep Dive

Every VLM has three core components. Understanding each one lets you reason about tradeoffs in capability, cost, and customizability.

### Component 1: Vision Encoder

The vision encoder converts raw pixel data into a compact vector representation. It is almost universally based on a **Vision Transformer (ViT)** architecture.

**How ViT works:**
1. Image is divided into non-overlapping patches (e.g., 16×16 pixels each)
2. Each patch is flattened into a vector and linearly projected
3. A learned position embedding is added so the model knows where each patch is
4. The sequence of patch embeddings is processed by transformer encoder layers
5. The output is a sequence of vectors — one per patch — representing visual features

For a 224×224 image with 16×16 patches: (224/16)² = 196 patches → 196 output vectors.
For a 336×336 image with 14×14 patches: (336/14)² = ~576 patches.

**Common vision encoders used in production:**

- **CLIP ViT-L/14 (OpenAI):** The most widely reused backbone. 307M parameters. Trained on 400M image-text pairs via contrastive loss. Used in LLaVA, Stable Diffusion, and many others. Output: 1024-dim vectors.
- **DINOv2 (Meta, 2023):** Self-supervised ViT trained without text labels; produces dense local features that are better for fine-grained spatial tasks than CLIP. Used in some specialized VLMs and robotics.
- **SigLIP (Google, 2023):** Sigmoid loss variant of contrastive training; more stable and scales better than CLIP's softmax loss. Used in PaliGemma and Gemini.
- **InternViT (Shanghai AI Lab):** Used in InternVL; trained at higher resolution natively.

The vision encoder is typically **frozen** during VLM training because it is expensive to fine-tune and its representations are already strong. The projection layer and LM backbone do most of the adaptation.

### Component 2: Projection Layer (Connector)

The vision encoder outputs vectors in its own embedding space (e.g., 1024-dim for CLIP ViT-L). The language model has its own embedding space (e.g., 4096-dim for LLaMA-7B). These don't match. The projection layer bridges them.

**Linear projection (LLaVA approach):**
- A single learned matrix W that maps from vision encoder dim → LM embedding dim
- Applied independently to each patch vector
- Extremely simple; adds almost no parameters or compute
- LLaVA's original result showed this is surprisingly effective — the quality bottleneck is training data, not connector complexity

**MLP projection (LLaVA-1.5 and most subsequent work):**
- Two-layer MLP with GELU activation: vision_dim → hidden → LM_dim
- Marginally better than linear; still fast at inference

**Q-Former (BLIP-2):**
- A small Transformer with a fixed set of learned query vectors (e.g., 32 queries)
- The queries attend to the full patch sequence from the vision encoder
- Output is 32 fixed-size vectors regardless of image resolution or patch count
- Advantage: constant-size visual representation; the LM sees exactly 32 visual tokens
- Disadvantage: lossy — 32 queries can't capture everything in a detailed image; more compute overhead than linear projection

The key practical insight: **connector complexity matters less than training data quality.** LLaVA-1.5 with a simple MLP outperforms architecturally more complex models trained on weaker data.

### Component 3: Language Model Backbone

After projection, visual patch vectors and text tokens are concatenated into a single sequence. The LM processes this sequence with standard causal attention and generates text output.

The input format is typically: `[system prompt tokens] [visual tokens from image 1] [text tokens] [visual tokens from image 2] [text tokens] ...`

The LM doesn't need any modification to its architecture. It processes visual tokens identically to text tokens. This is the key insight that made VLMs tractable — existing LLMs can be made multimodal without architectural surgery, just by prepending projected visual tokens.

**Why this works:** Cross-modal attention happens naturally through self-attention. A text token asking "what color is the car?" will attend to the patch tokens that represent the car region, because those patches produce activations that are relevant to the query after the projection aligns them.

### Resolution Tradeoff

Higher resolution preserves more detail but creates more patches, which costs more context window tokens. This creates a direct tradeoff:

| Resolution | Patches (16px patch) | Approx. token cost |
|---|---|---|
| 224×224 | 196 | ~200 tokens |
| 336×336 | 441 | ~450 tokens |
| 672×672 | 1,764 | ~1,800 tokens |
| 1024×1024 | 4,096 | ~4,100 tokens |

**High-resolution approaches — image tiling:**

Rather than upscaling and sending one huge image, modern systems split images into tiles:
- The image is divided into overlapping or non-overlapping crops (e.g., 336×336 tiles)
- Each tile is independently encoded by the vision encoder
- A thumbnail of the full image is also encoded to preserve global context
- All tile representations are concatenated before the LM

GPT-4V uses this approach. Claude 3+ uses a similar tile-based method. This lets the model read small text in images, count objects precisely, and understand detailed charts — all of which require higher effective resolution.

At "high detail" mode in Claude, a 1024×1024 image uses approximately 1,700 tokens. At "low detail" (single pass, resized to 512×512): ~65 tokens. The decision is consequential for cost at scale.

### Training Paradigm

VLM training typically proceeds in stages:

**Stage 1 — Projection alignment:**
- Freeze vision encoder and LM backbone
- Train only the projection layer on a large image-caption dataset (e.g., LAION, CC12M)
- Goal: teach the projection to map visual features into a space the LM can interpret
- Typically millions of image-text pairs; fast because only the connector is updated

**Stage 2 — Visual instruction tuning:**
- Unfreeze the LM backbone (or train with LoRA)
- Keep vision encoder frozen
- Fine-tune on instruction-following data: image + question → answer format
- LLaVA-Instruct, ShareGPT4V, and similar datasets are common sources
- This is where the model learns to follow user instructions about images

**Stage 3 (optional) — Full fine-tuning:**
- Unfreeze the vision encoder too
- Expensive; often not necessary unless you have a very domain-specific image distribution
- Some models fine-tune the vision encoder end-to-end for medical imaging, satellite imagery, etc.

---

## 3. Major VLM Architectures

### CLIP (OpenAI, 2021)

CLIP (Contrastive Language-Image Pretraining) is not a complete VLM — it is the **vision encoder** that almost every VLM uses.

**Training objective:** Contrastive learning on 400M web-scraped image-text pairs. For a batch of N image-text pairs, CLIP trains two encoders (image encoder + text encoder) such that the N matched pairs have high cosine similarity and the N²-N unmatched pairs have low similarity. This is the InfoNCE loss.

**Architecture:** ViT image encoder + Transformer text encoder, both producing 512-dim embeddings by default (larger variants produce 1024-dim).

**Zero-shot classification:** Given a set of class names, convert each to text ("a photo of a [class]"), embed with the text encoder, embed the query image with the image encoder, find the nearest neighbor by cosine similarity. No per-class training data needed. CLIP achieves 76.2% zero-shot accuracy on ImageNet with ViT-L/14.

**Why it matters:** CLIP's image encoder is the default visual backbone for downstream VLMs. Its embedding space is rich, general-purpose, and aligned with natural language concepts because it was trained on internet image-text pairs. This alignment is what lets projection layers succeed with so little complexity.

**Limitation:** CLIP's image encoder was trained on 224×224 images. At higher resolution it loses some quality without additional training. SigLIP and InternViT address this.

### LLaVA (Large Language and Vision Assistant)

**Architecture:** CLIP ViT-L/14 → linear projection → LLaMA or Vicuna

LLaVA's key contribution was showing that this absurdly simple design works. The projection layer is just one learned matrix. The training data was generated using GPT-4 to create instruction-following examples from image captions (visual instruction tuning).

**LLaVA-1.5 (2023):** Upgraded the linear projection to a 2-layer MLP, used CLIP ViT-L/14@336px (higher resolution encoder), and better training data. Outperformed significantly more complex architectures on VQA and MMBench benchmarks. Demonstrated that **training data quality > connector architecture.**

**LLaVA-1.6 / LLaVA-NeXT:** Added image tiling for higher effective resolution, expanded the training data further.

**Key lesson for builders:** If you're fine-tuning a VLM for a specific domain, the quality of your visual instruction data matters far more than which connector you use. Don't over-engineer the adapter.

### BLIP-2

**Architecture:** Frozen EVA-CLIP image encoder → Q-Former → frozen OPT or Flan-T5 LLM

**Q-Former detail:** The Q-Former has 32 learned query tokens that attend (via cross-attention) to the 256 patch representations from the vision encoder. It outputs 32 fixed vectors regardless of image complexity. This is both its strength (predictable compute) and weakness (information bottleneck).

**Two-stage training:**
1. Train Q-Former to align with frozen image encoder via image-text matching, image-text contrastive learning, and image-grounded text generation objectives — no LLM yet
2. Connect the Q-Former output to a frozen LLM via a linear projection; train on visual instruction data

BLIP-2 was important for demonstrating that you can connect large frozen components without end-to-end training. Its Q-Former design influenced InstructBLIP and subsequent systems.

**Practical limitation:** The 32 fixed query tokens create an information bottleneck for high-detail tasks. Document reading, fine-grained chart understanding, and counting are weaker than tile-based approaches.

### GPT-4V and GPT-4o

OpenAI has not disclosed the architecture. Empirical analysis of behavior suggests:

**GPT-4V (2023):** Vision capability added to GPT-4; tile-based high-resolution processing (images are split into 512×512 tiles, each processed independently, plus a thumbnail for global context). Strong at document reading, chart understanding, and complex reasoning about images.

**GPT-4o (2024):** "Omni" — processes text, image, and audio in a single model. Unlike GPT-4V which was text-model-first with vision added, GPT-4o appears to be natively multimodal with modalities integrated during pre-training. This enables lower latency (no separate pipeline handoffs) and better cross-modal reasoning.

GPT-4o's voice mode can detect emotion, tone, and speaking pace — capabilities that are impossible in an ASR-then-text pipeline. This is the concrete advantage of native audio integration.

**Token pricing (GPT-4o, as of early 2025):** High-detail image costs 85 + (170 × number of tiles) tokens. Low-detail: 85 tokens flat.

### Claude's Vision (Claude 3+)

Claude 3 Haiku, Sonnet, and Opus all support image input. Claude claude-sonnet-4-6 (current) supports images strongly.

**Supported formats:** JPEG, PNG, GIF, WebP
**Max image size:** 5MB per image
**Max images per request:** Up to 20 images
**Processing approach:** Tile-based for high resolution; strong at documents, technical diagrams, handwritten text, and multi-image comparison tasks

**Token costs:**
- Low detail: ~65 tokens per image (Anthropic resizes to 512×512)
- High detail: ~1,700 tokens for a 1024×1024 image

Claude 3's vision is particularly strong for:
- Reading text from images (OCR-quality or better for clean documents)
- Chart interpretation with quantitative reasoning
- Multi-image comparison ("how does this diagram differ from the one above?")
- Document understanding with mixed content

**API format:** Images are passed as content blocks alongside text blocks within a message. Each image is either a base64-encoded string with media type, or a URL reference.

### Gemini

**Gemini 1.0 Pro Vision / Ultra (2023):** Native multimodal — Gemini was designed from the start with multiple modalities, not vision added to a text model. Architecture details are not public, but training incorporated images, video, audio, and text together.

**Gemini 1.5 Pro (2024):** 1M+ token context window (2M in some variants). Video frames, images, and text all fit in the same long context. Key capability: process an entire 1-hour video (approximately 100K tokens at standard frame sampling) within a single context window. This is qualitatively different from GPT-4V's approach and makes long-form video understanding tractable.

**Gemini 2.0 Flash / 2.5 Pro:** Further improvements; Gemini 2.5 Pro achieves top-tier scores across multimodal benchmarks while maintaining long context. Also supports native audio output (not just audio input).

**Why native multimodal matters:** Models trained with all modalities together from the beginning can learn representations that truly integrate across modalities — a concept can be represented by its visual and textual features simultaneously. Adapter-based models are always bridging two separately learned spaces.

---

## 4. Document Understanding

Document understanding is distinct from general image understanding because documents have:

1. **Layout:** Spatial positioning carries meaning (header vs. body vs. footnote; column structure in tables)
2. **Mixed content:** Text, tables, charts, images, and stamps can all appear on the same page
3. **Structured extraction requirements:** Often you need specific fields, not a free-form description
4. **Scale:** A single contract can be 50 pages; financial reports are often 100+

### The Four Approaches

**1. OCR-then-LLM pipeline**

Process: Run an OCR engine over each page → feed extracted text to an LLM for reasoning or extraction.

- **Tools:** Tesseract (open source), AWS Textract, Google Cloud Vision API, Azure Document Intelligence, PaddleOCR
- **Cost:** OCR is cheap; LLM inference on text is much cheaper than on images
- **What you lose:** Table structure (OCR often linearizes tables incorrectly), chart content (rendered as alt text at best), visual layout (which column a value belongs to)
- **When to use:** Text-heavy documents with simple formatting — email threads, articles, plain contracts. If the document is basically text with some formatting, OCR + LLM is cheaper and reliable

**2. Vision-native document understanding**

Process: Send page images directly to a VLM; prompt it to extract, summarize, or answer questions.

- **Tools:** GPT-4V/o, Claude claude-sonnet-4-6, Gemini 1.5 Pro, specialized models like Qwen-VL, InternVL
- **Cost:** 10-30× more expensive per page than OCR + LLM due to image token cost
- **What you gain:** Preserves layout; correctly reads complex tables; understands charts; handles stamps, signatures, and mixed content
- **When to use:** Documents where layout matters — invoices (column alignment), financial tables, forms with checkboxes, research papers with complex figures

**3. Hybrid approach**

Process: Run OCR for the text layer; use VLM only for regions identified as charts, tables, or figures; combine in a final extraction step.

- Most cost-effective for high-volume production systems
- Requires a region classifier to route content appropriately
- More engineering complexity but 3-5× cheaper than pure vision-native on mixed documents

**4. Specialized document AI models**

Purpose-built for document understanding, not general VLMs:

- **Microsoft Document AI (Azure):** Pre-trained on millions of invoices, receipts, and forms; strong structured extraction for known document types with minimal prompting
- **AWS Textract:** Table extraction, form field detection, query-based extraction (ask "what is the invoice total?"); strong structured output for standard form types
- **Unstructured.io:** Open-source document preprocessing library; handles partitioning of complex documents into elements (title, narrative text, table, figure)

Use specialized tools when your document type is common (invoices, receipts, forms, W-2s) and the specialized model is trained for it. Use general VLMs when document types are varied, novel, or require reasoning beyond extraction.

### Production Decision Framework

| Document type | Recommendation | Rationale |
|---|---|---|
| Plain text contracts | OCR + LLM | Cheap; layout doesn't matter |
| Standard invoices at volume | AWS Textract / Azure Form Recognizer | Pre-trained; fast; cheap |
| Complex financial tables | VLM (Claude/GPT-4o) | Layout critical; VLM reads column structure |
| Research papers with figures | Hybrid | OCR body text; VLM for figures/charts |
| Mixed, novel document types | VLM + structured prompting | Can't pre-train on unknown types |

**Build your own benchmark.** Don't pick an approach based on generic demos. Collect 50-100 real examples from your actual document types, define your extraction targets, run all candidate approaches, and measure accuracy. The cost/quality tradeoff is different for every document distribution.

---

## 5. Multimodal RAG

Standard RAG pipelines are blind to visual content. A quarterly report's most important data is often in a chart or table image embedded in a PDF. Text-only embeddings of the surrounding caption miss almost all of the signal.

### The Four Retrieval Approaches

**Approach 1 — Text-only multimodal RAG**

Extract all text via OCR (including any text extracted from embedded images), embed with a standard text embedding model (text-embedding-3-large, BGE, etc.), and index normally. Image content is either ignored or represented only by its surrounding caption.

- Easiest to implement; works well when text contains most of the information
- Completely blind to charts, diagrams, and visual tables not accompanied by text description
- Appropriate starting point before you know if visual content matters in your corpus

**Approach 2 — Image embedding via CLIP**

Embed both text chunks and page images using CLIP or SigLIP (which operate in the same embedding space). At query time, embed the query as text, retrieve by cosine similarity against the combined index. Images retrieved by semantic similarity.

- Enables queries like "find the slide with the market share chart" even without text labels
- CLIP's image-text alignment is imperfect for detailed content retrieval; works better for topic-level matching than fine-grained fact retrieval
- Requires storing original images; generates image descriptions at query time using a VLM

**Approach 3 — VLM-generated summaries as retrievable text**

At index time: for each chart, table, figure, or page image, call a VLM to produce a detailed text description ("This bar chart shows quarterly revenue by region from Q1-Q4 2023. North America: $2.1B, $2.3B, $2.4B, $2.5B..."). Store this description in your text index as the searchable representation. Store the original image alongside it.

At query time: retrieve descriptions by standard text search; inject both the text description AND the original image as context to the generation LLM.

- Most reliably retrievable via standard text search
- Quality depends on VLM description quality at index time; descriptions may miss information
- Works well when your VLM can reliably describe your specific visual content types
- Indexing cost is high (VLM call per visual element) but retrieval is cheap

**Approach 4 — ColPali / Late Interaction (2024)**

ColPali (Contextualized Late Interaction over Vision-Language Models for efficient document Retrieval) represents document pages as multi-vector representations — one vector per image patch from a vision encoder (PaliGemma 3B fine-tuned for retrieval).

**How it works:**
1. Each document page image is encoded into N patch-level vectors (one per patch)
2. At query time, the text query is encoded into M token-level vectors
3. Retrieval score: MaxSim(query_token_vectors, page_patch_vectors) — for each query token, find its most similar page patch; sum these max similarities
4. This is "late interaction" — the full interaction score is computed at retrieval time, enabling fine-grained matching

**Why it matters:** ColPali can match a query like "revenue in APAC region" to the specific bar in a chart that represents APAC — not the page-level description but the actual visual region. Standard single-vector retrieval operates at page or chunk level; late interaction operates at patch level.

**Performance:** ColPali achieves state-of-the-art on DocVQA and other document retrieval benchmarks. On pages with dense visual content (charts, tables, diagrams), it significantly outperforms text-only approaches. On text-heavy pages, performance is comparable.

**Practical cost:** ColPali's fine-grained retrieval is more compute-intensive than standard dense retrieval. Best suited for production systems where visual document retrieval quality is critical.

### Recommended Starting Architecture

For most teams building multimodal RAG for the first time:

1. **Index time:** Use a VLM (Claude or GPT-4o) to generate text descriptions of all non-text elements (charts, tables, diagrams). Store descriptions + original images.
2. **Retrieval:** Standard text embedding + vector search across both text chunks and VLM-generated descriptions.
3. **Generation:** Retrieve top-K results; for any result backed by an image, inject both the text description and the original image into the generation context.
4. **Evaluate:** Measure faithfulness and retrieval accuracy on a labeled holdout. If visual retrieval is the bottleneck, upgrade to ColPali.

---

## 6. Audio and Speech

### Automatic Speech Recognition (ASR)

ASR converts spoken audio to text. This is the first step in any voice-powered AI pipeline.

**Whisper (OpenAI, 2022):**

Whisper is the default choice for production ASR. Open-source, no API cost, runs locally.

**Architecture:**
1. Audio waveform is converted to a log-Mel spectrogram (80 frequency bins, 30-second segments)
2. A CNN encoder processes the spectrogram into feature representations
3. A Transformer decoder generates text tokens autoregressively from the encoded features

**Training:** 680K hours of multilingual audio-text pairs scraped from the internet. This scale and diversity (multiple accents, recording conditions, languages) is Whisper's strength. It handles technical vocabulary, accented speech, and noisy audio better than models trained on curated speech corpora.

**Model sizes:**

| Variant | Parameters | VRAM | Speed (RTX 3090) |
|---|---|---|---|
| tiny | 39M | ~1 GB | ~10× realtime |
| base | 74M | ~1 GB | ~7× realtime |
| small | 244M | ~2 GB | ~4× realtime |
| medium | 769M | ~5 GB | ~2× realtime |
| large-v3 | 1.55B | ~10 GB | ~1× realtime |

**Quality:** Whisper large-v3 achieves below 5% Word Error Rate on most standard English benchmarks and below 10% WER in challenging conditions (accented speech, noisy audio). This is at or near human-level performance on clear audio.

**Production optimization — faster-whisper:**

faster-whisper is a CTranslate2-based reimplementation of Whisper. It achieves approximately 3× speedup over the original PyTorch implementation at the same quality level by using efficient CPU/GPU kernels and int8 quantization. For production deployments processing audio at scale, faster-whisper is the standard choice.

**Whisper limitations:**
- Maximum 30-second audio per pass; longer audio requires chunking with overlap
- Hallucination on silence or unintelligible audio (generates plausible-sounding but wrong text)
- Timestamp accuracy degrades on fast speech or overlapping speakers
- No speaker diarization natively (use pyannote-audio alongside Whisper)

**Other ASR options:**
- **Deepgram:** Managed API; low latency (can stream real-time); competitive WER; strong for voice interfaces requiring <300ms response
- **AssemblyAI:** Managed API; strong speaker diarization and sentiment analysis built in
- **Rev.ai:** Human+AI hybrid for high-stakes accuracy requirements
- **Google Speech-to-Text:** Strong for Google ecosystem integration; competitive pricing at scale

### Text-to-Speech (TTS)

Not LLM-native, but relevant for voice product decisions:

- **ElevenLabs:** Best-in-class voice cloning and naturalness; higher latency (~300-500ms first token); most expressive
- **OpenAI TTS:** Six preset voices; good quality; low latency; cheapest managed option at $0.015/1K chars
- **Google Cloud WaveNet:** Strong multilingual support; more robotic than ElevenLabs for complex expressive speech
- **Cartesia:** Low-latency streaming TTS optimized for real-time conversation; sub-100ms first chunk latency

### Audio Language Models — Native Audio Processing

**The key distinction:** Whisper gives you a transcript. It discards all acoustic information — tone, emotion, pace, speaker identity. A native audio model can reason about these properties.

**Practical capabilities of native audio models (Gemini 1.5, GPT-4o audio):**
- Detect emotion in speech ("the speaker sounds frustrated")
- Identify multiple speakers without explicit diarization
- Understand tone-dependent meaning (sarcasm, emphasis, hesitation)
- Respond to acoustic context in ways that transcript-only systems cannot

**Cost and trade-offs:** Native audio models cost significantly more than ASR + text LLM. For most applications, a transcript is sufficient. Use native audio processing only when:
- You need emotion detection or sentiment from voice tone
- Speaker identity matters (who said what, without a separate diarization pipeline)
- You are building real-time voice assistants where latency from pipeline handoffs is a problem
- The content contains meaningful non-verbal audio (music, sound effects alongside speech)

### The ASR-then-LLM Pipeline (Standard Approach)

For most production voice applications:

```
Audio → Whisper (ASR) → Text → LLM → Text response → TTS → Audio
```

This pipeline is:
- Cheap: Whisper is free; text LLM tokens are cheaper than audio tokens
- Debuggable: You can inspect the transcript at each step
- Flexible: Swap any component independently
- Reliable: Whisper's quality is predictable and measurable

The main cost is latency — each handoff adds time. For conversational applications where users hear a response, the pipeline adds ~500-1000ms per turn beyond LLM generation time. Native audio models can reduce this by eliminating handoffs.

---

## 7. Video Understanding

### The Frame Sampling Problem

Video is a sequence of images over time. The naive approach is to treat it as multiple images. The challenge is that most video is redundant — 10 seconds of someone talking is 250 frames at 25fps, but the visual information changes slowly.

**The core decision:** Which frames to process, and how many.

**Uniform sampling:** Select frames at a fixed interval (e.g., 1 frame per second, 1 frame per 10 seconds). Simple; predictable token cost. Misses fast-changing content and doesn't allocate compute to important moments.

**Keyframe extraction:** Select frames with high visual change using perceptual hashing (pHash) or optical flow. A new "scene" (high hash distance from previous frame) gets selected; stable footage is skipped. Better coverage of meaningful moments; variable compute.

**Shot detection:** Identify cut points (transitions between shots) and sample one frame per shot. Works well for produced video; poor for continuous footage without hard cuts.

**Query-guided sampling:** Use the text query to determine which temporal segments are relevant, then sample densely from those. Requires fast initial pass over the video — typically a lightweight model or audio transcript to identify candidate segments, then a VLM for the selected frames.

### Long Video: Gemini 1.5 Pro's Approach

Gemini 1.5 Pro's 1M+ token context window changes the long-video problem fundamentally. Instead of selecting frames, you can send more of them — up to an hour of video at 1fps uses approximately 100K-200K tokens, which fits within Gemini's context.

**What this enables:**
- "What happened in the first 20 minutes that caused the failure at 45:30?" — requires temporal reasoning across the full video
- Contract review by sending all pages as images in one request
- Long lecture understanding without summarization-then-reasoning

**Practical limitation:** 1M tokens at current pricing is expensive. A one-hour video analyzed with Gemini 1.5 Pro can cost $5-20 depending on configuration. For content platforms processing thousands of hours of video, frame sampling and lightweight models remain necessary.

### Video-native vs. Frame Sampling

Current production video AI systems are primarily **frame sampling** systems — they process video as a sequence of images. True video-native understanding would capture:
- Motion (not just keyframes, but the trajectory between them)
- Causality (this action caused that reaction)
- Temporal relationship (this happened before that)

Models like VideoLLaMA, VideoChatGPT, and Video-LLaVA explore video-native training where temporal representations are explicitly modeled. This is an active research area. For production use cases (2025-2026), frame sampling + strong VLM is the pragmatic approach.

### Practical Video Architecture for Production

For most production video understanding tasks:

1. **Extract audio transcript:** Whisper on the audio track gives you temporal anchors and content cues
2. **Sample keyframes:** Use pHash difference to identify meaningful frames (threshold ~10 bits Hamming distance between adjacent frames)
3. **Process frames with VLM:** Pass selected frames + transcript segments to Claude or GPT-4o for reasoning
4. **Temporal grounding:** Use transcript timestamps to link visual frames to time codes

This approach processes a 10-minute video with 20-30 keyframes + transcript for a total of approximately 30K-60K tokens — manageable and cost-effective.

---

## 8. Multimodal in Agentic Systems

### Agents That Act in Visual Environments

Agentic systems extend beyond answering questions to taking actions. In visual environments, this means:

- **Computer use:** The agent receives a screenshot of a desktop or web browser, reasons about the current state, and outputs tool calls that translate to mouse clicks, keyboard input, or scroll events
- **Web browsing:** Combining visual rendering of pages with DOM access; some agents use both, some use only one
- **Robot control:** Sensor inputs (camera, depth, lidar) combined with language reasoning for navigation and manipulation

### Claude's Computer Use (Beta)

Claude's computer use capability (released late 2024, currently beta) is the clearest example of vision-native agentic action.

**The loop:**
1. Take screenshot of current screen state
2. Send screenshot as image input to Claude with the task description
3. Claude reasons about what it sees ("I see a web browser with a form. The email field is empty.")
4. Claude outputs tool calls: `{"type": "mouse_click", "x": 452, "y": 318}` or `{"type": "type", "text": "user@example.com"}`
5. Execute the tool calls; take new screenshot; repeat

**The UI grounding challenge:** The hard part is mapping from abstract reasoning ("click the Submit button") to precise pixel coordinates. VLMs understand layout and UI semantics well but are imprecise about exact coordinates. Production computer use agents often combine:
- VLM for understanding and decision-making ("the Submit button is in the bottom right")
- A separate grounding model (e.g., SeeClick, ScreenAI) trained specifically to map UI descriptions to pixel coordinates

**Practical limitations:**
- Latency: each action requires a screenshot → API call → action cycle; even at 2 seconds per step, 20-step tasks take 40+ seconds
- Error recovery: VLMs need explicit error handling prompts to detect when actions fail
- Security: computer use agents running with user-level permissions are a significant attack surface; never run on systems with access to production credentials

### Vision as Tool Use

Computer use is mechanically identical to ReAct-style tool use — it's just that one of the tool outputs happens to be an image.

```
screenshot() → image → VLM → click(x, y) → screenshot() → image → VLM → type("text") → ...
```

The image is passed as a content block alongside text tool responses in the message sequence. The VLM processes both text tool outputs and image tool outputs using the same attention mechanism. No architectural difference from standard tool use.

This means the agent frameworks you already use (LangGraph, Claude Agent SDK, custom ReAct loops) work for computer use with minimal modification — you just add screenshot capture and input simulation to the tool set.

### Multimodal Perception in RAG-Augmented Agents

Agents that need to reason about document repositories combine:
1. Multimodal RAG (Section 5) as the retrieval layer
2. Standard agentic tool use to trigger retrieval, browse results, and synthesize answers
3. VLM at generation time to reason over retrieved text + images together

The architecture is the same as text-only agentic RAG with the retrieval layer upgraded to handle visual content.

---

## 9. Evaluation and Benchmarks

### Core Benchmark Categories

**Visual Question Answering (VQA) — General capability:**

- **MMBench:** Multi-choice VQA across 20 ability dimensions (object recognition, attribute understanding, relation reasoning, etc.). Comprehensive; widely used for model comparisons. English and Chinese variants.
- **SEED-Bench:** 19K multiple-choice questions across 12 evaluation dimensions; includes both image and video. Less contamination risk than MME.
- **MME:** 14 perception tasks + 4 cognition tasks scored on binary yes/no questions; gives granular breakdowns by task type

**Document Understanding:**

- **DocVQA:** Questions about scanned document images (invoices, forms, reports); requires reading text and understanding layout
- **InfoVQA:** Infographic understanding; requires reading charts, diagrams, and mixed visual-textual content

**Chart and Figure Understanding:**

- **ChartQA:** 20K questions about charts and figures from scientific papers and web; tests reading specific values, comparing quantities, identifying trends. Requires both OCR and quantitative reasoning.

**OCR Quality:**

- **TextVQA:** Questions that require reading text visible in natural scene images (signs, menus, labels)
- **ST-VQA:** Scene text visual question answering; emphasis on irregular and challenging text in scenes

**Video:**

- **EgoSchema:** 5K multiple-choice questions on 3-minute egocentric video clips; tests long-horizon temporal understanding
- **Video-MME:** Multi-choice questions across videos of different lengths (short/medium/long); evaluates how well models scale to longer content

### Critical Caveat: Benchmark Contamination

Benchmark contamination is severe in the multimodal space. Many VLMs are trained on web data that includes benchmark datasets and their answer keys. A model that has memorized DocVQA questions during training achieves inflated scores without having learned the underlying skill.

**The 39.4% drop finding:** Research measuring performance on "clean" versions of benchmarks (examples confirmed not in training data) found average accuracy drops of approximately 39% versus the contaminated benchmark numbers. This is not specific to multimodal, but the multimodal benchmarks are younger and less protected.

**What to do:**
1. Treat published benchmark rankings as directional, not ground truth
2. Build a private eval set from your own documents, images, and questions
3. Test on inputs the model cannot have seen — use internal data, recent events, or custom-generated test cases
4. Compare models on your specific task, not aggregate benchmark scores

**The right evaluation philosophy:** Define your task, collect representative inputs, define what "correct" looks like (exact match, F1, human rating), evaluate all candidate models on that set. That number matters; SEED-Bench numbers don't.

---

## 10. Building Multimodal Applications — Practical Guide

### Decision Tree: When to Use Multimodal vs. Pre-Processing

Work through this in order:

1. **Can structured parsing extract what you need?** If the document is machine-readable (e.g., a well-formed PDF with embedded text, a spreadsheet, a JSON API response), parse it directly. Zero API cost; fully reliable.

2. **Can OCR extract what you need?** If the document is a scan or image-based PDF and the content is primarily text with simple formatting, run OCR first. Test OCR accuracy on your actual documents. If WER is low and structure is preserved, proceed with text-only LLM reasoning.

3. **Does layout matter?** If the document has complex tables where column membership matters, forms with spatial structure, or mixed text/chart content where you need both — use a VLM.

4. **Do you know what to extract in advance?** If yes, structured prompting with JSON schema output works well. If no (you want the model to identify relevant information), VLM with open-ended extraction is appropriate.

5. **Is volume high?** At scale (>1K pages/day), hybrid approaches or specialized document AI are worth the engineering investment. Pure VLM per-page is 10-30× more expensive than OCR + LLM.

### Image Preprocessing Checklist

Before sending images to any VLM API:

- **Format:** Convert to JPEG for photos (smaller file size at same quality); use PNG for diagrams/text images where compression artifacts would obscure detail
- **Resolution normalization:** Don't send 4K screenshots for a task that only needs to read a form. Resize to the minimum resolution needed: if you're reading text, 1024×1024 max; if you're identifying object presence, 512×512 often suffices
- **File size:** Compress JPEG to under 2MB without visible quality loss. Use PIL/Pillow with quality=85 for most photos
- **Multi-page documents:** Process page by page, not all pages in one image. Send the relevant pages, not the entire document

### Token Cost Management

Token costs for images are significant at scale. The decisions matter:

**Low detail mode:**
- Claude resizes to max 512×512, encodes as single pass
- Cost: ~65 tokens per image
- Use for: thumbnail recognition, category classification, checking "is there a person in this photo?", simple yes/no about image content

**High detail mode:**
- Claude tiles at 512×512, processes each tile
- Cost: 65 + (number of tiles × 1290) tokens; a 1024×1024 image = 65 + (4 × 1290) = ~5,225 tokens

  Note: Anthropic's published calculation is approximately 1,700 tokens for 1024×1024 at high detail, varying by exact tile implementation.
- Use for: reading text in images, understanding chart values, document extraction, detailed inspection

**GPT-4o high detail:** 85 + (170 × tiles) tokens. More granular tiling formula.

**Cost math example:** At $3/1M tokens (Claude claude-sonnet-4-6), processing 10,000 documents with 5 pages each at high detail (~1,700 tokens/page) = 85M tokens = $255 just for image token costs. At low detail: 10,000 × 5 × 65 = 3.25M tokens = $9.75. Choose your detail level deliberately.

### Prompt Engineering for VLMs

VLMs respond better to explicit, spatial, and structured prompts. Key techniques:

**Be explicit about what to look at:**
- Weak: "What does this invoice say?"
- Strong: "This is an invoice image. Extract: (1) vendor name from the top header, (2) invoice number from the upper right, (3) all line items with their unit prices and quantities from the table, (4) the total amount due from the bottom."

**Reference visual elements by position:**
- "In the table in the upper-right quadrant..."
- "The bar chart on the left side shows..."
- "The text in the footer at the bottom..."

**Label multi-image inputs explicitly:**

When sending multiple images, label them clearly in your prompt:
```
Image 1: [Slide 3 from Q4 2024 deck]
Image 2: [Slide 3 from Q3 2024 deck]

Compare the revenue figures shown in Image 1 and Image 2. What changed between quarters?
```

Without explicit labels, VLMs can confuse which image they're referring to in their responses.

**Use JSON schema for structured extraction:**

```
Extract the following from this invoice image and return as JSON:
{
  "vendor_name": "string",
  "invoice_date": "YYYY-MM-DD",
  "invoice_number": "string",
  "line_items": [{"description": "string", "quantity": number, "unit_price": number}],
  "total_amount": number,
  "currency": "string"
}

If a field is not visible or not applicable, use null. Do not infer values not explicitly shown.
```

This dramatically reduces hallucination compared to free-form extraction. The JSON schema constrains the output space; the "do not infer" instruction directly addresses VLM confabulation.

### Error Modes Unique to VLMs

These failure patterns don't exist in text-only LLMs and require specific mitigations:

**1. Text hallucination (confabulation of text not present in the image)**

VLMs sometimes generate plausible-sounding text that isn't actually in the image — especially for small, blurry, or partially occluded text. Common in OCR-heavy tasks.

Mitigation: Ask the model to quote exact text it reads, not paraphrase. Cross-validate against OCR output where accuracy is critical.

**2. Spatial reasoning errors**

VLMs are unreliable at left/right distinctions, ordinal positions, and precise spatial comparisons. "The second item from the left" frequently returns the wrong item.

Mitigation: Don't rely on ordinal spatial references for critical extractions. Extract all items and let downstream logic sort/filter by position if needed.

**3. Counting errors**

VLMs are unreliable for counts above approximately 5-6 objects. "How many cars are in this parking lot?" for a crowded lot will be wrong.

Mitigation: Use dedicated object detection models (YOLO, Detectron2) for counting tasks. VLMs are appropriate for "are there any cars?" but not "count exactly how many."

**4. Hallucination under ambiguity**

When image quality is poor or content is ambiguous, VLMs will often generate a confident answer rather than expressing uncertainty. This is worse than text-only LLMs which tend to hedge more on low-confidence tasks.

Mitigation: Explicitly instruct the model to express uncertainty ("If you cannot clearly read any value, say 'unclear' rather than guessing"). Include image quality assessment as a first extraction field.

**5. Refusal on ambiguous content**

VLMs have stricter safety filtering than text-only LLMs on certain content categories (violence, nudity, medical imagery, weapons). Images that look benign to humans can trigger refusals based on visual classification.

Mitigation: Test your actual image distribution for refusal rate before deployment. For medical or security applications, the enterprise/API tier typically has configurable safety thresholds.

### Multimodal System Architecture Checklist

Before shipping a multimodal feature to production:

- [ ] Benchmarked on real examples from your actual image distribution (not demo images)
- [ ] Measured token cost at P50 and P99 image sizes; computed monthly cost at expected volume
- [ ] Decided on detail level (low/high) intentionally with cost/quality measurement
- [ ] Tested failure modes: blurry images, partially cropped images, multi-page documents, images with fine text
- [ ] Image size limits enforced upstream (reject > 5MB, reject unsupported formats)
- [ ] Structured output format specified in prompt; validated against schema before passing downstream
- [ ] Error handling for VLM refusals and unclear responses (null fields vs. retries)
- [ ] Logged a sample of image + response pairs for quality monitoring in production

---

## Key Takeaways for Technical PMs

1. **VLMs work by projecting image patches into the same space as text tokens.** The LM then attends to visual and text tokens identically. This explains both why VLMs work and their failure modes (no continuous spatial reasoning, no precise counting).

2. **The connector matters less than the training data.** LLaVA's linear projection outperformed complex architectures because the training data quality was better. Don't over-invest in architecture; invest in data.

3. **Resolution costs tokens.** High-detail images at 1024×1024 cost ~1,700 tokens with Claude. Low-detail costs ~65. Choose deliberately based on the task — reading small text needs high detail; detecting "is this a dog photo" does not.

4. **OCR + LLM beats VLM for most document tasks on cost.** VLM is worth the premium only when layout matters (complex tables, forms, charts). Build a benchmark on your actual documents before committing to either approach.

5. **Whisper is the standard ASR.** 680K hours of training data; <5% WER on English. Use faster-whisper in production for 3× speedup. For most applications, ASR-then-text-LLM is 10× cheaper than native audio and nearly as capable.

6. **Video is frame sampling in practice.** True temporal video understanding is a research frontier. Production systems sample keyframes, process with VLM, and ground to audio transcript timestamps. Gemini 1.5 Pro's 1M context is the closest to true long-video understanding.

7. **Benchmark numbers are inflated.** Test on your actual use case data, not on published benchmark rankings. Contamination causes ~39% inflation on average.

8. **VLMs hallucinate text and counts.** Don't trust VLM OCR output without validation. Don't trust counts above 5-6. Use explicit JSON schema output to constrain generation and reduce confabulation.

9. **Computer use is ReAct + screenshots.** The same agent loop works; you just add screenshot capture and input simulation as tools. The hard part is UI grounding (screenshot region → pixel coordinate), which often requires a separate specialized model.

10. **ColPali is the state of the art for visual document retrieval** when charts, tables, and diagrams contain information that text extraction would miss. It's more expensive than standard dense retrieval; benchmark before adopting.

---

*Sources: CLIP (Radford et al., OpenAI 2021), LLaVA (Liu et al., 2023), LLaVA-1.5 (Liu et al., 2023), BLIP-2 (Li et al., Salesforce 2023), Whisper (Radford et al., OpenAI 2022), ColPali (Faysse et al., 2024), Gemini Technical Report (Google 2023/2024), Anthropic API documentation (2024-2025), OpenAI API documentation (2024-2025). All model capabilities and pricing reflect state as of early-mid 2025.*

*Last updated: 2026-03-22*
