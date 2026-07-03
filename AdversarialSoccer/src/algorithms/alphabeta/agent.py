from __future__ import annotations

from algorithms.base import AdversarialSearchAgent
from engine.agent import TurnDecision
from engine.state import GameState

from .search import alphabeta_search


class AlphaBetaAgent(AdversarialSearchAgent):
    """Minimax with alpha-beta pruning — same optimal moves, fewer node expansions."""

    def decide_turn(self, state: GameState) -> TurnDecision | None:
        return self._decide_with_search(state, alphabeta_search)
