from convisoappsec.flowcli.common import CreateDeployException
from convisoappsec.logger import LOGGER
from convisoappsec.flowcli.projects.ls import Projects
from convisoappsec.flowcli.companies.ls import Companies
from convisoappsec.flow.graphql_api.v1.models.asset import AssetInput
from convisoappsec.flow.graphql_api.v1.models.project import CreateProjectInput, UpdateProjectInput
from convisoappsec.flow.graphql_api.v1.client import ConvisoGraphQLClient
from convisoappsec.common import safe_join_url
from convisoappsec.common.git_data_parser import GitDataParser
from .context import pass_flow_context


class RequirementsVerifier:

    @staticmethod
    @pass_flow_context
    def list_assets(flow_context, company_id, asset_name, scan_type):
        conviso_api = flow_context.create_conviso_graphql_client()

        asset_model = AssetInput(
            int(company_id),
            asset_name,
            scan_type
        )

        return conviso_api.assets.list_assets(asset_model)

    @staticmethod
    @pass_flow_context
    def create_asset(flow_context, company_id, asset_name, scan_type):
        conviso_api = flow_context.create_conviso_graphql_client()

        asset_model = AssetInput(
            int(company_id),
            asset_name,
            scan_type
        )

        return conviso_api.assets.create_asset(asset_model)

    @staticmethod
    @pass_flow_context
    def create_project(flow_context, company_id, asset_id, label):
        conviso_api = flow_context.create_conviso_graphql_client()

        project_model = CreateProjectInput(
            company_id,
            asset_id,
            label
            )
        
        return conviso_api.projects.create_project(project_model)

    @staticmethod
    @pass_flow_context
    def update_project(flow_context, project_id, asset_id):
        conviso_api = flow_context.create_conviso_graphql_client()

        project_model = UpdateProjectInput(
            project_id,
            asset_id,
        )

        conviso_api.projects.update_project(project_model)

    @staticmethod
    @pass_flow_context
    def prepare_context(flow_context, context, from_ast=False):
        """due to the new vulnerability management we need to do some checks before continuing the flow
        """
        project_code = context.params['project_code']
        new_management_flag = 'CONVISO_NEW_ISSUE_MANAGEMENT_ALLOWED_COMPANY'
        asset_target = None

        if from_ast is True:
            context.params['from_ast'] = True

        if project_code:
            projects = Projects()
            projects_filtered = projects.ls(
                flow_context=flow_context,
                project_code=project_code
                )

            if len(projects_filtered) == 0:
                raise CreateDeployException("Project doesn't exists!")

            LOGGER.info('Project found ...')

            project = projects_filtered[0]
            custom_features = project['company']['customFeatures']

            if not new_management_flag in custom_features:
                context.params['experimental'] = False

                return context

            assets = project['assets']
            asset_name = GitDataParser(context.params['repository_dir']).parse_name()

            if len(assets) == 0:
                LOGGER.info('Asset not found, creating ...')
                asset_target = RequirementsVerifier.create_asset(project['company']['id'], asset_name, 'SAST')
                RequirementsVerifier.update_project(project['id'], asset_target['id'])

            elif len(assets) == 1:
                LOGGER.info('Asset found ...')
                asset_target = assets[0]
            elif len(assets) > 1:
                for asset in assets:
                    if asset['name'] == asset_name:
                        LOGGER.info('Asset found ...')
                        asset_target = asset
                        break

            if not asset_target:
                LOGGER.info('Asset not found')
                raise CreateDeployException("Sorry, was not possible find the asset")

            context.params['asset_id'] = asset_target['id']
            context.params['experimental'] = True

            return context
        else:
            companies = Companies()
            company_id = context.params['company_id']

            if company_id is not None:
                companies_filtered = [companies.ls(flow_context, company_id=company_id)]
            else:
                companies_filtered = companies.ls(flow_context)

            if len(companies_filtered) > 1:
                raise CreateDeployException("Deploy not created. You have access to multiple companies, specify one using CONVISO_COMPANY_ID")

            company = companies_filtered[0]
            company_id = company['id']

            if new_management_flag not in company['customFeatures']:
                error_msg = "Deploy not created. The company '{}' does not have access to the new vulnerability management".format(company['label'])
                raise CreateDeployException(error_msg)

            asset_name = GitDataParser(context.params['repository_dir']).parse_name()

            if 'input_file' in context.params:
                # when is a execution from sarif only create an asset
                asset = RequirementsVerifier.create_asset(company['id'], asset_name, 'SAST')

                context.params['asset_id'] = asset['id']
                context.params['experimental'] = True

                return context

            project_label = asset_name + '_ast'
            projects = Projects()
            projects_filtered = projects.ls(
                flow_context=flow_context,
                project_label=project_label,
                company_id=company_id
            )

            if len(projects_filtered) == 1:
                project = projects_filtered[0]
                assets = project['assets']

                if len(assets) > 0:
                    for asset in assets:
                        if asset['name'] == asset_name:
                            LOGGER.info('Asset found ...')
                            asset_target = asset
                            break

                if not asset_target:
                    LOGGER.info('Asset not found, creating ...')
                    asset_target = RequirementsVerifier.create_asset(project['company']['id'], asset_name, 'SAST')
                    RequirementsVerifier.update_project(project['id'], asset_target['id'])

                context.params['project_code'] = project['apiCode']
                context.params['asset_id'] = asset_target['id']
                context.params['experimental'] = True

                return context
            elif not len(projects_filtered):
                LOGGER.info('Creating some things ...')
                asset = RequirementsVerifier.create_asset(company['id'], asset_name, 'SAST')
                project = RequirementsVerifier.create_project(company['id'], asset['id'], project_label)

                context.params['project_code'] = project['apiCode']
                context.params['asset_id'] = asset['id']
                context.params['experimental'] = True

                return context
            else:
                raise CreateDeployException("Deploy not created. More than one project found, you have specify a project code")
