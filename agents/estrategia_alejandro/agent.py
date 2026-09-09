"""
Agent for the Iterated Prisoner's Dilemma.

Counts the opponent's previous moves and plays the move that the opponent has
used most often.
"""

from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class AlejandroAgent(Agent):
    """
    Follow the opponent's most common move.

    The agent cooperates when both moves have appeared equally often. This
    tie-breaking rule makes the strategy cooperative during the opening and
    avoids choosing defection without historical evidence.
    """

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Return the opponent's most frequently used move.

        Parameters:
            own_history: This agent's moves in previous rounds. The majority
                strategy does not need this history.
            opponent_history: The opponent's moves in previous rounds.

        Returns:
            "C" when cooperation is at least as common as defection, otherwise
            "D".
        """
        if opponent_history.count(DEFECT) > opponent_history.count(COOPERATE):
            return DEFECT
        return COOPERATE