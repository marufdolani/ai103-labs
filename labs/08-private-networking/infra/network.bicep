// Lab 08: a network-isolated Foundry resource + storage reachable only through private endpoints.
// Deploys alongside the shared platform (it doesn't change it). Cost: ~USD 0.03/hour for 2 private endpoints.
targetScope = 'resourceGroup'

param location string = resourceGroup().location

@description('Object ID of the learner (gets Foundry User on the isolated resource so you can prove the network blocks you, not RBAC).')
param principalId string = ''

var token = substring(uniqueString(resourceGroup().id, 'lab08'), 0, 6)
var isoName = 'aif-iso-${token}'
var storageName = 'stiso${token}${substring(uniqueString(resourceGroup().id), 0, 6)}'

resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: 'vnet-ai103-${token}'
  location: location
  properties: {
    addressSpace: { addressPrefixes: [ '10.80.0.0/16' ] }
    subnets: [
      { name: 'private-endpoints', properties: { addressPrefix: '10.80.1.0/24' } }
      { name: 'apps', properties: { addressPrefix: '10.80.2.0/24' } }
    ]
  }
}

resource isolated 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: isoName
  location: location
  kind: 'AIServices'
  sku: { name: 'S0' }
  identity: { type: 'SystemAssigned' }
  properties: {
    customSubDomainName: isoName
    allowProjectManagement: true
    publicNetworkAccess: 'Disabled'
    networkAcls: { defaultAction: 'Deny' }
    disableLocalAuth: true
  }
}

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
  properties: {
    publicNetworkAccess: 'Disabled'
    allowSharedKeyAccess: false
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    networkAcls: { defaultAction: 'Deny', bypass: 'AzureServices' }
  }
}

var aiZones = [ 'privatelink.cognitiveservices.azure.com', 'privatelink.openai.azure.com', 'privatelink.services.ai.azure.com' ]

resource zones 'Microsoft.Network/privateDnsZones@2024-06-01' = [for z in concat(aiZones, [ 'privatelink.blob.${environment().suffixes.storage}' ]): {
  name: z
  location: 'global'
}]

resource links 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2024-06-01' = [for (z, i) in concat(aiZones, [ 'privatelink.blob.${environment().suffixes.storage}' ]): {
  parent: zones[i]
  name: 'link-${vnet.name}'
  location: 'global'
  properties: { virtualNetwork: { id: vnet.id }, registrationEnabled: false }
}]

resource peFoundry 'Microsoft.Network/privateEndpoints@2024-05-01' = {
  name: 'pe-${isoName}'
  location: location
  properties: {
    subnet: { id: vnet.properties.subnets[0].id }
    privateLinkServiceConnections: [ {
      name: 'foundry'
      properties: { privateLinkServiceId: isolated.id, groupIds: [ 'account' ] }
    } ]
  }
}

resource peFoundryDns 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-05-01' = {
  parent: peFoundry
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [for (z, i) in aiZones: {
      name: replace(z, '.', '-')
      properties: { privateDnsZoneId: zones[i].id }
    }]
  }
}

resource peBlob 'Microsoft.Network/privateEndpoints@2024-05-01' = {
  name: 'pe-${storageName}-blob'
  location: location
  properties: {
    subnet: { id: vnet.properties.subnets[0].id }
    privateLinkServiceConnections: [ {
      name: 'blob'
      properties: { privateLinkServiceId: storage.id, groupIds: [ 'blob' ] }
    } ]
  }
}

resource peBlobDns 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-05-01' = {
  parent: peBlob
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [ { name: 'blob', properties: { privateDnsZoneId: zones[3].id } } ]
  }
}

resource learnerRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(principalId)) {
  name: guid(isolated.id, principalId, '53ca6127-db72-4b80-b1b0-d745d6d5456d')
  scope: isolated
  properties: {
    principalId: principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '53ca6127-db72-4b80-b1b0-d745d6d5456d')
  }
}

output ISOLATED_FOUNDRY_NAME string = isolated.name
output ISOLATED_FOUNDRY_ID string = isolated.id
output ISOLATED_FOUNDRY_ENDPOINT string = 'https://${isoName}.cognitiveservices.azure.com/'
output ISOLATED_STORAGE_ID string = storage.id
output ISOLATED_PE_ID string = peFoundry.id
output ISOLATED_VNET_ID string = vnet.id
