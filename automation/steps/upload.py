"""Stage: upload the exported file via the configured upload provider.

Not part of build_default_pipeline() yet — this is Phase 4 work, added to the
pipeline once a real upload provider is implemented. See docs/roadmap.md.
"""

from __future__ import annotations

from automation.step import PipelineStep, StepResult
from core.config import get_settings
from core.models.episode import Episode
from upload.base import get_provider


class UploadStep(PipelineStep):
    name = "upload"

    def run(self, episode: Episode, context: dict) -> StepResult:
        settings = get_settings()
        provider = get_provider(settings)

        url = provider.upload(context.get("export_path"), episode.title, episode.hook, [])

        return StepResult(success=True, message=f"uploaded to {url}", data={"url": url})
