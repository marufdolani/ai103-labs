// =====================================================================================
// AI-103 Labs: shared platform (resource-group scope)
// One Foundry resource + project, model deployments, Azure AI Search, Storage,
// Log Analytics + Application Insights, project connections and least-privilege RBAC.
// Used by azd (infra/main.bicep) and by the "Deploy to Azure" button (azuredeploy.json).
// =====================================================================================
targetScope = 'resourceGroup'

@description('Azure region. East US 2 has the broadest model availability for these labs.')
param location string = resourceGroup().location

@description('Short environment name used to make resource names unique.')
@maxLength(16)
param environmentName string = 'ai103'

@description('Object ID of the person (or service principal) doing the labs. Leave empty to skip data-plane role assignments. Find it with: az ad signed-in-user show --query id -o tsv')
param principalId string = ''

@allowed([ 'User', 'ServicePrincipal', 'Group' ])
param principalType string = 'User'

@description('Keyless by default: API keys are disabled on the Foundry resource (lab 02 shows why).')
param disableLocalAuth bool = true

// ---------- Model choices (versions are parameters so you can roll forward without editing code) ----------
param chatModel string = 'gpt-5.4-mini'
param chatModelVersion string = '2026-03-17'
param chatCapacity int = 50

param smallModel string = 'gpt-5.4-nano'
param smallModelVersion string = '2026-03-17'
param smallCapacity int = 50

@description('Large multimodal model. Also the default Content Understanding completion model and evaluation judge.')
param largeModel string = 'gpt-5.2'
param largeModelVersion string = '2025-12-11'
param largeCapacity int = 30

param embeddingModel string = 'text-embedding-3-large'
param embeddingModelVersion string = '1'
param embeddingCapacity int = 50

param deployModelRouter bool = true
param modelRouterVersion string = '2025-11-18'

@description('Image generation (lab 39). Some image models need an access request; enable after approval.')
param deployImageModel bool = false
param imageModel string = 'gpt-image-1-mini'
param imageModelVersion string = '2025-10-06'

@description('Video generation with Sora (lab 40). Preview; check the version is not retired before enabling.')
param deployVideoModel bool = false
param videoModel string = 'sora-2'
param videoModelVersion string = '2025-12-08'

@description('Speech-capable models for labs 46-47 (transcribe, TTS, audio reasoning).')
param deployAudioModels bool = false

@description('Optional non-reasoning model so lab 18 can demonstrate temperature/top_p. Deprecated models may block new deployments in some subscriptions.')
param deployLegacyChat bool = false

var token = toLower(uniqueString(subscription().id, resourceGroup().id, environmentName))
var foundryName = 'aif-${environmentName}-${substring(token, 0, 6)}'
var projectName = 'proj-${environmentName}'
var searchName = 'srch-${environmentName}-${substring(token, 0, 6)}'
var storageName = take('st${replace(environmentName, '-', '')}${token}', 24)
var tags = { workload: 'ai103-labs', 'azd-env-name': environmentName }

// ---------- Monitoring ----------
resource logs 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-${environmentName}-${substring(token, 0, 6)}'
  location: location
  tags: tags
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-${environmentName}-${substring(token, 0, 6)}'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logs.id
    DisableLocalAuth: false
  }
}

// ---------- Storage (no shared keys, no public blobs) ----------
resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  tags: tags
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
  properties: {
    allowSharedKeyAccess: false
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storage
  name: 'default'
}

resource containers 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = [for c in [ 'labdata', 'translate-src', 'translate-out', 'search-docs' ]: {
  parent: blobService
  name: c
}]

// ---------- Azure AI Search (Basic, semantic ranker free tier, Entra + key auth) ----------
resource search 'Microsoft.Search/searchServices@2025-05-01' = {
  name: searchName
  location: location
  tags: tags
  sku: { name: 'basic' }
  identity: { type: 'SystemAssigned' }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'Default'
    semanticSearch: 'free'
    authOptions: { aadOrApiKey: { aadAuthFailureMode: 'http401WithBearerChallenge' } }
  }
}

