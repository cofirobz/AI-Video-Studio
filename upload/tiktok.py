"""TikTok upload provider — not yet implemented."""

from __future__ import annotations

from pathlib import Path

from upload.base import UploadProvider


class TikTokUpload(UploadProvider):
    def upload(self, video_path: Path, title: str, description: str, hashtags: list[str]) -> str:
        raise NotImplementedError("requires the TikTok API integration — see docs/roadmap.md")
