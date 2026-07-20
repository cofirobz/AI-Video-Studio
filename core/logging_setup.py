"""Root logging configuration, driven by config/logging.yaml."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from core.config import PROJECT_ROOT, Settings

_configured = False


def configure_logging(settings: Settings) -> None:
    """Idempotent — safe to call multiple times (e.g. once per CLI invocation)."""
    global _configured
    if _configured:
        return

    root = logging.getLogger()
    root.setLevel(settings.logging.level)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    if settings.logging.console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root.addHandler(console_handler)

    log_path = PROJECT_ROOT / settings.logging.file
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=settings.logging.max_bytes,
        backupCount=settings.logging.backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    _configured = True
