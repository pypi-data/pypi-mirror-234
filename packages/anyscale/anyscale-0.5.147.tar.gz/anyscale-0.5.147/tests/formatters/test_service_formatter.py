from unittest.mock import Mock, patch

from anyscale.formatters.service_formatter import format_service_config
from anyscale.models.service_model import ServiceConfig


def test_format_service_v2_config():
    """
    Tests that for a Service config with ray_serve_config field set,
    the formatter method will return both Service v1 and v2 configs.
    """
    ray_serve_config = {"runtime_env": {"pip": ["requests"], "working_dir": "."}}
    project_id = "test_project_id"
    build_id = "test_build_id"
    compute_config_id = "test_compute_config_id"
    version = "test_version"
    canary_percent = 60
    config_dict = {
        "name": "test_service",
        "ray_serve_config": ray_serve_config,
        "project_id": project_id,
        "build_id": build_id,
        "compute_config_id": compute_config_id,
        "version": version,
        "canary_percent": canary_percent,
    }
    mock_validate_successful_build = Mock()
    with patch.multiple(
        "anyscale.models.job_model",
        validate_successful_build=mock_validate_successful_build,
    ):
        service_config = ServiceConfig.parse_obj(config_dict)

    apply_service_config = format_service_config(service_config)

    assert apply_service_config.service_v2_config.project_id == project_id
    assert apply_service_config.service_v2_config.ray_serve_config == ray_serve_config
    assert apply_service_config.service_v2_config.version == version
    assert apply_service_config.service_v2_config.canary_percent == canary_percent
