"""YAML frontmatter + markdown body — the same convention Obsidian uses.

Used for script.md and checklist.md so they carry the same machine-readable
metadata (id, episode_id, created, updated, status, version) as episode.yaml
and the prompt records, while staying human-readable and hand-editable.
"""

from __future__ import annotations

from pathlib import Path

import yaml

_DELIMITER = "---"


def write_markdown(path: Path, metadata: dict, body: str) -> None:
    """Write a markdown file: a YAML frontmatter block, then the body text."""
    frontmatter = yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True)
    content = f"{_DELIMITER}\n{frontmatter}{_DELIMITER}\n\n{body}"
    path.write_text(content, encoding="utf-8")


def read_markdown(path: Path) -> tuple[dict, str]:
    """Read a file written by write_markdown, returning (metadata, body)."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith(f"{_DELIMITER}\n"):
        return {}, text

    _, frontmatter, body = text.split(_DELIMITER, 2)
    metadata = yaml.safe_load(frontmatter) or {}
    return metadata, body.lstrip("\n")
