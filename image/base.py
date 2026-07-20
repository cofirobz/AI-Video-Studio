"""Abstract interface for AI image generation providers.

The rest of the app only ever talks to ImageProvider — never to a specific
provider's SDK/API directly. Select the active provider via
config/providers.yaml (`image: <name>`).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from core.config import Settings


class ImageProvider(ABC):
    @abstractmethod
    def generate_image(self, prompt: str, output_path: Path) -> Path:
        """Generate an image from a prompt and write it to output_path."""


def get_provider(settings: Settings) -> ImageProvider:
    """Instantiate the image provider configured in config/providers.yaml."""
    from image.flux import FluxImage
    from image.gpt_image import GPTImage

    registry: dict[str, type[ImageProvider]] = {
        "gpt_image": GPTImage,
        "flux": FluxImage,
    }
    name = settings.providers.image
    try:
        return registry[name]()
    except KeyError:
        raise ValueError(f"Unknown image provider '{name}'. Available: {sorted(registry)}") from None
