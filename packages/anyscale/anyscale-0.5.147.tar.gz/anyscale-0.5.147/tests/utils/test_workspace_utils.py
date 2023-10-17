import os
import tempfile
from unittest.mock import Mock

import yaml

from anyscale.client.openapi_client.models import (
    SessionSshKey,
    SessionsshkeyResponse,
)
from anyscale.shared_anyscale_utils.project import CLUSTER_YAML_TEMPLATE
from anyscale.utils.workspace_utils import _get_ssh_key_info


def test_configure_ssh_key(base_mock_api_client: Mock) -> None:
    base_mock_api_client.get_session_ssh_key_api_v2_sessions_session_id_ssh_key_get = Mock(
        return_value=SessionsshkeyResponse(
            result=SessionSshKey(key_name="SSH_KEY", private_key="PRIVATE_KEY")
        )
    )
    input_config = yaml.safe_load(CLUSTER_YAML_TEMPLATE)
    input_config["head_node"] = {}
    input_config["worker_nodes"] = {}
    with tempfile.TemporaryDirectory() as directory:
        _get_ssh_key_info(input_config, "session_id", base_mock_api_client, directory)
        with open(os.path.join(directory, "SSH_KEY.pem")) as f:
            assert f.read() == "PRIVATE_KEY"
