import string
from urllib.parse import quote_plus, urlsplit

import pytest
from furl import furl
from hypothesis import assume, example, given
from hypothesis import strategies as st
from hypothesis.provisional import domains, urls

from ape_pie.client import is_base_url

printable_text = st.text(string.printable)


@given(domains())
def test_domain_without_protocol(item: str):
    assume(not item.startswith("http://"))
    assume(not item.startswith("https://"))

    assert is_base_url(item) is False


@given(st.text(string.printable))
@example("/some/absolute/path")
def test_random_text_without_protocol(item: str):
    assume(not item.startswith("http://"))
    assume(not item.startswith("https://"))

    try:
        is_base = is_base_url(item)
    except ValueError:
        # furl got something that it can't parse as a URL, and we do want to bubble
        # this error up to the caller
        pass
    else:
        assert is_base is False


@given(
    st.sampled_from(["https", "http", "ftp", "file"]),
    st.lists(printable_text.map(quote_plus)).map("/".join),
)
def test_protocol_but_no_netloc(protocol, path):
    url = f"{protocol}:///{path}"

    assert is_base_url(url) is False


@given(urls())
def test_rfc_3986_url(url):
    assert url.startswith("http://") or url.startswith("https://")
    bits = urlsplit(url)
    # not allowed for communication between hosts - it's a way to request a dynamically
    # allocated port number.
    assume(bits.port != 0)

    assert is_base_url(url) is True


@given(
    st.sampled_from(["ftp", "file", "madeupthing"]),
    domains(),
    st.lists(printable_text.map(quote_plus)).map("/".join),
)
def test_non_http_protocol(protocol, domain, path):
    url = f"{protocol}://{domain}/{path}"

    # we don't really care about the actual protocol, you *could* install a requests
    # adapter for non-http(s)
    assert is_base_url(url) is True


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/foo",
        furl("https://example.com/foo"),
    ],
)
def test_handle_str_or_furl_instance(url):
    assert is_base_url(url) is True
