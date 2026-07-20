"""Schema for a per-episode prompt instance — episodes/{id}/prompts/{kind}.yaml.

Distinct from core.prompt_library.PromptTemplate, which is the shared, reusable
template library (prompts/claude/, prompts/image/, etc.). A PromptRecord is one
episode's actual, editable prompt for one generation kind.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class PromptRecord(BaseModel):
    id: str = Field(description="'{episode_id}-{type}', e.g. 'my-episode-image'")
    episode_id: str
    provider: str = Field(description="Provider name this prompt targets, e.g. 'gpt_image'")
    type: str = Field(description="image | video | voice | thumbnail")
    status: str = "draft"   # draft | ready | generated | failed
    prompt: str = ""
    negative_prompt: str = ""
    notes: str = ""
    version: int = 1
    created: datetime = Field(default_factory=datetime.now)
    updated: datetime = Field(default_factory=datetime.now)
