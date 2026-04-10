# Chapter 2: How Large Language Models Actually Run

You already know how to size a database server. You know that a PostgreSQL instance handling 500 concurrent connections needs a certain amount of RAM for shared buffers, work memory, and connection overhead. You can estimate that a 2TB database with heavy read traffic needs specific IOPS and a certain number of CPU cores.

Running a large language model is the same kind of engineering problem — just with different hardware. The bottleneck moves from CPU and RAM to GPUs and VRAM, the workload shifts from disk I/O to matrix multiplication, and the scaling unit changes from "connections" to "tokens per second." But the thinking process is identical: understand the resource demands, match them to hardware, and plan for concurrent users.

This chapter gives you that understanding.

## Parameters, Precision, and Memory

A large language model is, at its core, a massive collection of numerical weights — called **parameters** — that encode everything the model learned during training. When someone sends a prompt, the model multiplies input data through these weights layer by layer to produce an output. Every single parameter must be loaded into GPU memory before the model can process a single token.

This is the fundamental constraint. Unlike a traditional application where you can page data in and out of RAM from disk, an LLM's parameters need to sit in VRAM (the GPU's dedicated memory) with extremely fast access. The entire model must be resident, all the time, for every request.

The memory footprint depends on two things: the number of parameters and the numerical precision used to store each one.

### Precision Formats

Each parameter is a number. How many bytes you use to store that number is called its **precision**:

- **FP16 (half precision)**: 2 bytes per parameter — full quality, no accuracy loss
- **INT8 (8-bit quantization)**: 1 byte per parameter — minimal quality loss for most tasks
- **INT4 (4-bit quantization)**: 0.5 bytes per parameter — noticeable quality reduction on complex reasoning, but viable for many production use cases

Think of it like audio bitrate. A 320kbps MP3 is nearly indistinguishable from a CD. A 128kbps MP3 is fine for background music. A 64kbps file works for voice calls. The "right" quality depends on the use case.

### Memory Math for Real Models

Here is what this means for two representative model sizes — a large frontier-class model (120B parameters) and a capable mid-size model (20B parameters):

| Model Size | FP16 (2 bytes) | INT8 (1 byte) | INT4 (0.5 bytes) |
|---|---|---|---|
| **120B parameters** | ~240 GB VRAM | ~120 GB VRAM | ~60-70 GB VRAM |
| **20B parameters** | ~40 GB VRAM | ~20 GB VRAM | ~10-12 GB VRAM |

A 120B model at full precision needs 240 GB of VRAM just for the weights. No single GPU on the market has that much memory, which means you must spread the model across multiple GPUs. A 20B model at INT4, on the other hand, fits comfortably on a single consumer-grade GPU with 24 GB of VRAM.

> **Key takeaway**: Model weights are the baseline memory cost — your "minimum RAM" equivalent. But just like a database server needs memory beyond the data files, an LLM needs VRAM beyond the model weights. The biggest additional consumer is the KV cache.

## The KV Cache: Where Concurrent Users Hit You

Here is where things get interesting for anyone thinking about multi-user deployments.

When a model processes a conversation, it computes intermediate values called **keys and values** (KV) for every token in the context. These get cached so the model does not have to recompute them for each new token it generates. This is the **KV cache**, and it grows with every token in every active conversation.

If you have run a database, think of the KV cache as the equivalent of connection-level session memory. Each active user consumes a share of memory proportional to the length of their conversation.

### The Math Gets Serious at Scale

Consider a realistic enterprise scenario: 100 concurrent users working with a 120B parameter model. Some are having straightforward Q&A sessions (4K-8K context). Others are running agentic workflows — code generation, document analysis, multi-step reasoning — that push to 32K-128K tokens per session.

A conservative average of 16K active context tokens across 100 users means 1.6 million tokens of KV cache state that must live in VRAM simultaneously. For a 120B model, that translates to roughly **80-150 GB of additional VRAM** on top of the model weights, depending on the model architecture and precision.

Let that sink in: the KV cache for 100 users can require as much VRAM as the model weights themselves.

| Component | 120B at FP16 | 120B at INT8 |
|---|---|---|
| Model weights | 240 GB | 120 GB |
| KV cache (100 users, 16K avg context) | 80-150 GB | 80-150 GB |
| Runtime overhead (activations, buffers) | 20-40 GB | 15-30 GB |
| **Total VRAM needed** | **340-430 GB** | **215-300 GB** |

