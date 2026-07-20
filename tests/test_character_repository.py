"""Smoke test: CharacterRepository round-trips a Character to/from YAML."""

from core.character_repository import CharacterRepository
from core.models.character import Character


def test_save_and_load_round_trip():
    repo = CharacterRepository()
    character = Character(id="__pytest_smoke_character__", name="Pytest Smoke Character")

    try:
        repo.save(character)
        loaded = repo.get(character.id)

        assert loaded.id == character.id
        assert loaded.name == character.name
    finally:
        repo.delete(character.id)

    assert not repo.exists(character.id)
