"""Workspace-directory-backed CRUD for Episode records.

Each episode is a self-contained folder: episodes/{id}/episode.yaml plus its
script.md, checklist.md, prompts/, assets/, renders/, exports/ — see
core/episode_generator.py for what populates those.
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

import yaml

from core.config import Settings, get_settings
from core.models.episode import Episode

logger = logging.getLogger(__name__)


class EpisodeRepository:
    def __init__(self, settings: Settings | None = None):
        self._settings = settings or get_settings()
        self._root = self._settings.paths.resolve("episodes")
        self._root.mkdir(parents=True, exist_ok=True)

    def workspace_dir(self, episode_id: str) -> Path:
        """The self-contained folder for one episode: episodes/{id}/."""
        return self._root / episode_id

    def _episode_file(self, episode_id: str) -> Path:
        return self.workspace_dir(episode_id) / "episode.yaml"

    def list_all(self) -> list[Episode]:
        return [self.get(p.parent.name) for p in sorted(self._root.glob("*/episode.yaml"))]

    def get(self, episode_id: str) -> Episode:
        with self._episode_file(episode_id).open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return Episode.model_validate(data)

    def save(self, episode: Episode) -> Path:
        if self.exists(episode.id):
            episode.version = self.get(episode.id).version + 1

        path = self._episode_file(episode.id)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(episode.model_dump(mode="json"), f, sort_keys=False, allow_unicode=True)
        logger.info("Saved episode '%s' to %s", episode.id, path)
        return path

    def delete(self, episode_id: str) -> None:
        shutil.rmtree(self.workspace_dir(episode_id), ignore_errors=True)

    def exists(self, episode_id: str) -> bool:
        return self._episode_file(episode_id).exists()
