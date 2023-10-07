import tempfile
from pathlib import Path

from jinja2 import Environment


class RenderContext:
    def __init__(self, output=Path | str | None):
        if output is None:
            output = tempfile.mkdtemp(prefix="unireport_")

        self.output_dir: Path = Path(output)

    def get_images_dir(self) -> Path:
        src_dir = self.output_dir / "src"
        if not src_dir.exists():
            src_dir.mkdir()

        return src_dir


class Plugin:
    def __init__(self):
        self.context: RenderContext | None = None

    def setup(self, _: Environment):
        pass

    def set_context(self, context: RenderContext):
        self.context = context
