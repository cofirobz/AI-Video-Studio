"""Abstract interface for AI voice (TTS) generation providers.

The rest of the app only ever talks to VoiceProvider — never to a specific
provider's SDK/API directly. Select the active provider via
config/providers.yaml (`voice: <name>`).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from core.config import Settings


class VoiceProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str, voice_reference: str | None, output_path: Path) -> Path:
        """Synthesize speech for text (optionally cloning/matching voice_reference)."""


def get_provider(settings: Settings) -> VoiceProvider:
    """Instantiate the voice provider configured in config/providers.yaml."""
    from voice.cartesia import CartesiaVoice
    from voice.elevenlabs import ElevenLabsVoice

    registry: dict[str, type[VoiceProvider]] = {
        "elevenlabs": ElevenLabsVoice,
        "cartesia": CartesiaVoice,
    }
    name = settings.providers.voice
    try:
        return registry[name]()
    except KeyError:
        raise ValueError(f"Unknown voice provider '{name}'. Available: {sorted(registry)}") from None
