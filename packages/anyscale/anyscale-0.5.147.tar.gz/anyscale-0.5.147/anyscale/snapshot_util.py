# This file is being deprecated and will be migrated to go/infra/config/anyscaled/systemd/config-template/snapshot_util.py
# NOTE: The logic in this file/module is only run from within an Anyscale workspace
import asyncio
import datetime
import json
import logging
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import time
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlparse

from anyscale.utils.imports.all import try_import_ray


logger = logging.getLogger(__name__)

# Built-in configs.
WORKING_DIR = os.environ.get("ANYSCALE_WORKING_DIR", "/home/ray")
# These files are saved per workspace.
CONFIGS_TO_SAVE = [
    ".bash_history",
    ".zsh_history",
]
# These files are saved per user.
CONFIGS_TO_REPLICATE = [
    ".workspacerc",
    ".gitconfig",
    ".vimrc",
    ".tmux.conf",
]

# Default cluster storage dir.
CLUSTER_STORAGE_DIR = "/mnt/cluster_storage"

# Default VSCode server dir.
VSCODE_DESKTOP_SERVER_DIR = "/home/ray/.vscode-server"

# Experimental configs propagated from the cluster config service.
EFS_IP = os.environ.get("ANYSCALE_EXPERIMENTAL_EFS_IP", "")
EFS_ROOT = os.environ.get("ANYSCALE_EXPERIMENTAL_EFS_ROOT", "")
EFS_TYPE = os.environ.get("ANYSCALE_EXPERIMENTAL_EFS_TYPE", "")
# Override with container-defined IP.
CUSTOM_EFS_IP = os.environ.get("CUSTOM_EFS_IP", "")
CUSTOM_EFS_ROOT = os.environ.get("CUSTOM_EFS_ROOT", "")
IDLE_TERMINATION_DIR = os.environ.get(
    "IDLE_TERMINATION_DIR", "/tmp/anyscale/idle_termination_reports"
)
if CUSTOM_EFS_IP:
    EFS_IP = CUSTOM_EFS_IP

if CUSTOM_EFS_ROOT:
    EFS_ROOT = CUSTOM_EFS_ROOT

WORKSPACE_ID = os.environ.get("ANYSCALE_EXPERIMENTAL_WORKSPACE_ID", "")
USERNAME = os.environ.get("ANYSCALE_EXPERIMENTAL_USERNAME", "unknown_user")
BASE_SNAPSHOT = os.environ.get("ANYSCALE_EXPERIMENTAL_BASE_SNAPSHOT") or None

# GitHub URI to use as the template for the new workspace. This is the URI you see
# when browsing the desired subdir in the web UI, e.g.:
#
# https://github.com/ray-project/ray/tree/master/release/ml_user_tests
#
WORKSPACE_TEMPLATE = os.environ.get("ANYSCALE_WORKSPACE_TEMPLATE") or None

# Other debug configs.
SNAPSHOT_INTERVAL = int(os.environ.get("WORKSPACE_SNAPSHOT_INTERVAL", 300))
EFS_WORKSPACE_DIR = os.environ.get("EFS_WORKSPACE_DIR", "/efs/workspaces")
EFS_JOB_DIR = os.environ.get("EFS_WORKSPACE_DIR", "/efs/jobs")
EFS_OBJECTS_DIR = os.environ.get("EFS_OBJECTS_DIR", "/efs/workspaces/shared_objects")
EFS_CREDS_DIR = os.environ.get("EFS_CREDS_DIR", "/efs/generated_credentials")
RAY_ML_DEV = bool(os.environ.get("RAY_ML_DEV"))
AUTOGC = bool(os.environ.get("AUTOGC_SNAPSHOTS", True))
SNAPSHOT_RETENTION_COUNT = max(int(os.environ.get("SNAPSHOT_RETENTION_COUNT", 5)), 1)
SNAPSHOT_RETENTION_HOURS = max(int(os.environ.get("SNAPSHOT_RETENTION_HOURS", 1)), 1)
SKIP_VSCODE_DESKTOP_SETUP = bool(os.environ.get("SKIP_VSCODE_DESKTOP_SETUP", False))

# This causes workspaces to use the $CWD as the runtime env working dir instead of
# always the workspace root.
RELATIVE_WORKING_DIR = bool(os.environ.get("RELATIVE_WORKING_DIR", True))


