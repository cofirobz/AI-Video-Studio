"""Smoke tests: core.frontmatter round-trips YAML frontmatter + markdown body."""

from pathlib import Path

from core.frontmatter import read_markdown, write_markdown


def test_write_then_read_round_trip(tmp_path: Path):
    path = tmp_path / "note.md"
    metadata = {"id": "abc", "episode_id": "abc-episode", "status": "draft", "version": 1}
    body = "# Title\n\nSome content.\n"

    write_markdown(path, metadata, body)
    read_metadata, read_body = read_markdown(path)

    assert read_metadata == metadata
    assert read_body == body


def test_read_without_frontmatter_returns_empty_metadata(tmp_path: Path):
    path = tmp_path / "plain.md"
    path.write_text("just text, no frontmatter\n", encoding="utf-8")

    metadata, body = read_markdown(path)

    assert metadata == {}
    assert body == "just text, no frontmatter\n"
