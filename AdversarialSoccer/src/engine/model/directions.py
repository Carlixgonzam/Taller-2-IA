from __future__ import annotations

from enum import StrEnum

from .position import Position


class Directions(StrEnum):
    """4-neighbourhood moves plus standing still."""

    STOP = "Stop"
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"


# Grid delta (dx, dy) applied by each direction step.
DIRECTION_VECTORS: dict[Directions, Position] = {
    Directions.STOP: (0, 0),
    Directions.NORTH: (0, 1),
    Directions.SOUTH: (0, -1),
    Directions.EAST: (1, 0),
    Directions.WEST: (-1, 0),
}
