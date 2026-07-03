"""Filesystem paths for project assets and source root."""

from __future__ import annotations

from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_ROOT.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
SCENARIOS_DIR = ASSETS_DIR / "scenarios"
REPLAY_TEMPLATE_PATH = ASSETS_DIR / "ui" / "replay_template.html"
