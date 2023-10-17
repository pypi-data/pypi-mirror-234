from typing import IO, Optional

import click

from anyscale.controllers.compute_config_controller import ComputeConfigController
from anyscale.util import validate_non_negative_arg
from anyscale.utils.entity_arg_utils import format_inputs_to_entity


@click.group(
    "compute-config",
    short_help="Manage compute configurations on Anyscale.",
    help="Manages compute configurations to define cloud resource types and limitations.",
)
def compute_config_cli() -> None:
    pass


@compute_config_cli.command(
    name="create",
    help=(
        "Creates a new compute config. This accepts a yaml that follows the schema defined "
        "at https://docs.anyscale.com/reference/python-sdk/models#createclustercomputeconfig"
    ),
)
@click.argument("cluster-compute-file", type=click.File("rb"), required=True)
@click.option(
    "--name",
    "-n",
    help="Name for the created compute config.",
    required=False,
    type=str,
)
def create_cluster_compute(
    cluster_compute_file: IO[bytes], name: Optional[str]
) -> None:
    ComputeConfigController().create(cluster_compute_file, name)


@compute_config_cli.command(
    name="delete", help="Delete the specified compute config.", hidden=True
)
@click.argument("cluster-compute-name", type=str, required=False)
@click.option(
    "--name",
    "-n",
    help="Name of the compute config to delete.",
    required=False,
    type=str,
)
@click.option(
    "--cluster-compute-id",
    "--id",
    help="Id of the compute config to delete. Must be provided if a compute name is not given.",
    required=False,
    type=str,
)
def delete_cluster_compute(
    cluster_compute_name: Optional[str],
    name: Optional[str],
    cluster_compute_id: Optional[str],
) -> None:
    if cluster_compute_name is not None and name is not None:
        raise click.ClickException(
            "Please only provide one of [CLUSTER_COMPUTE_NAME] or --name."
        )
    ComputeConfigController().delete(cluster_compute_name or name, cluster_compute_id)


@compute_config_cli.command(
    name="archive", help="Archive the specified compute config.",
)
@click.argument("cluster-compute-name", type=str, required=False)
@click.option(
    "--name",
    "-n",
    help="Name of the compute config to archive.",
    required=False,
    type=str,
)
@click.option(
    "--cluster-compute-id",
    "--id",
    help="Id of the compute config to archive. Must be provided if a compute name is not given.",
    required=False,
    type=str,
)
def archive_cluster_compute(
    cluster_compute_name: Optional[str],
    name: Optional[str],
    cluster_compute_id: Optional[str],
) -> None:
    if cluster_compute_name is not None and name is not None:
        raise click.ClickException(
            "Please only provide one of [CLUSTER_COMPUTE_NAME] or --name."
        )
    entity = format_inputs_to_entity(cluster_compute_name or name, cluster_compute_id)
    ComputeConfigController().archive(entity)


@compute_config_cli.command(
    name="list",
    help=(
        "List information about compute configs on Anyscale. By default only list "
        "compute configs you have created."
    ),
)
@click.option(
    "--name",
    "-n",
    required=False,
    default=None,
    help="List information about the compute config with this name.",
)
@click.option(
    "--cluster-compute-id",
    "--id",
    required=False,
    default=None,
    help=("List information about the compute config with this id."),
)
@click.option(
    "--include-shared",
    is_flag=True,
    default=False,
    help="Include all compute configs you have access to.",
)
@click.option(
    "--max-items",
    required=False,
    default=20,
    type=int,
    help="Max items to show in list.",
    callback=validate_non_negative_arg,
)
def list(  # noqa: A001
    name: Optional[str],
    cluster_compute_id: Optional[str],
    include_shared: bool,
    max_items: int,
) -> None:
    cluster_compute_controller = ComputeConfigController()
    cluster_compute_controller.list(
        cluster_compute_name=name,
        cluster_compute_id=cluster_compute_id,
        include_shared=include_shared,
        max_items=max_items,
    )


@compute_config_cli.command(
    name="get", help=("Get details about compute configuration."),
)
@click.argument("cluster-compute-name", required=False)
@click.argument("cluster-compute-version", required=False, default=None, type=int)
@click.option(
    "--cluster-compute-id",
    "--id",
    required=False,
    default=None,
    help=("Get details about compute configuration by this id."),
)
def get(
    cluster_compute_name: Optional[str],
    cluster_compute_id: Optional[str],
    cluster_compute_version: Optional[int],
) -> None:
    cluster_compute_controller = ComputeConfigController()
    cluster_compute_controller.get(
        cluster_compute_name=cluster_compute_name,
        cluster_compute_id=cluster_compute_id,
        cluster_compute_version=cluster_compute_version,
    )
