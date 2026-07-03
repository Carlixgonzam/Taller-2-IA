from __future__ import annotations

import time
from dataclasses import replace
from typing import TYPE_CHECKING

from tqdm import tqdm

from engine.model import MatchOutcome, ShootAction, Team
from engine.rules import step
from engine.scenario import Scenario
from engine.state import GameState
from ui import console

if TYPE_CHECKING:
    from algorithms.base import MultiAgentSearchAgent
    from ui.replay import ReplayDisplay


def run_soccer_mode(
    *,
    scenario: Scenario,
    display: ReplayDisplay,
    agent: MultiAgentSearchAgent,
) -> GameState:
    """Run one soccer simulation: one search per turn, then replay frames."""

    state = GameState.initial(scenario)
    display.initialize(state)

    console.section()

    progress = tqdm(
        total=scenario.max_turns,
        unit="turn",
        desc="Match",
    )
    nodes: list[int] = []
    decision_times: list[float] = []
    start = time.perf_counter()
    try:
        while state.outcome is MatchOutcome.IN_PROGRESS:
            decision = agent.decide_turn(state)
            if decision is None:
                state = replace(state, outcome=MatchOutcome.LOSS)
                break

            nodes.append(agent.metrics.nodes_expanded)
            decision_times.append(agent.metrics.decision_time)

            console.write_turn(
                progress.write,
                state.turn + 1,
                scenario.max_turns,
                agent.metrics.selected_value,
                agent.metrics.decision_time,
            )

            possessing_team = state.possession
            colombia_action = decision.colombia
            rival_action = decision.rival
            display.record_turn_actions(state, colombia_action, rival_action)
            state = step(state, colombia_action, rival_action)

            if state.outcome is MatchOutcome.WIN:
                display.record_goal(Team.COLOMBIA)
            elif state.outcome is MatchOutcome.LOSS:
                display.record_goal(Team.RIVAL)
            elif state.possession is possessing_team.opponent:
                possession_action = (
                    colombia_action if possessing_team is Team.COLOMBIA else rival_action
                )
                kind = "intercept" if isinstance(possession_action, ShootAction) else "pressure"
                display.record_turnover(state, kind=kind)
            display.update(state)
            progress.update(1)
            progress.set_postfix(
                nodes=agent.metrics.nodes_expanded,
                decision_s=f"{agent.metrics.decision_time:.2f}",
            )
    finally:
        progress.close()

    display.finish(state)

    elapsed = time.perf_counter() - start
    if state.outcome is MatchOutcome.WIN:
        outcome = "win"
    elif state.outcome is MatchOutcome.LOSS:
        outcome = "loss"
    elif state.outcome is MatchOutcome.DRAW:
        outcome = "draw"
    else:
        outcome = "unfinished"
    console.print_summary(
        outcome=outcome,
        turns=state.turn,
        avg_nodes=sum(nodes) / max(1, len(nodes)),
        avg_decision_s=sum(decision_times) / max(1, len(decision_times)),
        wall_s=elapsed,
    )
    return state
