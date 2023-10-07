from unittest.mock import patch

import pytest
import requests_mock
from hypothesis import given
from hypothesis import strategies as st
from requests.auth import HTTPBasicAuth
from requests_mock import ANY

from ape_pie import APIClient
from ape_pie.exceptions import InvalidURLError


class TestConfigAdapter:
    @staticmethod
    def get_client_base_url():
        return "https://from-factory.example.com"

    @staticmethod
    def get_client_session_kwargs():
        return {
            "verify": False,
            "timeout": 20,
            "auth": HTTPBasicAuth("superuser", "letmein"),
        }


def test_adapter_can_configure_session():
    adapter = TestConfigAdapter()

    client = APIClient.configure_from(adapter)

    assert client.verify is False
    assert client.auth is not None
    assert hasattr(client, "timeout") is False


http_methods = st.sampled_from(
    ["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]
)


def test_runtime_request_kwargs(requests_mock):
    m = requests_mock
    m.get(ANY, text="ok")
    adapter = TestConfigAdapter()

    with APIClient.configure_from(adapter) as client:
        client.get("https://from-factory.example.com/foo")

    assert m.last_request.url == "https://from-factory.example.com/foo"
    headers = m.last_request.headers
    assert "Authorization" in headers
    assert headers["Authorization"].startswith("Basic ") is True
    assert m.last_request.verify is False
    assert m.last_request.timeout == 20.0


def test_request_kwargs_overrule_defaults(requests_mock):
    m = requests_mock
    m.get(ANY, text="ok")
    adapter = TestConfigAdapter()

    with APIClient.configure_from(adapter) as client:
        client.get(
            "https://from-factory.example.com/foo",
            timeout=5,
            verify=True,
        )

    assert m.last_request.url == "https://from-factory.example.com/foo"
    headers = m.last_request.headers
    assert "Authorization" in headers
    assert headers["Authorization"].startswith("Basic ") is True
    assert m.last_request.verify is True
    assert m.last_request.timeout == 5.0


@given(method=http_methods)
def test_applies_to_any_http_method(method):
    adapter = TestConfigAdapter()

    with requests_mock.Mocker() as m, APIClient.configure_from(adapter) as client:
        m.register_uri(ANY, ANY)

        client.request(method, "https://from-factory.example.com/foo")

    assert len(m.request_history), 1
    assert m.last_request.url == "https://from-factory.example.com/foo"
    assert m.last_request.method, method
    headers = m.last_request.headers
    assert "Authorization" in headers
    assert headers["Authorization"].startswith("Basic ") is True
    assert m.last_request.verify is False
    assert m.last_request.timeout == 20.0


@given(method=http_methods)
def test_relative_urls_are_made_absolute(method):
    adapter = TestConfigAdapter()
    client = APIClient.configure_from(adapter)

    with (
        requests_mock.Mocker() as m,
        client,
    ):
        m.register_uri(ANY, ANY)

        client.request(method, "foo")

    assert len(m.request_history), 1
    assert m.last_request.url == "https://from-factory.example.com/foo"


@given(method=http_methods)
def test_relative_bytestring_urls_are_made_absolute(method):
    adapter = TestConfigAdapter()
    client = APIClient.configure_from(adapter)

    with (
        requests_mock.Mocker() as m,
        client,
    ):
        m.register_uri(ANY, ANY)

        client.request(method, b"foo")

    assert len(m.request_history), 1
    assert m.last_request.url == "https://from-factory.example.com/foo"


@given(method=http_methods)
def test_absolute_urls_must_match_base_url(method):
    adapter = TestConfigAdapter()
    client = APIClient.configure_from(adapter)

    with pytest.raises(InvalidURLError):
        client.request(method, "https://example.com/bar")


@given(method=http_methods)
def test_absolute_urls_must_match_base_url_happy_flow(method):
    adapter = TestConfigAdapter()
    client = APIClient.configure_from(adapter)

    with (
        requests_mock.Mocker() as m,
        client,
    ):
        m.register_uri(ANY, ANY)

        client.request(method, "https://from-factory.example.com/foo/bar")

    assert len(m.request_history), 1
    assert m.last_request.url == "https://from-factory.example.com/foo/bar"


@given(method=http_methods)
def test_discouraged_usage_without_context(method):
    client = APIClient("https://example.com")

    with (
        requests_mock.Mocker() as m,
        patch.object(client, "close", wraps=client.close) as mock_close,
    ):
        m.register_uri(ANY, ANY)

        client.request(method, "foo")

    assert len(m.request_history), 1
    mock_close.assert_called_once()


@given(method=http_methods)
def test_encouraged_usage_with_context_do_not_close_prematurely(method):
    client = APIClient("https://example.com")

    with (
        requests_mock.Mocker() as m,
        patch.object(client, "close", wraps=client.close) as mock_close,
        client,
    ):
        m.register_uri(ANY, ANY)

        client.request(method, "foo")

        # may not be called inside context block
        mock_close.assert_not_called()

    assert len(m.request_history), 1
    # must be called outside context block
    mock_close.assert_called_once()
