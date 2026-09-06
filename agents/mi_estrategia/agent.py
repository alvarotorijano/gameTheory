"""
Copycat Agent (Tit-for-Tat) for the Iterated Prisoner's Dilemma.

Cooperates on round 1, then plays the opponent's previous move.
This is a template for student agents to study and modify.
"""

from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class CopycatAgent(Agent):
    """
    Tit-for-Tat strategy: cooperate on round 1, then copy opponent's last move.

    This is one of the most famous strategies in game theory. It's proven to be
    very effective because it's:
    - Nice: starts with cooperation
    - Retaliatory: punishes defection immediately
    - Forgiving: returns to cooperation if opponent does

    This agent is provided as a template for student assignments.
    """

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Cooperate on round 1, then replicate opponent's last move.

        Parameters:
            own_history: This agent's past moves (unused in tit-for-tat).
            opponent_history: Opponent's past moves.

        Returns:
            "C" (cooperate) on round 1, otherwise opponent's last move.
        """
        if not opponent_history:
            # Round 1: start with cooperation (nice)
            return COOPERATE

        # Copy opponent's last move (tit-for-tat)
        return opponent_history[-1]
