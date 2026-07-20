"""Stage: export the finished render via the configured editor provider."""

from __future__ import annotations

from automation.step import PipelineStep, StepResult
from core.config import get_settings
from core.episode_repository import EpisodeRepository
from core.models.episode import Episode
from editor.base import get_provider


class ExportStep(PipelineStep):
    name = "export"

    def run(self, episode: Episode, context: dict) -> StepResult:
        settings = get_settings()
        provider = get_provider(settings)
        exports_dir = EpisodeRepository(settings).workspace_dir(episode.id) / "exports"

        export_path = provider.export(
            context.get("project"), context.get("timeline"), exports_dir / f"{episode.id}.mp4"
        )

        return StepResult(success=True, message="exported", data={"export_path": export_path})
