GET_ASSETS = """ 
query (
  $id: ID!,
  $name: String!,
  $page: Int,
  $limit: Int
) {
  assets(
    companyId: $id
    page: $page
    limit: $limit
    search: {
      name: $name
    }
  ) {
    collection {
      id
      name
      createdAt
    }

    metadata {
      currentPage
      limitValue
      totalCount
      totalPages
    }
  }
}
"""

GET_PROJECTS = """
query (
  $project_code: String!,
  $project_label: String!,
  $company_id: ID!,
  $page: Int,
  $limit: Int
) {
  projects(
    page: $page
    limit: $limit
    params: {
      apiCodeEq: $project_code
      labelEq: $project_label
      scopeIdEq: $company_id
      showHidden: true
    }
  ) {
    collection {
      id
      apiCode
      assets {
        id
        name
      }
      company {
        id
        customFeatures
      }
    }
    metadata {
      currentPage
      limitValue
      totalCount
      totalPages
    }
  }
}
"""

GET_COMPANY = """
query get_company($company_id: ID!) {
	company(id: $company_id) {
		id
		label
		customFeatures
	}
}
"""

GET_COMPANIES = """
query Companies {
  companies (
    limit: 50, 
    order: label,
    orderType: ASC
		
  )  {
    collection {
      id
      label
      customFeatures
    }
  }
}
"""
