from anyscale.client.openapi_client.models.apply_production_service_v2_model import (
    ApplyProductionServiceV2Model,
)
from anyscale.client.openapi_client.models.apply_service_config import (
    ApplyServiceConfig,
)
from anyscale.models.service_model import ServiceConfig


def format_service_config(service_config: ServiceConfig) -> ApplyServiceConfig:
    """
    This method formats the ServiceConfig into the API model ApplyServiceConfig.
    """
    service_name = service_config.name

    # We construct the Service v2 config model only if ray_serve_config is present
    if service_config.ray_serve_config:
        service_v2_config = ApplyProductionServiceV2Model(
            name=service_name,
            description=service_config.description or "Service updated from CLI",
            project_id=service_config.project_id,
            version=service_config.version,
            canary_percent=service_config.canary_percent,
            ray_serve_config=service_config.ray_serve_config,
            ray_gcs_external_storage_config=service_config.ray_gcs_external_storage_config,
            build_id=service_config.build_id,
            compute_config_id=service_config.compute_config_id,
        )
    else:
        service_v2_config = None
    return ApplyServiceConfig(service_v2_config=service_v2_config)


def format_service_config_v2(
    service_config: ServiceConfig,
) -> ApplyProductionServiceV2Model:
    if not service_config.ray_serve_config:
        raise RuntimeError(
            "ray_serve_config is expected for the Service configuration."
        )

    service_name = service_config.name

    return ApplyProductionServiceV2Model(
        name=service_name,
        description=service_config.description or "Service updated from CLI",
        project_id=service_config.project_id,
        version=service_config.version,
        canary_percent=service_config.canary_percent,
        ray_serve_config=service_config.ray_serve_config,
        ray_gcs_external_storage_config=service_config.ray_gcs_external_storage_config,
        build_id=service_config.build_id,
        compute_config_id=service_config.compute_config_id,
        rollout_strategy=service_config.rollout_strategy,
        config=service_config.config,
    )
