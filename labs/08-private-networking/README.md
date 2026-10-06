# Lab 08 · Network-isolate the AI platform

**Scenario.** Contoso's regulated business unit requires that no AI endpoint is reachable from the internet. You'll deploy a Foundry resource and storage reachable only through **private endpoints** in a VNet, then prove from your laptop that the public path is closed.

**Exam objectives.** D1 › *Configure security, including private networking*; *design Azure infrastructure for AI apps and agent-based solutions*.

**You will learn**
- `publicNetworkAccess: Disabled` + `networkAcls.defaultAction: Deny` on the Foundry resource.
- Private endpoint `groupIds: ['account']` and the **three** private DNS zones a Foundry resource needs: `privatelink.cognitiveservices.azure.com`, `privatelink.openai.azure.com`, `privatelink.services.ai.azure.com`.
- How to verify isolation: ARM configuration, private endpoint approval, and a blocked call from outside.

## Set up (extra infrastructure, ~5 minutes)
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmarufdolani%2Fai103-labs%2Fmain%2Flabs%2F08-private-networking%2Finfra%2Fazuredeploy.json)
```bash
source .env
az deployment group create -g $AZURE_RESOURCE_GROUP -n lab08-network \
  -f labs/08-private-networking/infra/network.bicep -p principalId=$(az ad signed-in-user show --query id -o tsv)
./lab env-merge $AZURE_RESOURCE_GROUP lab08-network
```
You get **Foundry User** on the isolated resource, so any refusal you see is the *network*, not RBAC.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Read `publicNetworkAccess`, `networkAcls.defaultAction` and private endpoint connection states from ARM. | That's what an auditor checks. |
| 2 | Read the private endpoint's NIC IP and FQDN records. | Inside the VNet, the FQDN resolves to this 10.80.x.x address. |
| 3 | Call the isolated endpoint from your machine with a valid token. | Expect **403** (public access disabled). |

## Run and test
```bash
./lab run 08 && ./lab validate 08      # one click: ./lab solve 08
```

## Explore
- Prove the private path: deploy a small VM or Azure Container Instance into the `apps` subnet and run the same call from there; it succeeds.
- **Agent Service with your own VNet** (standard setup) injects agent compute into a delegated subnet and keeps Cosmos DB, Storage and AI Search private too. Read *"Configure a private network for Foundry Agent Service"* on Microsoft Learn.
- `networkAcls.bypass: AzureServices` lets trusted Azure services (such as Search indexers using managed identity) through.

## Exam reflexes
- "No public internet exposure" → **private endpoints + public network access disabled + private DNS zones**.
- Agent state in your own resources inside a VNet → **standard agent setup with BYO VNet**.
- Private endpoint ≠ service endpoint: private endpoints give a private IP in your VNet.

## Clean up
```bash
az resource delete --ids $ISOLATED_PE_ID $ISOLATED_FOUNDRY_ID $ISOLATED_STORAGE_ID
```
Or simply keep it until `azd down`.
