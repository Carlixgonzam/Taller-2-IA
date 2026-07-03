from __future__ import annotations

import random
from collections.abc import Callable

from engine.model import MatchOutcome, Team, TeamAction
from engine.rules import get_legal_actions, step
from engine.state import GameState


def is_cutoff(state: GameState, depth: int) -> bool:
    """Return whether depth-limited search should stop and evaluate this state."""
    return depth == 0 or state.outcome is not MatchOutcome.IN_PROGRESS


def is_terminal(state: GameState) -> bool:
    """Return whether the match is no longer in progress."""
    return state.outcome is not MatchOutcome.IN_PROGRESS


def legal_actions(state: GameState, team: Team) -> list[TeamAction]:
    """Return legal joint actions for a team; an empty list is an engine error."""
    actions = get_legal_actions(state, team)
    if not actions:
        raise ValueError(f"No legal actions for {team.value}")
    return actions


def pick_rival_action(
    state: GameState,
    colombia_action: TeamAction,
    evaluation_function: Callable[[GameState], float],
    rng: random.Random,
    *,
    prob: float = 0.0,
) -> TeamAction:
    """Mixed rival reply: random with probability `prob`, else one-ply greedy MIN."""
    rival_actions = legal_actions(state, Team.RIVAL)
    if prob > 0 and rng.random() < prob:
        return rng.choice(rival_actions)
    return min(
        rival_actions,
        key=lambda action: evaluation_function(step(state, colombia_action, action)),
    )


def finish_search_root(
    colombia_action: TeamAction | None,
    rival_action: TeamAction | None,
    value: float,
) -> tuple[TeamAction, TeamAction, float]:
    """Unpack the root ply; leaves return no actions."""
    if colombia_action is None or rival_action is None:
        raise ValueError("No legal actions at search root")
    return colombia_action, rival_action, value
