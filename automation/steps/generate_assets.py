"""Stage: call image/video/voice generation providers for each scene.

Delegates entirely to whichever providers config/providers.yaml selects —
this step has no idea which concrete provider (Runway, ElevenLabs, ...) it's
talking to. Assets are written into this episode's own workspace.
"""

from __future__ import annotations

from automation.step import PipelineStep, StepResult
from core.config import get_settings
from core.episode_repository import EpisodeRepository
from core.models.episode import Episode
from image.base import get_provider as get_image_provider
from video.base import get_provider as get_video_provider
from voice.base import get_provider as get_voice_provider


class GenerateAssetsStep(PipelineStep):
    name = "generate_assets"

    def run(self, episode: Episode, context: dict) -> StepResult:
        settings = get_settings()
        image_provider = get_image_provider(settings)
        video_provider = get_video_provider(settings)
        voice_provider = get_voice_provider(settings)
        assets_dir = EpisodeRepository(settings).workspace_dir(episode.id) / "assets"

        for scene in episode.scenes:
            if scene.image_prompt:
                image_provider.generate_image(scene.image_prompt, assets_dir / f"scene_{scene.index}_image.png")
            if scene.video_prompt:
                video_provider.generate_clip(
                    scene.video_prompt, scene.duration_seconds or 0.0, assets_dir / f"scene_{scene.index}_video.mp4"
                )
            if scene.voice_line:
                voice_provider.synthesize(scene.voice_line, None, assets_dir / f"scene_{scene.index}_voice.mp3")

        raise NotImplementedError(
            f"configured providers (image={settings.providers.image}, video={settings.providers.video}, "
            f"voice={settings.providers.voice}) are not yet implemented — see docs/roadmap.md"
        )
