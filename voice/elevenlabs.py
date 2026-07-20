"""ElevenLabs voice generation provider — not yet implemented."""

from __future__ import annotations

from pathlib import Path

from voice.base import VoiceProvider


class ElevenLabsVoice(VoiceProvider):
    def synthesize(self, text: str, voice_reference: str | None, output_path: Path) -> Path:
        raise NotImplementedError("requires the ElevenLabs API integration — see docs/roadmap.md")
