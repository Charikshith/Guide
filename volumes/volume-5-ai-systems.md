# Volume 5 — AI Systems Engineering

> Goal: Where all previous knowledge converges. Requires Volume 0 (linear algebra, probability) and Volume 1 (encoding, Ch 9).
>
> **Chapters 1–20.** The Progressive Builds thread through the chapters (build #1 in Ch 4, #2 in Ch 9, #3 in Ch 11, #4 in Ch 14, #5 in Ch 15, #6 in Ch 17, #7 in Ch 20).

---

## Chapter 1 — LLM Internals

**Concept:** How a language model works — parameters, pretraining, the attention mechanism, and scaling laws (intuition, no deep math).

**Prereqs:** Vol 0 Ch 9.

**Diagram:** A high-level transformer block diagram (input → attention → FFN → output).

**Example:** tracing a token through embedding → attention → logits → softmax.

**Exercises:** (1) Explain why next-token prediction yields useful models. (2) Describe what "parameters" represent and why more scale helps.

**Mini project:** A tiny bigram/character-level model trained on a small corpus.

**Open source:** [`karpathy/nanoGPT`](https://github.com/karpathy/nanoGPT); [`huggingface/transformers`](https://github.com/huggingface/transformers).

**Interview:** "What does an LLM actually predict?" / "What is attention intuitively?"

**Checklist:** ☐ trace a forward pass ☐ explain logits → probabilities ☐ know what pretraining optimizes

---

## Chapter 2 — Tokenization

**Concept:** Turning text into tokens — BPE/WordPiece/SentencePiece; token limits and the bugs tokenization causes.

**Prereqs:** Vol 1 Ch 9.

**Diagram:** A BPE merge table turning "low lower lowest" into subword tokens.

**Example:** `tiktoken` counting tokens; why "climbing" and "climb" share a stem.

**Exercises:** (1) Implement a minimal BPE trainer. (2) Explain why tokenization breaks on some languages/whitespace.

**Mini project:** A tokenizer visualizer that highlights token boundaries.

**Open source:** [`openai/tiktoken`](https://github.com/openai/tiktoken); [`huggingface/tokenizers`](https://github.com/huggingface/tokenizers).

**Interview:** "Why do models use subword tokens?" / "How do you count tokens for cost?"

**Checklist:** ☐ train a BPE ☐ count tokens accurately ☐ know tokenization's failure modes

---

## Chapter 3 — Transformers

**Concept:** Self-attention, multi-head attention, positional encoding, and the encoder/decoder split.

**Prereqs:** Ch 1, Vol 0 Ch 9.

**Diagram:** Scaled dot-product attention (Q·Kᵀ/√d) and multi-head attention.

**Example:** computing attention weights for a short sequence by hand.

**Exercises:** (1) Implement attention in NumPy. (2) Explain why attention is O(n²) in sequence length.

**Mini project:** A from-scratch transformer block on small inputs, verified against a reference.

**Open source:** [`karpathy/nanoGPT`](https://github.com/karpathy/nanoGPT); [`huggingface/transformers`](https://github.com/huggingface/transformers).

**Interview:** "What does the attention mechanism compute?" / "Encoder vs decoder?"

**Checklist:** ☐ implement attention ☐ explain positional encoding ☐ know the O(n²) cost

---

## Chapter 4 — Inference & Serving

**Concept:** Autoregressive decoding, KV cache, batching, sampling (temperature/top-p/top-k), and throughput vs latency.

**Prereqs:** Ch 3.

**Diagram:** An autoregressive decode loop with the KV cache; a batching diagram.

**Example:** a generate loop with temperature and top-p sampling.

**Exercises:** (1) Implement greedy vs sampled decoding. (2) Explain how the KV cache speeds up generation.

**Mini project:** A minimal inference server with a REST endpoint and batching.

**Build #1:** An AI Chatbot — a chat endpoint with history, streaming, and sampling controls.

**Open source:** [`vllm-project/vllm`](https://github.com/vllm-project/vllm); [`huggingface/text-generation-inference`](https://github.com/huggingface/text-generation-inference).

**Interview:** "KV cache — why does it help?" / "Latency vs throughput in serving?"

**Checklist:** ☐ implement sampling ☐ stream tokens ☐ batch requests efficiently

---

## Chapter 5 — Quantization & Efficiency

**Concept:** FP16/INT8/INT4, GPTQ/AWQ, KV-cache quantization, and the accuracy/speed/memory trade-off.

**Prereqs:** Ch 4.

**Diagram:** A weight-matrix quantization diagram (float → int with scale/zero-point).

**Example:** loading a 4-bit model with `bitsandbytes`/`llama.cpp`.

**Exercises:** (1) Quantize a tensor and compute the error. (2) Compare memory of FP16 vs INT4 for a model size.

**Mini project:** Quantize a small model and measure speedup + quality change.

**Open source:** [`ggerganov/llama.cpp`](https://github.com/ggerganov/llama.cpp); [`bitsandbytes-foundation/bitsandbytes`](https://github.com/bitsandbytes-foundation/bitsandbytes).

**Interview:** "Why does quantization usually preserve quality?" / "What's the memory of a 7B model in INT4?"

**Checklist:** ☐ explain scale/zero-point ☐ run a quantized model ☐ measure quality impact

---

## Chapter 6 — Prompt Engineering & Structured Output

**Concept:** Instruction design, few-shot, chain-of-thought, system/user roles, and constrained/structured generation (JSON mode, function calling).

**Prereqs:** Ch 4.

**Diagram:** A prompt template with system/user/assistant roles and a few-shot block.

**Example:** a JSON-mode prompt; a function-calling schema.

**Exercises:** (1) Write a few-shot prompt that improves a task. (2) Enforce structured output with a schema.

**Mini project:** A prompt templating + structured-output library with validation.

**Open source:** [`dottxt-ai/outlines`](https://github.com/dottxt-ai/outlines); [`guidance-ai/guidance`](https://github.com/guidance-ai/guidance).

**Interview:** "Few-shot vs fine-tuning?" / "How do you force valid JSON?"

**Checklist:** ☐ separate roles cleanly ☐ use few-shot deliberately ☐ validate structured output

---

## Chapter 7 — Fine-Tuning, LoRA & PEFT

**Concept:** Full fine-tuning vs parameter-efficient methods; LoRA adapters, data prep, and when to fine-tune at all.

**Prereqs:** Ch 3.

**Diagram:** A LoRA diagram — frozen weights + low-rank adapters.

**Example:** a LoRA training config (rank, alpha, target modules).

**Exercises:** (1) Prepare a small instruction dataset. (2) Train a LoRA adapter and compare to base.

**Mini project:** Fine-tune a small model with LoRA on a custom task.

**Open source:** [`huggingface/peft`](https://github.com/huggingface/peft); [`unslothai/unsloth`](https://github.com/unslothai/unsloth).

**Interview:** "LoRA — how does it stay cheap?" / "When fine-tune vs RAG vs prompt?"

**Checklist:** ☐ curate a dataset ☐ train a LoRA ☐ evaluate before/after

---

## Chapter 8 — Alignment, RLHF & Guardrails

**Concept:** Instruction tuning, RLHF/DPO, and guardrails for safety (input/output filtering, jailbreak resistance).

**Prereqs:** Ch 7.

**Diagram:** An RLHF loop (SFT → reward model → PPO/DPO).

**Example:** a DPO preference pair; a guardrail that blocks a prompt-injection attempt.

**Exercises:** (1) Build a preference dataset of chosen/rejected pairs. (2) Add input + output guardrails to a pipeline.

**Mini project:** A guarded endpoint with prompt-injection detection and output filtering.

**Open source:** [`huggingface/trl`](https://github.com/huggingface/trl); [`guardrails-ai/guardrails`](https://github.com/guardrails-ai/guardrails).

**Interview:** "RLHF vs DPO?" / "How do you defend against prompt injection?"

**Checklist:** ☐ understand the alignment pipeline ☐ filter inputs and outputs ☐ test jailbreak resistance

---

## Chapter 9 — Embeddings & RAG

**Concept:** Embeddings as semantic vectors, retrieval-augmented generation, chunking, reranking, and context management.

**Prereqs:** Ch 6, Vol 0 Ch 9.

**Diagram:** A RAG pipeline: chunk → embed → index → retrieve → rerank → prompt → generate.

**Example:** a semantic search query returning top-k chunks.

**Exercises:** (1) Chunk a document and embed it. (2) Add a reranker to improve retrieval.

**Mini project:** A RAG pipeline over a set of documents with a vector index.

**Build #2:** A RAG Platform — ingestion, embeddings, retrieval, reranking, and citation-grounded answers.

**Open source:** [`langchain-ai/langchain`](https://github.com/langchain-ai/langchain); [`run-llama/llama_index`](https://github.com/run-llama/llama_index).

**Interview:** "Why chunk, and how big?" / "How does reranking help?"

**Checklist:** ☐ build an index ☐ tune chunk size ☐ ground answers in citations

---

## Chapter 10 — Vector Databases

**Concept:** ANN indexes (HNSW/IVF), similarity metrics, hybrid search, and Qdrant/Milvus operations.

**Prereqs:** Ch 9.

**Diagram:** An HNSW graph (layers + nearest-neighbor hops).

**Example:** a Qdrant upsert + cosine search; a hybrid (dense+sparse) query.

**Exercises:** (1) Insert and query vectors with metadata filters. (2) Compare cosine vs dot vs Euclidean for a task.

**Mini project:** A hybrid search service (dense vectors + keyword) on Qdrant.

**Open source:** [`qdrant/qdrant`](https://github.com/qdrant/qdrant); [`milvus-io/milvus`](https://github.com/milvus-io/milvus).

**Interview:** "HNSW — how does it stay fast?" / "When hybrid search over pure vector?"

**Checklist:** ☐ run ANN queries ☐ filter by metadata ☐ choose a similarity metric deliberately

---

## Chapter 11 — Agent Frameworks & Tool Use

**Concept:** ReAct-style agents, tool calling, planning loops, and frameworks (LangGraph, and the patterns beneath them).

**Prereqs:** Ch 6.

**Diagram:** An agent loop: plan → call tool → observe → repeat until done.

**Example:** a tool-calling loop that calls `search()` then `calculator()`.

**Exercises:** (1) Build an agent with two tools. (2) Add a planner that decomposes a task.

**Mini project:** A tool-calling agent with bounded iterations and error recovery.

**Build #3:** An AI Coding Assistant — read/write files, run commands, plan and execute tasks.

**Open source:** [`langchain-ai/langgraph`](https://github.com/langchain-ai/langgraph); [`openai/openai-python`](https://github.com/openai/openai-python) (tool calling).

**Interview:** "How does tool calling work under the hood?" / "How do you keep an agent from looping forever?"

**Checklist:** ☐ define tool schemas ☐ bound the loop ☐ handle tool errors gracefully

---

## Chapter 12 — Agent Memory

**Concept:** Short-term (context) vs long-term memory, summarization, and retrieval-backed memory.

**Prereqs:** Ch 9, Ch 11.

**Diagram:** A memory hierarchy: working context → summarized history → vector-store long-term memory.

**Example:** compressing old turns into a summary; retrieving relevant past facts.

**Exercises:** (1) Implement conversation summarization. (2) Store and retrieve long-term memory via embeddings.

**Mini project:** An agent with persistent memory across sessions.

**Open source:** [`mem0ai/mem0`](https://github.com/mem0ai/mem0); [`letta-ai/letta`](https://github.com/letta-ai/letta).

**Interview:** "Short vs long-term memory in agents?" / "How do you prevent context overflow?"

**Checklist:** ☐ summarize history ☐ retrieve relevant memories ☐ cap context budget

---

## Chapter 13 — MCP & A2A

**Concept:** The Model Context Protocol (tools/resources for agents) and Agent-to-Agent protocol (interoperability).

**Prereqs:** Ch 11.

**Diagram:** An MCP client ↔ server diagram (tools/resources/prompts); an A2A agent-to-agent handshake.

**Example:** an MCP server exposing a `get_weather` tool; an A2A task exchange between agents.

**Exercises:** (1) Build an MCP server with one tool. (2) Design an A2A message exchange for a task hand-off.

**Mini project:** An MCP server + client, plus a two-agent A2A hand-off.

**Open source:** [`modelcontextprotocol/python-sdk`](https://github.com/modelcontextprotocol/python-sdk); [`a2aproject/A2A`](https://github.com/a2aproject/A2A).

**Interview:** "What does MCP standardize?" / "Why A2A over ad-hoc APIs?"

**Checklist:** ☐ expose tools via MCP ☐ hand off tasks between agents ☐ know when each protocol applies

---

## Chapter 14 — Multi-Agent Systems

**Concept:** Orchestration vs choreography, agent roles, shared state, and coordination patterns.

**Prereqs:** Ch 12, Ch 13.

**Diagram:** An orchestrator fanning out to specialist agents, then aggregating.

**Example:** a researcher-writer-critic trio on one task.

**Exercises:** (1) Design a multi-agent team for a task. (2) Implement an orchestrator that aggregates sub-results.

**Mini project:** A small multi-agent system with defined roles and a coordinator.

**Build #4:** An AI Workflow Engine — DAG-based task graphs with agents at each node.

**Open source:** [`langchain-ai/langgraph`](https://github.com/langchain-ai/langgraph); [`crewAIInc/crewAI`](https://github.com/crewAIInc/crewAI).

**Interview:** "Orchestration vs choreography?" / "How do agents share context?"

**Checklist:** ☐ assign clear roles ☐ aggregate results ☐ bound coordination overhead

---

## Chapter 15 — Voice Agents

**Concept:** Speech-to-text, LLM turn-taking, text-to-speech, latency budgets, and interruption handling.

**Prereqs:** Ch 11.

**Diagram:** An audio pipeline: mic → STT → LLM → TTS → speaker, with a turn-taking loop.

**Example:** a streaming STT + LLM + TTS loop under a latency budget.

**Exercises:** (1) Wire STT → LLM → TTS into one loop. (2) Add interruption (barge-in) handling.

**Mini project:** A voice assistant with low-latency turn-taking.

**Build #5:** A Voice Agent — full STT/LLM/TTS with interruptions and conversation state.

**Open source:** [`openai/whisper`](https://github.com/openai/whisper); [`pipecat-ai/pipecat`](https://github.com/pipecat-ai/pipecat).

**Interview:** "How do you hit low latency in voice?" / "What is barge-in?"

**Checklist:** ☐ stream audio ☐ handle interruptions ☐ keep turn-taking under budget

---

## Chapter 16 — AI Observability

**Concept:** Tracing LLM calls, token usage, latency, and quality signals; the three pillars applied to AI.

**Prereqs:** Vol 2 Ch 14.

**Diagram:** A trace of an agent run (spans: retrieval, LLM call, tool call).

**Example:** OpenTelemetry + Langfuse spans for each LLM/tool call.

**Exercises:** (1) Instrument an agent with spans. (2) Add token/latency metrics per step.

**Mini project:** Add full observability to an agent pipeline with a trace dashboard.

**Open source:** [`langfuse/langfuse`](https://github.com/langfuse/langfuse); [`open-telemetry/opentelemetry-python`](https://github.com/open-telemetry/opentelemetry-python).

**Interview:** "What do you trace in an LLM app?" / "Which metrics matter for cost?"

**Checklist:** ☐ trace every LLM/tool call ☐ track token cost ☐ alert on quality regressions

---

## Chapter 17 — Evaluation

**Concept:** Golden datasets, LLM-as-judge, offline vs online eval, and regression testing for prompts/models.

**Prereqs:** Ch 16.

**Diagram:** An eval pipeline: golden set → run → score (exact/LLM-judge) → gate.

**Example:** an LLM-as-judge rubric; an offline eval that gates a model upgrade.

**Exercises:** (1) Build a golden dataset. (2) Write an LLM-judge with a rubric.

**Mini project:** An eval harness with offline scoring and a CI gate.

**Build #6:** A Multi-Agent Framework (Pi Mono Agents style) — plus an eval suite that scores agent runs.

**Open source:** [`langfuse/langfuse`](https://github.com/langfuse/langfuse); [`confident-ai/deepeval`](https://github.com/confident-ai/deepeval).

**Interview:** "How do you evaluate an LLM app?" / "LLM-as-judge — pros/cons?"

**Checklist:** ☐ own a golden dataset ☐ score with a rubric ☐ gate changes on eval

---

## Chapter 18 — Cost & Latency Optimization

**Concept:** Caching (semantic + exact), batching, streaming, model routing, and reducing tokens.

**Prereqs:** Ch 16.

**Diagram:** A request path with cache hits, batching, and a small/large model router.

**Example:** a semantic cache; routing easy calls to a small model, hard ones to a large model.

**Exercises:** (1) Add a semantic cache. (2) Build a model router by task difficulty.

**Mini project:** An optimized pipeline with cache + routing, showing cost/latency before/after.

**Open source:** [`zilliztech/GPTCache`](https://github.com/zilliztech/GPTCache); [`vllm-project/vllm`](https://github.com/vllm-project/vllm) (batching).

**Interview:** "How do you cut LLM cost without hurting quality?" / "Semantic vs exact cache?"

**Checklist:** ☐ cache aggressively ☐ route by difficulty ☐ stream and batch

---

## Chapter 19 — AI Security

**Concept:** Prompt injection, jailbreaks, data exfiltration, and securing the AI supply chain.

**Prereqs:** Ch 8, Vol 2 Ch 10.

**Diagram:** An attack surface diagram for an AI app (inputs, tools, data stores).

**Example:** a prompt-injection attack on a tool-calling agent; a guardrail that blocks exfiltration.

**Exercises:** (1) Craft and defend against a prompt injection. (2) Add an exfiltration filter on tool outputs.

**Mini project:** A red-team exercise on an agent + hardened guardrails.

**Open source:** [`guardrails-ai/guardrails`](https://github.com/guardrails-ai/guardrails); [`OWASP/LLM-Top-10`](https://github.com/OWASP/LLM-Top-10).

**Interview:** "What is indirect prompt injection?" / "How do you stop data exfiltration?"

**Checklist:** ☐ treat model output as untrusted ☐ sandbox tool calls ☐ red-team before release

---

## Chapter 20 — GPU Infrastructure & the AI OS

**Concept:** GPU serving infrastructure, model deployment, and integrating every prior chapter into one system.

**Prereqs:** Ch 4, Ch 18, Vol 4.

**Diagram:** A full AI platform architecture: GPU pool → serving → agents → tools → observability.

**Example:** vLLM on GPU nodes behind a gateway; an AI OS orchestrating agents + tools + memory.

**Exercises:** (1) Size GPU capacity for a serving workload. (2) Architect an AI platform end to end.

**Mini project:** A deployment manifest + capacity plan for a serving cluster.

**Build #7:** An AI Operating System — agents, tools, memory, MCP/A2A, observability, eval, and security unified into one platform.

**Open source:** [`vllm-project/vllm`](https://github.com/vllm-project/vllm); [`kubernetes/kubernetes`](https://github.com/kubernetes/kubernetes) (orchestration).

**Interview:** "How do you serve models on GPUs at scale?" / "What is an 'AI OS'?"

**Checklist:** ☐ size GPU capacity ☐ deploy a serving cluster ☐ integrate all subsystems into one coherent platform

---

**Exit criteria:** Complete the 7 progressive builds, ending at the AI Operating System.