def optimize_git_repo(directory: str, shared_repo: str) -> None:
    """Optimize the space usage of a git repo by syncing objects to a shared repo.

    Any objects in the source repo will be replicated to the shared repo, and then
    deleted from the source repo. The source repo is setup to reference objects in
    the shared repo via the `.git/objects/info/alternates` mechanism.

    Args:
        directory: The directory to optimize.
        shared_repo: The path that should be used to hold shared objects. This path
            will be created if it doesn't already exist. Multiple checkouts of the
            same repo can share the objects stored in the shared repo.
    """
    start = time.time()
    objects_path = f"{directory}/.git/objects"
    if os.path.exists(objects_path):
        if not os.path.exists(shared_repo):
            os.makedirs(os.path.dirname(shared_repo), exist_ok=True)
            # TODO(ekl) it's faster to do a copy of just the objects dir, but it seems
            # we need to git clone in order for alternates to be recognized as valid.
            subprocess.check_call(
                f"git clone --bare {directory}/ {shared_repo}/", shell=True,
            )
        shared_objects_dir = os.path.join(shared_repo, "objects")
        subprocess.check_call(
            f"rsync -a {objects_path}/ {shared_objects_dir}/", shell=True
        )
        subprocess.check_call("rm -rf {}".format(objects_path), shell=True)  # noqa
        os.makedirs(os.path.join(objects_path, "info"), exist_ok=True)
        with open(os.path.join(objects_path, "info/alternates"), "w") as f:
            f.write(f"{shared_objects_dir}\n")
    logger.info(
        "Synced git objects for {} to {} in {}s.".format(
            directory, shared_repo, time.time() - start
        )
    )


def create_snapshot_zip(directory: str, auto: bool) -> str:
    """Create a snapshot of the given directory.

    The snapshot will include all git tracked files as well as unstaged
    (but otherwise trackable) files. It will also include the full
    contents of the `.git` folder. To optimize the disk space usage of
    snapshots, call `optimize_git_repo` on the repo directory prior to
    calling `create_snapshot_zip`.

    Args:
        directory: Path of the directory to snapshot.

    Returns:
        Path of a .zip file that contains the snapshot files.
    """

    start = time.time()
    orig = os.path.abspath(os.curdir)
    prefix = "snapshot_{}_".format(
        datetime.datetime.now(datetime.timezone.utc).isoformat()
    )
    if auto:
        prefix += "auto_"
    target = tempfile.mktemp(suffix=".zip", prefix=prefix)
    is_git_workspace = os.path.exists(os.path.join(WORKING_DIR, ".git"))
    is_within_workspace = os.path.abspath(directory).startswith(
        os.path.abspath(WORKING_DIR)
    )
    try:
        os.chdir(directory)
        if is_git_workspace and is_within_workspace:
            subprocess.check_call(
                "(git ls-files -co --exclude-standard || true; find .git || true) | "
                f"zip --symlinks -@ -0 -q {target}",
                shell=True,
            )
        else:
            for child in os.listdir("."):
                if os.path.exists(os.path.join(child, ".git")):
                    raise ValueError(
                        f"Git repo detected in sub-directory {child}. Please ensure "
                        "that your git repo is cloned in the top-level workspace "
                        f"directory with 'git clone <repo> .' at {directory}."
                    )
            subprocess.check_call(
                f"find . | zip --symlinks -@ -0 -q {target}", shell=True,
            )
    finally:
        os.chdir(orig)

    assert os.path.exists(target), target
    logger.info(
        "Created snapshot for {} at {} of size {} in {}s.".format(
            directory, target, os.path.getsize(target), time.time() - start
        )
    )
    return target


def unpack_snapshot_zip(zip_path: str, directory: str) -> None:
    """Unpack a snapshot to the given directory.

    Args:
        zip_path: Path of the zip returned by create_snapshot_zip.
        directory: Output directory to unpack the zip into.
    """

    start = time.time()
    os.makedirs(directory, exist_ok=True)
    subprocess.check_call(f"unzip -X -o -q {zip_path} -d {directory}", shell=True)
    logger.info(
        "Unpacked snapshot {} to {} in {}s.".format(
            zip_path, directory, time.time() - start
        )
    )


