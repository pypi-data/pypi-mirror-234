import requests

DEFAULT_TIMEOUT = 30


class TokenAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers.update({"Authorization": f"Bearer {self.token}"})
        return request


class GrafanaClient:
    def __init__(
        self,
        auth,
        host="localhost",
        port=None,
        url_path_prefix="",
        protocol="http",
        timeout=DEFAULT_TIMEOUT,
    ):
        self.auth = auth
        self.timeout = timeout
        self.url_host = host
        self.url_port = port
        self.url_path_prefix = url_path_prefix
        self.url_protocol = protocol

        def construct_api_url():
            params = {
                "protocol": self.url_protocol,
                "host": self.url_host,
                "url_path_prefix": self.url_path_prefix,
            }

            if self.url_port is None:
                url_pattern = "{protocol}://{host}/{url_path_prefix}"
            else:
                params["port"] = self.url_port
                url_pattern = "{protocol}://{host}:{port}/{url_path_prefix}"

            return url_pattern.format(**params)

        self.grafana_root = construct_api_url()

        self.session = requests.Session()

        if auth is not None:
            if isinstance(auth, requests.auth.AuthBase):
                pass
            elif isinstance(auth, tuple):
                self.auth = requests.auth.HTTPBasicAuth(*auth)
            else:
                self.auth = TokenAuth(auth)

    def __getattr__(self, method):
        def __http_method_override(url, **kwargs):
            __url = self.grafana_root + url
            method_call = getattr(self.session, method.lower())
            return method_call(
                __url,
                auth=self.auth,
                verify=self.verify,
                timeout=self.timeout,
                **kwargs,
            )

        return __http_method_override
