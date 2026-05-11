# ADR-002: RAG Pipeline Design for Document Search

**Date**: 2026-02-01
**Status**: Accepted
**Deciders**: Lead Engineer (Promethean Labs)

## Context

The system must answer questions against a corpus of approximately 10,000 documents totalling roughly 50GB of PDF content. The primary use case was a Copilot Studio agent used to surface relevant information across a large document corpus, replacing a previously manual review process.

Quality dimensions in priority order:
1. **Citation accuracy** — the retrieved chunk must actually contain the answer
2. **Answer correctness** — the generative response must faithfully represent the retrieved content
3. **Coverage** — all relevant documents must be surfaced, not just the most similar
4. **Response latency** — under 10 seconds for a full query-retrieve-generate cycle

Two primary architectural approaches were evaluated over a 3-week period on a test corpus of 500 documents with a 200-question evaluation set drawn from previous manual reviews.

**Option A: Azure AI Search Integrated Vectorization**
Use Azure AI Search's indexer skillset pipeline for both indexing and retrieval. The indexer calls Azure OpenAI for embeddings during indexing via a built-in vectorizer skill. Search queries use the hybrid search API — a single request combining BM25 keyword scoring with HNSW vector search, followed by semantic reranking via the `@search.rerankerScore`.

**Option B: Qdrant + BM25 Separate Indexes with RRF Fusion**
Maintain a Qdrant vector database (on AKS) for semantic search and Azure AI Search (Basic tier, keyword-only) for BM25. A retrieval orchestration service merges results from both sources using Reciprocal Rank Fusion before passing to the generative model.

A secondary decision within Option A was the chunking strategy: fixed-size (512 tokens, 64-token overlap) versus sentence-level chunking with a 400-token ceiling. This was evaluated on the same test set.

## Decision

**Option A: Azure AI Search Integrated Vectorization** with hybrid search (BM25 + vector) and semantic reranking enabled (S1 tier).

**Chunking**: Sentence-level chunking, maximum 400 tokens, minimum 50 tokens (short trailing sentences merged with the preceding chunk). Each chunk carries `page_number` and `chunk_sequence` metadata to enable adjacent-chunk retrieval when context is needed beyond the returned chunk.

**Generation**: GPT-4o (Azure OpenAI) with a system prompt that instructs the model to answer only from retrieved context and to include the `source_url` from each cited chunk. The context window receives the top 10 reranked chunks (by `@search.rerankerScore`), not all 50 retrieved candidates.

**Retrieval parameters**: `top: 50`, `queryType: semantic`, vector weight 0.5, return top 10 by reranker score to generation.

## Consequences

### Positive
- Single infrastructure component manages both keyword and vector search. No orchestration service, no RRF implementation, no Kubernetes cluster.
- Azure AI Search semantic reranking consistently outperformed manual RRF fusion in our evaluation (see data below).
- Sentence-level chunks improve citation precision — the retrieved text is more likely to contain the exact relevant passage rather than a padded fixed-size window that averages across multiple paragraphs.
- The indexer pipeline is idempotent: re-indexing a document (e.g., after a correction) updates the existing record without creating duplicates (key is the base64-encoded blob URL).
- `DefaultAzureCredential` works identically for both the indexer pipeline and the query service — consistent auth pattern across the system.

### Negative
- Azure AI Search S1 tier is required for semantic reranking (~$250/month for 1 search unit). Basic tier does not support semantic configurations. This is a hard cost floor.
- Sentence-level chunking requires a preprocessing step before the Azure AI Search indexer can process documents. This is implemented as a Python Azure Function invoked as a Web API skill in the skillset — adding an additional compute dependency.
- Vector index storage is approximately 3x the raw text storage (1,536 dimensions × 4 bytes × number of chunks). For 50GB of source content split into ~1M chunks, budget approximately 6GB of additional vector storage.
- Migrating to a different embedding model later requires re-indexing the entire corpus. The embedding model (text-embedding-ada-002) is baked into the vector dimensions and cannot be changed without a full reindex.

### Neutral
- The decision to use Azure OpenAI for embeddings rather than a self-hosted model aligned with the client's existing Azure OpenAI deployment and avoided a new infrastructure component. Both options produce similar embedding quality for English text.

## Evaluation Results

Test set: 200 questions derived from previous manual reviews. Questions were categorized as specific-passage (answer in one place), coverage (answer requires checking multiple documents), and synthesis (answer requires combining information from multiple documents).

| Configuration | Citation Recall | Answer Accuracy | P95 Latency |
|--------------|----------------|-----------------|-------------|
| Fixed-size chunks + semantic reranking | 71% | 68% | 4.2s |
| Sentence-level chunks + semantic reranking | 83% | 79% | 4.8s |
| Sentence-level chunks + RRF fusion (Option B) | 85% | 80% | 7.1s |
| Sentence-level chunks + semantic reranking, top 10 to generation | 83% | 81% | 4.8s |

**Citation Recall**: proportion of questions where the cited chunk actually contained the answer.
**Answer Accuracy**: proportion of generated answers judged correct by subject-matter expert review.

Sentence-level chunking improved citation recall by 12 percentage points over fixed-size chunking on the same retrieval architecture — the single highest-impact improvement in the evaluation.

Option B (RRF fusion with Qdrant) scored 2 percentage points higher on citation recall than Option A at the cost of 2.3 seconds additional latency and significantly higher infrastructure complexity.

## Alternatives Considered

### Option B: Qdrant on AKS + BM25 Separate Indexes with RRF Fusion

Rejected due to operational overhead. Running Qdrant on AKS adds a Kubernetes cluster, persistent volume management, custom backup procedures, and a service the client's team must monitor and patch. The client does not have Kubernetes expertise, and a 2-percentage-point retrieval improvement did not justify adding a stateful distributed system with no on-call support.

The latency disadvantage (7.1s vs 4.8s P95) was also a concern — the team's workflow requires near-real-time responses during active review sessions.

### Fixed-Size Chunking (512 tokens, 64-token overlap)

Evaluated directly against sentence-level chunking on the test set. Fixed-size chunking scored 12 percentage points lower on citation recall. The additional indexing time from sentence-level chunking (+30% due to the preprocessing Azure Function) was deemed acceptable given the retrieval quality improvement.

The specific failure mode with fixed-size chunking was sentence truncation: documents in this corpus frequently contain long conditional sentences. Fixed-size chunking split these mid-sentence, and the retrieved chunk would contain the first half of a statement but not the concluding context — causing the generative model to produce incomplete or incorrect answers.

### Copilot Studio Native Knowledge Source (Azure AI Search)

Evaluated for rapid prototyping. The native knowledge source retrieves a maximum of 5 documents. In testing, the relevant passage was outside the top-5 results for 34% of coverage-type questions (where the answer required synthesizing information from multiple documents across a large corpus). Native knowledge source was rejected for the production implementation; it remains useful for small corpora or simpler use cases where top-5 retrieval is sufficient.