// ---------- Microsoft Foundry resource + project ----------
resource foundry 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: foundryName
  location: location
  tags: tags
  kind: 'AIServices'
  sku: { name: 'S0' }
  identity: { type: 'SystemAssigned' }
  properties: {
    customSubDomainName: foundryName
    allowProjectManagement: true
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: disableLocalAuth
  }
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  parent: foundry
  name: projectName
  location: location
  tags: tags
  identity: { type: 'SystemAssigned' }
  properties: {
    displayName: 'AI-103 hands-on labs'
    description: 'Project used by all AI-103 labs'
  }
}

var coreDeployments = [
  { name: chatModel, model: chatModel, version: chatModelVersion, sku: 'GlobalStandard', capacity: chatCapacity }
  { name: smallModel, model: smallModel, version: smallModelVersion, sku: 'GlobalStandard', capacity: smallCapacity }
  { name: largeModel, model: largeModel, version: largeModelVersion, sku: 'GlobalStandard', capacity: largeCapacity }
  { name: embeddingModel, model: embeddingModel, version: embeddingModelVersion, sku: 'GlobalStandard', capacity: embeddingCapacity }
  // Deliberately tiny deployment (1K TPM) used by lab 04 to provoke HTTP 429s.
  { name: '${smallModel}-throttled', model: smallModel, version: smallModelVersion, sku: 'GlobalStandard', capacity: 1 }
]
var routerDeployments = deployModelRouter ? [ { name: 'model-router', model: 'model-router', version: modelRouterVersion, sku: 'GlobalStandard', capacity: 30 } ] : []
var imageDeployments = deployImageModel ? [ { name: imageModel, model: imageModel, version: imageModelVersion, sku: 'GlobalStandard', capacity: 1 } ] : []
var videoDeployments = deployVideoModel ? [ { name: videoModel, model: videoModel, version: videoModelVersion, sku: 'GlobalStandard', capacity: 1 } ] : []
var audioDeployments = deployAudioModels ? [
  { name: 'gpt-4o-mini-transcribe', model: 'gpt-4o-mini-transcribe', version: '2025-12-15', sku: 'GlobalStandard', capacity: 10 }
  { name: 'gpt-4o-mini-tts', model: 'gpt-4o-mini-tts', version: '2025-12-15', sku: 'GlobalStandard', capacity: 10 }
  { name: 'gpt-audio-mini', model: 'gpt-audio-mini', version: '2025-12-15', sku: 'GlobalStandard', capacity: 10 }
] : []
var legacyDeployments = deployLegacyChat ? [ { name: 'gpt-4.1-mini', model: 'gpt-4.1-mini', version: '2025-04-14', sku: 'GlobalStandard', capacity: 30 } ] : []
var allDeployments = concat(coreDeployments, routerDeployments, imageDeployments, videoDeployments, audioDeployments, legacyDeployments)

@batchSize(1)
resource deployments 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = [for d in allDeployments: {
  parent: foundry
  name: d.name
  sku: { name: d.sku, capacity: d.capacity }
  properties: {
    model: { format: 'OpenAI', name: d.model, version: d.version }
    versionUpgradeOption: 'NoAutoUpgrade'
    raiPolicyName: 'Microsoft.DefaultV2'
  }
  dependsOn: [ project ]
}]

// ---------- Project connections ----------
resource searchConnection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-06-01' = {
  parent: project
  name: 'search'
  properties: {
    category: 'CognitiveSearch'
    target: 'https://${search.name}.search.windows.net'
    authType: 'AAD'
    isSharedToAll: true
    metadata: { ApiType: 'Azure', ResourceId: search.id, location: location }
  }
}

resource appInsightsConnection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-06-01' = {
  parent: project
  name: 'appinsights'
  properties: {
    category: 'AppInsights'
    target: appInsights.id
    authType: 'ApiKey'
    isSharedToAll: true
    credentials: { key: appInsights.properties.ConnectionString }
    metadata: { ApiType: 'Azure', ResourceId: appInsights.id }
  }
}

