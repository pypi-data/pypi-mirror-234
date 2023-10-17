from functools import partial
import json
import os
from typing import Any, MutableMapping

from pydantic import BaseModel

from anyscale.client.openapi_client.api.default_api import DefaultApi
from anyscale.util import get_working_dir


class SSHKeyInfo(BaseModel):
    user: str
    key_path: str


class WorkspaceCommandContext(BaseModel):
    ssh: SSHKeyInfo
    working_dir: str
    head_ip: str
    project_id: str


def _get_ssh_key_info(
    cluster_config: MutableMapping[str, Any],
    session_id: str,
    api_client: DefaultApi,
    ssh_dir: str = "~/.ssh",
) -> SSHKeyInfo:
    # TODO (yiran): cleanup SSH keys if session no longer exists.
    def _write_ssh_key(name: str, ssh_key: str) -> str:
        key_path = os.path.join(os.path.expanduser(ssh_dir), f"{name}.pem")
        os.makedirs(os.path.dirname(key_path), exist_ok=True)

        with open(key_path, "w", opener=partial(os.open, mode=0o600)) as f:
            f.write(ssh_key)

        return key_path

    ssh_key = api_client.get_session_ssh_key_api_v2_sessions_session_id_ssh_key_get(
        session_id
    ).result

    key_path = _write_ssh_key(ssh_key.key_name, ssh_key.private_key)

    return SSHKeyInfo(user=cluster_config["auth"]["ssh_user"], key_path=key_path)


def extract_workspace_parameters_from_cluster_config(
    cluster_id: str, project_id: str, api_client: DefaultApi, ssh_dir: str,
) -> WorkspaceCommandContext:
    """
    This function pulls relevant fields from the legacy cluster config
    to populate a `WorkspaceCommandContext`.

    TODO: Remove any reliance on cluster configs.
    NOTE: Any additional fields that need to go into the WorkspaceCommandContext
    should be passed via actual API calls, and not pulled from cluster configs.
    """

    cluster_config = json.loads(
        api_client.get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get(
            cluster_id
        ).result.config_with_defaults
    )

    head_ip = api_client.get_session_head_ip_api_v2_sessions_session_id_head_ip_get(
        cluster_id
    ).result.head_ip

    ssh_info = _get_ssh_key_info(cluster_config, cluster_id, api_client, ssh_dir)
    return WorkspaceCommandContext(
        ssh=ssh_info,
        project_id=project_id,
        head_ip=head_ip,
        working_dir=get_working_dir(cluster_config, project_id, api_client) + "/",
    )
