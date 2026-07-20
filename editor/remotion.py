"""Remotion (React-based programmatic video) editor provider — not yet implemented."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.config import RenderSettings
from editor.base import EditorProvider

_NOT_IMPLEMENTED = "Remotion integration not yet implemented — see docs/roadmap.md"


class RemotionEditor(EditorProvider):
    def create_project(self, name: str) -> Any:
        raise NotImplementedError(_NOT_IMPLEMENTED)

    def create_timeline(self, project: Any, name: str, render_settings: RenderSettings) -> Any:
        raise NotImplementedError(_NOT_IMPLEMENTED)

    def import_media(self, project: Any, file_paths: list[Path]) -> list[Any]:
        raise NotImplementedError(_NOT_IMPLEMENTED)

    def add_subtitles(self, timeline: Any, captions_path: Path) -> None:
        raise NotImplementedError(_NOT_IMPLEMENTED)

    def render(self, project: Any, render_settings: RenderSettings, output_path: Path) -> Path:
        raise NotImplementedError(_NOT_IMPLEMENTED)

    def export(self, project: Any, timeline: Any, export_path: Path) -> Path:
        raise NotImplementedError(_NOT_IMPLEMENTED)
