"""Enums shared by episode and character models."""

from enum import StrEnum


class Platform(StrEnum):
    YOUTUBE_SHORTS = "youtube_shorts"
    TIKTOK = "tiktok"


class PublishingStatus(StrEnum):
    DRAFT = "draft"
    IN_PRODUCTION = "in_production"
    READY_TO_PUBLISH = "ready_to_publish"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ProductionStage(StrEnum):
    """Mirrors the pipeline stages tracked in the Obsidian vault's Episode Progress Tracker."""

    IDEA = "idea"
    SCRIPT = "script"
    VOICE = "voice"
    VISUALS = "visuals"
    EDIT = "edit"
    QC = "qc"
    THUMBNAIL = "thumbnail"
    PUBLISHED = "published"


class CharacterStatus(StrEnum):
    CONCEPT = "concept"
    IN_DEVELOPMENT = "in_development"
    ACTIVE = "active"
    RETIRED = "retired"