resource storageConnection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-06-01' = {
  parent: project
  name: 'storage'
  properties: {
    category: 'AzureBlob'
    target: storage.properties.primaryEndpoints.blob
    authType: 'AAD'
    isSharedToAll: true
    metadata: { ApiType: 'Azure', ResourceId: storage.id, AccountName: storage.name, ContainerName: 'labdata' }
  }
}

// ---------- Diagnostics: Foundry logs + metrics to Log Analytics (labs 10, 16) ----------
resource foundryDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'to-log-analytics'
  scope: foundry
  properties: {
    workspaceId: logs.id
    logs: [ { categoryGroup: 'allLogs', enabled: true } ]
    metrics: [ { category: 'AllMetrics', enabled: true } ]
  }
}

resource searchDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'to-log-analytics'
  scope: search
  properties: {
    workspaceId: logs.id
    logs: [ { categoryGroup: 'allLogs', enabled: true } ]
    metrics: [ { category: 'AllMetrics', enabled: true } ]
  }
}

// ---------- RBAC (built-in role IDs) ----------
var roles = {
  foundryUser: '53ca6127-db72-4b80-b1b0-d745d6d5456d'
  cognitiveServicesUser: 'a97b65f3-24c7-4388-baec-2e87135dc908'
  cognitiveServicesOpenAIUser: '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'
  searchIndexDataContributor: '8ebe5a00-799e-43f5-93ac-243d3dce84a7'
  searchIndexDataReader: '1407120a-92aa-4202-b7e9-c0e197c71c8f'
  searchServiceContributor: '7ca78c08-252a-4471-8644-bb5ff32d4ba0'
  storageBlobDataContributor: 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
  storageBlobDataReader: '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1'
  logAnalyticsReader: '73c42c96-874c-492b-b04d-ab87d138a893'
  monitoringReader: '43d0d8ad-25c7-4714-9337-8ba259a9fe05'
}

var hasUser = !empty(principalId)

// You (the learner): build in the project, call all Foundry Tools, use Search + Storage data planes, read logs.
resource userFoundryUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (hasUser) {
  name: guid(foundry.id, principalId, roles.foundryUser)
  scope: foundry
  properties: { principalId: principalId, principalType: principalType, roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.foundryUser) }
}
resource userCogUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (hasUser) {
  name: guid(foundry.id, principalId, roles.cognitiveServicesUser)
  scope: foundry
  properties: { principalId: principalId, principalType: principalType, roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.cognitiveServicesUser) }
}
resource userSearchData 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (hasUser) {
  name: guid(search.id, principalId, roles.searchIndexDataContributor)
  scope: search
  properties: { principalId: principalId, principalType: principalType, roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.searchIndexDataContributor) }
}
resource userSearchSvc 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (hasUser) {
  name: guid(search.id, principalId, roles.searchServiceContributor)
  scope: search
  properties: { principalId: principalId, principalType: principalType, roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.searchServiceContributor) }
}
resource userBlob 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (hasUser) {
  name: guid(storage.id, principalId, roles.storageBlobDataContributor)
  scope: storage
  properties: { principalId: principalId, principalType: principalType, roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.storageBlobDataContributor) }
}
resource userLogs 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (hasUser) {
  name: guid(logs.id, principalId, roles.logAnalyticsReader)
  scope: logs
  properties: { principalId: principalId, principalType: principalType, roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.logAnalyticsReader) }
}
resource userMonitoring 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (hasUser) {
  name: guid(resourceGroup().id, principalId, roles.monitoringReader)
  properties: { principalId: principalId, principalType: principalType, roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.monitoringReader) }
}

