import json
import os

import rich_click as click

from servicefoundry.cli.const import COMMAND_CLS, GROUP_CLS
from servicefoundry.lib.infra.install_truefoundry import InfraController
from servicefoundry.logger import logger


@click.group(
    name="bootstrap",
    cls=GROUP_CLS,
)
def bootstrap():
    """
    Boostrap infrastructure and components for Truefoundry platform
    """
    pass


@click.command(
    name="cloud-infra",
    cls=COMMAND_CLS,
    help="Bootstrap Cloud Infrastructure for Truefoundry",
)
@click.option(
    "--dry-run",
    "--dry_run",
    is_flag=True,
    default=False,
)
@click.option(
    "--file",
    is_flag=False,
)
def bootstrap_cloud_infra(dry_run: bool, file: str):
    # If file doesn't exist, then print error
    if file and not os.path.exists(file):
        logger.error(
            f"File at path: {file} not found. Please make sure input file exists"
        )
        return
    infra_controller = InfraController(dry_run=dry_run, config_file_path=file)
    infra_controller.create_infra_using_terraform()


@click.command(
    name="truefoundry",
    cls=COMMAND_CLS,
    help="Bootstrap Truefoundry Agent on an existing kubernetes cluster",
)
@click.option(
    "--dry-run",
    "--dry_run",
    is_flag=True,
    default=False,
)
@click.option(
    "--local",
    is_flag=True,
    default=False,
)
@click.option(
    "--file",
    is_flag=False,
)
def bootstrap_truefoundry(dry_run: bool, file: str, local: bool):
    # If file doesn't exist, then print error
    if not file:
        logger.error("Input file needs to be provided")
        return
    if file and not os.path.exists(file):
        logger.error(
            f"File at path: {file} not found. Please make sure input file exists"
        )
        return
    infra_controller = InfraController(dry_run=dry_run, config_file_path=file)
    infra_controller.install_truefoundry_to_k8s(local)
    return


@click.command(
    name="cluster",
    cls=COMMAND_CLS,
    help="Bootstrap Kubernetes cluster with the control plane",
)
@click.option(
    "--cluster-token",
    "--cluster_token",
    prompt=True,
)
@click.option("--org", prompt=True)
@click.option("--control-plane-url", prompt=True)
def bootstrap_agent_cluster(cluster_token: str, org: str, control_plane_url: str):
    config = {
        "provider": "aws",
        "tenant_name": org,
        "control_plane_url": control_plane_url,
        "tfy_agent": {"cluster_token": cluster_token},
    }
    input_file = f"{org}-input.yaml"
    with open(input_file, "w") as f:
        f.write(json.dumps(config, indent=2))
    infra_controller = InfraController(dry_run=False, config_file_path=input_file)
    infra_controller.install_truefoundry_to_k8s(local=False)
    return


def get_infra_command():
    bootstrap.add_command(bootstrap_cloud_infra)
    bootstrap.add_command(bootstrap_truefoundry)
    bootstrap.add_command(bootstrap_agent_cluster)
    return bootstrap
