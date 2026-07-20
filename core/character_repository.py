"""YAML-backed CRUD for Character records under paths.characters."""

from __future__ import annotations

import logging
from pathlib import Path

import yaml

from core.config import Settings, get_settings
from core.models.character import Character

logger = logging.getLogger(__name__)


class CharacterRepository:
    def __init__(self, settings: Settings | None = None):
        self._settings = settings or get_settings()
        self._dir = self._settings.paths.resolve("characters")
        self._dir.mkdir(parents=True, exist_ok=True)

    def _path(self, character_id: str) -> Path:
        return self._dir / f"{character_id}.yaml"

    def list_all(self) -> list[Character]:
        return [self.get(p.stem) for p in sorted(self._dir.glob("*.yaml"))]

    def get(self, character_id: str) -> Character:
        with self._path(character_id).open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return Character.model_validate(data)

    def save(self, character: Character) -> Path:
        path = self._path(character.id)
        with path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(character.model_dump(mode="json"), f, sort_keys=False, allow_unicode=True)
        logger.info("Saved character '%s' to %s", character.id, path)
        return path

    def delete(self, character_id: str) -> None:
        self._path(character_id).unlink(missing_ok=True)

    def exists(self, character_id: str) -> bool:
        return self._path(character_id).exists()
