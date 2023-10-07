import uuid
from urllib.parse import parse_qs, urlparse

from jinja2 import Environment

from unireport.exceptions import RendererException
from unireport.plugin import Plugin

from .api import GrafanaAPI


class GrafanaPlugin(Plugin):
    def __init__(self, api: GrafanaAPI):
        super().__init__()

        self.api: GrafanaAPI = api

    def setup(self, env: Environment):
        super().setup(env)

        env.globals["render_grafana_dashboard"] = self.render_grafana_dashboard

    def render_grafana_dashboard(self, url: str, **kwargs) -> str:
        result = urlparse(url)
        params = parse_qs(result.query)
        params.update(**kwargs)

        response = self.api.query_raw(f"render{result.path}", params=params)
        response.raise_for_status()
        header = response.headers
        content_type = header.get("content-type")
        if content_type not in ("image/png",):
            raise RendererException(f"Invalid content-type {content_type}")

        dashboard_id = "_".join(result.path.split("/")[-2:])
        dashboard_filename = (
            self.context.get_images_dir() / f"{dashboard_id}_{uuid.uuid1()}.png"
        )
        with open(dashboard_filename, "wb") as f:
            f.write(response.content)

        relative = dashboard_filename.relative_to(self.context.output_dir)
        return str(relative)
