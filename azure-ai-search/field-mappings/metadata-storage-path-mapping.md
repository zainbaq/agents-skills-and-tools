# Surfacing Blob URLs for Citations via `metadata_storage_path`

## The Problem

When you index documents from Azure Blob Storage into Azure AI Search, each document's blob URL is available as the `metadata_storage_path` system field on the source document. This URL is essential for RAG citation links — when a user asks a question and the system retrieves a document chunk, the response needs to include a link back to the source so the user can verify the answer.

By default, `metadata_storage_path` is NOT mapped to your index. You must configure a field mapping explicitly. This catches teams off guard because the field is visible in the indexer debug session but absent from actual search results.

## The Field Mapping

Add this to your indexer's `fieldMappings` array:

```json
{
  "sourceFieldName": "metadata_storage_path",
  "targetFieldName": "source_url"
}
```

Declare `source_url` in your index schema as:

```json
{
  "name": "source_url",
  "type": "Edm.String",
  "retrievable": true,
  "filterable": true,
  "searchable": false
}
```

Set `searchable: false` — you want to retrieve this field with results, not search against it.

## The ID Mapping Gotcha

If you use `metadata_storage_path` as your document key, you must base64-encode it. The raw value contains characters (`/`, `=`, `:`) that are invalid in Azure AI Search document key fields:

```json
{
  "sourceFieldName": "metadata_storage_path",
  "targetFieldName": "id",
  "mappingFunction": {
    "name": "base64Encode"
  }
}
```

Add a second, separate mapping without the encoding function to also capture the raw URL in `source_url`. Both mappings can reference the same source field:

```json
[
  {
    "sourceFieldName": "metadata_storage_path",
    "targetFieldName": "id",
    "mappingFunction": { "name": "base64Encode" }
  },
  {
    "sourceFieldName": "metadata_storage_path",
    "targetFieldName": "source_url"
  }
]
```

## Decoding IDs Back to URLs

When you need to look up the source document from a search result's `id` field:

**Python:**
```python
import base64

def decode_blob_url(encoded_id: str) -> str:
    # Azure uses URL-safe base64 — pad if necessary
    padding = 4 - len(encoded_id) % 4
    if padding != 4:
        encoded_id += "=" * padding
    return base64.b64decode(encoded_id.encode()).decode("utf-8")
```

**C#:**
```csharp
public static string DecodeBlobUrl(string encodedId)
{
    int padding = encodedId.Length % 4;
    if (padding > 0) encodedId += new string('=', 4 - padding);
    return Encoding.UTF8.GetString(Convert.FromBase64String(encodedId));
}
```

## SAS Token Considerations

In production, your blob container should be private (no anonymous read access). The `metadata_storage_path` URL alone will return a 403 for any client without storage account access.

**Option 1: Generate SAS token at query time (recommended for most cases)**

```python
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta, timezone

def get_citation_url(blob_url: str, account_name: str, account_key: str) -> str:
    # Parse container and blob name from the URL
    # blob_url format: https://<account>.blob.core.windows.net/<container>/<blob>
    parts = blob_url.replace("https://", "").split("/")
    container = parts[1]
    blob_name = "/".join(parts[2:])

    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    return f"{blob_url}?{sas_token}"
```

**Option 2: Use managed identity with a short-lived delegation SAS**

Preferred when the application uses managed identity (no account key stored):

```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

credential = DefaultAzureCredential()
service_client = BlobServiceClient(
    account_url=f"https://{account_name}.blob.core.windows.net",
    credential=credential
)

user_delegation_key = service_client.get_user_delegation_key(
    key_start_time=datetime.now(timezone.utc),
    key_expiry_time=datetime.now(timezone.utc) + timedelta(hours=1)
)

sas_token = generate_blob_sas(
    account_name=account_name,
    container_name=container,
    blob_name=blob_name,
    user_delegation_key=user_delegation_key,
    permission=BlobSasPermissions(read=True),
    expiry=datetime.now(timezone.utc) + timedelta(hours=1),
)
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `source_url` is `null` for all results | Field mapping not configured | Add the `fieldMappings` entry above |
| `source_url` present but URL returns 403 | Container is private, no SAS | Generate SAS token at query time |
| Indexer fails with "Invalid document key" | `metadata_storage_path` used as key without encoding | Add `"mappingFunction": { "name": "base64Encode" }` |
| Different URL format than expected | Using Gen2 Data Lake endpoint vs Blob endpoint | Ensure datasource connection string uses `.blob.core.windows.net`, not `.dfs.core.windows.net` |
| `id` and `source_url` both null | Blob Storage firewall blocking indexer | Add Azure AI Search service IP ranges to storage firewall allowlist |
