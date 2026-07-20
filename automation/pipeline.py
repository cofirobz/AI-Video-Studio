"""Orchestrates an ordered sequence of PipelineStep objects for one episode."""

from __future__ import annotations

import logging

from automation.step import PipelineStep
from core.models.episode import Episode

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, steps: list[PipelineStep]):
        self._steps = steps

    def run(self, episode: Episode) -> dict:
        """Run each step in order. Stops at the first failed or not-yet-implemented step."""
        context: dict = {}
        for step in self._steps:
            logger.info("[%s] starting stage '%s'", episode.id, step.name)
            try:
                result = step.run(episode, context)
            except NotImplementedError as exc:
                logger.warning(
                    "[%s] stage '%s' is not implemented yet (%s) - stopping pipeline here. "
                    "See docs/roadmap.md for the phase that implements it.",
                    episode.id,
                    step.name,
                    exc,
                )
                break
            except Exception:
                logger.exception("[%s] stage '%s' raised an unexpected error", episode.id, step.name)
                break

            if not result.success:
                logger.error("[%s] stage '%s' failed: %s", episode.id, step.name, result.message)
                break

            logger.info("[%s] stage '%s' complete: %s", episode.id, step.name, result.message)
            context.update(result.data)

        return context


def build_default_pipeline() -> Pipeline:
    """The idea-to-export sequence. Upload is a separate, later stage — see automation/steps/upload.py."""
    from automation.steps.export import ExportStep
    from automation.steps.generate_assets import GenerateAssetsStep
    from automation.steps.generate_prompts import GeneratePromptsStep
    from automation.steps.generate_script import GenerateScriptStep
    from automation.steps.import_to_editor import ImportToEditorStep
    from automation.steps.render import RenderStep

    return Pipeline(
        [
            GenerateScriptStep(),
            GeneratePromptsStep(),
            GenerateAssetsStep(),
            ImportToEditorStep(),
            RenderStep(),
            ExportStep(),
        ]
    )
