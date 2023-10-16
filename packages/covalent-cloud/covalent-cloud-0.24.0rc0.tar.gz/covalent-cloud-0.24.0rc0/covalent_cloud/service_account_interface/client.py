# Copyright 2023 Agnostiq Inc.

from typing import Optional

from covalent_cloud.shared.classes.api import DispatcherAPI
from covalent_cloud.shared.classes.settings import Settings


def get_client(settings: Optional[Settings] = None) -> DispatcherAPI:
    """
    A factory / getter method for the Dispatcher API client.

    Args:
        None

    Returns:
        An instance of `DispatcherAPI` client.

    """

    return DispatcherAPI(settings=settings)
