"""Stage: render this episode's timeline via the configured editor provider."""

from __future__ import annotations

from automation.step import PipelineStep, StepResult
from core.config import get_settings
from core.episode_repository import EpisodeRepository
from core.models.episode import Episode
from editor.base import get_provider


class RenderStep(PipelineStep):
    name = "render"

    def run(self, episode: Episode, context: dict) -> StepResult:
        settings = get_settings()
        provider = get_provider(settings)
        renders_dir = EpisodeRepository(settings).workspace_dir(episode.id) / "renders"

        output_path = provider.render(context.get("project"), settings.render, renders_dir / f"{episode.id}.mp4")

        return StepResult(success=True, message="rendered", data={"render_path": output_path})
