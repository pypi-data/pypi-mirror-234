
CREATE_SAST_FINDING_INPUT = """ 
mutation createSastFinding($input: CreateSastFindingInput!) {
  createSastFinding(input: $input) {
    issue {
      id
    }
  }
}
"""

CREATE_SCA_FINDING_INPUT = """ 
mutation createScaFinding($input: CreateScaFindingInput!) {
	createScaFinding(input: $input) {
		issue {
			id
		}
	}
}
"""