def unpack_github_dir(github_tree_uri: str, out_dir: str) -> None:
    """Download a GitHub tree URI for a directory.

    Args:
        github_tree_uri: URL for a directory, for example:
            "https://github.com/ray-project/ray/tree/master/release/ml_user_tests"
        out_dir: The output dir to put files, which must be empty.
    """

    if "github.com" not in github_tree_uri:
        raise ValueError("Only GitHub URLs are supported by load_package().")

    # Normalize dir URIs.
    if github_tree_uri.endswith("/"):
        github_tree_uri = github_tree_uri[:-1]

    URL_FORMAT = ".*github.com/([^/]*)/([^/]*)/tree/([^/]*)/(.*)"
    match = re.match(URL_FORMAT, github_tree_uri)
    if not match:
        raise ValueError(f"GitHub URL must be of format {URL_FORMAT}")
    gh_user = match.group(1)
    gh_repo = match.group(2)
    gh_branch = match.group(3)
    gh_subdir = match.group(4)

    logger.info(
        f"Attempting download, gh_user={gh_user}, gh_repo={gh_repo}, "
        f"gh_branch={gh_branch}, gh_subdir={gh_subdir}"
    )

    tmp = tempfile.mktemp(prefix=f"github_{gh_repo}", suffix=".tar.gz")
    subprocess.check_call(
        [
            "wget",
            f"--output-document={tmp}",
            f"https://github.com/{gh_user}/{gh_repo}/tarball/{gh_branch}",
        ]
    )
    logger.info(f"Downloaded tarball to {tmp}")

    # The directory we want to extract is a subdir within the zip, e.g.,
    # ray-project-fc17342/release/ml_user_tests/ray-lightning
    top_dir = tarfile.open(tmp).getnames()[0]
    tar_path = top_dir + "/" + gh_subdir
    # Calculate the depth to the subdir and strip those leading components.
    strip = tar_path.count("/") + 1
    tar_command = [
        "tar",
        "xzf",
        tmp,
        "-C",
        out_dir,
        tar_path,
        f"--strip-components={strip}",
    ]
    logger.info(f"Extract command is {tar_command}")
    subprocess.check_call(tar_command)


def compute_content_hash(zip_path: str) -> bytes:
    """Return the md5 hash of a given zipfile on disk."""
    md5 = subprocess.check_output(
        f"unzip -p {zip_path} | md5sum -b | cut -f1 -d ' '", shell=True
    )
    md5 = md5.strip()
    return md5


def get_or_create_snapshot_zip(directory: str, auto: bool) -> str:
    """Create a snapshot zip, or return the last snapshot if unchanged.

    A corresponding .md5 file is created alongside the snapshot zip.
    """
    new_zip = create_snapshot_zip(directory, auto)
    new_hash = compute_content_hash(new_zip)
    # Ignore the base snapshot in auto save mode. This means we will always generate
    # a new snapshot within the autosave interval, allowing the base snapshot to be
    # safely garbage collected.
    old_zip = find_latest(ignore_base_snapshot=auto)
    if old_zip:
        try:
            with open(old_zip + ".md5", "rb") as f:
                old_hash: Optional[bytes] = f.read().strip()
        except Exception:  # noqa: BLE001
            logger.warning("Failed to read md5 file")
            old_hash = None
    else:
        old_hash = None
    logger.info(f"Content hashes {old_hash!r} vs {new_hash!r}")
    if old_hash == new_hash:
        logger.info("Content hash unchanged, not saving new snapshot.")
        os.unlink(new_zip)
        assert old_zip is not None
        return old_zip
    else:
        with open(new_zip + ".md5", "wb") as f:
            f.write(new_hash)
        return new_zip


def do_snapshot(auto: bool = False):
    """Command to create a snapshot within an Anyscale workspace.

    Can be run via `python -m anyscale.snapshot_util snapshot`.
    """

    try:
        workspace_dir = os.path.join(EFS_WORKSPACE_DIR, WORKSPACE_ID)
        snapshot_dir = os.path.join(workspace_dir, "snapshots")

        is_empty = len(os.listdir(WORKING_DIR)) == 0

        # directory is empty, no need to snapshot
        if is_empty:
            return

        # TODO(ekl) should we isolate the objects by workspace or repo?
        optimize_git_repo(WORKING_DIR, EFS_OBJECTS_DIR)
        zip = get_or_create_snapshot_zip(WORKING_DIR, auto)  # noqa: A001

        # If the zip was already on EFS, we're done.
        if zip.startswith(snapshot_dir):
            return

        # Otherwise, move the zip into EFS along with its md5 file.
        os.makedirs(snapshot_dir, exist_ok=True)
        shutil.move(zip, os.path.join(snapshot_dir, os.path.basename(zip)))
        shutil.move(
            zip + ".md5", os.path.join(snapshot_dir, os.path.basename(zip) + ".md5")
        )
        for config in CONFIGS_TO_SAVE:
            source = os.path.join("/home/ray", config)
            if os.path.exists(source):
                shutil.copy(source, os.path.join(workspace_dir, config))

        # report successful idle termination status
        report_idle_termination_activity()

    except Exception:
        logger.exception("Failed to create a snapshot")
        # report error idle termination status
        report_idle_termination_error("Failed to create a snapshot")

    if AUTOGC:
        gc_snapshots()


def report_idle_termination_activity():
    if os.path.exists(IDLE_TERMINATION_DIR):
        with open(f"{IDLE_TERMINATION_DIR}/workspace.json", "w") as f:
            f.write(json.dumps({"last_activity_timestamp": time.time()}))
    else:
        logger.warning(
            f"Did not report workspace idle termination status because {IDLE_TERMINATION_DIR} is not mounted."
        )


