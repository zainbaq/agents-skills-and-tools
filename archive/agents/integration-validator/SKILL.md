# Integration Validator Sub-Agent

## What It Does

Validates API integrations and external service connections for contract correctness, resilience, auth, and observability. Built from production experience debugging Power Automate → Azure Function connectivity on private networks, Azure AI Search field mapping gaps, and Copilot Studio connection reference failures across environments. Has Bash access to run validation scripts. No memory — integration contracts change frequently and stale memory causes false positives.

## When to Invoke

- "Validate the Azure AI Search integration in `backend/services/search.py`"
- "Why is the Power Automate HTTP connector getting 401s?"
- "Why are my search results missing the source URL?"
- "Check if the retry logic in the OpenAI client is correct"
- "Validate this custom connector before we deploy to UAT"
- "Why can't Power Automate reach my Azure Function?"
- "The Azure portal data import wizard isn't working — what now?"

## How to Install

```bash
# Project-scoped
cp agents/integration-validator/integration-validator.md .claude/agents/integration-validator.md

# User-scoped
cp agents/integration-validator/integration-validator.md ~/.claude/agents/integration-validator.md
```

## Example Usage

```
Use the integration-validator agent to validate the Azure AI Search integration
in backend/services/search_client.py. Confirm the hybrid search request shape
matches the REST API spec and that the managed identity auth is correct.
```

## Configuration Notes

| Setting | Value | Reason |
|---------|-------|--------|
| Model | sonnet | Systematic contract checking; no adversarial reasoning needed |
| Tools | Read, Glob, Grep, Bash, WebFetch | Bash for running test scripts; WebFetch for pulling API docs |
| Memory | none | Contracts change; stale memory causes false positives |
| Color | orange | "Warning / check before proceeding" signal |

## Common Integration Failure Patterns

Production-sourced failures this agent catches:

1. **`metadata_storage_path` not mapped** — blob URL never appears in search results; `source_url` is null for every document. Must be explicitly added to `fieldMappings` in the indexer definition.
2. **Power Automate → ILB ASE direct call** — timeouts with no useful error. The function has no public inbound endpoint. Fix: route via APIM with VNet integration, or on-premises data gateway.
3. **Azure portal "Import data" wizard silent failure** — wizard produces an empty index when storage has firewall rules or private endpoints. Fix: create datasource, index, and indexer directly via REST API.
4. **Copilot Studio delegated auth in production** — every new user gets an OAuth consent prompt. Fix: migrate to service principal or managed identity (application-level auth).
5. **Token not cached** — OAuth2 token fetched on every API call, triggering rate limits at scale
6. **Fixed sleep retry** — `time.sleep(5)` without backoff, causing thundering herd on recovery
7. **`@search.rerankerScore` accessed unconditionally** — absent on non-semantic queries, crashes the result parser
