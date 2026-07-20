"""Loads config/*.yaml into typed settings; API keys come from the environment, never YAML."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"


class ProjectSettings(BaseModel):
    name: str = "AI Shorts Studio"
    version: str = "0.1.0"
    environment: str = "development"
    default_platforms: list[str] = Field(default_factory=lambda: ["youtube_shorts", "tiktok"])
    timezone: str = "UTC"


class PathsSettings(BaseModel):
    episodes: str = "episodes"
    characters: str = "characters"
    prompts: str = "prompts"
    assets: str = "assets"
    voices: str = "voices"
    music: str = "music"
    logs: str = "logs"
    templates: str = "templates"

    def resolve(self, name: str) -> Path:
        """Absolute path for a configured folder, e.g. settings.paths.resolve('episodes')."""
        return PROJECT_ROOT / getattr(self, name)


class RenderSettings(BaseModel):
    resolution_width: int = 1080
    resolution_height: int = 1920
    fps: int = 30
    codec: str = "H.264"
    bitrate_mbps: int = 20
    output_format: str = "mp4"


class VideoSettings(BaseModel):
    aspect_ratio: str = "9:16"
    min_duration_seconds: int = 15
    max_duration_seconds: int = 60
    hook_duration_seconds: float = 2.0
    safe_margin_percent: int = 10


class LoggingSettings(BaseModel):
    level: str = "INFO"
    file: str = "logs/studio.log"
    max_bytes: int = 5_000_000
    backup_count: int = 3
    console: bool = True


class AutomationStageToggle(BaseModel):
    enabled: bool = False
    max_retries: int = 1


class AutomationSettings(BaseModel):
    generate_script: AutomationStageToggle = Field(default_factory=AutomationStageToggle)
    generate_prompts: AutomationStageToggle = Field(default_factory=lambda: AutomationStageToggle(enabled=True))
    generate_assets: AutomationStageToggle = Field(default_factory=AutomationStageToggle)
    import_to_editor: AutomationStageToggle = Field(default_factory=AutomationStageToggle)
    render: AutomationStageToggle = Field(default_factory=AutomationStageToggle)
    export: AutomationStageToggle = Field(default_factory=AutomationStageToggle)
    upload: AutomationStageToggle = Field(default_factory=AutomationStageToggle)


class APISettings(BaseModel):
    """Populated from environment variables / .env — never stored in YAML or committed."""

    anthropic_api_key: str | None = None
    image_gen_api_key: str | None = None
    video_gen_api_key: str | None = None
    tts_api_key: str | None = None
    upload_api_key: str | None = None


class ProviderSettings(BaseModel):
    """Which provider implementation each category resolves to — see editor/, video/,
    image/, voice/, upload/, storage/base.py's get_provider(). Swapping providers is a
    one-line change here, never a code change.
    """

    editor: str = "davinci"
    video: str = "runway"
    image: str = "gpt_image"
    voice: str = "elevenlabs"
    upload: str = "youtube"
    storage: str = "local"


class Settings(BaseModel):
    project: ProjectSettings = Field(default_factory=ProjectSettings)
    paths: PathsSettings = Field(default_factory=PathsSettings)
    render: RenderSettings = Field(default_factory=RenderSettings)
    video: VideoSettings = Field(default_factory=VideoSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    automation: AutomationSettings = Field(default_factory=AutomationSettings)
    api: APISettings = Field(default_factory=APISettings)
    providers: ProviderSettings = Field(default_factory=ProviderSettings)


def _load_yaml(name: str) -> dict:
    path = CONFIG_DIR / name
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@lru_cache
def get_settings() -> Settings:
    """Load and cache settings from config/*.yaml plus environment-sourced API keys."""
    load_dotenv(PROJECT_ROOT / ".env")

    return Settings(
        project=ProjectSettings(**_load_yaml("settings.yaml")),
        paths=PathsSettings(**_load_yaml("paths.yaml")),
        render=RenderSettings(**_load_yaml("render_settings.yaml")),
        video=VideoSettings(**_load_yaml("video_settings.yaml")),
        logging=LoggingSettings(**_load_yaml("logging.yaml")),
        automation=AutomationSettings(**_load_yaml("automation.yaml")),
        providers=ProviderSettings(**_load_yaml("providers.yaml")),
        api=APISettings(
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            image_gen_api_key=os.getenv("IMAGE_GEN_API_KEY"),
            video_gen_api_key=os.getenv("VIDEO_GEN_API_KEY"),
            tts_api_key=os.getenv("TTS_API_KEY"),
            upload_api_key=os.getenv("UPLOAD_API_KEY"),
        ),
    )
