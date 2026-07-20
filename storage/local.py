"""Local filesystem storage provider — the only fully implemented one.

No external API is involved, so this backend works today: remote_key is
treated as a path relative to the project root.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from core.config import PROJECT_ROOT
from storage.base import StorageProvider


class LocalStorage(StorageProvider):
    def save(self, local_path: Path, remote_key: str) -> str:
        destination = PROJECT_ROOT / remote_key
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(local_path, destination)
        return str(destination)

    def load(self, remote_key: str, local_path: Path) -> Path:
        source = PROJECT_ROOT / remote_key
        local_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, local_path)
        return local_path
