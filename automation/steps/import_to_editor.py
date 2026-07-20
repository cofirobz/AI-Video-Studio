"""Stage: create/open an editor project and import this episode's assets.

Delegates to whichever editor config/providers.yaml selects (DaVinci Resolve,
Remotion, ffmpeg, ...) — this step has no idea which one it's talking to.
"""

from __future__ import annotations

from automation.step import PipelineStep, StepResult
from core.config import get_settings
from core.episode_repository import EpisodeRepository
from core.models.episode import Episode
from editor.base import get_provider


class ImportToEditorStep(PipelineStep):
    name = "import_to_editor"

    def run(self, episode: Episode, context: dict) -> StepResult:
        settings = get_settings()
        provider = get_provider(settings)
        assets_dir = EpisodeRepository(settings).workspace_dir(episode.id) / "assets"

        project = provider.create_project(episode.id)
        timeline = provider.create_timeline(project, episode.id, settings.render)
        provider.import_media(project, sorted(assets_dir.glob("*")))

        return StepResult(
            success=True,
            message="imported into editor",
            data={"project": project, "timeline": timeline},
        )
