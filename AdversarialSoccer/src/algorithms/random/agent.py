from __future__ import annotations

from algorithms.base import MultiAgentSearchAgent
from engine.agent import TurnDecision
from engine.model import Team
from engine.rules import get_legal_actions
from engine.state import GameState


class RandomAgent(MultiAgentSearchAgent):
    """Pick independent uniform random legal actions for both teams each turn."""

    def __init__(self, *, seed: int | None = None) -> None:
        super().__init__(seed=seed)

    def decide_turn(self, state: GameState) -> TurnDecision | None:
        start = self._reset_metrics()
        colombia_actions = get_legal_actions(state, Team.COLOMBIA)
        rival_actions = get_legal_actions(state, Team.RIVAL)
        if not colombia_actions or not rival_actions:
            raise ValueError("No legal actions for at least one team")

        colombia_action = self.random.choice(colombia_actions)
        rival_action = self.random.choice(rival_actions)
        self.metrics.nodes_expanded = 1
        self.metrics.selected_value = self.evaluation_function(state)
        self._finish_metrics(start)
        return TurnDecision(colombia_action, rival_action)
