from __future__ import annotations

from enum import StrEnum

from .position import Position


class Team(StrEnum):
    """Teams in the adversarial soccer simulation."""

    COLOMBIA = "Colombia"
    RIVAL = "Rival"

    @property
    def opponent(self) -> Team:
        """Return the other team."""
        return Team.RIVAL if self is Team.COLOMBIA else Team.COLOMBIA

    def is_ahead_on_attack_axis(
        self,
        origin: Position,
        target: Position,
        *,
        inclusive: bool = True,
    ) -> bool:
        """
        Return whether target lies ahead of origin on this team's attack axis.

        Colombia attacks toward increasing x; Rival toward decreasing x.
        """
        if self is Team.COLOMBIA:
            return target[0] >= origin[0] if inclusive else target[0] > origin[0]
        return target[0] <= origin[0] if inclusive else target[0] < origin[0]
