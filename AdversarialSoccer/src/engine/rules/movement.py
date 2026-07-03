from __future__ import annotations

from engine.geometry import apply_direction, apply_joint_moves
from engine.model import Directions, MovesAction, Position, ShootAction, Team, TeamAction
from engine.state import GameState


def is_valid_move(
    state: GameState,
    team: Team,
    player_index: int,
    direction: Directions,
) -> bool:
    """
    Return whether a single player step is legal.

    STOP is always allowed. Moving teams with the ball cannot enter a cell
    occupied by an opponent; the opponent may still move onto the ball carrier.
    """
    if direction is Directions.STOP:
        return True
    origin = state.get_team_positions(team)[player_index]
    target = apply_direction(origin, direction)
    if not state.scenario.is_legal_cell(target):
        return False
    if state.has_ball(team) and target in state.get_team_positions(team.opponent):
        return False
    return True


def is_valid_joint_moves(
    state: GameState,
    team: Team,
    moves: tuple[Directions, ...],
) -> bool:
    """Return whether every player move is legal and no two teammates share a cell."""
    positions = state.get_team_positions(team)
    if len(moves) != len(positions):
        return False

    for idx, direction in enumerate(moves):
        if not is_valid_move(state, team, idx, direction):
            return False
    targets = apply_joint_moves(positions, moves)
    return len(set(targets)) == len(targets)


def positions_after_action(
    state: GameState,
    team: Team,
    action: TeamAction,
) -> tuple[Position, ...]:
    """Return team positions after a legal move or shoot action (shoot: no movement)."""
    positions = state.get_team_positions(team)
    match action:
        case ShootAction():
            return positions
        case MovesAction(moves=moves):
            return apply_joint_moves(positions, moves)
