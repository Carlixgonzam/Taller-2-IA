from __future__ import annotations

from engine.geometry import (
    manhattan_distance,
    path_blocked,
    segment_intercepted,
    sorted_by_manhattan_distance,
    within_manhattan_range,
)
from engine.model import Position, Team
from engine.state import GameState


def compute_shot_plan(
    state: GameState,
    team: Team,
    *,
    opponents: list[Position] | None = None,
) -> tuple[Position, Position] | None:
    """
    Return (carrier, target) for the engine-resolved shot or pass.

    Resolution order:
    1. Nearest open goal mouth (Colombia attacks rival_goal at high x;
       Rival attacks own_goal at low x).
    2. Teammates strictly ahead on the attack axis, then nearest in Manhattan
       distance (Colombia: +x; Rival: -x).

    Returns None when the team does not have the ball or no lane is clear.

    If opponents are provided, they are used to check for interceptions,
    for example in the context of a planned shot.
    """
    if not state.has_ball(team):
        return None

    carrier = state.get_team_positions(team)[state.ball_owner]
    if opponents is None:
        opponents = list(state.get_team_positions(team.opponent))
    max_range = state.scenario.max_shot_distance

    for goal_cell in sorted_by_manhattan_distance(carrier, state.get_team_goal(team)):
        if not within_manhattan_range(carrier, goal_cell, max_range):
            continue
        if (
            path_blocked(state.scenario, carrier, goal_cell)
            or segment_intercepted(carrier, goal_cell, tuple(opponents)) is not None
        ):
            continue
        return carrier, goal_cell

    teammates = sorted(
        (
            (idx, pos)
            for idx, pos in enumerate(state.get_team_positions(team))
            if idx != state.ball_owner
        ),
        key=lambda item: (
            0 if team.is_ahead_on_attack_axis(carrier, item[1], inclusive=False) else 1,
            manhattan_distance(carrier, item[1]),
        ),
    )
    for _idx, teammate in teammates:
        if not within_manhattan_range(carrier, teammate, max_range):
            continue
        if (
            path_blocked(state.scenario, carrier, teammate)
            or segment_intercepted(carrier, teammate, tuple(opponents)) is not None
        ):
            continue
        return carrier, teammate
    return None
