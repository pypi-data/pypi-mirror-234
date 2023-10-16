# Copyright 2023 Agnostiq Inc.


"""Models for /api/v1/resultv2 endpoints"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .asset import AssetSchema
from .lattice import (
    LATTICE_ERROR_FILENAME,
    LATTICE_INPUTS_FILENAME,
    LATTICE_RESULTS_FILENAME,
    LatticeSchema,
)

METADATA_KEYS = {
    "start_time",
    "end_time",
    "dispatch_id",
    "root_dispatch_id",
    "status",
    "num_nodes",
}


ASSET_KEYS = {
    "inputs",
    "result",
    "error",
}


ASSET_FILENAME_MAP = {
    "inputs": LATTICE_INPUTS_FILENAME,
    "result": LATTICE_RESULTS_FILENAME,
    "error": LATTICE_ERROR_FILENAME,
}


class ResultMetadata(BaseModel):
    dispatch_id: str
    root_dispatch_id: str
    status: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]


class ResultAssets(BaseModel):
    inputs: AssetSchema
    result: AssetSchema
    error: AssetSchema


class ResultSchema(BaseModel):
    metadata: ResultMetadata
    assets: ResultAssets
    lattice: LatticeSchema
