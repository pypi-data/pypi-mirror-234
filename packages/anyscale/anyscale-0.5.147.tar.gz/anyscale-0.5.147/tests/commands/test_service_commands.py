from typing import Generator
from unittest.mock import Mock, patch

from click.testing import CliRunner
import pytest

from anyscale.commands.service_commands import rollout


@pytest.fixture()
def mock_service_controller() -> Generator[Mock, None, None]:
    mock_service_controller = Mock()

    with patch(
        "anyscale.commands.service_commands.ServiceController",
        new=mock_service_controller,
    ):
        yield mock_service_controller


def test_rollout_strategy(mock_service_controller):
    """Tests the logic for setting `rollout_strategy`.

    This can either be set by `--rollout-strategy` or the `-i / --in-place` alias (but not both).
    """
    runner = CliRunner()

    # --rollout-strategy provided directly.
    runner.invoke(rollout, args=["--rollout-strategy=IN_PLACE", "-f", "file"])
    mock_service_controller().rollout.assert_called_once_with(
        "file",
        name=None,
        version=None,
        canary_percent=None,
        rollout_strategy="IN_PLACE",
    )
    mock_service_controller().reset_mock()

    runner.invoke(rollout, args=["--rollout-strategy=ROLLOUT", "-f", "file"])
    mock_service_controller().rollout.assert_called_once_with(
        "file",
        name=None,
        version=None,
        canary_percent=None,
        rollout_strategy="ROLLOUT",
    )
    mock_service_controller().reset_mock()

    # -i / --in-place used.
    runner.invoke(rollout, args=["-i", "-f", "file"])
    mock_service_controller().rollout.assert_called_once_with(
        "file",
        name=None,
        version=None,
        canary_percent=None,
        rollout_strategy="IN_PLACE",
    )
    mock_service_controller().reset_mock()

    runner.invoke(rollout, args=["--in-place", "-f", "file"])
    mock_service_controller().rollout.assert_called_once_with(
        "file",
        name=None,
        version=None,
        canary_percent=None,
        rollout_strategy="IN_PLACE",
    )
    mock_service_controller().reset_mock()

    # Provided both -i / --in-place and --rollout-strategy should error.
    result = runner.invoke(
        rollout, args=["-i", "--rollout-strategy=ROLLOUT", "-f", "file"]
    )
    assert result.exception is not None

    result = runner.invoke(
        rollout, args=["--in-place", "--rollout-strategy=ROLLOUT", "-f", "file"]
    )
    assert result.exception is not None
