"""Majority-history strategy for the Iterated Prisoner's Dilemma."""

from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class MyAgent(Agent):
    """
    Cooperate when the opponent has cooperated at least as often as they have
    defected; otherwise, defect.
    """

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Follow the majority of the opponent's previous moves.

        Parameters:
            own_history: This agent's past moves.
            opponent_history: Opponent's past moves.

        Returns:
            "C" if cooperation exceeds or ties defection, otherwise "D".
        """
        cooperation_count = opponent_history.count(COOPERATE)
        defection_count = opponent_history.count(DEFECT)

        if defection_count > cooperation_count:
            return DEFECT

        return COOPERATE
