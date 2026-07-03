from __future__ import annotations

from dataclasses import dataclass

from engine.model import MatchOutcome, Position, Team
from engine.scenario import Scenario


@dataclass(slots=True)
class GameState:
    """
    Snapshot of the soccer grid at one turn.

    Holds live player positions, possession, turn count, and match outcome.
    Field setup is read from scenario (immutable). Game rules live in engine.rules.

    Coordinates are (x, y) with y = 0 at the bottom row.
    Colombia attacks toward x = scenario.width - 1.
    """

    scenario: Scenario
    colombia_positions: tuple[Position, ...]
    rival_positions: tuple[Position, ...]
    possession: Team
    ball_owner: int
    turn: int = 0
    outcome: MatchOutcome = MatchOutcome.IN_PROGRESS

    @classmethod
    def initial(cls, scenario: Scenario) -> GameState:
        """Build turn-zero state from a loaded scenario."""
        return cls(
            scenario=scenario,
            colombia_positions=tuple(scenario.initial_colombia_positions),
            rival_positions=tuple(scenario.initial_rival_positions),
            possession=scenario.initial_possession,
            ball_owner=scenario.initial_ball_owner,
        )

    def team_size_for(self, team: Team) -> int:
        """Return how many players team has in this scenario."""
        return len(self.get_team_positions(team))

    def get_team_positions(self, team: Team) -> tuple[Position, ...]:
        """Return field positions for team, indexed by player id."""
        return self.colombia_positions if team is Team.COLOMBIA else self.rival_positions

    def get_ball_position(self) -> Position:
        """Return the grid cell where the ball currently is."""
        return self.get_team_positions(self.possession)[self.ball_owner]

    def get_team_goal(self, team: Team) -> set[Position]:
        """Return mouth cells of the goal team attacks."""
        return self.scenario.rival_goal if team is Team.COLOMBIA else self.scenario.own_goal

    def has_ball(self, team: Team) -> bool:
        """Return whether team currently has possession."""
        return self.possession is team
