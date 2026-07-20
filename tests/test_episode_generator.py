"""Tests for core.episode_generator.create_episode()."""

import yaml

from core.episode_generator import create_episode
from core.episode_repository import EpisodeRepository
from core.frontmatter import read_markdown
from core.models.prompt_record import PromptRecord


def _cleanup(episode_id: str) -> None:
    EpisodeRepository().delete(episode_id)


def test_create_episode_scaffolds_full_workspace():
    scaffold = create_episode("Pytest Generator Episode")

    try:
        assert scaffold.episode.id == "pytest-generator-episode"
        assert scaffold.episode.title == "Pytest Generator Episode"

        assert scaffold.workspace_dir.is_dir()
        assert scaffold.episode_path == scaffold.workspace_dir / "episode.yaml"
        assert scaffold.script_path == scaffold.workspace_dir / "script.md"
        assert scaffold.checklist_path == scaffold.workspace_dir / "checklist.md"

        for subfolder in ("prompts", "assets", "renders", "exports"):
            assert (scaffold.workspace_dir / subfolder).is_dir()

        for kind in ("image", "video", "voice", "thumbnail"):
            record_path = scaffold.prompt_paths[kind]
            assert record_path == scaffold.workspace_dir / "prompts" / f"{kind}.yaml"
            with record_path.open("r", encoding="utf-8") as f:
                record = PromptRecord.model_validate(yaml.safe_load(f))
            assert record.episode_id == scaffold.episode.id
            assert record.type == kind
            assert record.status == "draft"

        script_metadata, script_body = read_markdown(scaffold.script_path)
        assert script_metadata["episode_id"] == scaffold.episode.id
        assert script_metadata["status"] == "draft"
        assert "Pytest Generator Episode" in script_body

        checklist_metadata, checklist_body = read_markdown(scaffold.checklist_path)
        assert checklist_metadata["episode_id"] == scaffold.episode.id
        assert "Pytest Generator Episode" in checklist_body

        loaded = EpisodeRepository().get(scaffold.episode.id)
        assert loaded.id == scaffold.episode.id
    finally:
        _cleanup(scaffold.episode.id)


def test_create_episode_disambiguates_id_on_title_collision():
    first = create_episode("Pytest Collision Episode")
    try:
        second = create_episode("Pytest Collision Episode")
        try:
            assert first.episode.id == "pytest-collision-episode"
            assert second.episode.id == "pytest-collision-episode-2"
        finally:
            _cleanup(second.episode.id)
    finally:
        _cleanup(first.episode.id)
