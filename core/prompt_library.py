"""Loads and renders prompt templates stored as YAML under prompts/<category>/."""

from __future__ import annotations

import logging

import yaml
from pydantic import BaseModel, Field

from core.config import Settings, get_settings

logger = logging.getLogger(__name__)

CATEGORIES = ["claude", "claude_code", "image", "video", "voice", "thumbnail"]


class PromptTemplate(BaseModel):
    name: str
    category: str
    description: str = ""
    template: str
    variables: list[str] = Field(default_factory=list)

    def render(self, **kwargs: str) -> str:
        missing = [v for v in self.variables if v not in kwargs]
        if missing:
            raise KeyError(f"Missing variables for prompt '{self.name}': {missing}")
        return self.template.format(**kwargs)


class PromptLibrary:
    def __init__(self, settings: Settings | None = None):
        self._settings = settings or get_settings()
        self._dir = self._settings.paths.resolve("prompts")
        self._templates: dict[str, PromptTemplate] = {}
        self.reload()

    def reload(self) -> None:
        self._templates.clear()
        for category in CATEGORIES:
            category_dir = self._dir / category
            if not category_dir.exists():
                continue
            for file in sorted(category_dir.glob("*.yaml")):
                with file.open("r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                template = PromptTemplate.model_validate(data)
                self._templates[template.name] = template
        logger.info("Loaded %d prompt templates", len(self._templates))

    def get(self, name: str) -> PromptTemplate:
        return self._templates[name]

    def list_by_category(self, category: str) -> list[PromptTemplate]:
        return [t for t in self._templates.values() if t.category == category]

    def render(self, name: str, **kwargs: str) -> str:
        return self.get(name).render(**kwargs)
