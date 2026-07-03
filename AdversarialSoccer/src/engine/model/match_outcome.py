from __future__ import annotations

from enum import StrEnum


class MatchOutcome(StrEnum):
    """Terminal status from Colombia's perspective."""

    IN_PROGRESS = "in_progress"
    WIN = "win"
    LOSS = "loss"
    DRAW = "draw"
