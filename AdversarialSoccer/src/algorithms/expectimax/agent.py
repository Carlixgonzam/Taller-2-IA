from __future__ import annotations

from functools import partial

from algorithms.base import AdversarialSearchAgent
from engine.agent import TurnDecision
from engine.state import GameState

from .search import expectimax_search


class ExpectimaxAgent(AdversarialSearchAgent):
    """Expectimax with mixed rival behaviour (optimal MIN vs random)."""

    def __init__(self, *, depth: int = 2, prob: float = 0.0, seed: int | None = None) -> None:
        super().__init__(depth=depth, seed=seed)
        self.prob = prob

    def decide_turn(self, state: GameState) -> TurnDecision | None:
        return self._decide_with_search(state, partial(expectimax_search, prob=self.prob))
