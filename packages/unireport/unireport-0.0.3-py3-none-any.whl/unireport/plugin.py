from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment


@dataclass
class RenderContext:
    output: Path | None = None


class Plugin:
    def __init__(self):
        self.context: RenderContext | None = None

    def setup(self, _: Environment):
        pass

    def set_context(self, context: RenderContext):
        self.context = context
