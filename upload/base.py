"""Abstract interface for platform upload providers.

The rest of the app only ever talks to UploadProvider — never to a specific
platform's SDK/API directly. Select the active provider via
config/providers.yaml (`upload: <name>`).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from core.config import Settings


class UploadProvider(ABC):
    @abstractmethod
    def upload(self, video_path: Path, title: str, description: str, hashtags: list[str]) -> str:
        """Upload the video and return its published URL (or platform id)."""


def get_provider(settings: Settings) -> UploadProvider:
    """Instantiate the upload provider configured in config/providers.yaml."""
    from upload.tiktok import TikTokUpload
    from upload.youtube import YouTubeUpload

    registry: dict[str, type[UploadProvider]] = {
        "youtube": YouTubeUpload,
        "tiktok": TikTokUpload,
    }
    name = settings.providers.upload
    try:
        return registry[name]()
    except KeyError:
        raise ValueError(f"Unknown upload provider '{name}'. Available: {sorted(registry)}") from None
