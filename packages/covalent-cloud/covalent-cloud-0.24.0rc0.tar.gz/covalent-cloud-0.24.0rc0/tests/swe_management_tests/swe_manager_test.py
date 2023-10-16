# Copyright 2023 Agnostiq Inc.

"""Unit tests for software environment management module."""

import json
import os
from unittest.mock import ANY, MagicMock

from covalent_cloud.service_account_interface.auth_config_manager import AuthConfigManager
from covalent_cloud.shared.classes.settings import settings
from covalent_cloud.swe_management.swe_manager import (
    API_KEY,
    COVALENT_CLOUD_URL,
    create_env,
    delete_env,
    get_pip_pkgs,
    unpack_conda_pkgs,
)

TEMP_REQUIREMENT_FILEPATH = "/tmp/requirements.txt"
TEMP_ENV_YML_FILEPATH = "/tmp/environment.yml"
PIP_PKGS = [
    "numpy==1.19.5",
    "pandas==0.0.1",
    "scikit-learn",
    "aiohttp>1.0.0",
    "boto3<=1.0.0",
    "matplotlib<=1.0.0,>.0.3.4",
    "request!=1.0.0",
]
CONDA_ENV_YML = """
name: mockenv
channels:
  - javascript
dependencies:
  - python=3.9
  - bokeh=2.4.2
  - conda-forge::numpy=1.21.*
  - nodejs=16.13.*
  - flask
  - pip
  - pip:
    - Flask-Testing
"""
CONDA_CHANNELS = ["javascript"]
CONDA_DEPENDENCIES = [
    "python=3.9",
    "bokeh=2.4.2",
    "conda-forge::numpy=1.21.*",
    "nodejs=16.13.*",
    "flask",
    "pip",
    {"pip": ["Flask-Testing"]},
]
MOCK_CONDA_ENV_NAME = "mockenv"
MOCK_PIP_PKGS = ["mock-package-1", "mock-package-2"]
MOCK_CHANNELS = ["mock-channel-1", "mock-channel-2"]
MOCK_DEPENDENCIES = [
    "mock-dependency-1",
    "mock-dependency-2",
    {"pip": ["mock-pip-dependency-1", "mock-pip-dependency-2"]},
]
MOCK_VARIABLES = [
    {"name": "mock-variable-1", "value": "1", "sensitive": True},
    {"name": "mock-variable-2", "value": "2", "sensitive": False},
]


def create_temp_requirement_file():
    """Create a temporary requirements.txt file."""
    with open(TEMP_REQUIREMENT_FILEPATH, "w") as f:
        for pkg in PIP_PKGS:
            f.write(pkg + "\n")


def remove_temp_requirement_file():
    """Remove the temporary requirements.txt file."""
    os.remove(TEMP_REQUIREMENT_FILEPATH)


def create_conda_env_file():
    """Create a temporary conda environment.yml file."""
    with open(TEMP_ENV_YML_FILEPATH, "w") as f:
        f.write(CONDA_ENV_YML)


def remove_conda_env_file():
    """Remove the temporary conda environment.yml file."""
    os.remove(TEMP_ENV_YML_FILEPATH)


def test_get_pip_pkgs_str():
    """Test the get pip packages function."""
    create_temp_requirement_file()
    pip_pkgs = get_pip_pkgs(TEMP_REQUIREMENT_FILEPATH)
    assert pip_pkgs == PIP_PKGS
    remove_temp_requirement_file()


def test_get_pip_pkgs_list():
    """Test the get pip packages function."""
    create_temp_requirement_file()
    pip_pkgs = get_pip_pkgs(PIP_PKGS)
    assert pip_pkgs == PIP_PKGS
    remove_temp_requirement_file()


def test_get_pip_pkgs_list_with_requirements():
    """Test the get pip packages function."""
    create_temp_requirement_file()
    pip_pkgs = get_pip_pkgs(["mock-package", TEMP_REQUIREMENT_FILEPATH, "mock-package-2"])
    assert pip_pkgs == ["mock-package"] + PIP_PKGS + ["mock-package-2"]
    remove_temp_requirement_file()


def test_unpack_conda_pkgs_str():
    """Test the unpack conda packages function."""
    create_conda_env_file()
    channels, dependencies = unpack_conda_pkgs(TEMP_ENV_YML_FILEPATH)
    assert channels == CONDA_CHANNELS
    assert dependencies == CONDA_DEPENDENCIES
    remove_conda_env_file()


def test_unpack_conda_pkgs_list():
    """Test the unpack conda packages function."""
    create_conda_env_file()
    channels, dependencies = unpack_conda_pkgs(CONDA_DEPENDENCIES)
    assert channels == []
    assert dependencies == CONDA_DEPENDENCIES
    remove_conda_env_file()


def test_unpack_conda_pkgs_dict():
    """Test the unpack conda packages function."""
    create_conda_env_file()
    channels, dependencies = unpack_conda_pkgs(
        {
            "channels": CONDA_CHANNELS,
            "dependencies": CONDA_DEPENDENCIES,
        }
    )
    assert channels == CONDA_CHANNELS
    assert dependencies == CONDA_DEPENDENCIES
    remove_conda_env_file()


def test_create_env(mocker):
    """Test the create environment function."""
    MOCK_CREATE_DEPENDENCIES = ["mock-dependency-1", "mock-dependency-2"]
    AuthConfigManager.save_api_key(API_KEY)  # This will overite your local key

    temp_file_mock = mocker.patch("tempfile.NamedTemporaryFile")
    requests_mock = mocker.patch("requests.post")

    mock_file_handle = MagicMock()
    mock_file_handle.name = "mock_name"
    mock_ctx_mgr = MagicMock()
    mock_ctx_mgr.__enter__ = MagicMock(return_value=mock_file_handle)

    mocker.patch("covalent_cloud.swe_management.swe_manager.open", return_value=mock_ctx_mgr)

    get_pip_pkgs_mock = mocker.patch(
        "covalent_cloud.swe_management.swe_manager.get_pip_pkgs", return_value=MOCK_PIP_PKGS
    )
    unpack_conda_pkgs_mock = mocker.patch(
        "covalent_cloud.swe_management.swe_manager.unpack_conda_pkgs",
        return_value=(MOCK_CHANNELS, MOCK_CREATE_DEPENDENCIES),
    )

    create_env(MOCK_CONDA_ENV_NAME, MOCK_PIP_PKGS, MOCK_CREATE_DEPENDENCIES, MOCK_VARIABLES)

    get_pip_pkgs_mock.assert_called_once_with(MOCK_PIP_PKGS)
    unpack_conda_pkgs_mock.assert_called_once_with(MOCK_CREATE_DEPENDENCIES)

    data = {
        "name": MOCK_CONDA_ENV_NAME,
        "variables": json.dumps(MOCK_VARIABLES),
    }
    files = {"definition": mock_file_handle}
    requests_mock.assert_called_once_with(
        f"{settings.dispatcher_uri}/api/v2/envs", data=data, files=files, headers=ANY
    )


def test_delete_env(mocker):
    """Test the delete environment function."""
    requests_mock = mocker.patch("covalent_cloud.swe_management.swe_manager.requests")
    params = {"env_name": MOCK_CONDA_ENV_NAME, "api_key": API_KEY}
    delete_env(MOCK_CONDA_ENV_NAME)
    requests_mock.delete.assert_called_once_with(f"{COVALENT_CLOUD_URL}/delete_env", params=params)
