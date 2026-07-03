from __future__ import annotations

from engine.model import DIRECTION_VECTORS, Directions, Position


def apply_direction(origin: Position, direction: Directions) -> Position:
    """
    Return the cell reached from origin with one step in direction.

    Directions.STOP leaves origin unchanged.
    """
    dx, dy = DIRECTION_VECTORS[direction]
    return (origin[0] + dx, origin[1] + dy)


def apply_joint_moves(
    positions: tuple[Position, ...],
    moves: tuple[Directions, ...],
) -> tuple[Position, ...]:
    """Return each position after its paired direction is applied."""
    return tuple(
        apply_direction(position, direction)
        for position, direction in zip(positions, moves, strict=True)
    )
