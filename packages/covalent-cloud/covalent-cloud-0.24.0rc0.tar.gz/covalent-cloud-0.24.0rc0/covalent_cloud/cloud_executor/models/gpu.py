# Copyright 2023 Agnostiq Inc.


from enum import Enum

from pydantic.dataclasses import dataclass


class GPU_TYPES(Enum):
    V100 = "v100"


@dataclass
class GPU:
    type: GPU_TYPES = GPU_TYPES.V100
    num: int = 0
