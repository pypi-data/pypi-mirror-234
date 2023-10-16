# Copyright 2023 Agnostiq Inc.

import os
import platform
import time
from typing import Dict, List

import pennylane as qml
import requests
from covalent._shared_files import logger

from covalent_cloud.qelectron_sdk.executors.base import CloudQCluster, CloudQExecutor
from covalent_cloud.shared.classes.exceptions import CovalentSDKError

from ...._serialize.common import AssetType, _deserialize_asset, _serialize_asset
from ....shared.classes.api import QElectronAPI
from ...schemas.schemas import CircuitCreateSchema, QExecutorSpecs
from .base_client import BaseQClient

app_log = logger.app_log

"""QClient for a remote QServer"""

qserver_url = os.environ.get("COVALENT_CLOUD_QSERVER_URL", "https://api.quantum.dev.covalent.xyz/")


class RemoteQClient(BaseQClient):

    """
    Client for a remote QServer.
    """

    RESULT_POLL_FREQ = 5  # seconds

    def __init__(self) -> None:

        self.api_client = QElectronAPI(qserver_url, url_prefix="/api/v1")

        # Since the cloud qserver only tracks circuits and not
        # batches, the onus of assembling execution results within a
        # batch falls on the qclient.
        self._circuit_ids_by_batch_id: Dict[str, List[str]] = {}

    @property
    def selector(self):
        return self.deserialize(self.qserver.selector)

    @selector.setter
    def selector(self, selector_func):
        self.qserver.selector = self.serialize(selector_func)

    @property
    def database(self):
        return self.deserialize(self.qserver.database)

    # This will POST to the /circuits.
    def register(self, qscripts, executors, qelectron_info, qnode_specs) -> List[Dict]:
        allowed_executors = []

        # Each executor is a Pydantic model.
        # The variable `executors` contains one `QExecutor` or `QCluster`.
        real_executor = executors[0]

        # Unpack QCluster into allowed_executors and selectors.
        if isinstance(real_executor, CloudQCluster):
            selector = real_executor.selector
            for executor in real_executor.executors:
                attrs = executor.dict()
                name = attrs.get("name")
                allowed_executors.append(QExecutorSpecs(name=name, attributes=attrs))
        elif isinstance(real_executor, CloudQExecutor):
            selector = "random"
            attrs = real_executor.dict()
            name = attrs.get("name")
            allowed_executors.append(QExecutorSpecs(name=name, attributes=attrs))
        else:
            raise CovalentSDKError("Invalid quantum executor")

        circuit_name = qelectron_info.name
        circuit_description = qelectron_info.description

        dispatch_id = os.getenv("COVALENT_DISPATCH_ID")
        node_id = int(os.getenv("COVALENT_CURRENT_NODE_ID"))

        request_body = CircuitCreateSchema(
            python_version=platform.python_version(),
            dispatch_id=dispatch_id,
            node_id=node_id,
            circuit_name=circuit_name,
            circuit_description=circuit_description or "",
            qnode_specs=qnode_specs,
            allowed_qexecutors=allowed_executors,
            num_circuits=len(qscripts),
            selector=selector,
        )
        res = self.api_client.post(
            "/circuits",
            request_options={
                "data": request_body.json(),
            },
        )
        return res.json()

    def upload_asset(self, asset: bytes, url: str):
        raise NotImplementedError

    def start(self, circuit_ids: List[str]):
        res = self.api_client.post(
            "/qdispatches", request_options={"json": {"circuit_ids": circuit_ids}}
        )
        return res

    def submit(
        self, qscripts: List[qml.tape.QuantumScript], executors, qelectron_info, qnode_specs
    ) -> str:
        """
        Submit a batch of circuits to the qserver.

            Circuit submission consists of three stages:

            1. Register the circuits by POSTIng to /circuits. Save the
            returned sequence of circuit_ids.

            2. Upload circuits (qscripts) and circuit strings to the URLs returned in
            the previous response.

            3. Start the circuits by POSTing to /qdispatch
        """
        circuit_schemas = self.register(qscripts, executors, qelectron_info, qnode_specs)
        # app_log.debug(f"circuit_schemas: {circuit_schemas}")
        circuit_ids = list(map(lambda circuit: circuit.get("circuit_id"), circuit_schemas))

        if len(circuit_ids) == 0:
            raise CovalentSDKError(
                "No circuits were returned by the qserver after submission, no valid batch id available.",
                "remote_qclient/no-circuits-created",
            )

        # Identify a batch of circuits by the first circuit ID in the batch.
        batch_id = circuit_schemas[0]["batch_id"]
        self._circuit_ids_by_batch_id[batch_id] = circuit_ids

        # Upload serialized circuits and diagrams to the presigned S3 URLs.
        for i, qscript in enumerate(qscripts):
            circuit_url = circuit_schemas[i]["assets"]["circuit"]["uri"]
            circuit_str_url = circuit_schemas[i]["assets"]["circuit_string"]["uri"]

            # Get serialized qscript and circuit diagram string.
            ser_circuit = self.serialize(qscript)
            circuit_str = qscript.draw().encode("utf-8")

            # Upload assets to S3 using presigned URLs.
            requests.put(circuit_url, data=ser_circuit, timeout=None).raise_for_status()
            requests.put(circuit_str_url, data=circuit_str, timeout=None).raise_for_status()

        self.start(circuit_ids)

        return batch_id

    def get_remaining_circuit_ids(self, batch_id: str) -> List[str]:
        """Returns circuit IDs for all pending results."""
        res = self.api_client.get(f"/circuits/batches/{batch_id}")
        circuits = res.json()
        remaining_circuit_ids = []
        for circuit in circuits:
            if circuit.get("status") not in ["COMPLETED", "FAILED"]:
                remaining_circuit_ids.append(circuit.get("circuit_id"))
        return remaining_circuit_ids

    def get_results(self, batch_id: str):
        # Get all circuits to query for results.
        remaining_circuit_ids = self._circuit_ids_by_batch_id[batch_id]
        while len(remaining_circuit_ids) > 0:
            remaining_circuit_ids = self.get_remaining_circuit_ids(batch_id)
            time.sleep(self.RESULT_POLL_FREQ)

        deserialized_results = []
        for circuit_id in self._circuit_ids_by_batch_id[batch_id]:

            # Get the circuit info.
            circuit_info = self.api_client.get(f"/circuits/{circuit_id}").json()

            # Check if the circuit completed successfully.
            if circuit_info["status"] != "COMPLETED":
                error_msg = circuit_info["error"]
                raise RuntimeError(f"Circuit {circuit_id} failed to execute:\n{error_msg}")

            # Download results.
            result_uri = circuit_info["assets"]["result"]["uri"]
            res = requests.get(result_uri, timeout=None)
            res.raise_for_status()

            deserialized_results.append(self.deserialize(res.content))

        return deserialized_results

    def serialize(self, obj):
        return _serialize_asset(obj, AssetType.OBJECT)

    def deserialize(self, ser_obj):
        return _deserialize_asset(ser_obj, AssetType.OBJECT)
