# Power Automate: Hybrid Semantic Search Flow Pattern

A pattern for calling Azure AI Search hybrid search (keyword + vector + semantic reranking) from a Power Automate flow, designed for use as a Copilot Studio action or a standalone automation.

## Why Not Use the Native Copilot Studio Knowledge Source?

Copilot Studio's built-in Azure AI Search knowledge source is quick to configure but has a hard cap of 5 retrieval results. For high-recall use cases — where an agent must scan a corpus of thousands of documents to surface all relevant passages — 5 results is insufficient. This pattern retrieves 50–100 results and applies semantic reranking, giving the generative model far more evidence to synthesize from.

## Architecture

```
User Query
    │
    ▼
[Copilot Studio Action] or [HTTP Request Trigger]
    │
    ├── [HTTP: Get Embedding]
    │   POST https://{openai}.openai.azure.com/openai/deployments/
    │         text-embedding-ada-002/embeddings?api-version=2024-02-01
    │   Auth: Managed Identity
    │   Body: { "input": "<user query>" }
    │
    ├── [HTTP: Hybrid Search]
    │   POST https://{search}.search.windows.net/indexes/
    │         docs-index/docs/search?api-version=2024-07-01
    │   Auth: Managed Identity
    │   Body: hybrid query (keyword + vector + semantic)
    │
    └── [Compose: Format Citations]
        Returns: array of { content, source_url, score, reranker_score }
```

## Step-by-Step Flow Actions

### Step 1: Initialize Variables

```
Name: query
Type: String
Value: triggerBody()?['query']
```

### Step 2: Get Embedding from Azure OpenAI

**Action**: HTTP

| Field | Value |
|-------|-------|
| Method | POST |
| URI | `https://{your-openai-resource}.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2024-02-01` |
| Authentication | Managed Identity |
| Audience | `https://cognitiveservices.azure.com` |
| Content-Type | `application/json` |
| Body | `{"input": "@{variables('query')}"}` |

Parse the response:
```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "embedding": { "type": "array", "items": { "type": "number" } }
        }
      }
    }
  }
}
```

### Step 3: Hybrid Search Request

**Action**: HTTP

| Field | Value |
|-------|-------|
| Method | POST |
| URI | `https://{your-search-service}.search.windows.net/indexes/docs-index/docs/search?api-version=2024-07-01` |
| Authentication | Managed Identity |
| Audience | `https://search.azure.com` |
| Content-Type | `application/json` |

**Body**:
```json
{
  "search": "@{variables('query')}",
  "queryType": "semantic",
  "semanticConfiguration": "semantic-config",
  "captions": "extractive",
  "answers": "extractive|count-3",
  "vectorQueries": [
    {
      "kind": "vector",
      "vector": "@{body('Get_Embedding')?['data'][0]['embedding']}",
      "fields": "content_vector",
      "k": 50,
      "weight": 0.5
    }
  ],
  "select": "chunk_id, content, source_url, file_name, page_number, document_type",
  "top": 50,
  "count": false
}
```

The `weight: 0.5` balances the vector score equally with the keyword BM25 score before semantic reranking. Adjust based on your query patterns — increase for semantic-heavy queries (natural language), decrease for keyword-heavy (exact domain terminology).

### Step 4: Format Citations

**Action**: Apply to each (on `body('Hybrid_Search')?['value']`)

Inside the loop, compose a citation object:
```json
{
  "chunk_id": "@{items('Apply_to_each')['chunk_id']}",
  "content": "@{items('Apply_to_each')['content']}",
  "source_url": "@{items('Apply_to_each')['source_url']}",
  "file_name": "@{items('Apply_to_each')['file_name']}",
  "page_number": "@{items('Apply_to_each')['page_number']}",
  "relevance_score": "@{items('Apply_to_each')['@search.score']}",
  "reranker_score": "@{items('Apply_to_each')['@search.rerankerScore']}"
}
```

Append to a result array variable.

### Step 5: Response

Return the result array to the Copilot Studio action or HTTP caller. The Copilot Studio generative answer node then uses the `content` fields as grounding context and the `source_url` fields for citations.

## Authentication: Managed Identity Setup

The Power Automate flow's connection must use Managed Identity. The managed identity requires these RBAC role assignments:

| Resource | Role |
|----------|------|
| Azure AI Search service | Search Index Data Reader |
| Azure OpenAI resource | Cognitive Services OpenAI User |

**Never use API keys in Power Automate flows** — keys can't be rotated without updating every flow that references them. Managed identity removes this operational risk entirely.

To assign roles via Azure CLI:
```bash
# Get the Power Automate managed identity object ID from the connection resource
IDENTITY_ID="<managed-identity-object-id>"

# Azure AI Search role
az role assignment create \
  --role "Search Index Data Reader" \
  --assignee-object-id $IDENTITY_ID \
  --assignee-principal-type ServicePrincipal \
  --scope /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Search/searchServices/{name}

# Azure OpenAI role
az role assignment create \
  --role "Cognitive Services OpenAI User" \
  --assignee-object-id $IDENTITY_ID \
  --assignee-principal-type ServicePrincipal \
  --scope /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{name}
```

## Throttling and Limits

| Component | Limit | Mitigation |
|-----------|-------|-----------|
| Azure AI Search S1 | 36 QPS | Cache embeddings for repeated queries; deduplicate at the flow level |
| Azure OpenAI ada-002 | Varies by TPM quota | Use a separate deployment for RAG vs chat to avoid quota contention |
| Power Automate HTTP action | 240-second timeout | Azure AI Search hybrid search typically returns in <3 seconds for 50 results |

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `401` on Search HTTP action | Managed identity not assigned Search role | Assign `Search Index Data Reader` on the Search resource |
| `401` on OpenAI HTTP action | Managed identity not assigned OpenAI role | Assign `Cognitive Services OpenAI User` on the OpenAI resource |
| Empty `value` array in search results | Vector field dimension mismatch | Verify embedding dimension matches index schema (1536 for ada-002) |
| `rerankerScore` missing from results | Semantic config name wrong or semantic search not enabled | Check `semanticConfiguration` name matches the index schema exactly |
| Flow fails with `InvalidTemplate` | Expression error in vector embedding reference | Ensure embedding path is `body('Get_Embedding')?['data'][0]['embedding']` exactly |
