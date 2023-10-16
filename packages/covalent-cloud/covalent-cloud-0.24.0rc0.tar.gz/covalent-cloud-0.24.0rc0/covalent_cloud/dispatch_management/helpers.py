# Copyright 2023 Agnostiq Inc.


"""Module for Covalent Cloud dispatching and related functionalities."""

import os
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, wait
from copy import deepcopy
from functools import wraps
from pathlib import Path
from typing import Callable, List, Optional

import requests
from covalent._results_manager.result import Result
from covalent._shared_files import logger
from covalent._shared_files.defaults import parameter_prefix
from covalent._workflow.lattice import Lattice
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TaskID

from .._serialize.result import merge_response_manifest, serialize_result, strip_local_uris
from ..shared.classes.api import APIClient
from ..shared.classes.exceptions import (
    CovalentAPIKeyError,
    CovalentGenericAPIError,
    CovalentSDKError,
)
from ..shared.classes.settings import Settings, settings
from ..shared.schemas.asset import AssetSchema
from ..shared.schemas.result import ResultSchema

_dispatch_executor = ThreadPoolExecutor()

_VALID_EXECUTORS = {"cloud"}

dispatch_cache_dir = Path(settings.dispatch_cache_dir)
dispatch_cache_dir.mkdir(parents=True, exist_ok=True)

app_log = logger.app_log


class AssetUploadThreadFailure(CovalentSDKError):
    message: str = "One or more asset upload threads did not finish execution."
    code: str = "dispatch/asset-upload-thread/fail"

    def __init__(self) -> None:
        super().__init__(self.message, self.code)


class AssetUploadException(CovalentSDKError):
    message: str = "One or more asset upload raised exceptions."
    code: str = "dispatch/asset-upload/exception"

    def __init__(self, msg: str = ""):
        super().__init__(message=msg, code=self.code)


def validate_executors(lat: Lattice) -> bool:
    # Check lattice default executor and workflow_executor

    valid_lattice_executors = True
    valid_electron_executors = True

    if lat.metadata["executor"] not in _VALID_EXECUTORS:
        app_log.debug(f"Found illegal lattice executor: {lat.metadata['executor']}")
        valid_lattice_executors = False
    if lat.metadata["workflow_executor"] not in _VALID_EXECUTORS:
        app_log.debug(
            f"Found illegal lattice workflow executor: {lat.metadata['workflow_executor']}"
        )
        valid_lattice_executors = False

    tg = lat.transport_graph

    for i in tg._graph.nodes:
        name = tg.get_node_value(i, "name")

        if name.startswith(parameter_prefix):
            continue

        metadata = tg.get_node_value(i, "metadata")
        if metadata["executor"] not in _VALID_EXECUTORS:
            app_log.debug(f"Found illegal electron executor: {metadata['executor']} in node {i}")
            valid_electron_executors = False
            break

    return valid_lattice_executors and valid_electron_executors


def inject_parameter_outputs(lat: Lattice):
    # Hack to pre-compute the output of parameter nodes. This will be
    # no longer needed once OS develop does the same during
    # `build_graph`.

    tg = lat.transport_graph
    if not tg._graph.nodes:
        return

    for node_id in tg._graph.nodes:
        name = tg.get_node_value(node_id, "name")
        if name.startswith(parameter_prefix):
            value = tg.get_node_value(node_id, "value")
            tg.set_node_value(node_id, "output", value)


# For multistage dispatches


def register(
    orig_lattice: Lattice,
    settings: Settings = settings,
) -> Callable:
    """
    Wrapping the dispatching functionality to allow input passing
    and server address specification.

    Afterwards, send the lattice to the dispatcher server and return
    the assigned dispatch id.

    Args:
        orig_lattice: The lattice/workflow to send to the dispatcher server.
        dispatcher_addr: The address of the dispatcher server.  If None then then defaults to the address set in Covalent's config.

    Returns:
        Wrapper function which takes the inputs of the workflow as arguments
    """

    dispatcher_addr = settings.dispatcher_uri

    @wraps(orig_lattice)
    def wrapper(*args, **kwargs) -> str:
        """
        Send the lattice to the dispatcher server and return
        the assigned dispatch id.

        Args:
            *args: The inputs of the workflow.
            **kwargs: The keyword arguments of the workflow.

        Returns:
            The dispatch id of the workflow.
        """

        lattice = deepcopy(orig_lattice)

        lattice.build_graph(*args, **kwargs)

        # Temporary workaround until OS develop also
        # does this during `build_graph.

        inject_parameter_outputs(lattice)

        with tempfile.TemporaryDirectory() as tmp_dir:
            manifest = prepare_manifest(lattice, tmp_dir)
            return_manifest = register_manifest(manifest, settings)
            dispatch_id = return_manifest.metadata.dispatch_id

            path = dispatch_cache_dir / f"{dispatch_id}"

            with open(path, "w") as f:
                f.write(manifest.json())

            upload_assets(manifest)

            return dispatch_id

    return wrapper


