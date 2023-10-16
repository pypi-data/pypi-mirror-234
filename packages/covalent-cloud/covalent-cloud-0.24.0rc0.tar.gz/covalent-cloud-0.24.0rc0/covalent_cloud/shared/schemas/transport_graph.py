# Copyright 2023 Agnostiq Inc.

"""Models for /api/v1/resultv2 endpoints"""

from typing import List

from pydantic import BaseModel

from .edge import EdgeSchema
from .electron import ElectronSchema


class TransportGraphSchema(BaseModel):
    nodes: List[ElectronSchema]
    links: List[EdgeSchema]
