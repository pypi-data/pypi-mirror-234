# Copyright 2023 Agnostiq Inc.

import os
from pathlib import Path
from typing import Union

from pydantic import BaseModel, BaseSettings


class AuthSettings(BaseModel):
    """
    Authentication settings.

    token: Authentication token.
    api_key: API key.
    config_file: Path to the config file. Defaults to "~/.config/covalent_cloud/credentials.toml".
    config_file_section: Section in the config file. Defaults to "auth".
    config_file_token_keyname: Keyname for the token in the config file. Defaults to "token".
    config_file_api_key_keyname: Keyname for the API key in the config file. Defaults to "api_key".

    """

    token: str = ""  # AUTH__TOKEN env
    api_key: str = ""  # api_key
    config_file: str = str(
        Path(os.environ.get("HOME")) / Path(".config/covalent_cloud") / Path("credentials.toml")
    )  # AUTH__CONFIG_FILE env
    config_file_section: str = "auth"
    config_file_token_keyname: str = "token"
    config_file_api_key_keyname: str = "api_key"


class Settings(BaseSettings):
    """
    Settings for the Covalent Cloud.

    auth: Authentication settings.
    dispatcher_uri: URI for the dispatcher. Defaults to "https://api.covalent.xyz".
    dispatcher_port: Port for the dispatcher. Defaults to None.
    dispatch_cache_dir: Directory for the dispatch cache. Defaults to "~/.cache/covalent/dispatches".
    results_dir: Directory for the results. Defaults to "~/.cache/covalent/results".
    validate_executors: Whether to validate executors. Defaults to True.

    """

    auth: AuthSettings = AuthSettings()

    dispatcher_uri: str = "https://api.covalent.xyz"
    dispatcher_port: Union[int, None] = None

    dispatch_cache_dir: str = os.environ["HOME"] + "/.cache" + "/covalent/dispatches"
    results_dir: str = os.environ["HOME"] + "/.cache" + "/covalent/results"

    validate_executors: bool = True

    class Config:
        env_prefix = "COVALENT_CLOUD_"
        env_nested_delimiter = "__"


settings = Settings()
