import json
import click
import click_log
from convisoappsec.common.box import ContainerWrapper
from convisoappsec.common import strings
from convisoappsec.flow.graphql_api.beta.models.issues.sca import CreateScaFindingInput
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.common import (
    asset_id_option,
    on_http_error,
    project_code_option,
)
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.logger import LOGGER
from convisoappsec.common.graphql.errors import ReponseError
from convisoappsec.flowcli.requirements_verifier import RequirementsVerifier
from copy import deepcopy as clone


click_log.basic_config(LOGGER)


@click.command()
@click_log.simple_verbosity_option(LOGGER)
@project_code_option(
    help="Not required when --no-send-to-flow option is set",
    required=False
)
@asset_id_option(required=False)
@click.option(
    '-r',
    '--repository-dir',
    default=".",
    show_default=True,
    type=click.Path(
        exists=True,
        resolve_path=True,
    ),
    required=False,
    help="The source code repository directory.",
)
@click.option(
    "--send-to-flow/--no-send-to-flow",
    default=True,
    show_default=True,
    required=False,
    help="""Enable or disable the ability of send analysis result
    reports to flow. When --send-to-flow option is set the --project-code
    option is required""",
    hidden=True
)
@click.option(
    "--custom-sca-tags",
    hidden=True,
    required=False,
    multiple=True,
    type=(str, str),
    help="""It should be passed as <repository_name> <image_tag>. It accepts multiple values"""
)
@click.option(
    "--scanner-timeout",
    hidden=True,
    required=False,
    default=7200,
    type=int,
    help="Set timeout for each scanner"
)
@click.option(
    "--parallel-workers",
    hidden=True,
    required=False,
    default=2,
    type=int,
    help="Set max parallel workers"
)
@click.option(
    "--deploy-id",
    default=None,
    required=False,
    hidden=True,
    envvar=("CONVISO_DEPLOY_ID", "FLOW_DEPLOY_ID")
)
@click.option(
    '--experimental',
    default=False,
    is_flag=True,
    hidden=True,
    help="Enable experimental features.",
)
@click.option(
    "--company-id",
    required=False,
    envvar=("CONVISO_COMPANY_ID", "FLOW_COMPANY_ID"),
    help="Company ID on Conviso Platform",
)
@click.option(
    '--from-ast',
    default=False,
    is_flag=True,
    hidden=True,
    help="Internal use only.",
)
@help_option
@pass_flow_context
@click.pass_context
def run(
    context,
    flow_context,
    project_code,
    asset_id,
    company_id,
    repository_dir,
    send_to_flow,
    custom_sca_tags,
    scanner_timeout,
    parallel_workers,
    deploy_id,
    experimental,
    from_ast
):
    '''
      This command will perform SCA analysis at the source code. The analysis
      results can be reported or not to flow application.
    '''
    context.params['company_id'] = company_id if company_id is not None else None

    if not from_ast:
        prepared_context = RequirementsVerifier.prepare_context(clone(context))

        params_to_copy = [
            'project_code', 'asset_id', 'repository_dir', 'send_to_flow',
            'deploy_id', 'custom_sca_tags', 'scanner_timeout',
            'parallel_workers', 'experimental'
        ]

        for param_name in params_to_copy:
            context.params[param_name] = (
                locals()[param_name] or prepared_context.params[param_name]
            )

    perform_command(
        flow_context,
        context.params['project_code'],
        context.params['asset_id'],
        context.params['repository_dir'],
        context.params['send_to_flow'],
        context.params['custom_sca_tags'],
        context.params['scanner_timeout'],
        context.params['parallel_workers'],
        context.params['deploy_id'],
        context.params['experimental']
    )


def deploy_results_to_conviso(
    conviso_api, results_filepaths, project_code, deploy_id=None
):
    results_context = click.progressbar(
        results_filepaths, label="Sending SCA reports to Conviso Platform"
    )
    default_report_type = "sca"

    with results_context as reports:
        for report_name in reports:
            report_file = open(report_name)
            conviso_api.findings.create(
                project_code=project_code,
                commit_refs=None,
                finding_report_file=report_file,
                default_report_type=default_report_type,
                deploy_id=deploy_id,
            )
            report_file.close()
    pass


