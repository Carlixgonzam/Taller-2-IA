from __future__ import annotations

from algorithms.base import AdversarialSearchAgent
from engine.agent import TurnDecision
from engine.state import GameState

from .search import minimax_search


class MinimaxAgent(AdversarialSearchAgent):
    """Minimax: Colombia (MAX) vs rival (MIN)."""

    def decide_turn(self, state: GameState) -> TurnDecision | None:
        return self._decide_with_search(state, minimax_search)