def start(
    dispatch_id: str,
    settings: Settings = settings,
) -> Callable:
    """
    Wrapping the dispatching functionality to allow input passing
    and server address specification.

    Afterwards, send the lattice to the dispatcher server and return
    the assigned dispatch id.

    Args:
        orig_lattice: The lattice/workflow to send to the dispatcher server.
        dispatcher_addr: The address of the dispatcher server.  If None then then defaults to the address set in Covalent's config.

    Returns:
        Wrapper function which takes the inputs of the workflow as arguments
    """

    dispatcher_addr = settings.dispatcher_uri
    client = APIClient(host_uri=dispatcher_addr, settings=settings)
    endpoint = f"/api/v1/dispatchv2/start/{dispatch_id}"

    try:
        r = client.put(endpoint)
    except requests.exceptions.HTTPError as e:
        print(e.response.text, file=sys.stderr)
        raise e
    return r.content.decode("utf-8").strip().replace('"', "")


def prepare_manifest(lattice, storage_path) -> ResultSchema:
    """Prepare a built-out lattice for submission"""

    result_object = Result(lattice)
    return serialize_result(result_object, storage_path)


def register_manifest(
    manifest: ResultSchema,
    settings: Settings = settings,
    parent_dispatch_id: Optional[str] = None,
    push_assets: bool = True,
) -> ResultSchema:
    """Submits a manifest for registration.

    Returns:
        Dictionary representation of manifest with asset remote_uris filled in

    Side effect:
        If push_assets is False, the server will
        automatically pull the task assets from the submitted asset URIs.

    Raises:
        CovalentAPIKeyError: If the API key is invalid.

    """
    dispatcher_addr = settings.dispatcher_uri

    stripped = strip_local_uris(manifest) if push_assets else manifest
    client = APIClient(host_uri=dispatcher_addr, settings=settings)
    endpoint = "/api/v2/lattices"

    if parent_dispatch_id:
        endpoint = f"{endpoint}/{parent_dispatch_id}"

    try:
        r = client.post(endpoint, request_options={"data": stripped.json()})
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401 and e.response.json()["code"] == "auth/unauthorized":
            raise CovalentAPIKeyError(
                message="A valid API key is required to register a dispatch.",
                code=e.response.json()["code"],
            ) from e
        else:
            raise CovalentGenericAPIError(error=e)

    parsed_resp = ResultSchema.parse_obj(r.json())

    return merge_response_manifest(manifest, parsed_resp)


def upload_assets(manifest: ResultSchema):
    assets = _extract_assets(manifest)
    _upload(assets)


def _extract_assets(manifest: ResultSchema) -> List[AssetSchema]:
    # workflow-level assets
    dispatch_assets = manifest.assets
    assets = [asset for key, asset in dispatch_assets]
    lattice = manifest.lattice
    lattice_assets = lattice.assets
    assets.extend(asset for key, asset in lattice_assets)
    # Node assets
    tg = lattice.transport_graph
    nodes = tg.nodes
    for node in nodes:
        node_assets = node.assets
        assets.extend(asset for key, asset in node_assets)
    return assets


def _upload(assets: List[AssetSchema]) -> None:
    """Upload assets to remote storage.

    Args:
        assets: List of AssetSchema objects to upload.

    Raises:
        RuntimeError: If any of the assets fail to upload.

    """
    total_assets = len(assets)
    _upload_futures = []

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>4.1f}%",
        MofNCompleteColumn(),
    ) as progress:
        task = progress.add_task("[green]Uploading assets...", total=total_assets)

        for asset in assets:
            fut = _dispatch_executor.submit(
                _upload_asset, asset.uri, asset.remote_uri, task, progress
            )
            _upload_futures.append(fut)

        done, _ = wait(_upload_futures)

        if len(done) < total_assets:
            raise AssetUploadThreadFailure

        _exceptions = []
        for fut in done:
            if ex := fut.exception(timeout=0.1):
                _exceptions.append(ex)

        if _exceptions:
            msg = f"Attempted and failed to upload {len(_exceptions)} out of {total_assets} due to raised exceptions."
            print(msg, file=sys.stderr)
            app_log.debug(_exceptions)
            raise AssetUploadException(msg)


def _upload_asset(local_uri: str, remote_uri: str, task: TaskID, progress: Progress) -> None:
    """Upload a single asset to remote storage.

    Args:
        local_uri: Local URI of the asset to upload.
        remote_uri: Remote URI to upload the asset to.
        task: Task ID of the progress bar task.
        progress: Progress bar object.

    Raises:
        requests.exceptions.HTTPError: If the upload fails.

    """
    scheme_prefix = "file://"
    if local_uri.startswith(scheme_prefix):
        local_path = local_uri[len(scheme_prefix) :]
    else:
        local_path = local_uri

    try:
        if os.path.getsize(local_path) == 0:
            r = requests.put(remote_uri, headers={"Content-Length": "0"}, data="")
        else:
            with open(local_path, "rb") as f:
                r = requests.put(remote_uri, data=f)
                r.raise_for_status()
    except Exception:
        raise

    if r.status_code == requests.codes.ok:
        progress.advance(task, advance=1)
        progress.refresh()
