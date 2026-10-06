// Lab 06: API Management (Basic v2) as an AI gateway in front of the Foundry resource.
// - Managed identity to the backend (no model keys anywhere)
// - Per-subscription token-per-minute limits with llm-token-limit
// - Two consumer subscriptions (app-a, app-b) to show isolation
targetScope = 'resourceGroup'

param location string = resourceGroup().location

@description('Name of the existing Foundry resource (FOUNDRY_ACCOUNT_NAME in .env).')
param foundryAccountName string

@description('Email for the API Management publisher (required by APIM).')
param publisherEmail string

param publisherName string = 'Contoso AI Platform'

@description('Token budget per consumer per minute.')
param tokensPerMinute int = 2000

var apimName = 'apim-ai103-${substring(uniqueString(resourceGroup().id), 0, 8)}'
var openAIUserRole = '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'

resource foundry 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: foundryAccountName
}

resource apim 'Microsoft.ApiManagement/service@2024-05-01' = {
  name: apimName
  location: location
  sku: { name: 'BasicV2', capacity: 1 }
  identity: { type: 'SystemAssigned' }
  properties: {
    publisherEmail: publisherEmail
    publisherName: publisherName
  }
}

resource apimToFoundry 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(foundry.id, apim.id, openAIUserRole)
  scope: foundry
  properties: {
    principalId: apim.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', openAIUserRole)
  }
}

resource api 'Microsoft.ApiManagement/service/apis@2024-05-01' = {
  parent: apim
  name: 'openai'
  properties: {
    displayName: 'Foundry OpenAI v1'
    path: 'openai'
    protocols: [ 'https' ]
    serviceUrl: 'https://${foundryAccountName}.openai.azure.com/openai'
    subscriptionRequired: true
  }
}

resource opPost 'Microsoft.ApiManagement/service/apis/operations@2024-05-01' = {
  parent: api
  name: 'post-any'
  properties: { displayName: 'POST any', method: 'POST', urlTemplate: '/*' }
}

resource opGet 'Microsoft.ApiManagement/service/apis/operations@2024-05-01' = {
  parent: api
  name: 'get-any'
  properties: { displayName: 'GET any', method: 'GET', urlTemplate: '/*' }
}

resource policy 'Microsoft.ApiManagement/service/apis/policies@2024-05-01' = {
  parent: api
  name: 'policy'
  properties: {
    format: 'rawxml'
    value: '<policies><inbound><base /><authentication-managed-identity resource="https://cognitiveservices.azure.com" /><llm-token-limit counter-key="@(context.Subscription.Id)" tokens-per-minute="${tokensPerMinute}" estimate-prompt-tokens="true" remaining-tokens-header-name="x-remaining-tokens" tokens-consumed-header-name="x-consumed-tokens" /></inbound><backend><base /></backend><outbound><base /></outbound><on-error><base /></on-error></policies>'
  }
}

resource subs 'Microsoft.ApiManagement/service/subscriptions@2024-05-01' = [for app in [ 'app-a', 'app-b' ]: {
  parent: apim
  name: app
  properties: {
    displayName: app
    scope: '/apis/${api.name}'
    state: 'active'
  }
}]

output APIM_GATEWAY_URL string = apim.properties.gatewayUrl
output APIM_RESOURCE_ID string = apim.id
output APIM_TOKENS_PER_MINUTE string = string(tokensPerMinute)
