from __future__ import annotations

from colorama import Fore, Style
from colorama import init as colorama_init

colorama_init(autoreset=True)

_WIDTH = 40


def title(text: str) -> None:
    """Print a highlighted banner title."""
    line = "═" * _WIDTH
    print(f"{Fore.CYAN}{Style.BRIGHT}{line}")
    print(f"  {text}")
    print(f"{line}{Style.RESET_ALL}")


def section() -> None:
    """Print a horizontal rule."""
    print(f"{Fore.CYAN}{'─' * _WIDTH}{Style.RESET_ALL}")


def info(label: str, value: str) -> None:
    """Print one aligned label/value line."""
    print(f"  {label:<12}: {value}")


def write_turn(
    writer,
    turn: int,
    max_turns: int,
    value: float,
    decision_s: float,
) -> None:
    """Write a formatted turn line through writer (e.g. tqdm.write)."""
    metrics = f"{Fore.YELLOW}value={value:.1f} · {decision_s:.2f}s{Style.RESET_ALL}"
    writer(f"Turn {turn:>2}/{max_turns}  {metrics}")


def print_summary(
    *,
    outcome: str,
    turns: int,
    avg_nodes: float,
    avg_decision_s: float,
    wall_s: float,
) -> None:
    """Print the final match summary block."""
    section()
    if outcome == "win":
        outcome_text = f"{Fore.GREEN}{Style.BRIGHT}WIN{Style.RESET_ALL}"
    elif outcome == "loss":
        outcome_text = f"{Fore.RED}{Style.BRIGHT}LOSS{Style.RESET_ALL}"
    elif outcome == "draw":
        outcome_text = f"{Fore.YELLOW}{Style.BRIGHT}DRAW{Style.RESET_ALL}"
    else:
        outcome_text = f"{Fore.YELLOW}UNFINISHED{Style.RESET_ALL}"

    info("Result", outcome_text)
    info("Turns", str(turns))
    nodes_dec = (
        f"{Fore.YELLOW}{avg_nodes:.1f} · {avg_decision_s:.4f}s/dec · "
        f"{wall_s:.2f}s total{Style.RESET_ALL}"
    )
    info("Nodes/dec", nodes_dec)
    section()
    print(f"{Fore.CYAN}{'═' * _WIDTH}{Style.RESET_ALL}")
