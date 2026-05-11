---
name: api-design
description: >
  Design a RESTful or GraphQL API. Use when asked to design a new API, review
  an existing API design for consistency, or produce an OpenAPI specification.
  Invoke with /api-design followed by the resource or feature name.
allowed-tools: Read, Glob, Grep, WebFetch
---

When this skill is invoked, design a complete API. Always read the existing API codebase first — a new endpoint should be indistinguishable in style from existing endpoints.

## Before Designing

Read the existing API to identify:
- URL structure and versioning strategy (path prefix `/api/v1`, header-based, etc.)
- Auth mechanism in use (Bearer JWT, API key header, session cookie, managed identity)
- Error response envelope format — match it exactly
- Pagination strategy (cursor-based, offset, Link header)
- Field naming convention in request/response bodies (camelCase vs snake_case)
- HTTP client in use and any custom middleware

## REST API Standards

### URL Structure

```
/api/v1/{resource}                     # collection endpoints
/api/v1/{resource}/{id}                # single resource
/api/v1/{resource}/{id}/{sub-resource} # nested (max 1 level deep)
```

Use kebab-case for multi-word resource names: `/api/v1/extraction-jobs`

### HTTP Methods

| Method | Use | Success Code |
|--------|-----|-------------|
| GET | Read resource or collection | 200 |
| POST | Create resource or trigger async action | 201 (create) / 202 (async) |
| PUT | Replace resource entirely | 200 |
| PATCH | Partial update (changed fields only) | 200 |
| DELETE | Remove resource | 204 (no body) |

For long-running operations (document extraction, embedding generation, bulk indexing): use **202 Accepted** with a `Location` header pointing to a status endpoint. Do not make callers wait synchronously for operations that take more than a few seconds — Power Automate HTTP actions, Copilot Studio actions, and browser clients all have hard timeout limits.

### Field Conventions

- **IDs**: UUID v4. Never expose auto-increment integers in public APIs.
- **Timestamps**: ISO 8601 with timezone — `2026-05-11T14:30:00Z`
- **Enums**: `SCREAMING_SNAKE_CASE` strings, not integers
- **Azure resource references**: use the full resource URL or a logical name, never an internal database ID

### Standard Error Envelope

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Human-readable description suitable for logging",
    "details": [
      { "field": "document_url", "message": "must be a valid Azure Blob Storage URL" }
    ],
    "trace_id": "abc-123"
  }
}
```

Standard codes: `VALIDATION_FAILED`, `NOT_FOUND`, `UNAUTHORIZED`, `FORBIDDEN`, `CONFLICT`, `TOO_MANY_REQUESTS`, `INTERNAL_ERROR`

Include `trace_id` on every error response. In Azure-hosted services this should be the Application Insights operation ID, enabling end-to-end correlation from the Power Automate run history through to the backend log.

### Pagination

Use cursor-based pagination for any collection that can grow:

```json
{
  "data": [...],
  "pagination": {
    "cursor": "eyJpZCI6MTAwfQ==",
    "has_more": true,
    "limit": 20
  }
}
```

### Async Job Pattern

For long-running operations (extraction pipelines, bulk indexing, embedding generation):

```
POST /api/v1/extraction-jobs
→ 202 Accepted
   Location: /api/v1/extraction-jobs/{job-id}

GET /api/v1/extraction-jobs/{job-id}
→ 200 OK
   { "status": "RUNNING" | "COMPLETED" | "FAILED", "result": {...} }
```

Power Automate supports this pattern natively via the "Until" loop action polling a status endpoint. Design the status response to include enough detail to diagnose failures without requiring a separate log lookup.

## Output Format

Produce all five of these:

### 1. Resource Model
JSON schema for the resource — all fields, types, required vs optional, example values.

### 2. Endpoints Table
| Method | Path | Description | Request | Response |

### 3. OpenAPI 3.0 Snippet
```yaml
/api/v1/{resource}:
  post:
    summary: ...
    requestBody: ...
    responses:
      '202':
        description: Job accepted
        headers:
          Location:
            schema: { type: string }
```

### 4. Edge Cases
Document explicitly:
- 404 (resource not found)
- Duplicate create (409 Conflict vs idempotent 200?)
- Async job already running (409 or queue it?)
- Caller timeout before async job completes

### 5. Breaking Change Analysis
If modifying an existing API: list every backward-incompatible change and how it will be handled (versioning, deprecation period, migration guide for Power Automate custom connectors).

## GraphQL (when requested)

Apply the read-first approach, then produce:
- Schema definition (types, queries, mutations, subscriptions)
- Resolver outline with N+1 risk analysis (which fields need DataLoader)
- Subscription transport recommendation (WebSocket vs SSE)
