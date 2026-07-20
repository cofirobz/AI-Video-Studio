"""DaVinci Resolve Studio editor provider.

Prerequisites (not automated here):
  1. DaVinci Resolve Studio must be running.
  2. Preferences > System > General > "External scripting using" must be set
     to "Local" (or "Network").
  3. RESOLVE_SCRIPT_API, RESOLVE_SCRIPT_LIB, and PYTHONPATH environment
     variables must point at Resolve's scripting modules — see Resolve's
     README_Developer.txt, typically under
     "C:/ProgramData/Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting".

Once those are in place, `import DaVinciResolveScript as dvr_script` succeeds
and `dvr_script.scriptapp("Resolve")` returns the live Resolve object this
provider would wrap.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.config import RenderSettings
from editor.base import EditorProvider

_NOT_IMPLEMENTED = "DaVinci Resolve Studio scripting API integration not yet implemented — see docs/roadmap.md"


class DaVinciEditor(EditorProvider):
    def __init__(self) -> None:
        self._resolve: Any | None = None

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
