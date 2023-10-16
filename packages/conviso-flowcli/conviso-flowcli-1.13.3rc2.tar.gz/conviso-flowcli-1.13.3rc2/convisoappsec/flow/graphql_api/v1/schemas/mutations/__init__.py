CREATE_ASSET = """ 
mutation (
  $companyId: Int!, 
  $name: String!, 
  $scanType: AssetScan!
) {
  createAsset(
    input: { 
      companyId: $companyId, 
      name: $name, 
      scanType: $scanType
    }
  ) {
    asset {
      id
      name
      createdAt
    }
    errors
  }
}
"""

CREATE_PROJECT = """
mutation (
  $companyId: Int!,
  $assetsIds: [Int!],
  $label: String!,
  $startDate: ISO8601Date!,
  $goal: String!,
  $scope: String!
) {
  createProject (
    input: {
      companyId: $companyId,
      assetsIds: $assetsIds,
      label: $label,
      startDate: $startDate,
      typeId: 33,
      playbooksIds: 1,
      goal: $goal,
      scope: $scope
    }
  ) {
    project {
      id
      apiCode
      assets {
        id
      }
    }
  }
}
"""

UPDATE_PROJECT = """
mutation (
  $projectId: ID!,
  $assetsIds: [Int!]
) {
  updateProject (
    input: {
      id: $projectId,
      assetsIds: $assetsIds
    }
  ) {
    msg
  }
}
"""
