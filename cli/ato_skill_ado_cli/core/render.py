from __future__ import annotations

import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def _env() -> Environment:
    return Environment(loader=FileSystemLoader("templates"), autoescape=False)


def render_markdown(template: str, data: dict) -> str:
    return _env().get_template(template).render(**data)


def render_markdown_custom(template_path: str, data: dict) -> str:
    template_file = Path(template_path)
    env = Environment(loader=FileSystemLoader(str(template_file.parent)), autoescape=False)
    return env.get_template(template_file.name).render(**data)


def write_manifest(path: Path, manifest: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
