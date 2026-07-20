"""Stage: turn an episode's hook/story into a full scene-by-scene script.

Intended behavior: call Claude via the Anthropic API using the
'script_generator' prompt from core.prompt_library, parse the response into
Scene entries on the episode, and write the full text into the episode
workspace's script.md (see core/frontmatter.py).
"""

from __future__ import annotations

from automation.step import PipelineStep, StepResult
from core.models.episode import Episode


class GenerateScriptStep(PipelineStep):
    name = "generate_script"

    def run(self, episode: Episode, context: dict) -> StepResult:
        raise NotImplementedError("requires the Anthropic API integration — see docs/roadmap.md")
