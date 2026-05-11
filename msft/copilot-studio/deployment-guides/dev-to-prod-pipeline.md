# Copilot Studio: Dev-to-Prod Deployment Pipeline

How to promote a Copilot Studio agent from development through UAT to production using Power Platform solutions and the Power Platform CLI. This guide covers what to include in a solution, how to handle environment-specific configuration, and the common failure modes that catch teams off guard.

## Environment Strategy

| Environment | Purpose | Access | Data |
|-------------|---------|--------|------|
| Dev | Feature development and builder iteration | Agent builders only | Synthetic or anonymized |
| UAT | Stakeholder testing and acceptance sign-off | Business users + builders | Sanitized production copy |
| Production | Live users | All licensed users | Real data |

Each environment has its own Azure AI Search instance, Azure OpenAI resource, and Power Automate connections. **Never share infrastructure between environments** — a reindex in dev should not affect production response times.

## What to Package in a Solution

A Power Platform solution is the deployment unit. Everything the agent depends on must be in the same solution, or the import will fail with missing dependency errors.

**Include**:
- The Copilot Studio agent (bot)
- All Custom Connectors used by the agent
- All Power Automate flows triggered by the agent
- Environment Variables (one per environment-specific configuration value)
- Any Dataverse tables created for the agent

**Do NOT include**:
- Connection references (connections are created per-environment and mapped during import)
- Hardcoded configuration values — use Environment Variables instead

**Naming convention**: Use a solution publisher prefix to avoid naming collisions across teams. For Promethean Labs: `pml_` (e.g., `pml_DocumentAgent`).

## Solution Setup

```bash
# Install Power Platform CLI
npm install -g @microsoft/powerplatform-cli

# Authenticate
pac auth create --url https://{dev-org}.crm.dynamics.com

# Create a new solution (if not already created in the portal)
pac solution create \
  --name "DocumentAgent" \
  --publisher-name "PrometheanLabs" \
  --publisher-prefix "pml"
```

Add all components to the solution via the Power Platform Maker portal (Solutions → Add existing → Bot, Cloud flow, Custom connector, etc.) or via CLI:

```bash
# Add a flow to the solution
pac solution add-reference \
  --path . \
  --name "DocumentAgent" \
  --component-id {flow-guid} \
  --component-type 29
```

## Deployment Steps

### Step 1: Export from Dev

```bash
# Export as unmanaged (preserves editability in the target environment)
pac solution export \
  --path ./exports/agent-dev.zip \
  --name DocumentAgent \
  --managed false

# For production, export as managed (prevents direct edits in production)
pac solution export \
  --path ./exports/agent-prod.zip \
  --name DocumentAgent \
  --managed true
```

Commit the exported zip to source control. The zip is the deployment artifact.

### Step 2: Import to UAT

```bash
pac auth create --url https://{uat-org}.crm.dynamics.com

pac solution import \
  --path ./exports/agent-dev.zip \
  --environment {uat-env-id}
```

During import you will be prompted to:
1. **Map connection references** — select or create the UAT connections for each referenced connector (Azure AI Search, Power Automate HTTP, etc.)
2. **Set environment variable values** — provide UAT-specific values for each variable

Set environment variables before the import completes to avoid a second import cycle:

```bash
pac env set-variable \
  --name "pml_AzureSearchEndpoint" \
  --value "https://search-uat.search.windows.net" \
  --environment {uat-env-id}

pac env set-variable \
  --name "pml_AzureSearchIndexName" \
  --value "docs-uat" \
  --environment {uat-env-id}
```

### Step 3: UAT Validation

Before sign-off, run through this checklist with a business user (not the builder):

- [ ] Agent responds correctly to the top 10 representative questions
- [ ] Citations resolve to readable documents (SAS tokens or permissions are correct)
- [ ] Out-of-scope questions trigger the fallback, not hallucinated answers
- [ ] Authentication works for users in all expected Entra ID groups
- [ ] Power Automate flows complete successfully (check flow run history)
- [ ] Escalation path works end-to-end (escalation creates a ticket or notification)
- [ ] Telemetry is flowing (check Copilot Studio Analytics dashboard)

### Step 4: Promote to Production

```bash
pac auth create --url https://{prod-org}.crm.dynamics.com

pac solution import \
  --path ./exports/agent-prod.zip \
  --environment {prod-env-id}
```

Map production connections and set production environment variables:

```bash
pac env set-variable \
  --name "pml_AzureSearchEndpoint" \
  --value "https://search-prod.search.windows.net" \
  --environment {prod-env-id}
```

Publish the agent in the Copilot Studio portal after import completes. Solutions import in draft state — the agent is not live until published.

## Environment Variables Reference

Define all environment-specific configuration as Environment Variables. This makes the solution portable with no code changes between environments.

| Variable Name | Dev | UAT | Prod |
|--------------|-----|-----|------|
| `pml_AzureSearchEndpoint` | `https://search-dev.search.windows.net` | `https://search-uat.search.windows.net` | `https://search-prod.search.windows.net` |
| `pml_AzureSearchIndexName` | `docs-dev` | `docs-uat` | `docs` |
| `pml_OpenAIEndpoint` | `https://openai-dev.openai.azure.com` | `https://openai-uat.openai.azure.com` | `https://openai-prod.openai.azure.com` |
| `pml_MaxSearchResults` | `10` | `50` | `50` |

## Rollback

To roll back to the previous version, re-import the previous managed solution export:

```bash
pac solution import \
  --path ./exports/agent-prod-v1.2.0.zip \
  --environment {prod-env-id} \
  --upgrade
```

The `--upgrade` flag replaces the current solution version with the imported version. The previous agent configuration is restored.

**Keep your export artifacts**. Store every exported zip in source control or an artifact store tagged with the version. If you lose the export, you cannot roll back.

## Automating with GitHub Actions

For teams doing frequent deployments, automate with the [Power Platform Actions](https://github.com/microsoft/powerplatform-actions):

```yaml
# .github/workflows/deploy-uat.yml
name: Deploy to UAT

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Power Platform CLI
        run: npm install -g @microsoft/powerplatform-cli

      - name: Authenticate to UAT
        run: |
          pac auth create \
            --url ${{ secrets.UAT_ORG_URL }} \
            --applicationId ${{ secrets.SP_CLIENT_ID }} \
            --clientSecret ${{ secrets.SP_CLIENT_SECRET }} \
            --tenantId ${{ secrets.TENANT_ID }}

      - name: Import Solution
        run: |
          pac solution import \
            --path ./exports/agent-dev.zip \
            --environment ${{ secrets.UAT_ENV_ID }}
```

The service principal used for CI/CD authentication needs the **System Administrator** or **System Customizer** role in the target environment.

## Common Deployment Failures

| Error | Cause | Fix |
|-------|-------|-----|
| "Missing dependency" on import | Flow or connector not in the solution | Add the component to the solution before export |
| Connection reference mapping fails | Connection not created in target environment | Create the connection manually before import |
| Environment variable not found | Variable not added to the solution | Add the variable to the solution in the source environment |
| Agent not publishing after import | Content moderation policy blocking generative content | Review the agent's topic for policy violations or enable content moderation exceptions |
| Managed solution import fails with version conflict | Lower version being imported over higher version | Export with a higher version number, or use `--upgrade` flag |
| Flow fails post-import with 401 | Managed identity permissions not set in target | Assign RBAC roles to the managed identity in the target Azure subscription |
