"""Abstract interface for AI video-clip generation providers.

The rest of the app only ever talks to VideoProvider — never to a specific
provider's SDK/API directly. Select the active provider via
config/providers.yaml (`video: <name>`).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from core.config import Settings


class VideoProvider(ABC):
    @abstractmethod
    def generate_clip(self, prompt: str, duration_seconds: float, output_path: Path) -> Path:
        """Generate a video clip from a prompt and write it to output_path."""


def get_provider(settings: Settings) -> VideoProvider:
    """Instantiate the video provider configured in config/providers.yaml."""
    from video.kling import KlingVideo
    from video.runway import RunwayVideo
    from video.veo import VeoVideo

    registry: dict[str, type[VideoProvider]] = {
        "runway": RunwayVideo,
        "veo": VeoVideo,
        "kling": KlingVideo,
    }
    name = settings.providers.video
    try:
        return registry[name]()
    except KeyError:
        raise ValueError(f"Unknown video provider '{name}'. Available: {sorted(registry)}") from None
