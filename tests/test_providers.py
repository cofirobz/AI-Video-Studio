"""Smoke tests for the provider registries: config-driven selection, and the
one real implementation (storage/local.py).
"""

from pathlib import Path

import pytest

from core.config import get_settings
from editor.base import get_provider as get_editor
from editor.davinci import DaVinciEditor
from image.base import get_provider as get_image
from image.gpt_image import GPTImage
from storage.base import get_provider as get_storage
from storage.local import LocalStorage
from upload.base import get_provider as get_upload
from upload.youtube import YouTubeUpload
from video.base import get_provider as get_video
from video.runway import RunwayVideo
from voice.base import get_provider as get_voice
from voice.elevenlabs import ElevenLabsVoice


def test_get_provider_resolves_configured_default_for_each_category():
    settings = get_settings()
    assert isinstance(get_editor(settings), DaVinciEditor)
    assert isinstance(get_video(settings), RunwayVideo)
    assert isinstance(get_image(settings), GPTImage)
    assert isinstance(get_voice(settings), ElevenLabsVoice)
    assert isinstance(get_upload(settings), YouTubeUpload)
    assert isinstance(get_storage(settings), LocalStorage)


def test_unknown_provider_name_raises_clear_error():
    settings = get_settings().model_copy(deep=True)
    settings.providers.image = "not-a-real-provider"

    with pytest.raises(ValueError, match="Unknown image provider"):
        get_image(settings)


def test_local_storage_actually_copies_a_file(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("hello", encoding="utf-8")
    destination = tmp_path / "restored.txt"

    provider = LocalStorage()
    saved_ref = provider.save(source, "tmp/__pytest_storage_test__.txt")
    saved_path = Path(saved_ref)
    try:
        provider.load("tmp/__pytest_storage_test__.txt", destination)
        assert destination.read_text(encoding="utf-8") == "hello"
    finally:
        saved_path.unlink(missing_ok=True)
        try:
            saved_path.parent.rmdir()
        except OSError:
            pass
