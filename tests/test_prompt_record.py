"""Smoke test: PromptRecord serializes/deserializes via YAML like the other models."""

import yaml

from core.models.prompt_record import PromptRecord


def test_round_trip_via_yaml(tmp_path):
    record = PromptRecord(
        id="my-episode-image", episode_id="my-episode", provider="gpt_image", type="image", prompt="a cat"
    )
    path = tmp_path / "image.yaml"

    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(record.model_dump(mode="json"), f)

    with path.open("r", encoding="utf-8") as f:
        loaded = PromptRecord.model_validate(yaml.safe_load(f))

    assert loaded.id == record.id
    assert loaded.episode_id == record.episode_id
    assert loaded.prompt == "a cat"
    assert loaded.status == "draft"
    assert loaded.version == 1
