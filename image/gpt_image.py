"""OpenAI GPT Image generation provider — not yet implemented."""

from __future__ import annotations

from pathlib import Path

from image.base import ImageProvider


class GPTImage(ImageProvider):
    def generate_image(self, prompt: str, output_path: Path) -> Path:
        raise NotImplementedError("requires the GPT Image API integration — see docs/roadmap.md")
