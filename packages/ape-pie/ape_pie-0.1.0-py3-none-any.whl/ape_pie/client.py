"""
Implements an API client class as a :class:`requests.Session` subclass.

Some inspiration was taken from https://github.com/guillp/requests_oauth2client/,
notably:

* Implementing the client as a ``Session`` subclass
* Providing a base_url and making this absolute
"""
from contextlib import contextmanager
from typing import Any

# See https://github.com/gruns/furl/issues/148 for ongoing furl typing
from furl import furl  # type: ignore
from requests import Response, Session

from .exceptions import InvalidURLError
from .typing import ConfigAdapter

sentinel = object()


def is_base_url(url: str | furl) -> bool:
    """
    Check if a URL is not a relative path/URL.

    A URL is considered a base URL if it has:

    * a scheme
    * a netloc

    Protocol relative URLs like //example.com cannot be properly handled by requests,
    as there is no default adapter available.
    """
    if not isinstance(url, furl):
        url = furl(url)
    return bool(url.scheme and url.netloc)


class APIClient(Session):
    """
    A client instance, pinning a :class:`requests.Session` to a particular base URL.

    You can use the usual requests API, e.g. ``client.post("some-url")`` after
    instantiating a client instance. Whenever you use a relative URL, it will be
    appended to the :attr:`base_url`.

    The client prevents making requests to a different base/root than the configured
    base URL, so you don't accidentally leak session-wide credentials to places they
    were not intended to go.

    :arg base_url: The base URL of the API/service you intend to consume. Relative URLs
      in requests will be joined against this, while absolute/fully qualified URLs will
      be validated against the base URL.
    :arg request_kwargs: a mapping of keyword arguments you would typically pass to
      :meth:`requests.Session.request` or set on the session after instantiating it.
      They act as session-wide defaults which can be overridden on a per-request basis.
    :arg kwargs: any additional keyword arguments are simply ignored, but you may want
      to consume them if you're defining more specific client classes for your own
      needs.
    """

    base_url: str
    _request_kwargs: dict[str, Any]
    _in_context_manager: bool = False

    def __init__(
        self,
        base_url: str,
        request_kwargs: dict[str, Any] | None = None,
        **kwargs: Any,  # subclasses may require additional configuration
    ):
        # base class does not take any kwargs
        super().__init__()
        # normalize to dict
        request_kwargs = request_kwargs or {}

        self.base_url = base_url

        # set the attributes that requests.Session supports directly, but only if an
        # actual value was provided.
        for attr in self.__attrs__:
            val = request_kwargs.pop(attr, sentinel)
            if val is sentinel:
                continue
            setattr(self, attr, val)

        # store the remainder so we can inject it in the ``request`` method.
        self._request_kwargs = request_kwargs

    def __enter__(self):
        self._in_context_manager = True
        return super().__enter__()

    def __exit__(self, *args):
        self._in_context_manager = False
        return super().__exit__(*args)

    @classmethod
    def configure_from(cls, adapter: ConfigAdapter, **kwargs):
        base_url = adapter.get_client_base_url()
        session_kwargs = adapter.get_client_session_kwargs()
        return cls(base_url, session_kwargs, **kwargs)

    def request(
        self, method: str | bytes, url: str | bytes, *args, **kwargs
    ) -> Response:
        """
        Pre-process a request before calling the parent method.

        See the upstream :meth:`requests.Session.request` documentation for the API
        reference.
        """
        for attr, val in self._request_kwargs.items():
            kwargs.setdefault(attr, val)
        url = self.to_absolute_url(url)
        with self._maybe_close_session():
            return super().request(method, url, *args, **kwargs)

    @contextmanager
    def _maybe_close_session(self):
        """
        Clean up resources to avoid leaking them.

        A requests session uses connection pooling when used in a context manager, and
        the __exit__ method will properly clean up this connection pool when the block
        exists. However, it's also possible to instantiate and use a client outside a
        context block which potentially does not clean up any resources.

        We detect these situations and close the session if needed.
        """
        _should_close = not self._in_context_manager
        try:
            yield
        finally:
            if _should_close:
                self.close()

    def to_absolute_url(self, maybe_relative_url: str | bytes) -> str:
        # similar string normalization as in PreparedRequest.prepare_url
        if isinstance(maybe_relative_url, bytes):
            _maybe_relative_url = maybe_relative_url.decode("utf8")
        else:
            _maybe_relative_url = str(maybe_relative_url)

        base_furl = furl(self.base_url)
        # absolute here should be interpreted as "fully qualified url", with a protocol
        # and netloc
        is_absolute = is_base_url(_maybe_relative_url)
        if is_absolute:
            # we established the target URL is absolute, so ensure that it's contained
            # within the self.base_url domain, otherwise you risk sending credentials
            # intended for the base URL to some other domain.
            has_same_base = _maybe_relative_url.startswith(self.base_url)
            if not has_same_base:
                raise InvalidURLError(
                    f"Target URL {_maybe_relative_url} has a different base URL than "
                    f"the client ({self.base_url})."
                )
            return _maybe_relative_url
        fully_qualified = base_furl / _maybe_relative_url
        return str(fully_qualified)
