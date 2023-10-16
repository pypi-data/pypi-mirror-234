# Copyright 2023 Agnostiq Inc.


import os

import requests
from furl import furl

from covalent_cloud.service_account_interface.auth_config_manager import AuthConfigManager
from covalent_cloud.shared.classes.settings import Settings, settings


class APIClient:

    api_key: str
    uri_components: furl
    auth_config: AuthConfigManager

    @property
    def host(self):
        return self.uri_components.host

    @property
    def port(self):
        return self.uri_components.port

    @property
    def scheme(self):
        return self.uri_components.scheme

    def __init__(self, host_uri, port=None, headers=None, settings=None, url_prefix="") -> None:
        if headers is None:
            headers = {}
        if settings is None:
            settings = Settings()

        self.uri_components = furl(host_uri)
        self.settings = settings
        self.headers = headers
        self.url_prefix = url_prefix

        if port:
            self.uri_components.set(port=port)

    def get_global_headers(self):
        auth_headers = AuthConfigManager.get_auth_request_headers(self.settings)
        return {**auth_headers, **self.headers}

    def get_request_options(self, request_options):
        request_options = request_options or {}
        provided_headers = request_options.get("headers") or {}
        options = {
            **request_options,
            "headers": {
                **self.get_global_headers(),
                **provided_headers,
            },
        }
        return options

    def prepare_request(self, endpoint, request_options=None):
        uri_components = self.uri_components.copy()
        uri_components.path = uri_components.path / self.url_prefix / endpoint
        uri = uri_components.url
        options = self.get_request_options(request_options)
        return uri, options

    def post(self, endpoint, request_options=None):
        uri, options = self.prepare_request(endpoint, request_options)
        res = requests.post(uri, **options)
        res.raise_for_status()
        return res

    def get(self, endpoint, request_options=None):
        uri, options = self.prepare_request(endpoint, request_options)
        res = requests.get(uri, **options)
        res.raise_for_status()
        return res

    def delete(self, endpoint, request_options=None):
        uri, options = self.prepare_request(endpoint, request_options)
        res = requests.delete(uri, **options)
        res.raise_for_status()
        return res

    def put(self, endpoint, request_options=None):
        uri, options = self.prepare_request(endpoint, request_options)
        res = requests.put(uri, **options)
        res.raise_for_status()
        return res


class QElectronAPI(APIClient):
    def __init__(self, host_uri, url_prefix="") -> None:
        super().__init__(host_uri, url_prefix=url_prefix)

    def get_global_headers(self):
        return {"X-SESSION-TOKEN": os.getenv("COVALENT_JOB_SESSION_TOKEN")}


class DispatcherAPI(APIClient):
    def __init__(self, headers=None, settings: Settings = settings) -> None:
        if headers is None:
            headers = {}
        super().__init__(
            host_uri=settings.dispatcher_uri,
            port=settings.dispatcher_port,
            headers=headers,
            settings=settings,
        )
