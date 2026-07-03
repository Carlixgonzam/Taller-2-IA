from __future__ import annotations

from dataclasses import dataclass, field

from engine.model import TeamAction
from engine.state import GameState


@dataclass
class MCTSNode:
    """One node in the Monte Carlo search tree."""

    state: GameState
    parent: MCTSNode | None = None
    colombia_action: TeamAction | None = None
    rival_action: TeamAction | None = None
    children: list[MCTSNode] = field(default_factory=list)
    untried_actions: list[TeamAction] = field(default_factory=list)
    visits: int = 0
    total_value: float = 0.0
