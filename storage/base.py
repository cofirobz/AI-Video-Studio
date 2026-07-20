"""Abstract interface for storage backends.

The rest of the app only ever talks to StorageProvider — never to a specific
backend directly. Select the active provider via config/providers.yaml
(`storage: <name>`).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from core.config import Settings


class StorageProvider(ABC):
    @abstractmethod
    def save(self, local_path: Path, remote_key: str) -> str:
        """Persist local_path under remote_key. Returns a reference (path/URL) to it."""

    @abstractmethod
    def load(self, remote_key: str, local_path: Path) -> Path:
        """Fetch remote_key to local_path. Returns local_path."""


def get_provider(settings: Settings) -> StorageProvider:
    """Instantiate the storage provider configured in config/providers.yaml."""
    from storage.local import LocalStorage

    registry: dict[str, type[StorageProvider]] = {
        "local": LocalStorage,
    }
    name = settings.providers.storage
    try:
        return registry[name]()
    except KeyError:
        raise ValueError(f"Unknown storage provider '{name}'. Available: {sorted(registry)}") from None