// Search service identity: read blobs for indexers, call embedding/model deployments for integrated vectorization.
resource searchToBlob 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storage.id, search.id, roles.storageBlobDataReader)
  scope: storage
  properties: { principalId: search.identity.principalId, principalType: 'ServicePrincipal', roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.storageBlobDataReader) }
}
resource searchToFoundry 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(foundry.id, search.id, roles.cognitiveServicesUser)
  scope: foundry
  properties: { principalId: search.identity.principalId, principalType: 'ServicePrincipal', roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.cognitiveServicesUser) }
}
resource searchToOpenAI 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(foundry.id, search.id, roles.cognitiveServicesOpenAIUser)
  scope: foundry
  properties: { principalId: search.identity.principalId, principalType: 'ServicePrincipal', roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.cognitiveServicesOpenAIUser) }
}

// Foundry resource identity: storage for Document Translation / Content Understanding.
resource foundryToBlob 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storage.id, foundry.id, roles.storageBlobDataContributor)
  scope: storage
  properties: { principalId: foundry.identity.principalId, principalType: 'ServicePrincipal', roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.storageBlobDataContributor) }
}

// Project identity: agents use it for the Azure AI Search tool and knowledge grounding.
resource projectToSearchData 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(search.id, project.id, roles.searchIndexDataContributor)
  scope: search
  properties: { principalId: project.identity.principalId, principalType: 'ServicePrincipal', roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.searchIndexDataContributor) }
}
resource projectToSearchSvc 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(search.id, project.id, roles.searchServiceContributor)
  scope: search
  properties: { principalId: project.identity.principalId, principalType: 'ServicePrincipal', roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.searchServiceContributor) }
}
resource projectToBlob 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storage.id, project.id, roles.storageBlobDataContributor)
  scope: storage
  properties: { principalId: project.identity.principalId, principalType: 'ServicePrincipal', roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.storageBlobDataContributor) }
}

// ---------- Outputs (become environment variables / .env) ----------
output AZURE_LOCATION string = location
output AZURE_RESOURCE_GROUP string = resourceGroup().name
output AZURE_SUBSCRIPTION_ID string = subscription().subscriptionId
output FOUNDRY_ACCOUNT_NAME string = foundry.name
output FOUNDRY_RESOURCE_ID string = foundry.id
output FOUNDRY_ENDPOINT string = 'https://${foundryName}.cognitiveservices.azure.com/'
output FOUNDRY_OPENAI_ENDPOINT string = 'https://${foundryName}.openai.azure.com/'
output FOUNDRY_PROJECT_NAME string = project.name
output PROJECT_ENDPOINT string = 'https://${foundryName}.services.ai.azure.com/api/projects/${projectName}'
output PROJECT_RESOURCE_ID string = project.id
output CHAT_MODEL string = chatModel
output SMALL_MODEL string = smallModel
output LARGE_MODEL string = largeModel
output EMBEDDING_MODEL string = embeddingModel
output THROTTLED_MODEL string = '${smallModel}-throttled'
output ROUTER_MODEL string = deployModelRouter ? 'model-router' : ''
output IMAGE_MODEL string = deployImageModel ? imageModel : ''
output VIDEO_MODEL string = deployVideoModel ? videoModel : ''
output AUDIO_MODELS_ENABLED string = string(deployAudioModels)
output LEGACY_CHAT_MODEL string = deployLegacyChat ? 'gpt-4.1-mini' : ''
output SEARCH_SERVICE_NAME string = search.name
output SEARCH_ENDPOINT string = 'https://${search.name}.search.windows.net'
output SEARCH_CONNECTION_NAME string = searchConnection.name
output STORAGE_ACCOUNT_NAME string = storage.name
output STORAGE_BLOB_ENDPOINT string = storage.properties.primaryEndpoints.blob
output STORAGE_RESOURCE_ID string = storage.id
output LOG_ANALYTICS_WORKSPACE_ID string = logs.properties.customerId
output LOG_ANALYTICS_RESOURCE_ID string = logs.id
output APPINSIGHTS_RESOURCE_ID string = appInsights.id
output APPLICATIONINSIGHTS_CONNECTION_STRING string = appInsights.properties.ConnectionString
