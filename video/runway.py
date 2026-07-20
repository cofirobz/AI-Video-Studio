"""Runway video generation provider — not yet implemented."""

from __future__ import annotations

from pathlib import Path

from video.base import VideoProvider


class RunwayVideo(VideoProvider):
    def generate_clip(self, prompt: str, duration_seconds: float, output_path: Path) -> Path:
        raise NotImplementedError("requires the Runway API integration — see docs/roadmap.md")
