"""
Do Be Evil Agent for the Iterated Prisoner's Dilemma.

A deceptive strategy that cooperates initially to build trust, then betrays
when the opponent shows two consecutive cooperations.
"""

from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class doBeEvil(Agent):
    """
    Deceptive strategy: cooperate until opponent shows two consecutive cooperations,
    then defect to exploit the opponent's trust.

    This agent waits for the opponent to establish a pattern of mutual cooperation,
    then backstabs them when they are most vulnerable.
    """

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Decide the agent's move.

        Parameters:
            own_history: List of own moves in prior rounds.
            opponent_history: List of opponent's moves in prior rounds.

        Returns:
            "C" (cooperate) or "D" (defect).
        """
        # If opponent has just shown two cooperations in a row, betray them
        if (opponent_history and len(opponent_history) >= 2 and
            opponent_history[-1] == COOPERATE and
            opponent_history[-2] == COOPERATE):
            return DEFECT

        # Otherwise, cooperate to build trust
        return COOPERATE