Notice that quantizing the model weights helps with the first row, but the KV cache does not shrink proportionally — it depends on the model's hidden dimensions and number of attention heads, not the weight precision. This is why quantization alone does not solve the multi-user scaling problem.

> **Key takeaway**: When sizing GPU infrastructure, the model weights are the floor, not the ceiling. For multi-user deployments, the KV cache often dominates your memory planning. Every additional concurrent user with a long context window costs real VRAM.

## Throughput: Tokens Per Second Per User

Memory determines whether a model fits. **Throughput** determines whether the experience is acceptable.

A good interactive experience requires **30-50 tokens per second** per user. Below 20 tokens/sec, users perceive noticeable lag. Above 50, the output appears essentially instant — the bottleneck becomes reading speed, not generation speed.

For 100 concurrent users, that means your infrastructure must sustain **3,000-5,000 tokens per second in aggregate**. This is the equivalent of sizing network bandwidth for concurrent connections — each user needs a guaranteed minimum, and the infrastructure must handle the aggregate peak.

Throughput depends on GPU compute power (measured in TFLOPS), memory bandwidth (how fast data moves between VRAM and compute units), and how efficiently the serving software schedules work across multiple requests.

## GPU Hardware: A Practical Comparison

If you are used to comparing Xeon versus EPYC processors and DDR4 versus DDR5 memory, this table is your GPU equivalent:

| GPU | VRAM | Memory Bandwidth | FP16 TFLOPS | Purchase Price (per unit) | Typical Use Case |
|---|---|---|---|---|---|
| **NVIDIA H100 SXM** | 80 GB HBM3 | 3.35 TB/s | 989 | $25,000-40,000 | Frontier models, high-throughput production |
| **NVIDIA H200 SXM** | 141 GB HBM3e | 4.8 TB/s | 989 | $30,000-45,000 | Large models needing maximum VRAM |
| **NVIDIA A100 SXM** | 80 GB HBM2e | 2.0 TB/s | 312 | $15,000-17,000 | Previous gen, good price/performance |
| **NVIDIA A100** | 40 GB HBM2e | 1.6 TB/s | 312 | $10,000-12,000 | Budget production, smaller models |
| **NVIDIA L40S** | 48 GB GDDR6X | 864 GB/s | 362 | $7,000-10,000 | Inference-optimized, data center |
| **NVIDIA RTX 4090** | 24 GB GDDR6X | 1.0 TB/s | 330 | $1,600-2,000 | Development, light production |

A few things stand out. The H100 and H200 are in a different league on memory bandwidth — 3-5x faster than the L40S. For LLM inference, memory bandwidth is often the bottleneck, because generating each token requires reading the entire model weights from memory. The H200's 141 GB of VRAM is also notable: it can hold a 120B model at INT8 on a single GPU (though you would still need multiple GPUs for throughput at scale).

The RTX 4090 deserves attention for a different reason. At roughly $1,800, it delivers surprisingly capable inference performance for smaller models. Its 24 GB of VRAM limits what it can run, but for a quantized 20B model, it is a legitimate option.

## Concrete Configurations: What Serves 100 Users

Let us put the pieces together with specific hardware configurations.

### Configuration 1: 120B Model for 100 Users

A 120B model at INT8 needs ~120 GB for weights plus 80-150 GB for KV cache. You need substantial aggregate VRAM and compute.

**Hardware**: 8x H100 80GB node (640 GB total VRAM, NVLink interconnect)

One such node — costing $200,000-400,000 — provides enough VRAM and bandwidth to serve **20-30 concurrent users** at good throughput. The model weights consume about 120 GB (at INT8), leaving ~520 GB for KV cache, activations, and batching overhead. That sounds generous until you account for long-context agentic sessions eating 1-2 GB of KV cache each.

For 100 concurrent users, plan for **3-4 nodes** — a total investment of $600,000-1,600,000 in GPU hardware alone, before racks, networking, power, and cooling.

### Configuration 2: 20B Model for 100 Users

A 20B model is a fundamentally different proposition. At FP16, the weights need ~40 GB. At INT8, ~20 GB. At INT4, ~10-12 GB.

