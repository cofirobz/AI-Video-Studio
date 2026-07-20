"""Stage: gather per-scene image/video prompts via the local PromptLibrary.

No external API calls — implemented now (unlike the other stages) to prove the
pipeline wiring works end-to-end up to the first stage that needs a provider.
"""

from __future__ import annotations

import logging

from automation.step import PipelineStep, StepResult
from core.models.episode import Episode
from core.prompt_library import PromptLibrary

logger = logging.getLogger(__name__)


class GeneratePromptsStep(PipelineStep):
    name = "generate_prompts"

    def __init__(self, library: PromptLibrary | None = None):
        self._library = library or PromptLibrary()

    def run(self, episode: Episode, context: dict) -> StepResult:
        if not episode.scenes:
            return StepResult(success=False, message="episode has no scenes to build prompts for")

        prompts_by_scene = {
            scene.index: {
                "image_prompt": scene.image_prompt or "",
                "video_prompt": scene.video_prompt or "",
            }
            for scene in episode.scenes
        }

        return StepResult(
            success=True,
            message=f"prepared prompts for {len(episode.scenes)} scene(s) "
            f"from a library of {len(self._library.list_by_category('image')) + len(self._library.list_by_category('video'))} templates",
            data={"prompts_by_scene": prompts_by_scene},
        )
