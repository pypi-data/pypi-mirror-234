from typing import Optional

import click
from typing_extensions import Literal

from anyscale.cli_logger import BlockLogger
from anyscale.controllers.service_controller import ServiceController
from anyscale.util import validate_non_negative_arg


log = BlockLogger()  # CLI Logger


@click.group(
    "service", help="Interact with production services running on Anyscale.",
)
def service_cli() -> None:
    pass


@service_cli.command(
    name="rollout",
    help="Rollout a v2 service to Anyscale. Please contact support for details.",
)
@click.option(
    "-f",
    "--service-config-file",
    required=True,
    help="The path of the service configuration file.",
)
@click.option("--name", "-n", required=False, default=None, help="Name of service.")
@click.option("--version", required=False, default=None, help="Version of service.")
@click.option(
    "--canary-percent",
    required=False,
    default=None,
    type=int,
    help="The percentage of traffic to send to the canary version of the service.",
)
@click.option(
    "--rollout-strategy",
    required=False,
    default=None,
    type=click.Choice(["ROLLOUT", "IN_PLACE"], case_sensitive=False),
    help="Strategy for rollout.",
)
@click.option(
    "-i",
    "--in-place",
    "in_place",
    is_flag=True,
    show_default=True,
    default=False,
    help="Alias for `--rollout-strategy=IN_PLACE`.",
)
def rollout(
    service_config_file: str,
    name: Optional[str],
    version: Optional[str],
    canary_percent: Optional[int],
    rollout_strategy: Optional[Literal["ROLLOUT", "IN_PLACE"]],
    in_place: bool,
) -> None:
    """Start or update a service rollout to a new version.

    This is *only* supported for v2 services.
    """
    if in_place:
        if rollout_strategy is not None:
            raise click.ClickException(
                "Only one of `--in-place/-i` and `--rollout-strategy` can be provided."
            )
        rollout_strategy = "IN_PLACE"

    service_controller = ServiceController()
    service_controller.rollout(
        service_config_file,
        name=name,
        version=version,
        canary_percent=canary_percent,
        rollout_strategy=rollout_strategy,
    )


@service_cli.command(name="list", help="Display information about existing services.")
@click.option(
    "--name", "-n", required=False, default=None, help="Filter by service name."
)
@click.option(
    "--service-id", "--id", required=False, default=None, help="Filter by service id."
)
@click.option(
    "--project-id", required=False, default=None, help="Filter by project id."
)
@click.option(
    "--created-by-me",
    help="List services created by me only.",
    is_flag=True,
    default=False,
)
@click.option(
    "--max-items",
    required=False,
    default=10,
    type=int,
    help="Max items to show in list.",
    callback=validate_non_negative_arg,
)
def list(  # noqa: A001
    name: Optional[str],
    service_id: Optional[str],
    project_id: Optional[str],
    created_by_me: bool,
    max_items: int,
) -> None:
    """List services based on the provided filters.

    This returns both v1 and v2 services.
    """
    service_controller = ServiceController()
    service_controller.list(
        name=name,
        service_id=service_id,
        project_id=project_id,
        created_by_me=created_by_me,
        max_items=max_items,
    )


@service_cli.command(name="archive", help="Archive a service.")
@click.option("--service-id", "--id", required=False, help="ID of service.")
@click.option("--name", "-n", required=False, help="Name of service.")
@click.option("--project-id", required=False, help="Filter by project id.")
@click.option(
    "--service-config-file", "-f", help="The path of the service configuration file.",
)
def archive(
    service_id: Optional[str],
    name: Optional[str],
    project_id: Optional[str],
    service_config_file: Optional[str],
) -> None:
    """Archive a service, which must already be terminated.

    This is currently only supported for v1 services but should be extended to v2.
    """
    service_controller = ServiceController()
    service_id = service_controller.get_service_id(
        service_id=service_id,
        service_name=name,
        service_config_file=service_config_file,
        project_id=project_id,
    )
    service_controller.archive(service_id)


@service_cli.command(
    name="rollback", help="Attempt to rollback a v2 service asynchronously."
)
@click.option(
    "--service-id", "--id", default=None, help="ID of service.",
)
@click.option("--name", "-n", required=False, default=None, help="Name of service.")
@click.option("--project-id", required=False, help="Filter by project id.")
@click.option(
    "--service-config-file", "-f", help="The path of the service configuration file.",
)
def rollback(
    service_id: Optional[str],
    name: Optional[str],
    project_id: Optional[str],
    service_config_file: Optional[str],
) -> None:
    """Perform a rollback for a service that is currently in a rollout.

    This *only* applies to v2 services.
    """
    service_controller = ServiceController()
    service_id = service_controller.get_service_id(
        service_id=service_id,
        service_name=name,
        service_config_file=service_config_file,
        project_id=project_id,
    )
    service_controller.rollback(service_id)


@service_cli.command(
    name="terminate", help="Attempt to terminate a service asynchronously."
)
@click.option(
    "--service-id", "--id", required=False, help="ID of service.",
)
@click.option("--name", "-n", required=False, help="Name of service.")
@click.option("--project-id", required=False, help="Filter by project id.")
@click.option(
    "--service-config-file", "-f", help="The path of the service configuration file.",
)
def terminate(
    service_id: Optional[str],
    name: Optional[str],
    project_id: Optional[str],
    service_config_file: Optional[str],
) -> None:
    """Terminate a service.

    This applies to both v1 and v2 services.
    """
    service_controller = ServiceController()
    service_id = service_controller.get_service_id(
        service_id=service_id,
        service_name=name,
        service_config_file=service_config_file,
        project_id=project_id,
    )
    service_controller.terminate(service_id)