| Setup | Hardware | Estimated Cost | Concurrent Users |
|---|---|---|---|
| **Full precision** | 2x H100 80 GB | $50,000-80,000 | ~100 users |
| **INT8 quantized** | 4x A6000 or L40S (48 GB each) | $28,000-40,000 | ~100 users |
| **INT4 quantized** | 2x RTX 4090 (24 GB each) | $3,200-4,000 | Lighter loads, 20-40 users |
| **Single GPU** | 1x H100 or A100 80 GB | $15,000-40,000 | 50-80 users |

A single H100 or A100 80 GB can comfortably hold a 20B model at FP16 with ample room left for KV cache, serving 50-80 concurrent users at good throughput. Two H100s at FP16 handle 100 users with headroom.

The economics here are striking. Where a 120B model requires over half a million dollars in GPUs for 100 users, a 20B model can serve the same user count for under $80,000 — and with INT8 quantization on L40S cards, under $40,000.

> **Key takeaway**: The jump from 20B to 120B is not a 6x cost increase — it is closer to 10-20x when you factor in KV cache, multi-node networking, and the premium pricing of top-tier GPUs. The question for your clients is whether that quality difference justifies the cost difference for their specific use case.

## Serving Software: The Engine Room

Having the right GPUs is necessary but not sufficient. The software layer that sits between the model and incoming requests makes an enormous difference in how many users your hardware can actually serve. This is analogous to the difference between running a raw MySQL binary and running it behind a properly configured connection pooler with query optimization.

### Key Serving Frameworks

**vLLM** is the current standard for production LLM serving. Its key innovation is **PagedAttention** — a memory management technique for the KV cache that works like virtual memory paging in an operating system. Instead of pre-allocating maximum context length for every request, it allocates KV cache memory in pages and reclaims them dynamically. This alone can improve throughput by 2-4x compared to naive serving.

**Text Generation Inference (TGI)** from Hugging Face is another solid production option, particularly well-integrated with the Hugging Face model ecosystem. It supports quantization, tensor parallelism, and continuous batching out of the box.

**llama.cpp** takes a different approach — it is optimized for running quantized models on consumer hardware, including CPU-only inference. Performance is lower than GPU-native frameworks, but it runs anywhere and is remarkably efficient for its weight class.

**MLX** is Apple's framework for running models on Apple Silicon. If your clients have fleets of M2/M3/M4 MacBooks or Mac Studios, MLX enables local inference using the unified memory architecture. A Mac Studio with 192 GB of unified memory can run a 70B model — something we will explore in Chapter 6.

### Three Techniques That Matter

**Tensor parallelism** splits a model across multiple GPUs within a single node. Each GPU holds a slice of every layer and they communicate over high-speed NVLink interconnects during each forward pass. This is how you run a 120B model across 8 H100s — the model is too large for any single GPU, so you partition it. Think of it as RAID striping, but for neural network layers instead of disk blocks.

**Continuous batching** is what makes multi-user serving economically viable. Instead of processing one request at a time (or waiting to fill a fixed batch), the serving framework dynamically adds new requests to the running batch and removes completed ones. A user who asks a short question gets their response without waiting for another user's 4,000-token generation to finish. This is the LLM equivalent of HTTP/2 multiplexing — interleaving multiple streams on the same connection.

**Speculative decoding** uses a small, fast "draft" model to predict several tokens ahead, then verifies them in a single pass through the large model. When the predictions are correct (which is often the case for routine text), you get multiple tokens for the compute cost of one verification step. The speedup is typically 1.5-2.5x for suitable workloads. It is essentially branch prediction for language models — speculate, verify, and accept or reject.

## What This Means for Your Infrastructure Business

If you currently manage server infrastructure for clients, everything in this chapter maps to skills you already have. Capacity planning, performance monitoring, memory management, multi-node orchestration — these are your core competencies applied to new hardware.

The critical differences are:

1. **Capital intensity is higher.** A well-equipped database server costs $20,000-50,000. A single 8-GPU inference node costs $200,000-400,000. The stakes per deployment are an order of magnitude larger.

2. **The workload is memory-bound, not compute-bound.** Traditional servers often have idle RAM. GPU inference is almost always constrained by VRAM — you will spend more time optimizing memory allocation than CPU utilization.

3. **The model-hardware fit matters enormously.** Choosing a 120B model where a fine-tuned 20B would suffice does not just waste money — it can make the entire business case collapse. Model selection is now an infrastructure decision.

The next chapter takes these hardware realities and turns them into a full cost comparison against commercial APIs. When does self-hosting make sense? At what user count? For which workloads? The answer, as you might expect, depends entirely on the numbers.
