"""
My agent.

Coopera por defecto. En cada ronda, se fija en las 5 rondas anteriores del rival. Si entre esas 5 rondas
hay más de dos DEFECT, entonces yo hago DEFECT. 
"""


from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class AdaptiveAgent(Agent):
    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Decide the next move based on the opponent's last five moves.

        Parameters:
            own_history: This agent's moves in previous rounds.
            opponent_history: Opponent's moves in previous rounds.

        Returns:
            "C" (cooperate) or "D" (defect).
        """

        # During the first five rounds, cooperate.
        if len(opponent_history) < 5:
            return COOPERATE

        # Look at the opponent's last five moves.
        recent_moves = opponent_history[-5:]

        # Count how many times the opponent defected.
        defections = recent_moves.count(DEFECT)

        # If the opponent defected at least three times,
        # defend ourselves by defecting.
        if defections >= 3:
            return DEFECT

        # Otherwise, continue cooperating.
        return COOPERATE