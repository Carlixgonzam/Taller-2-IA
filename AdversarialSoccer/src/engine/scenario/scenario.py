from __future__ import annotations

from dataclasses import dataclass

from engine.model import Position, Team

from .constants import (
    DEFAULT_MAX_SHOT_DISTANCE,
    DEFAULT_MAX_TURNS,
    MAX_FIELD_HEIGHT,
    MAX_FIELD_WIDTH,
    MIN_FIELD_HEIGHT,
    MIN_FIELD_WIDTH,
)
from .field import (
    build_walls_and_goals,
    parse_possession,
    to_positions,
)


@dataclass(slots=True)
class Scenario:
    """
    Immutable match setup loaded from a YAML file.

    Field geometry and spawn positions never change during play;
    dynamic positions live on GameState.
    """

    width: int
    height: int
    walls: set[Position]
    initial_colombia_positions: list[Position]
    initial_rival_positions: list[Position]
    rival_goal: set[Position]
    own_goal: set[Position]
    max_turns: int
    max_shot_distance: int
    initial_possession: Team
    initial_ball_owner: int

    @classmethod
    def from_yaml(cls, name: str, data: dict[str, object]) -> Scenario:
        """Parse and validate a scenario mapping loaded from YAML."""
        size = data.get("size")
        if not isinstance(size, list) or len(size) != 2:
            raise ValueError(f"Scenario {name}: size must be [width, height].")
        width, height = int(size[0]), int(size[1])
        too_small = width < MIN_FIELD_WIDTH or height < MIN_FIELD_HEIGHT
        too_large = width > MAX_FIELD_WIDTH or height > MAX_FIELD_HEIGHT
        if too_small or too_large:
            raise ValueError(
                f"Scenario {name}: field must be at least "
                f"{MIN_FIELD_WIDTH}x{MIN_FIELD_HEIGHT} and at most "
                f"{MAX_FIELD_WIDTH}x{MAX_FIELD_HEIGHT}."
            )

        initial_colombia = to_positions(data["colombia"], "colombia")
        initial_rival = to_positions(data["rival"], "rival")
        if not initial_colombia or not initial_rival:
            raise ValueError(f"Scenario {name}: both teams need at least one player.")

        possession = parse_possession(data.get("possession", "colombia"))
        ball_owner = int(data.get("ball_owner", 0))
        team_positions = initial_colombia if possession is Team.COLOMBIA else initial_rival
        if ball_owner < 0 or ball_owner >= len(team_positions):
            raise ValueError(f"Scenario {name}: ball_owner out of range for {possession.value}.")

        max_turns = int(data["max_turns"]) if "max_turns" in data else DEFAULT_MAX_TURNS
        max_shot_distance = (
            int(data["max_shot_distance"])
            if "max_shot_distance" in data
            else DEFAULT_MAX_SHOT_DISTANCE
        )

        walls, own_goal, rival_goal = build_walls_and_goals(width, height)

        all_positions = initial_colombia + initial_rival
        if len(set(all_positions)) != len(all_positions):
            raise ValueError(f"Scenario {name}: two players share the same cell.")
        for pos in all_positions:
            if pos in walls or pos in own_goal or pos in rival_goal:
                raise ValueError(f"Scenario {name}: player at {pos} is not on open field.")

        return cls(
            width=width,
            height=height,
            walls=walls,
            initial_colombia_positions=initial_colombia,
            initial_rival_positions=initial_rival,
            rival_goal=rival_goal,
            own_goal=own_goal,
            max_turns=max_turns,
            max_shot_distance=max_shot_distance,
            initial_possession=possession,
            initial_ball_owner=ball_owner,
        )

    def in_bounds(self, pos: Position) -> bool:
        """Return whether pos lies inside the field rectangle."""
        return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height

    def is_wall(self, pos: Position) -> bool:
        """Return whether pos is a perimeter wall cell."""
        return pos in self.walls

    def is_goal(self, pos: Position) -> bool:
        """Return whether pos is a goal-mouth cell on either end line."""
        return pos in self.own_goal or pos in self.rival_goal

    def is_legal_cell(self, pos: Position) -> bool:
        """Return whether a player may occupy pos (open field, not wall or goal)."""
        return self.in_bounds(pos) and not self.is_wall(pos) and not self.is_goal(pos)
