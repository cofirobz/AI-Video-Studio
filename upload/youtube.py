"""YouTube Shorts upload provider — not yet implemented."""

from __future__ import annotations

from pathlib import Path

from upload.base import UploadProvider


class YouTubeUpload(UploadProvider):
    def upload(self, video_path: Path, title: str, description: str, hashtags: list[str]) -> str:
        raise NotImplementedError("requires the YouTube Data API integration — see docs/roadmap.md")
