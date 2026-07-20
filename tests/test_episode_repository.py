"""Smoke tests: EpisodeRepository manages a self-contained workspace folder per episode."""

from core.episode_repository import EpisodeRepository
from core.models.episode import Episode


def test_save_and_load_round_trip():
    repo = EpisodeRepository()
    episode = Episode(id="__pytest_smoke_episode__", title="Pytest Smoke Episode", hook="A test hook")

    try:
        repo.save(episode)
        loaded = repo.get(episode.id)

        assert loaded.id == episode.id
        assert loaded.title == episode.title
        assert loaded.hook == episode.hook
    finally:
        repo.delete(episode.id)

    assert not repo.exists(episode.id)


def test_workspace_dir_matches_episode_yaml_location():
    repo = EpisodeRepository()
    episode = Episode(id="__pytest_smoke_workspace__", title="Pytest Smoke Workspace")

    try:
        path = repo.save(episode)
        assert path == repo.workspace_dir(episode.id) / "episode.yaml"
    finally:
        repo.delete(episode.id)


def test_save_bumps_version_on_update():
    repo = EpisodeRepository()
    episode = Episode(id="__pytest_smoke_version__", title="Pytest Smoke Version")

    try:
        repo.save(episode)
        assert repo.get(episode.id).version == 1

        repo.save(episode)
        assert repo.get(episode.id).version == 2
    finally:
        repo.delete(episode.id)


def test_delete_removes_whole_workspace():
    repo = EpisodeRepository()
    episode = Episode(id="__pytest_smoke_delete__", title="Pytest Smoke Delete")
    repo.save(episode)
    (repo.workspace_dir(episode.id) / "assets").mkdir(exist_ok=True)

    repo.delete(episode.id)

    assert not repo.workspace_dir(episode.id).exists()
