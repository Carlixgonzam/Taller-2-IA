from __future__ import annotations

from engine.geometry import segment_intercepted
from engine.model import MatchOutcome, Position, Team
from engine.state import GameState


def check_pressure_turnover(state: GameState) -> tuple[Team, int] | None:
    """Return (possession, ball_owner) when an opponent shares the ball cell."""
    ball = state.get_ball_position()
    stealing_team = state.possession.opponent
    for idx, position in enumerate(state.get_team_positions(stealing_team)):
        if position == ball:
            return stealing_team, idx
    return None


def resolve_committed_shot(
    state: GameState,
    team: Team,
    origin: Position,
    target: Position,
) -> tuple[MatchOutcome, Team, int]:
    """Return (outcome, possession, ball_owner) after a shoot or pass."""
    opponents = state.get_team_positions(team.opponent)

    interceptor = segment_intercepted(origin, target, opponents)
    if interceptor is not None:
        return state.outcome, team.opponent, interceptor

    if target in state.get_team_goal(team):
        outcome = MatchOutcome.WIN if team is Team.COLOMBIA else MatchOutcome.LOSS
        return outcome, state.possession, state.ball_owner

    for idx, teammate in enumerate(state.get_team_positions(team)):
        if teammate == target and idx != state.ball_owner:
            return state.outcome, state.possession, idx

    raise ValueError(f"Shoot target {target} is not open: no goal, teammate, or interceptor.")
