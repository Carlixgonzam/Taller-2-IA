from __future__ import annotations

import random
from collections.abc import Callable

from algorithms.base import EvaluationFunction
from algorithms.base.search import finish_search_root, is_cutoff, legal_actions
from engine.model import Team, TeamAction
from engine.rules import step
from engine.state import GameState


def minimax_search(
    state: GameState,
    depth: int,
    evaluation_function: EvaluationFunction,
    rng: random.Random,
    *,
    on_expand: Callable[[], None] | None = None,
) -> tuple[TeamAction, TeamAction, float]:
    """
    Depth-limited minimax from the root: Colombia MAX action, rival MIN reply, and value.

    Each ply is one simultaneous timestep: Colombia chooses, the rival replies, then `step(...)`.
    Leaf when `depth == 0` or the match is over → `evaluation_function(state)`.

    Tips:
    - Use `legal_actions(state, team)` and `step(state, colombia_action, rival_action)`.
    - Per ply: `max` over Colombia actions of `min` over rival replies.
    - Recurse with `ply(successor, depth - 1)[2]`; only the root needs the returned actions.
    - At the rival layer, `min((action, value), ..., key=lambda item: item[1])` compares by value.
    - Optional: cache `(state, depth)` with a hashable key to speed up search.
    """

    def ply(state: GameState, depth: int) -> tuple[TeamAction | None, TeamAction | None, float]:
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

                value = ply(successor, depth - 1)[2]

                if value < worst_value:
                    worst_value = value
                    worst_rival_action = rival_action

            if worst_value > best_value:
                best_value = worst_value
                best_colombia_action = colombia_action
                best_rival_action = worst_rival_action

        return best_colombia_action, best_rival_action, best_value
        
        # --- SOLUTION END ---
    
    return finish_search_root(*ply(state, depth))