def report_idle_termination_error(err: str):
    content = {"error": err}
    if os.path.exists(IDLE_TERMINATION_DIR):
        with open(f"{IDLE_TERMINATION_DIR}/workspace.json", "w") as f:
            f.write(json.dumps(content))
    else:
        logger.warning(
            f"Did not report workspace idle termination status because {IDLE_TERMINATION_DIR} is not mounted."
        )


def gc_snapshots() -> None:
    """Garbage collect snapshots older than X hours.

    This is safe since when we clone a workspace, the autosave loop will generate a
    new snapshot, so the clone will be decoupled from the original.
    """
    workspace_dir = os.path.join(EFS_WORKSPACE_DIR, WORKSPACE_ID)
    snapshot_dir = os.path.join(workspace_dir, "snapshots")
    if not os.path.exists(snapshot_dir):
        return
    snapshots = sorted([x for x in os.listdir(snapshot_dir) if x.endswith(".zip")])
    # Never GC the latest SNAPSHOT_RETENTION_COUNT snapshot.
    snapshots = snapshots[:-SNAPSHOT_RETENTION_COUNT]
    horizon = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
        hours=SNAPSHOT_RETENTION_HOURS
    )

    logger.debug(
        f"Snapshot retention count: {SNAPSHOT_RETENTION_COUNT}, snapshot retention hours: {SNAPSHOT_RETENTION_HOURS}"
    )

    prefix = f"snapshot_{horizon.isoformat()}_"
    # GC snapshots older than SNAPSHOT_RETENTION_HOURS hour.
    for snapshot in snapshots:
        if snapshot < prefix:
            full_path = os.path.join(snapshot_dir, snapshot)
            md5 = full_path + ".md5"
            logger.info(f"Deleting old snapshot {full_path}")
            try:
                os.unlink(full_path)
                os.unlink(md5)
            except Exception:
                logger.exception("Failed to delete snapshot")


def find_latest(ignore_base_snapshot: bool) -> Optional[str]:
    """Return path to latest .zip snapshot, if it exists."""
    workspace_dir = os.path.join(EFS_WORKSPACE_DIR, WORKSPACE_ID)
    snapshot_dir = os.path.join(workspace_dir, "snapshots")
    if not os.path.exists(snapshot_dir):
        if ignore_base_snapshot:
            return None
        else:
            return find_base_snapshot()
    snapshots = sorted([x for x in os.listdir(snapshot_dir) if x.endswith(".zip")])
    if not snapshots:
        return find_base_snapshot()
    return os.path.join(snapshot_dir, snapshots[-1])


def find_base_snapshot_from_job(job_id: str) -> Optional[str]:
    if not job_id:
        logger.info("Invalid base snapshot, no job id")
        return None
    logger.info(f"Base snapshot from job {job_id}")

    # find service snapshot URI from remote storage
    from anyscale.authenticate import get_auth_api_client

    auth_api_client = get_auth_api_client(log_output=False)
    api_client = auth_api_client.api_client
    job = api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get(
        job_id
    ).result
    if (
        job
        and job.config
        and job.config.runtime_env
        and job.config.runtime_env.working_dir
    ):
        return job.config.runtime_env.working_dir

    # fallback to find job snapshot in EFS
    job_efs_snapshot = os.path.join(EFS_JOB_DIR, job_id, "working_dir.zip")
    if os.path.exists(job_efs_snapshot):
        return job_efs_snapshot

    return None


def find_base_snapshot_from_service(service_id: str) -> Optional[str]:
    if not service_id:
        logger.info("Invalid base snapshot, no service id")
        return None
    logger.info(f"Base snapshot from service {service_id}")

    # find service snapshot URI from remote storage
    from anyscale.authenticate import get_auth_api_client

    auth_api_client = get_auth_api_client(log_output=False)
    api_client = auth_api_client.api_client
    service = api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get(
        service_id
    ).result
    if service and service.config and service.config.ray_serve_config:
        runtime_env = service.config.ray_serve_config.get("runtime_env", {})
        if "working_dir" in runtime_env:
            return runtime_env["working_dir"]

    return None


def find_base_snapshot_from_workspace(
    workspace_id: str, iso_time: str
) -> Optional[str]:
    if not workspace_id or not iso_time:
        logger.info("Invalid base snapshot, no workspace id or time")
        return None
    logger.info(f"Base snapshot from workspace {workspace_id} and {iso_time}")
    snapshot_dir = os.path.join(EFS_WORKSPACE_DIR, workspace_id, "snapshots")
    snapshot_time = f"snapshot_{iso_time}_"
    if not os.path.exists(snapshot_dir):
        return None
    # Find the latest matching snapshot before the time stamp
    snapshots = sorted(
        [
            x
            for x in os.listdir(snapshot_dir)
            if x.endswith(".zip") and x < snapshot_time
        ]
    )
    if not snapshots:
        return None
    return os.path.join(snapshot_dir, snapshots[-1])


