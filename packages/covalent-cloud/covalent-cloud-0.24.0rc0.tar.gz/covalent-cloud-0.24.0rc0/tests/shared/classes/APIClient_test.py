# Copyright 2023 Agnostiq Inc.


from covalent_cloud.shared.classes.api import APIClient
from covalent_cloud.shared.classes.settings import AuthSettings, Settings


class TestAPIClient:

    MOCK_URI = "https://www.example.com"

    def test_get_global_headers(self, mocker):
        MOCK_API_KEY = "mock-api-key"  # pragma: allowlist secret
        # substituting token avoids fetching/creating from config file
        settings = Settings(auth=AuthSettings(api_key=MOCK_API_KEY))
        MOCK_GLOBAL_HEADERS = {
            "x-api-key": MOCK_API_KEY,
        }
        api = APIClient(host_uri=self.MOCK_URI, headers={"CLIENT": "TEST"}, settings=settings)
        assert api.get_global_headers() == {"CLIENT": "TEST", **MOCK_GLOBAL_HEADERS}

    def test_prepare_request(self, mocker):
        # substituting token avoids fetching/creating from config file
        MOCK_API_KEY = "mock_api_key"  # pragma: allowlist secret
        settings = Settings(auth=AuthSettings(api_key=MOCK_API_KEY))
        api = APIClient(host_uri="http://some.site/", headers={}, settings=settings)
        uri, options = api.prepare_request("/test", {"data": 123})
        assert uri == "http://some.site/test"
        assert options == {
            "headers": {
                "x-api-key": MOCK_API_KEY,
            },
            "data": 123,
        }

    def test_get_request_options(self, mocker):
        # substituting token avoids fetching/creating from config file
        MOCK_API_KEY = "mock_api_key"  # pragma: allowlist secret
        settings = Settings(auth=AuthSettings(api_key=MOCK_API_KEY))
        api = APIClient(host_uri=self.MOCK_URI, headers={}, settings=settings)
        options = api.get_request_options({"body": {"a": 1}})
        assert options["body"] == {"a": 1}

    def test_post(self, mocker):

        api_mock = APIClient(host_uri=self.MOCK_URI)
        requests_mock = mocker.patch("covalent_cloud.shared.classes.api.requests")

        MOCK_REQUEST_OPTIONS = {"json": {"a": 1}, "data": b"ef8"}

        mocker.patch.object(api_mock, "get_request_options", return_value=MOCK_REQUEST_OPTIONS)
        api_mock.post("/api/v0/resource", MOCK_REQUEST_OPTIONS)
        requests_mock.post.assert_called_with(
            f"{self.MOCK_URI}/api/v0/resource", **MOCK_REQUEST_OPTIONS
        )

    def test_get(self, mocker):

        api_mock = APIClient(host_uri=self.MOCK_URI)
        requests_mock = mocker.patch("covalent_cloud.shared.classes.api.requests")

        MOCK_REQUEST_OPTIONS = {
            "params": {"a": 1},
        }

        mocker.patch.object(api_mock, "get_request_options", return_value=MOCK_REQUEST_OPTIONS)
        api_mock.get("/api/v0/resource", MOCK_REQUEST_OPTIONS)
        requests_mock.get.assert_called_with(
            f"{self.MOCK_URI}/api/v0/resource", **MOCK_REQUEST_OPTIONS
        )

    def test_delete(self, mocker):

        api_mock = APIClient(host_uri=self.MOCK_URI)
        requests_mock = mocker.patch("covalent_cloud.shared.classes.api.requests")

        mocker.patch.object(api_mock, "get_request_options")
        api_mock.delete("/api/v0/resource")
        requests_mock.delete.assert_called_with(f"{self.MOCK_URI}/api/v0/resource")

    def test_put(self, mocker):

        api_mock = APIClient(host_uri=self.MOCK_URI)
        requests_mock = mocker.patch("covalent_cloud.shared.classes.api.requests")

        MOCK_REQUEST_OPTIONS = {
            "json": {"a": 1},
        }

        mocker.patch.object(api_mock, "get_request_options", return_value=MOCK_REQUEST_OPTIONS)
        api_mock.put("/api/v0/resource", MOCK_REQUEST_OPTIONS)
        requests_mock.put.assert_called_with(
            f"{self.MOCK_URI}/api/v0/resource", **MOCK_REQUEST_OPTIONS
        )
