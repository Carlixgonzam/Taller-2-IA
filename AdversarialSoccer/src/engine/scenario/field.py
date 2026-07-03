from __future__ import annotations

from engine.model import Position, Team

from .constants import MIN_GOAL_HEIGHT


def goal_opening_rows(height: int) -> range:
    """Return the y-indices of goal-mouth cells along the left and right borders."""
    interior_top = 1
    interior_bottom = height - 2
    interior_size = interior_bottom - interior_top + 1
    goal_rows = max(MIN_GOAL_HEIGHT, interior_size // 4)
    if interior_size % 2 != goal_rows % 2:
        goal_rows += 1
    goal_rows = min(goal_rows, interior_size)
    padding = interior_size - goal_rows
    start = interior_top + padding // 2
    return range(start, start + goal_rows)


def build_walls_and_goals(
    width: int,
    height: int,
) -> tuple[set[Position], set[Position], set[Position]]:
    """Build perimeter walls and goal mouths for a rectangular pitch."""
    goal_ys = goal_opening_rows(height)
    own_goal = {(0, y) for y in goal_ys}
    rival_goal = {(width - 1, y) for y in goal_ys}
    walls = {
        (x, y)
        for x in range(width)
        for y in range(height)
        if x in {0, width - 1} or y in {0, height - 1}
    }
    walls -= own_goal
    walls -= rival_goal
    return walls, own_goal, rival_goal


def to_positions(values: object, key: str) -> list[Position]:
    """Parse a YAML list of [x, y] pairs into grid positions."""
    if not isinstance(values, list):
        raise ValueError(f"Scenario key {key} must be a list of [x, y] positions.")
    return [(int(item[0]), int(item[1])) for item in values]


def parse_possession(value: object) -> Team:
    """Parse the initial ball-possession team from YAML."""
    if str(value).strip().lower() == "colombia":
        return Team.COLOMBIA
    if str(value).strip().lower() == "rival":
        return Team.RIVAL
    raise ValueError("possession must be colombia or rival.")
