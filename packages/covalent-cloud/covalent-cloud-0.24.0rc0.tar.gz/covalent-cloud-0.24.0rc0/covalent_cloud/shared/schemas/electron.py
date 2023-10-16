# Copyright 2023 Agnostiq Inc.

"""Models for /api/v1/resultv2 endpoints"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .asset import AssetSchema

ELECTRON_METADATA_KEYS = {
    "task_group_id",
    "name",
    "start_time",
    "end_time",
    "status",
    # electron metadata
    "executor",
    "executor_data",
}

ELECTRON_ASSET_KEYS = {
    "function",
    "function_string",
    "output",
    "value",
    "error",
    "stdout",
    "stderr",
    # electron metadata
    "deps",
    "call_before",
    "call_after",
}

ELECTRON_FUNCTION_FILENAME = "function.pkl"
ELECTRON_FUNCTION_STRING_FILENAME = "function_string.txt"
ELECTRON_VALUE_FILENAME = "value.pkl"
ELECTRON_STDOUT_FILENAME = "stdout.log"
ELECTRON_STDERR_FILENAME = "stderr.log"
ELECTRON_ERROR_FILENAME = "error.log"
ELECTRON_RESULTS_FILENAME = "results.pkl"
ELECTRON_DEPS_FILENAME = "deps.pkl"
ELECTRON_CALL_BEFORE_FILENAME = "call_before.pkl"
ELECTRON_CALL_AFTER_FILENAME = "call_after.pkl"
ELECTRON_STORAGE_TYPE = "file"


ASSET_FILENAME_MAP = {
    "function": ELECTRON_FUNCTION_FILENAME,
    "function_string": ELECTRON_FUNCTION_STRING_FILENAME,
    "value": ELECTRON_VALUE_FILENAME,
    "output": ELECTRON_RESULTS_FILENAME,
    "deps": ELECTRON_DEPS_FILENAME,
    "call_before": ELECTRON_CALL_BEFORE_FILENAME,
    "call_after": ELECTRON_CALL_AFTER_FILENAME,
    "stdout": ELECTRON_STDOUT_FILENAME,
    "stderr": ELECTRON_STDERR_FILENAME,
    "error": ELECTRON_ERROR_FILENAME,
}


class ElectronAssets(BaseModel):
    function: AssetSchema
    function_string: AssetSchema
    value: AssetSchema
    output: AssetSchema
    error: Optional[AssetSchema]
    stdout: Optional[AssetSchema]
    stderr: Optional[AssetSchema]

    # electron_metadata
    deps: AssetSchema
    call_before: AssetSchema
    call_after: AssetSchema


class ElectronMetadata(BaseModel):
    task_group_id: int
    name: str
    executor: str
    executor_data: dict
    sub_dispatch_id: Optional[str]
    status: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]


class ElectronSchema(BaseModel):
    id: int
    metadata: ElectronMetadata
    assets: ElectronAssets
