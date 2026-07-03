from __future__ import annotations

from dataclasses import dataclass

from .directions import Directions
from .position import Position


@dataclass(frozen=True, slots=True)
class ShootAction:
    """Shoot or pass: all players stay; the engine uses origin and target."""

    origin: Position
    target: Position


@dataclass(frozen=True, slots=True)
class MovesAction:
    """Simultaneous move: one direction per player (including STOP)."""

    moves: tuple[Directions, ...]


TeamAction = ShootAction | MovesAction
