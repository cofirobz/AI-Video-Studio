"""Small helpers shared by the CLI and the episode generator."""

from __future__ import annotations

import re

import yaml

from core.config import Settings


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "untitled"


def load_yaml_template(settings: Settings, filename: str) -> dict:
    path = settings.paths.resolve("templates") / filename
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
