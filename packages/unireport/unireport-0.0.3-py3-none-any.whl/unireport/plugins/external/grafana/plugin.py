import uuid
from urllib.parse import parse_qs, urlparse

from jinja2 import Environment

from unireport.plugin import Plugin

from .api import GrafanaAPI


class GrafanaPlugin(Plugin):
    def __init__(self, api: GrafanaAPI):
        super().__init__()

        self.api: GrafanaAPI = api

    def setup(self, env: Environment):
        super().setup(env)

        env.globals["render_grafana_dashboard"] = self.render_grafana_dashboard

    def render_grafana_dashboard(self, url: str) -> str:
        result = urlparse(url)
        params = parse_qs(result.query)
        dashboard_id = "_".join(result.path.split("/")[-2:])
        dashboard_filename = f"{dashboard_id}_{uuid.uuid1()}.png"
        response = self.api.query_raw(f"render{result.path}", params=params)
        response.raise_for_status()
        with open(self.context.output / dashboard_filename, "wb") as f:
            f.write(response.content)

        return dashboard_filename