def find_base_snapshot() -> Optional[str]:  # noqa: PLR0911
    """
        Find the base snapshot for the job/service/workspace used to create current workspace.

        Returns:
            If exists, return the EFS path or URI of the base snapshot.
            otherwise, return None.
    """
    if not BASE_SNAPSHOT:
        return None
    try:
        base_data = json.loads(BASE_SNAPSHOT)
    except Exception:
        logger.exception("Failed to parse base snapshot info")
        return None

    # Jobs snapshot
    if "from_job" in base_data:
        job_id = base_data["from_job"].get("job_id")
        return find_base_snapshot_from_job(job_id=job_id)

    # Services snapshot
    if "from_service" in base_data:
        service_id = base_data["from_service"].get("service_id")
        return find_base_snapshot_from_service(service_id=service_id)

    # Workspace snapshot
    if "from_workspace" in base_data:
        workspace_id = base_data["from_workspace"].get("workspace_id")
        iso_time = base_data["from_workspace"].get("iso_time")
        return find_base_snapshot_from_workspace(workspace_id, iso_time)

    logger.info(
        "Failed to find base snapshot since it's not from job/service/workspace"
    )
    return None


def _is_uri(uri: str) -> bool:
    """Check if the given string is a valid URI.
    Note that this function does not check if the URI is accessable."""
    parsed_uri = urlparse(uri)
    return bool(parsed_uri.scheme and parsed_uri.netloc)


def _move_files(src_dir: str, dest_dir: str) -> None:
    """
    Moves all files in the source directory to the destination directory.

    Exceptions:
        1. shutil.Error: raised when a general error occurs, such as a file already existing in the destination directory with the same name as a file being moved.
        2. OSError: raised when a file-related system error occurs, such as an invalid source or destination file path, or a permission error.
        3. IOError: raised when an input/output error occurs, such as a disk error or a file being locked by another process.
    """
    try:
        # create the destination directory if it doesn't exist
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # get a list of all files in the source directory
        files = os.listdir(src_dir)

        # loop through all files and move them to the destination directory
        for file in files:
            src_path = os.path.join(src_dir, file)
            dest_path = os.path.join(dest_dir, file)
            shutil.move(src_path, dest_path)

    except Exception as e:
        logger.exception(
            f"Failed to move files from {src_dir} to {dest_dir} due to {e}"
        )
        raise


def _download_and_unpack_snapshot_uri(snapshot_uri: str, working_dir: str) -> None:
    """
    Download the snapshot from the given URI and unpack it to the working directory.
    The snapshot will be first downloaded to a temporary directory and then moved to the working directory.

    Args:
        snapshot_uri: URI pointing to the snapshot.
        working_dir: Output directory to be polulated with the downloaded contents.
    """

    try:
        # use Ray DeveloperAPI to download the snapshot from remote buckets
        from ray._private.runtime_env.packaging import download_and_unpack_package

        with tempfile.TemporaryDirectory() as temp_dir:
            unpacked_dir = asyncio.run(
                download_and_unpack_package(
                    pkg_uri=snapshot_uri, base_directory=temp_dir
                )
            )
            _move_files(src_dir=unpacked_dir, dest_dir=working_dir)

            logger.info(f"Downloaded snapshot from {snapshot_uri} to {working_dir}")
    except Exception as e:
        logger.exception(f"Failed to download snapshot from {snapshot_uri} due to {e}")
        raise


def restore_latest():
    """Command to restore the latest snapshot within an Anyscale workspace.

    Can be run via `python -m anyscale.snapshot_util restore`.
    """

    # Step 1: Find the latest snapshot.
    latest = find_latest(ignore_base_snapshot=False)
    logger.info(f"Latest snapshot found was {latest}")
    if not latest:
        # No snapshot found: fallback to template or blank workspace.
        if WORKSPACE_TEMPLATE:
            unpack_github_dir(WORKSPACE_TEMPLATE, WORKING_DIR)
        return

    # Step 2: Download/Unpack the snapshot.
    if _is_uri(latest):
        _download_and_unpack_snapshot_uri(snapshot_uri=latest, working_dir=WORKING_DIR)
    else:
        unpack_snapshot_zip(latest, WORKING_DIR)

    # Step 3: Copy over the config files.
    workspace_dir = os.path.join(EFS_WORKSPACE_DIR, WORKSPACE_ID)
    for config in CONFIGS_TO_SAVE:
        saved = os.path.join(workspace_dir, config)
        if os.path.exists(saved):
            shutil.copy(saved, os.path.join("/home/ray", config))


