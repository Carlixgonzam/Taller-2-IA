from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from engine.geometry import apply_direction
from engine.model import Directions, MovesAction, ShootAction, Team, TeamAction
from engine.state import GameState
from paths import REPLAY_TEMPLATE_PATH

_CELL_SIZE = 30
_FRAME_DELAY_MS = 800
_TURNOVER_HOLD_MS = 1500
_GOAL_HOLD_MS = 2400


class ReplayDisplay:
    """Record match frames and write soccer_replay.html."""

    def __init__(self) -> None:
        self._frames: list[dict[str, object]] = []
        self._pending_events: list[dict[str, object]] = []

    def initialize(self, state: GameState) -> None:
        """Reset frames and record the opening board state."""
        self._frames = []
        self._record_frame(state)

    def update(self, state: GameState) -> None:
        """Record a frame after each applied timestep."""
        self._record_frame(state)

    def finish(self, state: GameState) -> None:
        """Record the final frame and write soccer_replay.html."""
        self._record_frame(state)
        self._write_replay(state)

    def record_turn_actions(
        self,
        state: GameState,
        colombia_action: TeamAction,
        rival_action: TeamAction,
    ) -> None:
        """Record both teams' joint actions for one simultaneous timestep."""
        self._record_team_action(state, Team.COLOMBIA, colombia_action)
        self._record_team_action(state, Team.RIVAL, rival_action)

    def record_goal(self, team: Team) -> None:
        """Attach a goal marker to the next recorded frame."""
        self._pending_events.append(
            {
                "type": "Goal",
                "team": team.value,
            }
        )

    def record_turnover(self, state: GameState, *, kind: str = "pressure") -> None:
        """Attach a possession-change marker to the next recorded frame."""
        self._pending_events.append(
            {
                "team": state.possession.value,
                "type": "Turnover",
                "kind": kind,
                "from": list(state.get_ball_position()),
            }
        )

    def _record_team_action(
        self,
        state: GameState,
        team: Team,
        action: TeamAction,
    ) -> None:
        """Queue move or shoot events for one team action."""
        match action:
            case ShootAction(origin=origin, target=target):
                if state.possession is not team:
                    return
                self._pending_events.append(
                    {
                        "team": team.value,
                        "type": "Shoot",
                        "from": list(origin),
                        "to": list(target),
                    }
                )
            case MovesAction(moves=moves):
                positions = state.get_team_positions(team)
                for idx, direction in enumerate(moves):
                    if direction is Directions.STOP:
                        continue
                    start = positions[idx]
                    end = apply_direction(start, direction)
                    self._pending_events.append(
                        {
                            "team": team.value,
                            "type": "Move",
                            "player": idx,
                            "from": list(start),
                            "to": list(end),
                        }
                    )

    def _record_frame(self, state: GameState) -> None:
        """Append a deduplicated snapshot of the current board and pending events."""
        events = list(self._pending_events)
        frame: dict[str, object] = {
            "possession": state.possession.value,
            "ball": list(state.get_ball_position()),
            "colombia": [list(pos) for pos in state.colombia_positions],
            "rival": [list(pos) for pos in state.rival_positions],
            "events": events,
        }
        if any(event.get("type") == "Goal" for event in events):
            frame["holdMs"] = _GOAL_HOLD_MS
        elif any(event.get("type") == "Turnover" for event in events):
            frame["holdMs"] = _TURNOVER_HOLD_MS
        self._pending_events = []
        if not self._frames or self._frames[-1] != frame:
            self._frames.append(frame)

    def _write_replay(self, state: GameState) -> None:
        """Serialize frames and field metadata into soccer_replay.html."""
        scenario = state.scenario
        payload = {
            "width": scenario.width,
            "height": scenario.height,
            "cellSize": _CELL_SIZE,
            "frameDelayMs": _FRAME_DELAY_MS,
            "walls": [list(pos) for pos in sorted(scenario.walls)],
            "ownGoal": [list(pos) for pos in sorted(scenario.own_goal)],
            "rivalGoal": [list(pos) for pos in sorted(scenario.rival_goal)],
            "frames": self._frames,
        }
        output_path = Path.cwd() / "soccer_replay.html"
        template = REPLAY_TEMPLATE_PATH.read_text(encoding="utf-8")
        output_path.write_text(template.replace("__DATA__", json.dumps(payload)), encoding="utf-8")
        print(f"HTML graphic replay written to: {output_path}")
        self._open_replay(output_path)

    def _open_replay(self, output_path: Path) -> None:
        """Open the generated replay with the operating system default browser."""
        resolved = output_path.resolve()
        replay_uri = resolved.as_uri()
        openers = {
            "darwin": ["open", str(resolved)],
            "linux": ["xdg-open", str(resolved)],
            "win": ["cmd", "/c", "start", "", str(resolved)],
        }
        platform = "win" if sys.platform.startswith("win") else sys.platform.split("-", 1)[0]
        command = openers.get(platform)
        if command is None:
            print(f"Open this file in your browser: {replay_uri}")
            return
        try:
            subprocess.run(
                command,
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            print(f"Could not open automatically. Open this file in your browser: {replay_uri}")
