from __future__ import annotations

import ssl
from typing import Any, Callable, Iterator, Optional, Union

import OpenSSL
import requests
import requests.hooks
import urllib3
from urllib3 import Retry
from urllib3.contrib.pyopenssl import PyOpenSSLContext

import toolforge_weld
from toolforge_weld.kubernetes_config import Kubeconfig, ToolforgeKubernetesConfigError


# TODO: these are available natively starting with python 3.9
# but toolforge bastions run python 3.7 as of this writing
def _removesuffix(input_string: str, suffix: str) -> str:
    if suffix and input_string.endswith(suffix):
        return input_string[: -len(suffix)]  # noqa: E203
    return input_string


def _removeprefix(input_string: str, prefix: str) -> str:
    if prefix and input_string.startswith(prefix):
        return input_string[len(prefix) :]  # noqa: E203
    return input_string


# Unfortunately, there's no support for loading certificates directly from memory instead of reading it from the filesystem
# This helps work around that (from https://stackoverflow.com/questions/45410508/python-requests-ca-certificates-as-a-string)
class ClientSideCertificateHTTPAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, *args, cert, key, **kwargs):
        self._cert = cert
        self._key = key
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        # This is the one that works for us, might change :/
        ctx = PyOpenSSLContext(ssl.PROTOCOL_SSLv23)
        kwargs["ssl_context"] = ctx
        ctx._ctx.use_certificate(self._cert)
        ctx._ctx.use_privatekey(self._key)
        return super().init_poolmanager(*args, **kwargs)


ConnectionError = Union[
    requests.exceptions.HTTPError, requests.exceptions.ConnectionError
]
"""A type alias for any error types that might be handled by a connection error handler."""


class ToolforgeClient:
    """Toolforge API client."""

    def __init__(
        self,
        *,
        server: str,
        kubeconfig: Kubeconfig,
        user_agent: str,
        timeout: int = 10,
        exception_handler: Optional[
            Callable[[requests.exceptions.HTTPError], Exception]
        ] = None,
        connect_exception_handler: Optional[
            Callable[[ConnectionError], Exception]
        ] = None,
    ):
        self.exception_handler = exception_handler
        self.connect_exception_handler = connect_exception_handler

        self.timeout = timeout
        self.server = server
        self.session = requests.Session()

        if kubeconfig.client_cert_file and kubeconfig.client_key_file:
            self.session.cert = (
                str(kubeconfig.client_cert_file),
                str(kubeconfig.client_key_file),
            )
        elif kubeconfig.client_cert_data and kubeconfig.client_key_data:
            cert = OpenSSL.crypto.load_certificate(
                OpenSSL.crypto.FILETYPE_PEM, kubeconfig.client_cert_data.encode("utf-8")
            )
            key = OpenSSL.crypto.load_privatekey(
                OpenSSL.crypto.FILETYPE_PEM, kubeconfig.client_key_data
            )
            adapter = ClientSideCertificateHTTPAdapter(
                cert=cert, key=key, max_retries=Retry(total=10, backoff_factor=0.5)
            )
            self.session.mount(_removesuffix(self.server, "/"), adapter)
        elif kubeconfig.token:
            self.session.headers["Authorization"] = f"Bearer {kubeconfig.token}"
        else:
            raise ToolforgeKubernetesConfigError(
                "Kubernetes configuration is missing authentication details"
            )

        if kubeconfig.ca_file:
            self.session.verify = str(kubeconfig.ca_file)
        else:
            self.session.verify = False

            # T253412: Disable warnings about unverifed TLS certs when talking to the
            # Kubernetes API endpoint
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.session.headers[
            "User-Agent"
        ] = f"{user_agent} toolforge_weld/{toolforge_weld.__version__} python-requests/{requests.__version__}"

    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        try:
            response = self.session.request(method, **self.make_kwargs(url, **kwargs))
            response.raise_for_status()
            return response
        except requests.exceptions.ConnectionError as e:
            if self.connect_exception_handler:
                raise self.connect_exception_handler(e) from e
            raise e
        except requests.exceptions.HTTPError as e:
            # Raise a connection error on proxy (= api-gateway) level
            # errors to provide more uniform error messages.
            if e.response.status_code in (502, 503) and self.connect_exception_handler:
                raise self.connect_exception_handler(e) from e

            if self.exception_handler:
                raise self.exception_handler(e) from e
            raise e

    def make_kwargs(self, url: str, **kwargs) -> dict[str, Any]:
        """Setup kwargs for a Requests request."""
        kwargs["url"] = "{}/{}".format(
            _removesuffix(self.server, "/"), _removeprefix(url, "/")
        )

        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        return kwargs

    def get(self, url, **kwargs) -> dict[str, Any]:
        """GET request."""
        return self._make_request("GET", url, **kwargs).json()

    def post(self, url, **kwargs) -> dict[str, Any]:
        """POST request."""
        return self._make_request("POST", url, **kwargs).json()

    def put(self, url, **kwargs) -> dict[str, Any]:
        """PUT request."""
        return self._make_request("PUT", url, **kwargs).json()

    def delete(self, url, **kwargs) -> dict[str, Any]:
        """DELETE request."""
        return self._make_request("DELETE", url, **kwargs).json()

    def get_raw_lines(self, url, method: str = "GET", **kwargs) -> Iterator[str]:
        """Stream the raw lines from a specific API endpoint."""
        with self._make_request(
            method,
            url,
            headers=None,
            stream=True,
            **kwargs,
        ) as r:
            yield from r.iter_lines(decode_unicode=True)
