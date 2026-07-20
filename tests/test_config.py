"""Smoke tests for the settings loader."""

from core.config import get_settings


def test_settings_load_with_expected_defaults():
    settings = get_settings()
    assert settings.project.name
    assert settings.video.aspect_ratio == "9:16"
    assert settings.paths.episodes == "episodes"


def test_paths_resolve_relative_to_project_root():
    settings = get_settings()
    resolved = settings.paths.resolve("episodes")
    assert resolved.name == "episodes"
    assert resolved.is_absolute()


def test_provider_defaults_are_set():
    settings = get_settings()
    assert settings.providers.editor == "davinci"
    assert settings.providers.storage == "local"
