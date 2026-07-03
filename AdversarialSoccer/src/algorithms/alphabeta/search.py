from __future__ import annotations

import random
from collections.abc import Callable

from algorithms.base import EvaluationFunction
from algorithms.base.search import finish_search_root, is_cutoff, legal_actions
from engine.model import Team, TeamAction
from engine.rules import step
from engine.state import GameState


def alphabeta_search(
    state: GameState,
    depth: int,
    evaluation_function: EvaluationFunction,
    rng: random.Random,
    *,
    on_expand: Callable[[], None] | None = None,
) -> tuple[TeamAction, TeamAction, float]:
    """
    Depth-limited alpha-beta search: same moves as minimax, fewer node expansions.

    Same ply structure as `minimax_search`, with alpha/beta bounds threaded through recursion.

    Tips:
    - Prune the rival (MIN) loop when `score < alpha`; prune Colombia (MAX) when `score > beta`.
    - Use strict inequality — do not prune on equality.
    - Pass updated `alpha` / `beta` into each recursive `ply` call.
    """

    def ply(
        state: GameState,
        depth: int,
        alpha: float,
        beta: float,
    ) -> tuple[TeamAction | None, TeamAction | None, float]:
        if on_expand is not None:
            on_expand()

        if is_cutoff(state, depth):
            return None, None, evaluation_function(state)

        colombia_actions = legal_actions(state, Team.COLOMBIA)
        rival_actions = legal_actions(state, Team.RIVAL)

        ### YOUR CODE HERE ###
        # --- SOLUTION START ---
        
        # --- SOLUTION END ---

    return finish_search_root(*ply(state, depth, float("-inf"), float("inf")))