def deploy_results_to_conviso_beta(
    conviso_api, results_filepaths, asset_id
):
    results_context = click.progressbar(
        results_filepaths, label="Sending SCA reports to Conviso Platform"
    )

    duplicated_issues = 0

    with results_context as reports:
        for report_path in reports:
            report_file = open(report_path)
            report_content = json.load(report_file)
            issues = report_content.get("issues", [])

            for issue in issues:
                description = issue.get("description")

                if not description:
                    description = ""

                sanitezed_description = strings.parse_to_ascii(description)

                issue_model = CreateScaFindingInput(
                    asset_id = asset_id,
                    title = issue.get("title"),
                    description = sanitezed_description,
                    severity = issue.get("severity"),
                    solution = issue.get("solution"),
                    reference = parse_conviso_references(issue.get("references")),
                    file_name = issue.get("path"),
                    affected_version = issue.get("version"),
                    package = issue.get("component"),
                    cve = issue.get("cve", []),
                )

                try:
                    conviso_api.issues.create_sca(issue_model)
                except ReponseError as error:
                    if error.code == 'RECORD_NOT_UNIQUE':
                        duplicated_issues += 1
                    else:
                        raise(error)

    msg = "\U0001F4AC %s Issue/Issues ignored during duplication" % duplicated_issues
    LOGGER.info(msg)


def parse_conviso_references(references=[]):
    DIVIDER = "\n"

    return DIVIDER.join(references)

def perform_command(
    flow_context, project_code, asset_id, repository_dir, send_to_flow, custom_sca_tags, scanner_timeout, parallel_workers, deploy_id, experimental
):

    if send_to_flow and not experimental and not project_code:
        raise click.MissingParameter(
            "It is required when sending reports to Conviso Platform API.",
            param_type="option",
            param_hint="--project-code",
        )
    
    if send_to_flow and experimental and not asset_id:
        raise click.MissingParameter(
            "It is required when sending reports to Conviso Platform using experimental API.",
            param_type="option",
            param_hint="--asset-id",
        )

    try:
        REQUIRED_CODEBASE_PATH = '/code'
        DANDELION_IMAGE_NAME = 'scabox-dandelion'
        RAMPHASTOS_IMAGE_NAME = 'scabox-ramphastos'

        scanners = {
            DANDELION_IMAGE_NAME: {
                'repository_name': DANDELION_IMAGE_NAME,
                'tag': 'latest',
                'command': [
                    '-c', REQUIRED_CODEBASE_PATH,
                    '-f', 'json',
                    '-o', '/{}.json'.format(DANDELION_IMAGE_NAME)
                ],
                'repository_dir': repository_dir
            },
            RAMPHASTOS_IMAGE_NAME: {
                'repository_name': RAMPHASTOS_IMAGE_NAME,
                'tag': 'latest',
                'command': [
                    '-c', REQUIRED_CODEBASE_PATH,
                    '-f', 'json',
                    '-o', '/{}.json'.format(RAMPHASTOS_IMAGE_NAME)
                ],
                'repository_dir': repository_dir
            },
        }

        if custom_sca_tags:
            for custom_tag in custom_sca_tags:
                scan_name, tag = custom_tag
                if scan_name in scanners.keys():
                    scanners[scan_name]['tag'] = tag
                else:
                    raise click.BadOptionUsage(
                        option_name='--custom-sca-tags',
                        message="Custom scan {0} or tag {1} invalid".format(
                            scan_name, tag)
                    )

        conviso_rest_api = flow_context.create_conviso_rest_api_client()
        token = conviso_rest_api.docker_registry.get_sast_token()
        LOGGER.info('\U0001F4AC Preparing Environment')
        scabox = ContainerWrapper(
            token=token,
            containers_map=scanners,
            logger=LOGGER,
            timeout=scanner_timeout
        )
        LOGGER.info('\U0001F4AC Starting SCA')
        scabox.run()

        LOGGER.info('\U0001F4AC Processing Results')
        results_filepaths = []
        for unit in scabox.scanners:
            file_path = unit.results
            if file_path:
                results_filepaths.append(file_path)

        if send_to_flow:
            LOGGER.info("   Sending data to Conviso Platform...")
            if experimental:
                conviso_beta_api = flow_context.create_conviso_api_client_beta()
                deploy_results_to_conviso_beta(
                    conviso_beta_api,
                    results_filepaths,
                    asset_id,
                )
            else:
                deploy_results_to_conviso(
                    conviso_rest_api,
                    results_filepaths,
                    project_code,
                    deploy_id=deploy_id,
                )

        # TODO add CI Decision block code
        LOGGER.info('\U00002705 SCA Scan Finished')

    except Exception as e:
        on_http_error(e)
        raise click.ClickException(str(e)) from e


EPILOG = '''
Examples:

  \b
  1 - Reporting the results to flow api:
    1.1 - Running an analysis at all commit range:
      $ export CONVISO_API_KEY='your-api-key'
      $ export CONVISO_PROJECT_CODE='your-project-code'
      $ {command}

'''  # noqa: E501

SHORT_HELP = "Perform Source Composition analysis"

command = 'conviso sca run'
run.short_help = SHORT_HELP
run.epilog = EPILOG.format(
    command=command,
)
