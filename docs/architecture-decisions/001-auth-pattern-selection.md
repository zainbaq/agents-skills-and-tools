# ADR-001: Authentication Pattern for Azure AI Search and Azure OpenAI Integration

**Date**: 2026-01-15
**Status**: Accepted
**Deciders**: Lead Engineer (Promethean Labs), Client Security Architect

## Context

The document compliance RAG system required its backend API service (FastAPI on Azure App Service) to authenticate against Azure AI Search and Azure OpenAI to perform hybrid search queries and generate embeddings for a Copilot Studio agent.

Three authentication patterns were under consideration:

1. **Service Principal with client secret**: Register an application in Entra ID, generate a client secret, store it in Azure Key Vault, and retrieve it at runtime to exchange for an access token.

2. **System-assigned Managed Identity**: Enable a managed identity on the App Service. Azure automatically provisions and rotates credentials. The application uses the Azure SDK's `DefaultAzureCredential` to obtain tokens with no secret storage required.

3. **API key authentication**: Use Azure AI Search and Azure OpenAI's built-in API keys stored as App Service environment variables.

The system also needed to support a Power Automate flow calling the same Azure AI Search index. This added a fourth consideration: whether the same identity pattern could extend to Power Automate, or whether a separate pattern was needed for that traffic path.

The client's security policy required an audit trail of all access to the search and AI services. The compliance posture required that no long-lived secrets be present in application configuration.

## Decision

The backend API service uses a **system-assigned Managed Identity**, assigned the minimum required RBAC roles:
- Azure AI Search: `Search Index Data Reader`
- Azure OpenAI: `Cognitive Services OpenAI User`

The application code uses `DefaultAzureCredential` from the Azure SDK. This transparently uses managed identity in deployed environments and the developer's `az login` session locally — no code change between environments.

For the Power Automate path, **Azure API Management (APIM, Developer tier)** is deployed as a facade. APIM uses its own managed identity to authenticate to Azure AI Search. Power Automate authenticates to APIM using OAuth2 with Entra ID as the identity provider, configured on the Power Platform Custom Connector.

## Consequences

### Positive
- Zero secrets to rotate. The managed identity credential is automatically managed by the Azure platform.
- RBAC roles are narrowly scoped — the App Service identity cannot create or delete indexes, only read from them. A compromised application cannot modify the search configuration.
- Every token issuance appears in Entra ID sign-in logs, providing a complete access audit trail for compliance.
- `DefaultAzureCredential` eliminates environment-specific authentication code. Local development uses `az login` with the same roles assigned to the developer's user account.
- APIM centralizes logging for all inbound calls from Power Automate, making it easier to monitor and rate-limit per-environment.

### Negative
- Managed identity cannot be used directly by Power Automate cloud flows — Power Automate has no identity within the application's VNet. APIM adds an infrastructure component to deploy, configure, and monitor.
- APIM Developer tier costs approximately $50/month. Acceptable for this engagement but should be revisited if usage grows to justify Standard tier (~$250/month) for production SLA.
- Local development requires each developer to run `az login` and be assigned the same RBAC roles on the development Azure AI Search and OpenAI instances. This must be documented in the onboarding guide and scripted for repeatability.

### Neutral
- Switching to a different managed identity scope (user-assigned vs system-assigned) in the future is a one-line infrastructure change with no application code impact.

## Alternatives Considered

### Service Principal with Client Secret

Rejected because client secrets have expiry dates (maximum 2 years) and require a rotation process. Any failure to rotate before expiry causes an outage in a system that may have no on-call rotation. For a compliance-sensitive system where availability is a contractual requirement, adding a secret rotation dependency was not acceptable.

Additionally, the service principal secret must be stored somewhere — either in Key Vault (adding another dependency) or in App Service configuration (creating a bootstrapping problem: you need a credential to get Key Vault, and that credential needs to be stored somewhere).

### API Key Authentication

Rejected for similar reasons: API keys do not rotate automatically, can be exfiltrated from environment variables or logs, and do not appear in Entra ID audit logs. The client's security policy explicitly prohibited API key authentication for services handling sensitive documents.

### Entra ID Delegated Authentication (On-Behalf-Of Flow)

Rejected because the API service performs batch indexing operations as a background job with no interactive user session. Delegated auth requires a user's identity at the time of the call — it cannot be used for server-to-server or background workloads.
