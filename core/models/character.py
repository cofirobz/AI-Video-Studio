"""Character schema — mirrors the fields captured in the vault's Character Template."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from core.models.common import CharacterStatus


class VoiceProfile(BaseModel):
    tone: str = ""
    accent_style: str = ""
    reference_id: str | None = Field(
        default=None, description="TTS voice ID or voice-clone reference, once a provider is wired up"
    )


class Relationship(BaseModel):
    character_id: str
    description: str


class Character(BaseModel):
    id: str = Field(description="Slug used as the filename in characters/ and cross-referenced by episodes")
    name: str
    role: str = ""
    series: str = ""
    status: CharacterStatus = CharacterStatus.CONCEPT

    appearance: list[str] = Field(default_factory=list)
    personality: list[str] = Field(default_factory=list)
    voice: VoiceProfile = Field(default_factory=VoiceProfile)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    catchphrases: list[str] = Field(default_factory=list)
    relationships: list[Relationship] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
