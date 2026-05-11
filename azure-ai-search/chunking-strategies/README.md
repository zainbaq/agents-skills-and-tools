# Document Chunking Strategies for Azure AI Search

Chunking determines how source documents are split before being embedded and indexed. It is one of the highest-impact decisions in a RAG pipeline — the wrong strategy degrades retrieval precision, increases cost, or produces citations that don't contain the relevant answer.

## Why Chunking Matters

Embedding models have token limits (typically 8,192 tokens for `text-embedding-ada-002`). More importantly, retrieval precision degrades at both extremes:
- **Chunks too large**: the embedding averages too many topics; retrieved chunks are semantically diffuse and the relevant sentence is buried in noise
- **Chunks too small**: insufficient context for the model to generate a grounded answer; the relevant sentence exists but lacks the surrounding context needed

Azure AI Search's semantic reranker works best on chunks of 200–600 tokens in practice.

---

## Strategy 1: Fixed-Size Chunking

**How it works**: Split text into chunks of N tokens with M tokens of overlap between consecutive chunks.

**Typical parameters**: 512 tokens, 64-token overlap (12.5% overlap)

**When to use**:
- Uniform, structured documents (data exports, structured reports, forms)
- When you need predictable chunk counts for cost estimation
- Prototyping — fast to implement, easy to reason about

**Azure implementation** — use the [Text Split skill](https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-textsplit) in a skillset:

```json
{
  "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
  "name": "fixed-split",
  "context": "/document",
  "textSplitMode": "pages",
  "maximumPageLength": 2000,
  "pageOverlapLength": 200,
  "inputs": [{ "name": "text", "source": "/document/content" }],
  "outputs": [{ "name": "textItems", "targetName": "pages" }]
}
```

Note: `maximumPageLength` is in characters, not tokens. Approximately 4 characters per token for English text.

**Limitations**:
- Splits sentences and paragraphs mid-thought
- Overlap helps but doesn't fully recover context lost at boundaries
- Retrieved chunks may cut off mid-argument, reducing answer quality

---

## Strategy 2: Sentence-Level Chunking

**How it works**: Split on sentence boundaries, then group sentences into chunks that approach but do not exceed the target token limit.

**Target parameters**: max 400 tokens, min 50 tokens (merge trailing short sentences with the preceding chunk)

**When to use**:
- Narrative documents: contracts, policies, regulations, articles
- When citation accuracy matters (user needs to read the exact clause)
- Documents where truncating a sentence at a boundary changes meaning

**Implementation**: Azure AI Search's Text Split skill supports `sentence` mode:

```json
{
  "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
  "name": "sentence-split",
  "context": "/document",
  "textSplitMode": "sentences",
  "maximumPageLength": 1600,
  "inputs": [{ "name": "text", "source": "/document/content" }],
  "outputs": [{ "name": "textItems", "targetName": "sentences" }]
}
```

For grouping sentences into target-sized chunks, implement a custom Web API skill backed by an Azure Function:

```python
def group_sentences_into_chunks(
    sentences: list[str],
    max_tokens: int = 400,
    min_tokens: int = 50,
    tokenizer=tiktoken.get_encoding("cl100k_base")
) -> list[dict]:
    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = len(tokenizer.encode(sentence))
        if current_tokens + sentence_tokens > max_tokens and current_chunk:
            chunks.append({
                "content": " ".join(current_chunk),
                "chunk_sequence": len(chunks),
                "token_count": current_tokens
            })
            current_chunk = []
            current_tokens = 0
        current_chunk.append(sentence)
        current_tokens += sentence_tokens

    # Merge final short chunk with previous if below minimum
    if current_chunk:
        content = " ".join(current_chunk)
        if current_tokens < min_tokens and chunks:
            chunks[-1]["content"] += " " + content
            chunks[-1]["token_count"] += current_tokens
        else:
            chunks.append({
                "content": content,
                "chunk_sequence": len(chunks),
                "token_count": current_tokens
            })

    return chunks
```

**Limitations**:
- Requires a sentence splitter (spaCy, NLTK, or Azure's built-in with limitations)
- Variable chunk sizes make cost harder to predict
- Domain-specific abbreviations (e.g., "Ltd.", "et al.", "Fig.") can confuse sentence boundary detection

---

## Strategy 3: Semantic Chunking

**How it works**: Embed each sentence, compute cosine similarity between adjacent sentences, and split at points of low similarity (topic boundaries).

**When to use**:
- Long, multi-topic documents (annual reports, regulatory filings, comprehensive policies)
- When topic coherence within a chunk measurably improves answer quality
- Research databases where retrieval precision is worth the additional indexing cost

**Limitations**:
- Requires running embeddings twice per document (once for chunking, once for indexing) — approximately 2x the embedding cost
- Implementation complexity is high — not supported natively in Azure AI Search skillsets
- Must be implemented as a preprocessing step before the document reaches the indexer

**Implementation note**: As of 2026, implement semantic chunking as an Azure Function invoked before blob upload, or as a pre-processing step in the indexer skillset via a Web API skill.

---

## Our Recommendation for Document RAG

Based on production deployment of a document RAG pipeline (~10,000 PDF documents, 50GB):

**Use sentence-level chunking with:**
- Max chunk size: 400 tokens
- Min chunk size: 50 tokens (merge short trailing sentences)
- Page number metadata per chunk for citation

**Evaluation results** on a 200-question test set drawn from actual compliance queries:

| Strategy | Citation Recall | Answer Accuracy | Indexing Time |
|----------|----------------|-----------------|---------------|
| Fixed-size (512 tokens, 64 overlap) | 71% | 68% | Baseline |
| Sentence-level (400 max tokens) | 83% | 79% | +30% |
| Semantic chunking | 85% | 81% | +310% |

Sentence-level chunking captures 97% of the retrieval quality of semantic chunking at 10% of the additional cost. The marginal improvement from semantic chunking did not justify the infrastructure complexity or cost for this use case.

---

## Chunk Metadata to Preserve

Always carry these fields on every chunk:

| Field | Type | Purpose |
|-------|------|---------|
| `chunk_id` | string | Unique identifier: `{doc_id}::chunk_{n}` |
| `source_url` | string | Blob URL of source document (for citations) |
| `page_number` | int | Page in original document |
| `chunk_sequence` | int | Position within document (enables adjacent-chunk retrieval) |
| `document_type` | string | e.g., `contract`, `policy`, `regulation` |
| `last_modified` | datetime | For freshness filtering in queries |
| `token_count` | int | Useful for debugging and cost tracking |

The `chunk_id` format `{doc_id}::chunk_{n}` enables a useful retrieval pattern: when a retrieved chunk lacks context, fetch chunks `n-1` and `n+1` to expand the window around the relevant passage.
