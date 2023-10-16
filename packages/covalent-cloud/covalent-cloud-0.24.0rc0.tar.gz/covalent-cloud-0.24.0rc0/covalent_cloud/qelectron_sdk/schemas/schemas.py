# Copyright 2023 Agnostiq Inc.

import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class QNodeSpecs(BaseModel):
    gate_sizes: Dict[str, int]
    gate_types: Dict[str, int]
    num_operations: int
    num_observables: int
    num_diagonalizing_gates: int
    num_used_wires: int
    depth: int
    num_trainable_params: int = None
    num_device_wires: int
    device_name: str
    diff_method: Optional[str]
    expansion_strategy: str
    gradient_options: Dict[str, int]
    interface: Optional[str]
    gradient_fn: Optional[str]
    num_gradient_executions: Any = 0
    num_parameter_shift_executions: int = None


class AssetMetadata(BaseModel):
    uri: str
    size: int


class CircuitAssets(BaseModel):
    circuit: Optional[AssetMetadata] = None
    circuit_string: Optional[AssetMetadata] = None
    result: Optional[AssetMetadata] = None
    result_string: Optional[AssetMetadata] = None


class QExecutorSpecs(BaseModel):
    name: str
    attributes: Dict


# Request body for `/register`
class CircuitCreateSchema(BaseModel):
    """Request body for the /register endpoint"""

    python_version: str
    dispatch_id: uuid.UUID
    node_id: int
    circuit_name: str
    circuit_description: str
    qnode_specs: QNodeSpecs

    # Clarify
    allowed_qexecutors: List[QExecutorSpecs]

    # Number of circuits in the batch
    num_circuits: int

    # Object store URIs -- assigned by the server
    assets: Optional[CircuitAssets] = None

    # Unique ID of a circuit -- assigned by the server
    circuit_id: Optional[str] = None

    selector: Optional[str] = None
