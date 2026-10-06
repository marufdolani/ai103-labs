// azd entry point (subscription scope): creates the resource group, then the shared platform.
targetScope = 'subscription'

@minLength(1)
@maxLength(16)
@description('azd environment name, e.g. ai103')
param environmentName string

@minLength(1)
param location string

@description('Set automatically by azd to your signed-in user object ID.')
param principalId string = ''

// azd passes these as strings ("true"/"false") from environment variables.
param deployModelRouter string = 'true'
param deployImageModel string = 'false'
param deployVideoModel string = 'false'
param deployAudioModels string = 'false'
param deployLegacyChat string = 'false'
param principalType string = 'User'

resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-${environmentName}'
  location: location
  tags: { 'azd-env-name': environmentName, workload: 'ai103-labs' }
}

module core 'core.bicep' = {
  name: 'ai103-core'
  scope: rg
  params: {
    location: location
    environmentName: environmentName
    principalId: principalId
    principalType: principalType
    deployModelRouter: deployModelRouter == 'true'
    deployImageModel: deployImageModel == 'true'
    deployVideoModel: deployVideoModel == 'true'
    deployAudioModels: deployAudioModels == 'true'
    deployLegacyChat: deployLegacyChat == 'true'
  }
}

output AZURE_LOCATION string = core.outputs.AZURE_LOCATION
output AZURE_RESOURCE_GROUP string = core.outputs.AZURE_RESOURCE_GROUP
output AZURE_SUBSCRIPTION_ID string = core.outputs.AZURE_SUBSCRIPTION_ID
output FOUNDRY_ACCOUNT_NAME string = core.outputs.FOUNDRY_ACCOUNT_NAME
output FOUNDRY_RESOURCE_ID string = core.outputs.FOUNDRY_RESOURCE_ID
output FOUNDRY_ENDPOINT string = core.outputs.FOUNDRY_ENDPOINT
output FOUNDRY_OPENAI_ENDPOINT string = core.outputs.FOUNDRY_OPENAI_ENDPOINT
output FOUNDRY_PROJECT_NAME string = core.outputs.FOUNDRY_PROJECT_NAME
output PROJECT_ENDPOINT string = core.outputs.PROJECT_ENDPOINT
output PROJECT_RESOURCE_ID string = core.outputs.PROJECT_RESOURCE_ID
output CHAT_MODEL string = core.outputs.CHAT_MODEL
output SMALL_MODEL string = core.outputs.SMALL_MODEL
output LARGE_MODEL string = core.outputs.LARGE_MODEL
output EMBEDDING_MODEL string = core.outputs.EMBEDDING_MODEL
output THROTTLED_MODEL string = core.outputs.THROTTLED_MODEL
output ROUTER_MODEL string = core.outputs.ROUTER_MODEL
output IMAGE_MODEL string = core.outputs.IMAGE_MODEL
output VIDEO_MODEL string = core.outputs.VIDEO_MODEL
output AUDIO_MODELS_ENABLED string = core.outputs.AUDIO_MODELS_ENABLED
output LEGACY_CHAT_MODEL string = core.outputs.LEGACY_CHAT_MODEL
output SEARCH_SERVICE_NAME string = core.outputs.SEARCH_SERVICE_NAME
output SEARCH_ENDPOINT string = core.outputs.SEARCH_ENDPOINT
output SEARCH_CONNECTION_NAME string = core.outputs.SEARCH_CONNECTION_NAME
output STORAGE_ACCOUNT_NAME string = core.outputs.STORAGE_ACCOUNT_NAME
output STORAGE_BLOB_ENDPOINT string = core.outputs.STORAGE_BLOB_ENDPOINT
output STORAGE_RESOURCE_ID string = core.outputs.STORAGE_RESOURCE_ID
output LOG_ANALYTICS_WORKSPACE_ID string = core.outputs.LOG_ANALYTICS_WORKSPACE_ID
output LOG_ANALYTICS_RESOURCE_ID string = core.outputs.LOG_ANALYTICS_RESOURCE_ID
output APPINSIGHTS_RESOURCE_ID string = core.outputs.APPINSIGHTS_RESOURCE_ID
output APPLICATIONINSIGHTS_CONNECTION_STRING string = core.outputs.APPLICATIONINSIGHTS_CONNECTION_STRING
