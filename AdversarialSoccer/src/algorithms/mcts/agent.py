from __future__ import annotations

from algorithms.base import MultiAgentSearchAgent
from engine.agent import TurnDecision
from engine.state import GameState

from .search import mcts_search


class MCTSAgent(MultiAgentSearchAgent):
    """Monte Carlo Tree Search using UCT."""

    def __init__(
        self,
        *,
        iterations: int = 300,
        exploration: float = 1.4,
        prob: float = 0.0,
        seed: int | None = None,
    ) -> None:
        super().__init__(seed=seed)
        self.iterations = iterations
        self.exploration = exploration
        self.prob = prob

    def decide_turn(self, state: GameState) -> TurnDecision | None:
        start = self._reset_metrics()

        def on_expand() -> None:
            self.metrics.nodes_expanded += 1

        colombia_action, rival_action, value = mcts_search(
            state,
            self.evaluation_function,
            self.random,
            iterations=self.iterations,
            prob=self.prob,
            exploration=self.exploration,
            on_expand=on_expand,
        )
        self.metrics.selected_value = value
        self._finish_metrics(start)
        return TurnDecision(colombia_action, rival_action)
