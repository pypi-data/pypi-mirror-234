# Copyright 2023 Agnostiq Inc.

"""Models for /api/v1/resultv2 endpoints"""

from typing import Optional

from pydantic import BaseModel


class AssetSchema(BaseModel):
    digest_alg: Optional[str]
    digest: Optional[str]
    uri: Optional[str]
    remote_uri: Optional[str]

    # Size of the asset in bytes
    size: Optional[int]