# Copied from https://stackoverflow.com/a/50864227
def _split_s3_path(s3_path: str) -> Tuple[str, str]:
    path_parts = s3_path.replace("s3://", "").split("/")
    bucket = path_parts.pop(0)
    key = "/".join(path_parts)
    return bucket, key


def checkpoint_job(job_id, runtime_env: Dict[str, Any]) -> Dict[str, Any]:
    """ Deprecated in v2 stack: we are moving away from EFS and towards remote buckets.

    Checkpoint the runtime environment and working directory of a job.

    This function will modify runtime_env to point to the new working
    directory on EFS and return the modified runtime_env.
    """
    # For some reason, in a job Ray first calls the env_hook with runtime_env = None
    # and then a second time with the proper runtime_env -- do nothing in the former case.
    if not runtime_env:
        return runtime_env
    dest_dir = os.path.join(EFS_JOB_DIR, job_id)
    os.makedirs(dest_dir, exist_ok=True)
    if "working_dir" in runtime_env and runtime_env["working_dir"].endswith(".zip"):
        # We're a job, also save a replica of the zip in EFS so the job can be cloned
        # as a workspace at a later time.
        working_dir = os.path.join(dest_dir, "working_dir.zip")

        # We need a custom path for s3 urls because urllib.request.urlretrieve doesn't work for s3 urls
        if runtime_env["working_dir"].startswith("s3://"):
            import boto3

            bucket, key = _split_s3_path(runtime_env["working_dir"])
            # boto3 client initialized inside clusters already have AWS credentials set
            s3_client = boto3.client("s3")
            s3_client.download_file(bucket, key, working_dir)
        elif runtime_env["working_dir"].startswith("gs://"):
            # checkpoint_job is deprecated in v2 stack,
            # so we don't need to support gs:// uris here.
            # just return here to avoid breaking the code
            return runtime_env
        else:
            import urllib.request

            urllib.request.urlretrieve(runtime_env["working_dir"], working_dir)
        runtime_env["working_dir"] = working_dir
    # Save the runtime_env to be used later.
    with open(os.path.join(dest_dir, "runtime_env.json"), "w") as f:
        f.write(json.dumps(runtime_env))
    return runtime_env


def setup_ml_dev(runtime_env):
    """Env hook for Ray ML development.

    This enables development for Ray ML libraries, assuming the working dir is the
    entire Ray repo, by replicating library changes to all nodes in the cluster via
    runtime_env py_modules.

    To enable this hook, set RAY_ML_DEV=1.
    """
    if not runtime_env:
        runtime_env = {}
    ray = try_import_ray()

    sys_ray_module = os.path.dirname(ray.__file__)
    local_ray_module = os.path.join(WORKING_DIR, "python/ray")
    if not os.path.exists(local_ray_module):
        logger.info("RAY_ML_DEV was set, but could not find the local ray module.")
        return runtime_env
    tmp_module = "/tmp/ray_tmp_module/ray"
    shutil.rmtree(tmp_module, ignore_errors=True)
    shutil.copytree(sys_ray_module, tmp_module)
    # TODO(ekl) keep this in sync with setup-dev.py
    LIB_DIRS = [
        "rllib",
        "air",
        "tune",
        "serve",
        "train",
        "data",
        "experimental",
        "util",
        "workflow",
        "cloudpickle",
        "_private",
        "internal",
        "node.py",
        "cluster_utils.py",
        "ray_constants.py",
    ]
    for lib_dir in LIB_DIRS:
        src = os.path.join(local_ray_module, lib_dir)
        dst = os.path.join(tmp_module, lib_dir)
        logger.info(f"Copying files from {src} to {dst}.")
        if os.path.isdir(src):
            shutil.rmtree(dst)
            shutil.copytree(os.path.join(local_ray_module, lib_dir), dst)
        elif os.path.exists(src):
            shutil.copy(src, dst)
        else:
            logger.info(f"Did not find {src}")
    if "py_modules" not in runtime_env:
        runtime_env["py_modules"] = []
    runtime_env["py_modules"].append(tmp_module)
    return runtime_env


