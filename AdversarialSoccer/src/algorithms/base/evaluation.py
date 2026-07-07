from __future__ import annotations
from engine.geometry import manhattan_distance, nearest_to
from engine.model import MatchOutcome, Team
from engine.rules import compute_shot_plan
from engine.state import GameState

# los pesos fueron avance x=3.0, dist arco=2.0, tiro libre=4.0, pase libre=1.0,
# sin carril=-1.5, companero adelantado=0.5 c/u, peligro=-2.5, presion=-1.5,
# lado de arco=1.0, marcaje=-1.0, tiro libre rival=-3.0, spread=0.5, turno=-0.5.


def evaluation_function(state: GameState) -> float:
    if state.outcome is MatchOutcome.WIN:
        return 1000.0
    if state.outcome is MatchOutcome.LOSS:
        return -1000.0
    if state.outcome is MatchOutcome.DRAW:
        return 0.0
    sc = state.scenario
    norm = sc.width + sc.height
    b = state.get_ball_position()
    s = 0.0
    if state.has_ball(Team.COLOMBIA):
        s += 3.0 * (b[0] / (sc.width - 1))
        _, g = nearest_to(b, state.get_team_goal(Team.COLOMBIA))
        s += 2.0 * (1 - manhattan_distance(b, g) / norm)
        plan = compute_shot_plan(state, Team.COLOMBIA, opponents=list(state.rival_positions))
        if plan is None:
            s -= 1.5
        else:
            _, target = plan
            if target in state.get_team_goal(Team.COLOMBIA):
                s += 4.0
            else:
                s += 1.0
        ahead = 0
        for i in range(len(state.colombia_positions)):
            if i == state.ball_owner:
                continue
            p = state.colombia_positions[i]
            if Team.COLOMBIA.is_ahead_on_attack_axis(b, p, inclusive=False):
                ahead += 1
        s += 0.5 * ahead
    else:
        _, g = nearest_to(b, state.get_team_goal(Team.RIVAL))
        s -= 2.5 * (1 - manhattan_distance(b, g) / norm)
        _, def_pos = nearest_to(b, state.colombia_positions)
        s -= 1.5 * (manhattan_distance(b, def_pos) / norm)
        side = 0
        for p in state.colombia_positions:
            if p[0] <= b[0]:
                side += 1
        s += 1.0 * (side / len(state.colombia_positions))
        mark_sum = 0.0
        mark_n = 0
        for i in range(len(state.rival_positions)):
            if i == state.ball_owner:
                continue
            rp = state.rival_positions[i]
            _, m = nearest_to(rp, state.colombia_positions)
            mark_sum += manhattan_distance(rp, m)
            mark_n += 1
        if mark_n > 0:
            s -= 1.0 * (mark_sum / mark_n / norm)
        plan = compute_shot_plan(state, Team.RIVAL, opponents=list(state.colombia_positions))
        if plan is not None:
            _, target = plan
            if target in state.get_team_goal(Team.RIVAL):
                s -= 3.0
    rows = set()
    for p in state.colombia_positions:
        rows.add(p[1])
    s += 0.5 * (len(rows) / len(state.colombia_positions))
    s -= 0.5 * (state.turn / sc.max_turns)
    return s
