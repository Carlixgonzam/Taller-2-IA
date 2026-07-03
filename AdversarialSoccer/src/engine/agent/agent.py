from __future__ import annotations

from abc import ABC, abstractmethod

from engine.state import GameState

from .turn_decision import TurnDecision


class Agent(ABC):
    """Soccer agent: returns Colombia and rival actions together each turn."""

    @abstractmethod
    def decide_turn(self, state: GameState) -> TurnDecision | None:
        """Return joint Colombia and rival actions for the current state."""
