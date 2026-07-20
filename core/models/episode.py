"""Episode schema — mirrors the fields captured in the vault's Episode Template."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from core.models.common import Platform, ProductionStage, PublishingStatus


class Scene(BaseModel):
    index: int
    description: str = ""
    image_prompt: str | None = None
    video_prompt: str | None = None
    voice_line: str | None = None
    duration_seconds: float | None = None


class CaptionSettings(BaseModel):
    enabled: bool = True
    style: str = "default"
    font: str | None = None


class Episode(BaseModel):
    id: str = Field(description="Slug naming this episode's workspace folder: episodes/{id}/")
    title: str
    hook: str = ""
    story: str = ""

    series: str = ""
    characters: list[str] = Field(default_factory=list, description="Character ids referenced by this episode")
    scenes: list[Scene] = Field(default_factory=list)

    music: str | None = Field(default=None, description="Path under music/tracks/")
    sound_effects: list[str] = Field(default_factory=list, description="Paths under music/sound_effects/")
    captions: CaptionSettings = Field(default_factory=CaptionSettings)

    render_settings_override: dict = Field(
        default_factory=dict, description="Per-episode overrides merged onto config/render_settings.yaml"
    )

    stage: ProductionStage = ProductionStage.IDEA
    publishing_status: PublishingStatus = PublishingStatus.DRAFT
    platform_targets: list[Platform] = Field(default_factory=lambda: [Platform.YOUTUBE_SHORTS, Platform.TIKTOK])

    version: int = Field(default=1, description="Bumped by EpisodeRepository.save() on every update")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
