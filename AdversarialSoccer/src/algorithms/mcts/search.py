from __future__ import annotations

import random
from collections.abc import Callable

from algorithms.base import EvaluationFunction
from algorithms.base.search import is_terminal, legal_actions, pick_rival_action
from engine.model import Team, TeamAction
from engine.rules import step
from engine.state import GameState

from .node import MCTSNode
from .uct import uct_score


def _select(node: MCTSNode, exploration: float) -> MCTSNode:
    """Descend with UCT until the node can be expanded or rolled out."""
    while not is_terminal(node.state) and not node.untried_actions and node.children:
        node = max(
            node.children,
            key=lambda child: uct_score(
                child.total_value,
                child.visits,
                max(1, node.visits),
                exploration,
            ),
        )
    return node


def _expand(
    node: MCTSNode,
    evaluation_function: EvaluationFunction,
    rng: random.Random,
    prob: float,
) -> MCTSNode:
    """Try one untried Colombia action and attach a child node."""
    if is_terminal(node.state) or not node.untried_actions:
        return node

    colombia_action = node.untried_actions.pop(rng.randrange(len(node.untried_actions)))
    rival_action = pick_rival_action(
        node.state,
        colombia_action,
        evaluation_function,
        rng,
        prob=prob,
    )
    successor = step(node.state, colombia_action, rival_action)
    child = MCTSNode(
        state=successor,
        parent=node,
        colombia_action=colombia_action,
        rival_action=rival_action,
        untried_actions=(
            legal_actions(successor, Team.COLOMBIA) if not is_terminal(successor) else []
        ),
    )
    node.children.append(child)
    return child


def _rollout(
    state: GameState,
    evaluation_function: EvaluationFunction,
    rng: random.Random,
    prob: float,
) -> float:
    """One random joint step from state, then evaluate the successor."""
    if is_terminal(state):
        return evaluation_function(state)

    colombia_action = rng.choice(legal_actions(state, Team.COLOMBIA))
    rival_action = pick_rival_action(
        state,
        colombia_action,
        evaluation_function,
        rng,
        prob=prob,
    )
    return evaluation_function(step(state, colombia_action, rival_action))


def _backpropagate(node: MCTSNode, value: float) -> None:
    """Update visit counts and total value up to the root."""
    while node is not None:
        node.visits += 1
        node.total_value += value
        node = node.parent


def _best_root_move(root: MCTSNode) -> tuple[TeamAction, TeamAction, float]:
    """Return the root child with the highest average rollout value."""
    if not root.children:
        raise ValueError("MCTS produced no root children")

    best_child = max(
        root.children,
        key=lambda child: (
            child.total_value / child.visits,
            child.visits,
        ),
    )
    if best_child.colombia_action is None or best_child.rival_action is None:
        raise ValueError("MCTS child is missing actions")
    return (
        best_child.colombia_action,
        best_child.rival_action,
        best_child.total_value / best_child.visits,
    )


def mcts_search(
    state: GameState,
    evaluation_function: EvaluationFunction,
    rng: random.Random,
    *,
    iterations: int,
    prob: float = 0.0,
    exploration: float = 1.4,
    on_expand: Callable[[], None] | None = None,
) -> tuple[TeamAction, TeamAction, float]:
    """
    Monte Carlo tree search with UCT selection and a one-step rollout.

    Tips:
    - One iteration: select → expand → rollout → backpropagate.
    - Rival model matches Expectimax: greedy MIN with prob (1 - p), random with prob p.
    - Pick the root child with the highest average value (tie-break by visits).
    - Use legal_actions, step, and pick_rival_action; empty lists are errors.
    - Optional: merge repeated states with a hashable key to save memory.
    """
    root = MCTSNode(
        state=state,
        untried_actions=legal_actions(state, Team.COLOMBIA),
    )

    ### YOUR CODE HERE ###
    # --- SOLUTION START ---

    # --- SOLUTION END ---

    return _best_root_move(root)
