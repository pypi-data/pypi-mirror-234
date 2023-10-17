from unittest.mock import Mock

import pytest

from anyscale.cli_logger import CloudSetupLogger
from anyscale.client.openapi_client.models import (
    CloudAnalyticsEvent,
    CloudAnalyticsEventCloudProviderError,
    CloudAnalyticsEventError,
    CreateAnalyticsEvent,
)
from anyscale.utils.cloud_utils import CloudEventProducer


@pytest.mark.parametrize(
    ("internal_error", "cloud_provider_error"),
    [(True, False), (False, True), (False, False), (True, True)],
)
@pytest.mark.parametrize("exception", [True, False])
def test_cloud_event_producer_produce(internal_error, cloud_provider_error, exception):
    mock_api_client = Mock()
    mock_cloud_provider = Mock()
    mock_api_client.produce_analytics_event_api_v2_analytics_post = Mock()
    if exception:
        mock_api_client.produce_analytics_event_api_v2_analytics_post.side_effect = (
            Exception()
        )
    logger = CloudSetupLogger()
    mock_cloud_resource = Mock()
    if cloud_provider_error:
        logger.log_resource_error(mock_cloud_resource, "not_found", 404)
    mock_internal_error = "mock_internal_error" if internal_error else None
    expected_cloud_provider_error = (
        [
            CloudAnalyticsEventCloudProviderError(
                cloud_resource=mock_cloud_resource, error_code="not_found,404",
            )
        ]
        if cloud_provider_error
        else None
    )

    cloud_event_producer = CloudEventProducer(mock_api_client)
    cloud_event_producer.init_trace_context(Mock(), mock_cloud_provider, Mock())
    mock_event_name = Mock()
    succeeded = not (internal_error or cloud_provider_error)
    expected_error = None
    if internal_error or cloud_provider_error:
        expected_error = CloudAnalyticsEventError(
            internal_error=mock_internal_error,
            cloud_provider_error=expected_cloud_provider_error,
        )

    # shouldn't throw exceptions
    cloud_event_producer.produce(
        event_name=mock_event_name,
        succeeded=succeeded,
        logger=logger,
        internal_error=mock_internal_error,
    )

    mock_api_client.produce_analytics_event_api_v2_analytics_post.assert_called_once_with(
        CreateAnalyticsEvent(
            cloud_analytics_event=CloudAnalyticsEvent(
                trace_id=cloud_event_producer.trace_id,
                cloud_id=cloud_event_producer.cloud_id,
                succeeded=succeeded,
                command_name=cloud_event_producer.command_name,
                raw_command_input=cloud_event_producer.raw_command_input,
                cloud_provider=mock_cloud_provider,
                event_name=mock_event_name,
                error=expected_error,
            )
        )
    )
