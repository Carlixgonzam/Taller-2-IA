from __future__ import annotations

from engine.model import MatchOutcome, ShootAction, Team, TeamAction
from engine.state import GameState

from .movement import positions_after_action
from .turnover import check_pressure_turnover, resolve_committed_shot


def step(
    state: GameState,
    colombia_action: TeamAction,
    rival_action: TeamAction,
) -> GameState:
    """Apply one simultaneous turn and return a new successor state."""
    if state.outcome is not MatchOutcome.IN_PROGRESS:
        raise ValueError("Cannot step from a terminal state.")

    possessing_team = state.possession
    possession_action = colombia_action if possessing_team is Team.COLOMBIA else rival_action

    colombia_positions = positions_after_action(state, Team.COLOMBIA, colombia_action)
    rival_positions = positions_after_action(state, Team.RIVAL, rival_action)
    outcome = state.outcome
    possession = state.possession
    ball_owner = state.ball_owner
    turn = state.turn + 1

    after_move = GameState(
        scenario=state.scenario,
        colombia_positions=colombia_positions,
        rival_positions=rival_positions,
        possession=possession,
        ball_owner=ball_owner,
        turn=turn,
        outcome=outcome,
    )

    match possession_action:
        case ShootAction(origin=origin, target=target):
            outcome, possession, ball_owner = resolve_committed_shot(
                after_move, possessing_team, origin, target
            )

    if outcome is MatchOutcome.IN_PROGRESS and possession is possessing_team:
        after_shot = GameState(
            scenario=state.scenario,
            colombia_positions=colombia_positions,
            rival_positions=rival_positions,
            possession=possession,
            ball_owner=ball_owner,
            turn=turn,
            outcome=outcome,
        )
        pressure = check_pressure_turnover(after_shot)
        if pressure is not None:
            possession, ball_owner = pressure

    if turn >= state.scenario.max_turns and outcome is MatchOutcome.IN_PROGRESS:
        outcome = MatchOutcome.DRAW

    return GameState(
        scenario=state.scenario,
        colombia_positions=colombia_positions,
        rival_positions=rival_positions,
        possession=possession,
        ball_owner=ball_owner,
        turn=turn,
        outcome=outcome,
    )
