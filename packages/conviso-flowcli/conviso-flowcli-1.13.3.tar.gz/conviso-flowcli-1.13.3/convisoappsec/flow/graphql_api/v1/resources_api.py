from urllib.parse import urlparse

import jmespath

from convisoappsec.flow.graphql_api.v1.models.asset import AssetInput
from convisoappsec.flow.graphql_api.v1.models.project import CreateProjectInput, UpdateProjectInput
from convisoappsec.flow.graphql_api.v1.schemas import mutations, resolvers


class AssetsAPI(object):
    """ To operations on Asset's resources in Conviso Platform. """

    def __init__(self, conviso_graphql_client):
        self.__conviso_graphql_client = conviso_graphql_client

    def create_asset(self, asset_input: AssetInput):
        graphql_variables = asset_input.to_graphql_dict()

        graphql_body_response = self.__conviso_graphql_client.execute(
            mutations.CREATE_ASSET,
            graphql_variables
        )

        expected_path = 'createAsset.asset'

        asset = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return asset

    def get_by_company_id_or_name(self, company_id, asset_name, page, limit):
        graphql_variables = {
            "id": company_id,
            'name': asset_name,
            "page": page,
            "limit": limit
        }

        graphql_body_response = self.__conviso_graphql_client.execute(
            resolvers.GET_ASSETS,
            graphql_variables
        )

        expected_path = 'assets.collection'

        assets_by_company = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return assets_by_company

    def get_asset_url(self, company_id, asset_id):
        parsed_url = urlparse(self.__conviso_graphql_client.url)

        asset_path = '/scopes/{}/assets/{}'.format(
            company_id,
            asset_id
        )

        parsed_url = parsed_url._replace(path=asset_path)

        return parsed_url.geturl()

    def list_assets(self, params, page=1, limit=32):
        graphql_variables = {
            "id": params.company_id,
            "name": params.name,
            "page": page,
            "limit": limit
        }

        graphql_body_response = self.__conviso_graphql_client.execute(
            resolvers.GET_ASSETS,
            graphql_variables
        )

        expected_path = 'assets.collection'

        assets = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return assets

class ProjectsApi(object):
    """ To operations on Project's resources in Conviso Platform. """

    def __init__(self, conviso_graphql_client):
        self.__conviso_graphql_client = conviso_graphql_client

    def create_project(self, project_input: CreateProjectInput):
        graphql_variables = project_input.to_graphql_dict()

        graphql_body_response = self.__conviso_graphql_client.execute(
            mutations.CREATE_PROJECT,
            graphql_variables
        )

        expected_path = 'createProject.project'

        project = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return project

    def update_project(self, project_input: UpdateProjectInput):
        graphql_variables = project_input.to_graphql_dict()

        self.__conviso_graphql_client.execute(
            mutations.UPDATE_PROJECT,
            graphql_variables
        )

    def get_by_code_or_label(self, project_code, project_label, company_id, page=1, limit=32):
        graphql_variables = {
            "project_code": project_code,
            "project_label": project_label,
            "company_id": company_id,
            "page": page,
            "limit": limit
        }

        graphql_body_response = self.__conviso_graphql_client.execute(
            resolvers.GET_PROJECTS,
            graphql_variables
        )

        expected_path = 'projects.collection'

        projects = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return projects

class CompaniesApi(object):
    """ To operations on Companies resources in Conviso Platform. """

    def __init__(self, conviso_graphql_client):
        self.__conviso_graphql_client = conviso_graphql_client

    def get_company_by_id(self, company_id):
        graphql_variables = {
            "company_id": company_id,
        }

        graphql_body_response = self.__conviso_graphql_client.execute(
            resolvers.GET_COMPANY,
            graphql_variables
        )

        expected_path = 'company'
        company = jmespath.search(
            expected_path,
            graphql_body_response,
        )
        return company


    def get_companies(self, page=1, limit=10):
        graphql_variables = {
            "page": page,
            "limit": limit
        }

        graphql_body_response = self.__conviso_graphql_client.execute(
            resolvers.GET_COMPANIES,
            graphql_variables
        )

        expected_path = 'companies.collection'

        companies = jmespath.search(
            expected_path,
            graphql_body_response,
        )

        return companies
