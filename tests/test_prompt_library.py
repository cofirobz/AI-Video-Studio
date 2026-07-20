"""Smoke tests for PromptLibrary loading and rendering the seed templates."""

from core.prompt_library import PromptLibrary


def test_loads_seed_templates():
    library = PromptLibrary()
    assert library.get("script_generator").category == "claude"


def test_render_substitutes_variables():
    library = PromptLibrary()
    rendered = library.render("tts_line", voice_reference="ref-1", tone="excited", pace="fast", line="Hello!")
    assert "Hello!" in rendered