def env_hook(runtime_env) -> Dict[str, Any]:
    """Env hook for including the working dir in the runtime_env by default.

    This should be set as `RAY_RUNTIME_ENV_HOOK=anyscale.snapshot_util.env_hook`.
    """
    if not runtime_env:
        runtime_env = {}

    # If EFS fails to mount, we don't update the working_dir to EFS
    if not os.path.ismount("/efs"):
        return runtime_env

    if "ANYSCALE_EXPERIMENTAL_INITIAL_JOB_ID" in os.environ:
        return checkpoint_job(
            os.environ["ANYSCALE_EXPERIMENTAL_INITIAL_JOB_ID"], runtime_env
        )

    # Only fill in the working_dir if it's non-empty (to avoid empty zip errors).
    if not runtime_env.get("working_dir") and os.listdir(WORKING_DIR):
        optimize_git_repo(WORKING_DIR, EFS_OBJECTS_DIR)
        if RELATIVE_WORKING_DIR:
            zipfile = create_snapshot_zip(".", auto=False)
        else:
            zipfile = create_snapshot_zip(WORKING_DIR, auto=False)
        # Move the zip file to a consistent path so that we don't leak zip files as
        # jobs are run over time. This isn't thread safe: we assume one job at a time.
        # Note that the zip file isn't needed after the job starts successfully.
        final_path = "/tmp/ray_latest_runtime_env.zip"
        shutil.move(zipfile, final_path)
        runtime_env["working_dir"] = final_path
    if RAY_ML_DEV:
        runtime_env = setup_ml_dev(runtime_env)
    env_vars = runtime_env.get("env_vars", {})
    env_vars.update(_load_env_vars())
    # This if condition is a workaround for
    # https://github.com/anyscale/product/issues/11679
    if env_vars:
        runtime_env["env_vars"] = env_vars
    logger.info(f"Updated runtime env to {runtime_env}")
    return runtime_env


def setup_credentials():
    """Command to create SSH credentials for the workspace.

    We generate unique Anyscale SSH keys for each username. This call will inject
    the key for the current user into the workspace.
    """
    private_key = os.path.join(EFS_CREDS_DIR, USERNAME, "id_rsa")
    public_key = os.path.join(EFS_CREDS_DIR, USERNAME, "id_rsa.pub")
    os.path.join(EFS_CREDS_DIR, USERNAME, "env_vars.json")

    # setup ssh directory commands
    setup_ssh_directory_cmds = [
        "mkdir -p /home/ray/.ssh",
        # incase the directory is already created by docker, make sure we can write to it.
        "sudo chown ray /home/ray/.ssh",
    ]

    for cmd in setup_ssh_directory_cmds:
        try:
            subprocess.check_call(cmd, shell=True)
        except Exception:
            logger.exception(f"Error running {cmd}")

    if os.path.exists(private_key):
        # Copy down from EFS.
        shutil.copy(private_key, "/home/ray/.ssh/id_rsa")
        shutil.copy(public_key, "/home/ray/.ssh/id_rsa.pub")
    else:
        # Copy up to EFS.
        subprocess.check_call(
            "echo y | ssh-keygen -t rsa -f /home/ray/.ssh/id_rsa -N ''", shell=True
        )
        os.makedirs(os.path.dirname(private_key), exist_ok=True)
        shutil.copy("/home/ray/.ssh/id_rsa", private_key)
        shutil.copy("/home/ray/.ssh/id_rsa.pub", public_key)

    # Also put stored user env vars in the bashrc.
    env_vars = _load_env_vars()
    with open("/home/ray/.bashrc", "a") as bashrc:
        bashrc.write("\n")
        for key, value in env_vars.items():
            bashrc.write(f"export {key}='{value}'\n")


def _load_env_vars():
    env_store = os.path.join(EFS_CREDS_DIR, USERNAME, "env_vars.json")
    env_vars = {}
    if os.path.exists(env_store):
        try:
            with open(env_store) as f:
                env_vars = json.loads(f.read())
        except Exception:
            logger.exception("Error parsing env vars")
    return env_vars


def _save_env_vars(env_vars: dict):
    env_store = os.path.join(EFS_CREDS_DIR, USERNAME, "env_vars.json")
    with open(env_store, "w") as f:
        f.write(json.dumps(env_vars))
    print(f"Stored keys: {list(env_vars)}")


def get_env_var(key: str):
    env_vars = _load_env_vars()
    if key not in env_vars:
        raise KeyError("No value was put for", key)
    print(f"{key}={env_vars[key]}")


def del_env_var(key: str):
    env_vars = _load_env_vars()
    if key in env_vars:
        del env_vars[key]
    _save_env_vars(env_vars)


def put_env_var(key: str, value: str) -> None:
    env_vars = _load_env_vars()
    env_vars[key] = value
    _save_env_vars(env_vars)


