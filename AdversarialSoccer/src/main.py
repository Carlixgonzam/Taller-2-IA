from __future__ import annotations

import argparse

from algorithms import (
    AGENT_NAMES,
    AdversarialSearchAgent,
    ExpectimaxAgent,
    MCTSAgent,
    create_agent,
)
from engine.model import Team
from engine.rules import get_legal_actions
from engine.runner import run_soccer_mode
from engine.scenario import list_scenario_names, load_scenario
from engine.state import GameState
from ui import ReplayDisplay, console


def read_command() -> argparse.Namespace:
    """Parse CLI arguments for agent, scenario, and algorithm-specific settings."""
    parser = argparse.ArgumentParser(
        description="FIFA World Cup 2026 - Adversarial Soccer Simulator"
    )
    parser.add_argument(
        "-a",
        "--agent",
        required=True,
        choices=AGENT_NAMES,
        metavar="AGENT",
        help=f"Agent class ({', '.join(AGENT_NAMES)})",
    )
    parser.add_argument(
        "-s",
        "--scenario",
        dest="scenario",
        metavar="SCENARIO",
        required=True,
        help="Scenario name (without .yaml)",
    )
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=None,
        metavar="DEPTH",
        help="Search depth for Minimax, AlphaBeta, and Expectimax",
    )
    parser.add_argument(
        "-p",
        "--probability",
        type=float,
        default=None,
        metavar="PROBABILITY",
        help="Probability of a random rival action for Expectimax and MCTS",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=None,
        metavar="ITERATIONS",
        help="Number of iterations for MCTS rollouts",
    )
    parser.add_argument(
        "-r",
        "--random-seed",
        type=int,
        default=None,
        metavar="RANDOM_SEED",
        help="Random seed for reproducibility",
    )
    return parser.parse_args()


def main() -> None:
    """Load scenario, build the selected agent, and run one match."""
    args = read_command()
    agent = create_agent(
        args.agent,
        depth=args.depth,
        probability=args.probability,
        seed=args.random_seed,
        iterations=args.iterations,
    )

    scenario = load_scenario(args.scenario)
    if scenario is None:
        options = ", ".join(list_scenario_names())
        raise ValueError(f"Scenario {args.scenario} not found. Available: {options}")

    preview = GameState.initial(scenario)
    col_actions = len(get_legal_actions(preview, Team.COLOMBIA))
    riv_actions = len(get_legal_actions(preview, Team.RIVAL))
    roster = f"{len(preview.colombia_positions)}v{len(preview.rival_positions)}"

    console.title("T2 · Adversarial Soccer · Colombia 2026")
    console.info("Scenario", args.scenario)
    console.info("Agent", args.agent)
    if isinstance(agent, AdversarialSearchAgent):
        console.info("Depth", str(agent.depth))
    field_info = (
        f"{scenario.width}×{scenario.height}  ·  {roster}  ·  max {scenario.max_turns} turns"
    )
    console.info("Field", field_info)
    console.info("Joint branching", f"COL={col_actions}  RIV={riv_actions}")
    if isinstance(agent, (ExpectimaxAgent, MCTSAgent)):
        console.info("Random rival (p)", str(agent.prob))
    if isinstance(agent, MCTSAgent):
        console.info("MCTS iterations", str(agent.iterations))

    display = ReplayDisplay()
    run_soccer_mode(
        scenario=scenario,
        display=display,
        agent=agent,
    )


if __name__ == "__main__":
    main()
