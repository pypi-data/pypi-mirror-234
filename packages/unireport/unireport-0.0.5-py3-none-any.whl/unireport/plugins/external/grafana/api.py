from typing import Tuple, Union
from urllib.parse import urlparse

import requests

from unireport.plugins.external.grafana.client import GrafanaClient

DEFAULT_TIMEOUT = 10.0


class GrafanaAPI:
    def __init__(
        self,
        auth=None,
        host="localhost",
        port=None,
        url_path_prefix="",
        protocol="http",
        timeout=DEFAULT_TIMEOUT,
    ):
        self.client = GrafanaClient(
            auth,
            host=host,
            port=port,
            url_path_prefix=url_path_prefix,
            protocol=protocol,
            timeout=timeout,
        )
        self.url = None

    @classmethod
    def from_url(
        cls,
        url: str = "http://admin:admin@localhost:3000",
        credential: Union[str, Tuple[str, str], requests.auth.AuthBase] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        """
        Factory method to create a `GrafanaApi` instance from a URL.

        Accepts an optional credential, which is either an authentication
        token, or a tuple of (username, password).
        """

        if credential is not None and not isinstance(
            credential, (str, Tuple, requests.auth.AuthBase)
        ):
            raise TypeError(f"Argument 'credential' has wrong type: {type(credential)}")

        original_url = url
        url = urlparse(url)

        # Use username and password from URL.
        if credential is None and url.username:
            credential = (url.username, url.password)

        grafana = cls(
            credential,
            protocol=url.scheme,
            host=url.hostname,
            port=url.port,
            url_path_prefix=url.path.lstrip("/"),
            timeout=timeout,
        )
        grafana.url = original_url

        return grafana

    def query_raw(self, url, params=None):
        response = self.client.get(url, params=params)
        return response
