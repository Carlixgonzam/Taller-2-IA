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

        # --- SOLUTION END ---

    return finish_search_root(*ply(state, depth))
