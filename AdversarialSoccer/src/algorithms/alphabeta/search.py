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
        
        best_colombia_action = None
        best_rival_action = None
        best_value = float("-inf")

        for colombia_action in colombia_actions:

            worst_rival_action = None
            worst_value = float("inf")

            for rival_action in rival_actions:

                successor = step(state, colombia_action, rival_action)

                value = ply(successor, depth - 1, alpha, beta)[2]

                if value < worst_value:
                    worst_value = value
                    worst_rival_action = rival_action

                # poda Beta el rival ya encontro algo peor que lo que MAX puede
                # garantizar en otra rama, no hace falta seguir buscando aqui
                if worst_value < alpha:
                    break

            if worst_value > best_value:
                best_value = worst_value
                best_colombia_action = colombia_action
                best_rival_action = worst_rival_action

            # acutaliz alpha (max))
            alpha = max(alpha, best_value)

            # poda Alpha
            if best_value > beta:
                break

        return best_colombia_action, best_rival_action, best_value
    
        # --- SOLUTION END ---

    return finish_search_root(*ply(state, depth, float("-inf"), float("inf")))