def setup_nfs():
    """Setup EFS or FileStore mounts in the container."""
    EFS_MOUNT = f"sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport {EFS_IP}:/ /efs"
    FILE_STORE_MOUNT = f"sudo mount -o rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,nolock {EFS_IP}:/{EFS_ROOT} /efs"
    COMMANDS = [
        "sudo mkdir -p /efs",
        EFS_MOUNT if EFS_TYPE == "EFS" else FILE_STORE_MOUNT,
        "sudo mkdir -p /efs",
        "sudo chown ray /efs",
        f"mkdir -p /efs/workspaces/{WORKSPACE_ID}/cluster_storage",
        f"sudo ln -sf /efs/workspaces/{WORKSPACE_ID}/cluster_storage {CLUSTER_STORAGE_DIR}",
        f"mkdir -p /efs/users/{USERNAME}",
        f"sudo ln -sf /efs/users/{USERNAME} /mnt/user_storage",
        "mkdir -p /efs/shared_storage",
        "sudo ln -sf /efs/shared_storage /mnt/shared_storage",
    ]
    for config in CONFIGS_TO_REPLICATE:
        COMMANDS.append(f"ln -sf /mnt/user_storage/{config} /home/ray/{config}")
    for cmd in COMMANDS:
        try:
            subprocess.check_call(cmd, shell=True)
        except Exception:
            logger.exception(f"Error running {cmd}")
            raise

    # on first load, report an activity to signal healthy start
    report_idle_termination_activity()


def setup_vscode_desktop():
    """Setup vscode desktop extension directory."""

    if SKIP_VSCODE_DESKTOP_SETUP:
        return

    local_folder = VSCODE_DESKTOP_SERVER_DIR
    remote_folder = os.path.join(CLUSTER_STORAGE_DIR, "vscode_desktop")

    # create the local folder
    os.makedirs(local_folder, exist_ok=True)

    # create the remote sub folders and link them
    sub_folders = ["data", "extensions"]
    for folder in sub_folders:
        directory = f"{remote_folder}/{folder}"
        os.makedirs(directory, exist_ok=True)
        os.symlink(directory, f"{local_folder}/{folder}")


def setup_container(ray_params: Any, is_head: bool):  # noqa: ARG001, PLR0912
    """Setup the container synchronously prior to Ray start.

    This handles (1) mounting network storage, (2) restoring workspace data, and
    (3) restoring credentials. This is intended to be triggered via the Ray start hook,
    i.e., ``RAY_START_HOOK=anyscale.snapshot_util.setup_container``.
    """
    if os.path.exists("/tmp/initialized"):
        logger.info("Init previously completed, skipping.")
        return
    if not EFS_IP:
        logger.info("No EFS IP configured, skipping workspace container setup.")
    else:
        try:
            setup_nfs()
        except Exception:
            logger.exception("Failed to setup NFS")
            raise
        if not WORKSPACE_ID:
            logger.info("No workspace id configured, skipping workspace restore.")
        elif not is_head:
            logger.info("Not head node, skipping workspace restore.")
        else:
            try:
                restore_latest()
            except Exception:
                logger.exception("Failed to restore workspace")
            try:
                setup_credentials()
            except Exception:
                logger.exception("Failed to setup SSH credentials")
            try:
                setup_vscode_desktop()
            except Exception:
                logger.exception("Failed to setup VSCode desktop")
    with open("/tmp/initialized", "w") as f:
        f.write("ok")


def autosnapshot_loop():
    if not WORKSPACE_ID:
        logger.info("Workspaces disabled.")
        return
    logger.info(f"Started autosnapshot loop with interval {SNAPSHOT_INTERVAL}")
    while True:
        time.sleep(SNAPSHOT_INTERVAL)
        do_snapshot(auto=True)


def post_build():
    CMDS = [
        "pip install -U https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp38-cp38-manylinux2014_x86_64.whl",
        # TODO: remove this after next image release.
        "echo 'PROMPT_COMMAND=\"history -a\"' >> /home/ray/.bashrc",
        "echo '[ -e ~/.workspacerc ] && source ~/.workspacerc' >> /home/ray/.bashrc",
        f"echo 'export PATH={CLUSTER_STORAGE_DIR}/pypi/bin:$PATH' >> /home/ray/.bashrc",
    ]
    for cmd in CMDS:
        print("Executing", cmd)
        subprocess.check_call(cmd, shell=True)


if __name__ == "__main__":
    import sys

    # Since this is also a main script, we need to set the log level here
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(os.environ.get("ANYSCALE_LOGLEVEL", "WARN"))

    if sys.argv[1] == "snapshot":
        do_snapshot()
    elif sys.argv[1] == "post_build":
        post_build()
    elif sys.argv[1] == "autosnapshot":
        autosnapshot_loop()
    elif sys.argv[1] == "restore":
        restore_latest()
    elif sys.argv[1] == "gc":
        gc_snapshots()
    elif sys.argv[1] == "put_env":
        put_env_var(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "get_env":
        get_env_var(sys.argv[2])
    elif sys.argv[1] == "del_env":
        del_env_var(sys.argv[2])
    elif sys.argv[1] == "setup_credentials":
        setup_credentials()
    elif sys.argv[1] == "setup_container":
        setup_container(None, True)
    else:
        print("unknown arg")
