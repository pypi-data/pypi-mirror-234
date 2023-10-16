CREATE_OR_UPDATE_AGENT_MUTATION = """
mutation createOrUpdateAgent($authType:AuthTypeEnum!, $agentType:AgentTypeEnum!, $credentials:JSONString!, $endpoint:String!, $storageType:StorageTypeEnum!, $platform:PlatformTypeEnum, $upgradeable:Boolean, $wrapperType:String, $wrapperVersion:String, $imageVersion:String, $skipValidation:Boolean, $agentId:UUID, $dataCollectorId:UUID) {
  createOrUpdateAgent(authType:$authType, agentType:$agentType, credentials:$credentials, endpoint:$endpoint, platform:$platform, storageType:$storageType, dataCollectorId:$dataCollectorId, agentId:$agentId, skipValidation:$skipValidation, upgradeable:$upgradeable, wrapperType:$wrapperType, wrapperVersion:$wrapperVersion, imageVersion:$imageVersion) {
    agentId
    validationResult{
      success
      warnings{
        stackTrace
        friendlyMessage
        resolution
        cause
      }
      errors{
        stackTrace
        friendlyMessage
        resolution
        cause
      }
      validationName
      description
    }
  }  
}
"""

DELETE_AGENT_MUTATION = """
mutation deleteAgent($agentId:UUID!) {
  deleteAgent(agentId:$agentId) {
    success
  }
}
"""
