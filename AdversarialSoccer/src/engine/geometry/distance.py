from __future__ import annotations

from collections.abc import Iterable

from engine.model import Position


def manhattan_distance(a: Position, b: Position) -> int:
    """Return the L1 distance between two grid cells."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def within_manhattan_range(origin: Position, target: Position, max_range: int) -> bool:
    """Return whether target is within max_range Manhattan steps of origin."""
    return manhattan_distance(origin, target) <= max_range


def sorted_by_manhattan_distance(
    origin: Position,
    positions: Iterable[Position],
) -> list[Position]:
    """Return positions ordered nearest-first from origin in Manhattan distance."""
    return sorted(positions, key=lambda pos: manhattan_distance(origin, pos))


def nearest_to(origin: Position, candidates: Iterable[Position]) -> tuple[int, Position]:
    """
    Return (index, position) of the candidate closest to origin in Manhattan distance.

    Ties are broken by the lowest index among equidistant candidates.
    """
    indexed = list(enumerate(candidates))
    if not indexed:
        raise ValueError("candidates must not be empty")
    return min(indexed, key=lambda item: manhattan_distance(origin, item[1]))
