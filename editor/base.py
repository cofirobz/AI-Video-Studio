"""Abstract interface for video-editing/render backends (DaVinci Resolve, Remotion, ffmpeg, ...).

The rest of the app (automation/steps/*) only ever talks to EditorProvider —
never to a specific editor's SDK/API directly. Select the active provider via
config/providers.yaml (`editor: <name>`).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from core.config import RenderSettings, Settings


class EditorProvider(ABC):
    @abstractmethod
    def create_project(self, name: str) -> Any:
        """Create (or open) a project for this episode."""

    @abstractmethod
    def create_timeline(self, project: Any, name: str, render_settings: RenderSettings) -> Any:
        """Create a timeline sized per render_settings (resolution, fps)."""

    @abstractmethod
    def import_media(self, project: Any, file_paths: list[Path]) -> list[Any]:
        """Import files (voice, video, image, music, SFX) into the project."""

    @abstractmethod
    def add_subtitles(self, timeline: Any, captions_path: Path) -> None:
        """Import an .srt file onto the timeline's subtitle track."""

    @abstractmethod
    def render(self, project: Any, render_settings: RenderSettings, output_path: Path) -> Path:
        """Queue and run the render, writing under output_path. Returns the rendered file path."""

    @abstractmethod
    def export(self, project: Any, timeline: Any, export_path: Path) -> Path:
        """Export the rendered output to export_path, ready for upload."""


def get_provider(settings: Settings) -> EditorProvider:
    """Instantiate the editor provider configured in config/providers.yaml."""
    from editor.davinci import DaVinciEditor
    from editor.ffmpeg import FFmpegEditor
    from editor.remotion import RemotionEditor

    registry: dict[str, type[EditorProvider]] = {
        "davinci": DaVinciEditor,
        "remotion": RemotionEditor,
        "ffmpeg": FFmpegEditor,
    }
    name = settings.providers.editor
    try:
        return registry[name]()
    except KeyError:
        raise ValueError(f"Unknown editor provider '{name}'. Available: {sorted(registry)}") from None
