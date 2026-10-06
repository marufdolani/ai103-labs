# Lab 09 · Least-privilege RBAC for AI teams

**Scenario.** Contoso has four personas: app developers, a team lead who onboards developers, a platform admin who deploys models, and auditors. You'll read the built-in Foundry role definitions straight from Azure, compute what each one can actually do, and build a "least-privilege picker" the platform team can use for access requests.

**Exam objectives.** D1 › *Configure security, including … role policies*; *govern agent behaviour with … tool-access controls* (identity side).

**You will learn**
- The four Foundry roles (renamed in 2026): **Foundry User**, **Foundry Project Manager**, **Foundry Account Owner**, **Foundry Owner** (formerly "Azure AI …").
- `actions` (control plane) vs `dataActions` (data plane), `notActions`, and wildcard matching.
- Why Account Owner can deploy models but can't build agents, and why that split is deliberate.

## Set up
Nothing extra. Reading role definitions needs only Reader-level access.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Fetch each role definition from ARM (`roleDefinitions/{id}`). | Ground truth, not documentation memory. |
| 2 | `allows(role, operation)`: match `actions`/`dataActions` with wildcards, minus `notActions`/`notDataActions`. | This is how Azure evaluates permissions. |
| 3 | `least_privilege(needs)`: the lowest-ranked role that allows every needed operation. | Turns policy into an answer. |
| 4 | List *your* role assignments on the Foundry resource. | Verify what the platform template granted you. |

## Run and test
```bash
./lab run 09 && ./lab validate 09      # one click: ./lab solve 09
```

## Explore
- Create a test service principal (`az ad sp create-for-rbac --name ai103-dev --role "Foundry User" --scopes $FOUNDRY_RESOURCE_ID`), sign in as it and try to create a deployment: you'll get **403 AuthorizationFailed**.
- Project Manager and Account Owner use **conditional role-assignment delegation (ABAC)**: they can only assign specific roles.

## Exam reflexes
- Developer builds/evaluates agents, no model deployment → **Foundry User**.
- Lead manages a project, publishes agents, assigns Foundry User → **Foundry Project Manager**.
- Admin creates Foundry resources and deploys models → **Foundry Account Owner**.
- App identity querying a search index → **Search Index Data Reader**. Indexer reading blobs → **Storage Blob Data Reader**.

## Clean up
Delete any service principal you created: `az ad sp delete --id <appId>`.
