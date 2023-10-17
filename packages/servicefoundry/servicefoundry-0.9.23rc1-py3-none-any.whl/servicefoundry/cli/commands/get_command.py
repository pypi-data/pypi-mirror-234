import rich_click as click

from servicefoundry.cli.config import CliConfig
from servicefoundry.cli.const import COMMAND_CLS, GROUP_CLS
from servicefoundry.cli.display_util import print_entity_obj, print_json
from servicefoundry.cli.util import handle_exception_wrapper
from servicefoundry.lib.dao import application as application_lib
from servicefoundry.lib.dao import version as version_lib
from servicefoundry.lib.dao import workspace as workspace_lib

# TODO (chiragjn): --json should disable all non json console prints


@click.group(name="get", cls=GROUP_CLS)
def get_command():
    # TODO (chiragjn): Figure out a way to update supported resources based on ENABLE_* flags
    """
    Get Truefoundry resources

    \b
    Supported resources:
    - Workspace
    - Application
    - Application Version
    """
    pass


@click.command(name="workspace", cls=COMMAND_CLS, help="Get Workspace details")
@click.option(
    "-w",
    "--workspace-fqn",
    "--workspace_fqn",
    type=click.STRING,
    default=None,
    help="FQN of the Workspace",
    required=True,
)
@handle_exception_wrapper
def get_workspace(workspace_fqn):
    workspace = workspace_lib.get_workspace_by_fqn(workspace_fqn=workspace_fqn)
    if CliConfig.get("json"):
        print_json(data=workspace.dict())
    else:
        print_entity_obj("Workspace", workspace)


@click.command(name="application", cls=COMMAND_CLS, help="Get Application details")
@click.option(
    "--application-fqn",
    "--application_fqn",
    type=click.STRING,
    default=None,
    help="FQN of the application",
    required=True,
)
@handle_exception_wrapper
def get_application(application_fqn):
    application = application_lib.get_application(application_fqn=application_fqn)
    if CliConfig.get("json"):
        print_json(data=application.dict())
    else:
        print_entity_obj(
            "Application",
            application,
        )


@click.command(
    name="application-version", cls=COMMAND_CLS, help="Get Application Version details"
)
@click.option(
    "--application-fqn",
    "--application_fqn",
    type=click.STRING,
    default=None,
    help="FQN of the application",
    required=True,
)
@click.option(
    "--version",
    type=click.STRING,
    default=None,
    help="Version number of the application deployment",
    required=True,
)
@handle_exception_wrapper
def get_version(application_fqn, version):
    version = version_lib.get_version(application_fqn=application_fqn, version=version)
    if CliConfig.get("json"):
        print_json(data=version.dict())
    else:
        print_entity_obj("Version", version)


@click.command(name="job-run", cls=COMMAND_CLS, help="Get Job Run")
@click.option(
    "--application-fqn",
    "--application_fqn",
    type=click.STRING,
    default=None,
    help="FQN of the application",
    required=True,
)
@click.option(
    "--job-run-name",
    "--job_run_name",
    type=click.STRING,
    default=None,
    help="Run name of the job",
    required=True,
)
@handle_exception_wrapper
def get_job_run(application_fqn, job_run_name):
    job_run = application_lib.get_job_run(
        application_fqn=application_fqn, job_run_name=job_run_name
    )
    if CliConfig.get("json"):
        print_json(data=job_run.dict())
    else:
        print_entity_obj("Job Run", job_run)


def get_get_command():
    get_command.add_command(get_workspace)
    get_command.add_command(get_application)
    get_command.add_command(get_version)
    get_command.add_command(get_job_run)
    return get_command
