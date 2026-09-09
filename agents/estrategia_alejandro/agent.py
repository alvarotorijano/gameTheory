"""Alejandro's Grim Trigger agent for the Iterated Prisoner's Dilemma."""

from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class AlejandroAgent(Agent):
    """Cooperate until the opponent defects, then defect permanently."""

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Select a move using an irreversible defection trigger.

        Parameters:
            own_history: This agent's moves in all previous rounds.
            opponent_history: The opponent's moves in all previous rounds.

        Returns:
            "C" while the opponent has never defected, otherwise "D".
        """
        if DEFECT in opponent_history:
            return DEFECT

        return COOPERATE
