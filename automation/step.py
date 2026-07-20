"""Abstract base for a single automation pipeline stage."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from core.models.episode import Episode


@dataclass
class StepResult:
    success: bool
    message: str = ""
    data: dict = field(default_factory=dict)


class PipelineStep(ABC):
    name: str

    @abstractmethod
    def run(self, episode: Episode, context: dict) -> StepResult:
        """Execute this stage. `context` carries forward data produced by prior steps."""
        raise NotImplementedError
