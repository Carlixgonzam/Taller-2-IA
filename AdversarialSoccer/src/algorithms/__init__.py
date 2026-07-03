from algorithms.alphabeta import AlphaBetaAgent
from algorithms.base import AdversarialSearchAgent, MultiAgentSearchAgent, SearchMetrics
from algorithms.expectimax import ExpectimaxAgent
from algorithms.mcts import MCTSAgent, MCTSNode
from algorithms.minimax import MinimaxAgent
from algorithms.random import RandomAgent

AGENT_NAMES = (
    "MinimaxAgent",
    "AlphaBetaAgent",
    "ExpectimaxAgent",
    "MCTSAgent",
    "RandomAgent",
)

DEPTH_AGENTS = frozenset({"MinimaxAgent", "AlphaBetaAgent", "ExpectimaxAgent"})
MCTS_AGENT = "MCTSAgent"
RANDOM_AGENT = "RandomAgent"
PROBABILISTIC_RIVAL_AGENTS = frozenset({"ExpectimaxAgent", MCTS_AGENT})

_AGENTS: dict[str, type[MultiAgentSearchAgent]] = {
    "MinimaxAgent": MinimaxAgent,
    "AlphaBetaAgent": AlphaBetaAgent,
    "ExpectimaxAgent": ExpectimaxAgent,
    MCTS_AGENT: MCTSAgent,
    RANDOM_AGENT: RandomAgent,
}

DEFAULT_ITERATIONS = 300
DEFAULT_PROBABILITY = 0.0
DEFAULT_DEPTH = 1
DEFAULT_SEED = None


def get_agent_class(name: str) -> type[MultiAgentSearchAgent]:
    """Return the agent class for a CLI name."""
    try:
        return _AGENTS[name]
    except KeyError:
        available = ", ".join(AGENT_NAMES)
        raise ValueError(f"Unknown agent {name}. Available: {available}") from None


def create_agent(
    name: str,
    *,
    depth: int | None = None,
    probability: float = 0.0,
    seed: int | None = None,
    iterations: int | None = None,
) -> MultiAgentSearchAgent:
    """Build an agent with only the parameters that apply to its algorithm."""
    agent_class = get_agent_class(name)

    if name == RANDOM_AGENT:
        if depth is not None:
            raise ValueError(f"{name} does not use --depth")
        if iterations is not None:
            raise ValueError(f"{name} does not use --iterations")
        return agent_class(seed=seed if seed is not None else DEFAULT_SEED)

    if name == MCTS_AGENT:
        if depth is not None:
            raise ValueError(f"{name} does not use --depth")
        if iterations is not None and iterations <= 0:
            raise ValueError("--iterations must be positive")
        if probability is not None and (probability < 0 or probability > 1):
            raise ValueError("--probability must be between 0 and 1")
        if seed is not None and seed < 0:
            raise ValueError("--seed must be non-negative")
        return agent_class(
            iterations=iterations if iterations is not None else DEFAULT_ITERATIONS,
            prob=probability if probability is not None else DEFAULT_PROBABILITY,
            seed=seed if seed is not None else DEFAULT_SEED,
        )

    if iterations is not None:
        raise ValueError(f"{name} does not use --iterations")

    if name not in PROBABILISTIC_RIVAL_AGENTS and probability is not None:
        raise ValueError(
            f"{name} does not use --probability. "
            f"Use one of {sorted(PROBABILISTIC_RIVAL_AGENTS)} for a mixed rival."
        )

    resolved_depth = depth if depth is not None else DEFAULT_DEPTH
    resolved_probability = probability if probability is not None else DEFAULT_PROBABILITY
    resolved_seed = seed if seed is not None else DEFAULT_SEED

    if name in PROBABILISTIC_RIVAL_AGENTS:
        return agent_class(
            depth=resolved_depth,
            prob=resolved_probability,
            seed=resolved_seed,
        )

    return agent_class(
        depth=resolved_depth,
        seed=resolved_seed,
    )


__all__ = [
    "AdversarialSearchAgent",
    "AGENT_NAMES",
    "AlphaBetaAgent",
    "DEPTH_AGENTS",
    "ExpectimaxAgent",
    "MCTS_AGENT",
    "MCTSAgent",
    "MCTSNode",
    "MinimaxAgent",
    "MultiAgentSearchAgent",
    "PROBABILISTIC_RIVAL_AGENTS",
    "RandomAgent",
    "RANDOM_AGENT",
    "SearchMetrics",
    "create_agent",
    "get_agent_class",
]
