"""
Random Agent for the Iterated Prisoner's Dilemma.

Plays a random move each round (baseline fictitious opponent).
"""

import random
from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class RandomAgent(Agent):
    """
    Random strategy: play a random move each round.

    This agent serves as a baseline fictitious opponent for testing student strategies.
    It makes no decisions based on history—every move is equally likely to be
    cooperation or defection.
    """

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Return a random move (50% cooperate, 50% defect).

        Parameters:
            own_history: Ignored (not used by random strategy).
            opponent_history: Ignored (not used by random strategy).

        Returns:
            "C" (cooperate) or "D" (defect) with equal probability.
        """
        return random.choice([COOPERATE, DEFECT])
