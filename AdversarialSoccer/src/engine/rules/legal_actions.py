from __future__ import annotations

from itertools import product

from engine.model import Directions, MatchOutcome, MovesAction, ShootAction, Team, TeamAction
from engine.state import GameState

from .movement import is_valid_joint_moves
from .shots import compute_shot_plan


def get_legal_actions(state: GameState, team: Team) -> list[TeamAction]:
    """Return legal joint actions: optional shoot plus all valid move combinations."""
    if state.outcome is not MatchOutcome.IN_PROGRESS:
        return []

    actions: list[TeamAction] = []

    if state.has_ball(team):
        plan = compute_shot_plan(state, team)
        if plan is not None:
            origin, target = plan
            actions.append(ShootAction(origin, target))

    for moves in product(Directions, repeat=state.team_size_for(team)):
        if is_valid_joint_moves(state, team, moves):
            actions.append(MovesAction(moves))

    return actions
