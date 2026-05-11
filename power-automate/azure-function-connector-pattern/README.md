# Power Automate: Azure Function Connector Pattern for Private ILB ASE

How to call an Azure Function deployed inside an Internal Load Balancer App Service Environment (ILB ASE) from Power Automate, when the function has no public internet exposure.

## The Problem

An ILB ASE places all hosted apps on a private VNet with no inbound internet access. The internal load balancer IP is only routable from within the VNet or peered networks. Power Automate's cloud service cannot reach it directly — standard HTTP actions will time out or return connection errors.

The standard Azure Function connector in Power Platform also cannot reach private endpoints.

## Architecture Options

### Option A: Azure API Management as Gateway (Recommended)

```
Power Automate
    │
    ▼ (public HTTPS, OAuth2 subscription key)
Azure API Management (Developer/Standard tier)
    │  VNet integration — internal mode or external with backend policy
    ▼ (private VNet, internal DNS resolution)
ILB ASE — Azure Function App
```

APIM exposes a public HTTPS endpoint, validates authentication, and proxies to the private Azure Function backend. The Power Platform Custom Connector points to APIM's public URL.

**Why this is recommended:**
- Single place to manage auth, rate limiting, IP filtering, and response caching
- APIM can be integrated with Entra ID as the OAuth2 provider for the custom connector
- Centralizes logging and diagnostics for all inbound calls to private functions
- No changes required to the Azure Function itself

**Setup steps:**

1. **Configure APIM with VNet integration**
   - Developer tier: supports VNet injection for internal testing
   - Standard tier: required for production (supports external mode with backend routing to private IPs)

2. **Add the Azure Function as an APIM backend**
   ```json
   {
     "name": "extraction-backend",
     "url": "http://{ilb-internal-ip}/api",
     "protocol": "http",
     "tls": { "validateCertificateChain": false, "validateCertificateName": false }
   }
   ```
   Use the internal ILB IP or the private DNS hostname (e.g., `myapp.myase.appserviceenvironment.net`).

3. **Configure an APIM inbound policy** for authentication:
   ```xml
   <inbound>
     <validate-jwt header-name="Authorization" failed-validation-httpcode="401">
       <openid-config url="https://login.microsoftonline.com/{tenant}/.well-known/openid-configuration"/>
       <audiences><audience>{app-id-uri}</audience></audiences>
     </validate-jwt>
     <set-backend-service backend-id="extraction-backend" />
   </inbound>
   ```

4. **Create a Custom Connector in Power Platform**
   - Base URL: APIM's public URL (`https://{apim-name}.azure-api.net`)
   - Authentication: OAuth2 with Entra ID as the identity provider
   - Import the API definition from APIM (OpenAPI export)

---

### Option B: On-Premises Data Gateway (Simpler, No APIM Cost)

```
Power Automate
    │
    ▼ (encrypted tunnel via Azure Relay)
On-Premises Data Gateway (installed on a VM in the VNet)
    │ (private network call)
    ▼
ILB ASE — Azure Function App
```

The on-premises data gateway establishes an outbound connection to Azure Relay. Power Automate routes calls through this tunnel to reach private resources.

**When to use this option:**
- Existing data gateway already deployed for other connectors (Power BI, SQL Server)
- Budget constraints — no APIM license needed
- Lower traffic volume where APIM throughput isn't needed

**Limitations:**
- Higher latency than APIM (relay adds 100–300ms round-trip overhead)
- No API-level rate limiting, IP filtering, or response caching
- Gateway VM is an additional infrastructure dependency to manage
- Custom Connector with on-premises gateway has limited authentication options

**Setup:**
1. Install the [On-premises data gateway](https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-install) on a Windows VM inside the VNet (or a peered VNet with a route to the ILB ASE)
2. Register the gateway in Power Platform Admin Center
3. Create a Custom Connector using the gateway as the data gateway for the HTTP connection
4. Point the connector base URL to the ILB ASE internal hostname

---

### Option C: VNet-Injected Power Platform Environment (Premium)

Power Platform Premium environments support VNet injection, giving flows a dedicated subnet inside your Azure VNet. Flows in a VNet-injected environment can call private endpoints directly.

**Requirements:** Power Platform P2 or higher license per flow maker and runner.

**When to use:** Greenfield enterprise deployments where the licensing cost is acceptable and minimizing infrastructure components is a priority.

---

## Custom Connector Configuration (Option A)

The Custom Connector OpenAPI definition for the APIM-fronted Azure Function:

```yaml
swagger: "2.0"
info:
  title: Document Extraction API
  version: "1.0"
host: "{apim-name}.azure-api.net"
basePath: /extraction
schemes: [https]
securityDefinitions:
  oauth2:
    type: oauth2
    flow: accessCode
    authorizationUrl: https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize
    tokenUrl: https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
    scopes:
      "{app-id-uri}/.default": Access the Document Extraction API
paths:
  /extract:
    post:
      summary: Extract content from a document
      operationId: ExtractClauses
      parameters:
        - in: body
          name: body
          schema:
            type: object
            required: [document_url, schema_name]
            properties:
              document_url:
                type: string
                description: Blob URL of the document to extract from
              schema_name:
                type: string
                description: Name of the extraction schema to apply
      responses:
        "200":
          description: Extraction result
        "400":
          description: Validation error
        "500":
          description: Extraction failed
```

## NSG Rules Required

For the ILB ASE to receive traffic from APIM:

| Priority | Name | Direction | Source | Destination | Port | Action |
|----------|------|-----------|--------|-------------|------|--------|
| 100 | Allow-APIM-Inbound | Inbound | APIM subnet or IP | ASE subnet | 80, 443 | Allow |
| 200 | Allow-ASE-Management | Inbound | AppServiceManagement | Any | 454-455 | Allow |
| 300 | Allow-Load-Balancer | Inbound | AzureLoadBalancer | Any | Any | Allow |

The ASE management ports (454-455) are required for the App Service infrastructure to function — do not block them.

## Private DNS for the ILB ASE

The ILB ASE uses a custom DNS suffix (e.g., `myase.appserviceenvironment.net`). Within the VNet, this DNS suffix must resolve to the ILB's private IP.

```bash
# Create a private DNS zone for the ASE suffix
az network private-dns zone create \
  --resource-group {rg} \
  --name "myase.appserviceenvironment.net"

# Link it to the VNet
az network private-dns link vnet create \
  --resource-group {rg} \
  --zone-name "myase.appserviceenvironment.net" \
  --name "ase-dns-link" \
  --virtual-network {vnet-id} \
  --registration-enabled false

# Add A record pointing to the ILB private IP
az network private-dns record-set a add-record \
  --resource-group {rg} \
  --zone-name "myase.appserviceenvironment.net" \
  --record-set-name "*" \
  --ipv4-address {ilb-private-ip}
```

APIM must be configured to use the VNet's DNS server (or a custom DNS forwarder) to resolve the ASE hostname correctly when routing requests to the backend.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Custom Connector test returns timeout | APIM cannot reach ILB ASE | Check NSG rules; confirm APIM backend DNS resolves to ILB IP |
| `401` from custom connector | OAuth2 token invalid or wrong audience | Verify token audience matches `app-id-uri` in APIM JWT policy |
| `503` from APIM | Backend unhealthy — ASE function not responding | Check Function App is running; test direct call from a VM inside the VNet |
| DNS resolution fails from APIM | Private DNS zone not linked to APIM VNet | Link private DNS zone to the VNet containing APIM |
| Gateway-based connector shows "No data returned" | Gateway VM not in same VNet as ILB ASE | Move gateway to a VM with a route to the ASE subnet, or use VNet peering |
