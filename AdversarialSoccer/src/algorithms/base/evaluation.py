from __future__ import annotations

from engine.geometry import (
    manhattan_distance,
    nearest_to,
    path_blocked,
    segment_intercepted,
    sorted_by_manhattan_distance,
    within_manhattan_range,
)
from engine.model import MatchOutcome, Position, Team
from engine.rules import compute_shot_plan
from engine.state import GameState


def evaluation_function(state: GameState) -> float:
    """
    Estimate how good state is for Colombia (higher = better).

    Colombia attacks toward +x; the rival toward -x. Terminal scores must
    dominate: WIN/LOSS first, then possession-specific terms.

    With the ball (offense):
    - ball[0] / scenario.width and distance to the nearest rival-goal cell.
    - compute_shot_plan(state, Team.COLOMBIA): shoot if target is a goal mouth;
      prefer passes with Team.is_ahead_on_attack_axis.
    - path_blocked / segment_intercepted on shot and pass lanes.
    - Squad spread and teammates **ahead** of the ball so STOP-heavy lines score low.

    Without the ball (defense):
    - Distance from the ball to our goal mouth (danger).
    - Nearest Colombian to the ball (press).
    - Defenders behind the ball on x (goal-side).
    - Per-rival marking distance; segment_intercepted on rival shot/pass lanes.
    - Width via spread so everyone does not camp on one cell.

    General tips
    - Normalize distances with scenario.width + scenario.height.
    - state.turn / max_turns: small penalty to finish attacks.
    - Tune weights per scenario (1v1 vs 5v2); document choices in your report.

    Returns:
        Scalar utility from Colombia's perspective.
    """
    ### YOUR CODE HERE ###
    # --- SOLUTION START --- LO HICE PARA EL MINIMAX
    if state.outcome is MatchOutcome.WIN:
        return 10000

    if state.outcome is MatchOutcome.LOSS:
        return -10000

    return 0.0
    # --- SOLUTION END ---
