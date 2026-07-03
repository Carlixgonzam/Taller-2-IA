from __future__ import annotations

import random
import time
from collections.abc import Callable
from typing import Protocol

from engine.agent import Agent, TurnDecision
from engine.model import TeamAction
from engine.state import GameState

from .evaluation import evaluation_function
from .metrics import SearchMetrics

EvaluationFunction = Callable[[GameState], float]


class TurnSearch(Protocol):
    """Depth-limited search that returns Colombia action, rival reply, and value."""

    def __call__(
        self,
        state: GameState,
        depth: int,
        evaluation_function: EvaluationFunction,
        rng: random.Random,
        *,
        on_expand: Callable[[], None] | None = None,
    ) -> tuple[TeamAction, TeamAction, float]: ...


class MultiAgentSearchAgent(Agent):
    """Shared metrics, RNG, and evaluation for all search agents."""

    def __init__(self, *, seed: int | None = None) -> None:
        self.random = random.Random(seed) if seed is not None else random.Random()
        self.metrics = SearchMetrics()
        self.evaluation_function = evaluation_function

    def _reset_metrics(self) -> float:
        """Clear metrics and return a perf_counter start timestamp."""
        self.metrics = SearchMetrics()
        return time.perf_counter()

    def _finish_metrics(self, start: float) -> None:
        """Store elapsed decision time since _reset_metrics."""
        self.metrics.decision_time = time.perf_counter() - start


class AdversarialSearchAgent(MultiAgentSearchAgent):
    """Depth-limited game-tree agents (Minimax, Alpha-Beta, Expectimax)."""

    def __init__(self, *, depth: int = 2, seed: int | None = None) -> None:
        super().__init__(seed=seed)
        self.depth = depth

    def _on_expand(self, *, depth: int | None = None) -> None:
        """Record one expanded node for search metrics."""
        self.metrics.nodes_expanded += 1
        reached_depth = self.depth if depth is None else depth
        self.metrics.max_depth_reached = max(self.metrics.max_depth_reached, reached_depth)

    def _expand_callback(self) -> Callable[[], None]:
        """Return an on_expand hook for recursive search functions."""
        return lambda: self._on_expand()

    def _finish_turn_decision(
        self,
        start: float,
        colombia_action: TeamAction,
        rival_action: TeamAction,
        value: float,
    ) -> TurnDecision:
        """Store metrics and build the chosen joint turn."""
        self.metrics.selected_value = value
        self._finish_metrics(start)
        return TurnDecision(colombia_action, rival_action)

    def _decide_with_search(self, state: GameState, search: TurnSearch) -> TurnDecision:
        """Run a depth-limited search function and return the chosen joint turn."""
        start = self._reset_metrics()
        colombia_action, rival_action, value = search(
            state,
            self.depth,
            self.evaluation_function,
            self.random,
            on_expand=self._expand_callback(),
        )
        return self._finish_turn_decision(start, colombia_action, rival_action, value)
