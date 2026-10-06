// Lab 11: a custom guardrail (RAI policy) with strict thresholds, Prompt Shields,
// protected-material detection and a custom blocklist, applied to a new 'guarded' deployment.
targetScope = 'resourceGroup'

@description('FOUNDRY_ACCOUNT_NAME from .env')
param foundryAccountName string
param chatModel string = 'gpt-5.4-mini'
param chatModelVersion string = '2026-03-17'

resource foundry 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: foundryAccountName
}

resource blocklist 'Microsoft.CognitiveServices/accounts/raiBlocklists@2025-06-01' = {
  parent: foundry
  name: 'competitors'
  properties: { description: 'Competitor brand names marketing must never mention' }
}

resource items 'Microsoft.CognitiveServices/accounts/raiBlocklists/raiBlocklistItems@2025-06-01' = [for (term, i) in [ 'Fabrikam', 'Northwind Traders' ]: {
  parent: blocklist
  name: 'item${i}'
  properties: { pattern: term, isRegex: false }
}]

var harms = [ 'Hate', 'Sexual', 'Violence', 'Selfharm' ]
var promptHarmFilters = [for h in harms: { name: h, enabled: true, blocking: true, severityThreshold: 'Low', source: 'Prompt' }]
var completionHarmFilters = [for h in harms: { name: h, enabled: true, blocking: true, severityThreshold: 'Low', source: 'Completion' }]

resource policy 'Microsoft.CognitiveServices/accounts/raiPolicies@2025-06-01' = {
  parent: foundry
  name: 'strict-guardrail'
  properties: {
    basePolicyName: 'Microsoft.DefaultV2'
    mode: 'Blocking'
    contentFilters: concat(
      promptHarmFilters,
      completionHarmFilters,
      [
        { name: 'Jailbreak', enabled: true, blocking: true, source: 'Prompt' }
        { name: 'Indirect Attack', enabled: true, blocking: true, source: 'Prompt' }
        { name: 'Protected Material Text', enabled: true, blocking: true, source: 'Completion' }
        { name: 'Protected Material Code', enabled: true, blocking: false, source: 'Completion' }
      ]
    )
    customBlocklists: [
      { blocklistName: blocklist.name, blocking: true, source: 'Prompt' }
      { blocklistName: blocklist.name, blocking: true, source: 'Completion' }
    ]
  }
  dependsOn: [ items ]
}

resource guarded 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: foundry
  name: 'guarded-chat'
  sku: { name: 'GlobalStandard', capacity: 20 }
  properties: {
    model: { format: 'OpenAI', name: chatModel, version: chatModelVersion }
    raiPolicyName: policy.name
  }
}

output GUARDED_MODEL string = guarded.name
output GUARDRAIL_POLICY string = policy.name
