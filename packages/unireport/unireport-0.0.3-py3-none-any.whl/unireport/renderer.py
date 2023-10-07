from hashlib import md5
from pathlib import Path
from typing import List

from jinja2 import Environment, Template, select_autoescape

from .plugin import Plugin, RenderContext


class ReportRenderer:
    def __init__(self, jinja2_env: Environment | None = None):
        if jinja2_env is None:
            jinja2_env = Environment(autoescape=select_autoescape())

        self.env = jinja2_env
        self.plugins: List[Plugin] = []

    def register(self, *args):
        for plugin in args:
            plugin: Plugin
            self.plugins.append(plugin)
            plugin.setup(self.env)

    def render_from_file(
        self,
        template_filename: str,
        data: {},
        output: Path = None,
    ):
        template = self.env.get_template(template_filename)
        return self._render(template, data, output)

    def render_from_string(
        self,
        template_string: str,
        data: {},
        output: Path = None,
    ):
        template = self.env.from_string(template_string)
        digest = md5(template_string.encode("utf-8")).hexdigest()
        template.name = f"template_{digest}"
        return self._render(template, data, output)

    def _render(self, template: Template, data: {}, output: Path | None):
        context = RenderContext(output=output)
        for p in self.plugins:
            p.set_context(context)

        try:
            result = template.render(data)
            if output:
                result_file = output / template.name
                with open(result_file, "w", encoding="utf8") as f:
                    f.write(result)

            return result
        finally:
            for p in self.plugins:
                p.set_context(context)
