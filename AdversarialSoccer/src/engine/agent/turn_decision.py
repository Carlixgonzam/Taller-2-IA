from __future__ import annotations

from dataclasses import dataclass

from engine.model import TeamAction


@dataclass(slots=True)
class TurnDecision:
    """Both teams' joint actions for one simultaneous timestep."""

    colombia: TeamAction
    rival: TeamAction
