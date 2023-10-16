from convisoappsec.flow.graphql_api.beta.models.issues.normalize import Normalize

class CreateScaFindingInput:
    def __init__(
        self,
        asset_id,
        title,
        description,
        severity,
        solution,
        reference,
        file_name,
        affected_version,
        package,
        cve,
    ):
        self.asset_id = asset_id
        self.title = title
        self.description = description
        self.severity = Normalize.normalize_severity(severity)
        self.solution = solution
        self.reference = reference
        self.file_name = file_name
        self.affected_version = affected_version
        self.package = package

        if type(cve) is list:
            self.cve = ' , '.join(cve)
        elif type(cve) is str:
            self.cve = cve
        else:
            self.cve = ""

    def to_graphql_dict(self):
        """
        This function returns a dictionary containing various attributes of an
        asset in a GraphQL format.
        """
        return {
			"assetId": int(self.asset_id),
			"title": self.title,
			"description": self.description,
			"severity": self.severity,
			"solution": self.solution,
			"reference": self.reference,
			"fileName": self.file_name,
			"affectedVersion": self.affected_version,
			"package": self.package,
			"cve": self.cve,
		}
