from __future__ import annotations

from engine.model import Position
from engine.scenario import Scenario


def line_cells(start: Position, goal: Position) -> list[Position]:
    """
    Return grid cells along the straight segment from start to goal.

    Uses linear interpolation with rounding, so diagonals are 8-connected
    stair-steps. The list always includes both endpoints.
    """
    if start == goal:
        return [start]
    dx = goal[0] - start[0]
    dy = goal[1] - start[1]
    steps = max(abs(dx), abs(dy))
    cells: list[Position] = []
    for i in range(steps + 1):
        x = round(start[0] + dx * i / steps)
        y = round(start[1] + dy * i / steps)
        pos = (x, y)
        if not cells or cells[-1] != pos:
            cells.append(pos)
    return cells


def path_blocked(scenario: Scenario, start: Position, goal: Position) -> bool:
    """
    Return whether a wall lies on the open segment between start and goal.

    Endpoints are excluded; only interior cells of line_cells are checked.
    """
    return any(scenario.is_wall(cell) for cell in line_cells(start, goal)[1:-1])


def segment_intercepted(
    start: Position,
    goal: Position,
    opponent_positions: tuple[Position, ...],
) -> int | None:
    """
    Return the first opponent index on the lane after start, or None if clear.

    The start cell is excluded (ball carrier); the destination is included.
    Use path_blocked when a wall may close the lane without an interceptor.
    """
    for cell in line_cells(start, goal)[1:]:
        for idx, position in enumerate(opponent_positions):
            if position == cell:
                return idx
    return None
