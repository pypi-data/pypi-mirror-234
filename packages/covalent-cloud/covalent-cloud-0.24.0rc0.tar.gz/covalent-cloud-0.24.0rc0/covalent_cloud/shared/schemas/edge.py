# Copyright 2023 Agnostiq Inc.


"""Models for /api/v1/resultv2 endpoints"""

from typing import Optional

from pydantic import BaseModel

EDGE_METADATA_KEYS = {
    "edge_name",
    "param_type",
    "arg_index",
}


class EdgeMetadata(BaseModel):
    edge_name: str
    param_type: Optional[str]
    arg_index: Optional[int]


class EdgeSchema(BaseModel):
    source: int
    target: int
    metadata: EdgeMetadata
