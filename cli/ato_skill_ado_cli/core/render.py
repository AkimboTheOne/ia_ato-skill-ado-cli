from __future__ import annotations

import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def _env() -> Environment:
    return Environment(loader=FileSystemLoader("templates"), autoescape=False)


def render_markdown(template: str, data: dict) -> str:
    return _env().get_template(template).render(**data)


def write_manifest(path: Path, manifest: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

