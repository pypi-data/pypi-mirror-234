import shutil
import tempfile
from os.path import abspath

import click
import click_log

from convisoappsec.common.box import convert_sarif_to_sastbox1
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.common import project_code_option
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.logger import LOGGER

click_log.basic_config(LOGGER)


@click.command()
@project_code_option()
@click.option(
    "-i",
    "--input-file",
    required=True,
    type=click.Path(exists=True),
    help='The path to SARIF file.',
)
@help_option
@pass_flow_context
def import_sarif(flow_context, project_code, input_file):
    try:
        conviso_rest_api = flow_context.create_conviso_rest_api_client()

        perform_command(
            conviso_rest_api,
            project_code,
            input_file,
        )

    except Exception as err:
        raise click.ClickException(str(err)) from err


def perform_command(conviso_rest_api, project_code, input_file):
    print('Initializing importation of SARIF results to the Conviso Platform...')

    container_registry_token = conviso_rest_api.docker_registry.get_sast_token()
    temporary_dir_path = tempfile.mkdtemp(prefix='conviso_')
    temporary_sarif_path = copy_file_to_dir(input_file, temporary_dir_path)

    sastboxv1_filepath = convert_sarif_to_sastbox1(
        temporary_sarif_path,
        temporary_dir_path,
        container_registry_token
    )

    create_conviso_findings_from_sarif(
        conviso_api=conviso_rest_api,
        sastboxv1_filepath=sastboxv1_filepath,
        project_code=project_code
    )


def create_conviso_findings_from_sarif(conviso_api, sastboxv1_filepath, project_code):
    with open(sastboxv1_filepath) as report_file:
        status_code = conviso_api.findings.create(
            project_code=project_code,
            finding_report_file=report_file,
            default_report_type="sast",
            commit_refs=None,
            deploy_id=None,
        )

        if status_code < 210:
            print('The results were successfully imported!')
        else:
            print(
                'Results were not imported. Conviso will be notified of this error.')


def copy_file_to_dir(filepath, dir):
    source = abspath(filepath)

    filename = filepath.split('/')[-1]
    destination = '{}/{}'.format(abspath(dir), filename)

    shutil.copy(source, destination)
    return destination


import_sarif.epilog = '''
'''
EPILOG = '''
Examples:

  \b
  1 - Import results on SARIF file to Conviso Platform:
    $ export CONVISO_API_KEY='your-api-key'
    $ export CONVISO_PROJECT_CODE='your-project-code'
    $ {command} --input-file /path/to/file.sarif

'''  # noqa: E501

SHORT_HELP = "Perform import of vulnerabilities from SARIF file to Conviso Platform"

command = 'conviso findings import-sarif'
import_sarif.short_help = SHORT_HELP
import_sarif.epilog = EPILOG.format(
    command=command,
)
