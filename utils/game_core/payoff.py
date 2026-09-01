"""
Payoff scoring for the Iterated Prisoner's Dilemma.

Loads game configuration from config.json and provides functions to score rounds.
"""

import json
from pathlib import Path
from typing import Tuple

from .moves import COOPERATE, DEFECT


class PayoffConfig:
    """
    Game configuration loaded from config.json.

    Attributes:
        both_cooperate: Points awarded when both players cooperate.
        both_defect: Points awarded when both players defect.
        betrayed_cooperator: Points awarded to the cooperator when one defects.
        betrayer_reward: Points awarded to the defector when one betrays.
    """

    def __init__(self):
        """Load configuration from config.json in the project root."""
        config_path = Path(__file__).parent.parent.parent / "config.json"

        with open(config_path, "r") as f:
            config_data = json.load(f)

        payoff_data = config_data["payoff"]
        self.both_cooperate = payoff_data["both_cooperate"]
        self.both_defect = payoff_data["both_defect"]
        self.betrayed_cooperator = payoff_data["betrayed_cooperator"]
        self.betrayer_reward = payoff_data["betrayer_reward"]

        rounds_data = config_data["rounds"]
        self.default_rounds = rounds_data["default"]
        self.unknown_horizon_min = rounds_data["unknown_horizon_min"]
        self.unknown_horizon_max = rounds_data["unknown_horizon_max"]


_config = PayoffConfig()


def score_round(move_a: str, move_b: str) -> Tuple[int, int]:
    """
    Score one round of the Prisoner's Dilemma given both players' moves.

    Parameters:
        move_a: Move by player A ("C" for cooperate or "D" for defect).
        move_b: Move by player B ("C" for cooperate or "D" for defect).

    Returns:
        Tuple of (points_for_a, points_for_b).
    """
    if move_a == COOPERATE and move_b == COOPERATE:
        return (_config.both_cooperate, _config.both_cooperate)
    elif move_a == DEFECT and move_b == DEFECT:
        return (_config.both_defect, _config.both_defect)
    elif move_a == COOPERATE and move_b == DEFECT:
        return (_config.betrayed_cooperator, _config.betrayer_reward)
    elif move_a == DEFECT and move_b == COOPERATE:
        return (_config.betrayer_reward, _config.betrayed_cooperator)
    else:
        raise ValueError(f"Invalid moves: {move_a}, {move_b}")


def get_config() -> PayoffConfig:
    """
    Get the current game configuration.

    Returns:
        PayoffConfig object with all game parameters.
    """
    return _config
