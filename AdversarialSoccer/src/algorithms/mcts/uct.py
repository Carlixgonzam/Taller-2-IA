from __future__ import annotations

import math


def uct_score(
    total_value: float,
    visits: int,
    parent_visits: int,
    exploration: float,
) -> float:
    """
    Return the UCT selection score for an MCTS child node.

    Tips:
    - Unvisited children should score inf so every action is tried once.
    - Exploitation: total_value / visits.
    - Exploration: exploration * sqrt(log(parent_visits) / visits).
    """
    if visits == 0:
        return float("inf")

    explotacion = total_value / visits
    exploracion = exploration * math.sqrt(math.log(parent_visits) / visits)
    return explotacion + exploracion
