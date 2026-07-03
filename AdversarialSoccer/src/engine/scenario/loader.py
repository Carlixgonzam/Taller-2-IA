from __future__ import annotations

import yaml

from paths import SCENARIOS_DIR

from .scenario import Scenario


def load_scenario(name: str) -> Scenario | None:
    """Load a scenario by stem name from assets/scenarios/. Returns None if missing."""
    path = SCENARIOS_DIR / f"{name}.yaml"
    if not path.exists():
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Scenario {name} must be a YAML mapping.")
    return Scenario.from_yaml(name, data)


def list_scenario_names() -> list[str]:
    """Return sorted scenario stems available under assets/scenarios/."""
    return sorted(path.stem for path in SCENARIOS_DIR.glob("*.yaml"))
