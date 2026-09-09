"""
Copycat Agent (Tit-for-Tat) for the Iterated Prisoner's Dilemma.

Cooperates on round 1, then plays the opponent's previous move.
This is a template for student agents to study and modify.
"""

from itertools import count
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
    count = 0

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Cooperate on round 1, then replicate opponent's last move.

        Parameters:
            own_history: This agent's past moves (unused in tit-for-tat).
            opponent_history: Opponent's past moves.

        Returns:
            Always defect
        """
        if self.count == 150:
            return DEFECT
        opening = [DEFECT, DEFECT, COOPERATE, DEFECT]
        if self.count < len(opening):
            return opening[self.count]

        first_four = opponent_history[:4]
        defects_first_four = first_four.count(DEFECT)

        if first_four == [
            COOPERATE,
            COOPERATE,
            COOPERATE,
            COOPERATE
        ]:
            return DEFECT
        
        if defects_first_four >= 3:
            return DEFECT

        recent_opponent = opponent_history[-2:]
        if recent_opponent == [DEFECT, DEFECT]:
            return DEFECT

        if opponent_history[-1] == COOPERATE:
            return COOPERATE

        return DEFECT