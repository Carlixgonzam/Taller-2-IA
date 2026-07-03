from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SearchMetrics:
    """Counters and timing collected during one agent decision."""

    nodes_expanded: int = 0
    max_depth_reached: int = 0
    decision_time: float = 0.0
    selected_value: float = 0.0
