"""
Win-Stay, Lose-Shift Agent implementing Pavlov's strategy
"""

from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class CopycatAgent(Agent):
    """
    Pavlov: cooperate on round 1, then repeat action if it won last round otherwise switch action

    This strategy is specially good in tournaments where noise affects the agent's decisions.
    It won't stand out in a tournament without noise but it can score a lot of points by perpetually
    cooperating with other nice agents like Grim Trigger or Tit-For-Tat.
    """

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Cooperate on round 1, then repeat action if it caused a victory last round.

        Parameters:
            own_history: This agent's past moves.
            opponent_history: Opponent's past moves.

        Returns:
            "C" (cooperate) on round 1, otherwise opponent's last move.
        """
        if not opponent_history:
            # Round 1: start with cooperation (nice)
            return COOPERATE

        # Repeat decision while winning
        if (
            own_history[-1] == DEFECT and opponent_history[-1] == COOPERATE
            or own_history[-1] == COOPERATE and opponent_history[-1] == COOPERATE
        ):
            return own_history[-1]

        # If lost last round change strategy
        if own_history[-1] == COOPERATE:
            return DEFECT

        if own_history[-1] == DEFECT:
            return COOPERATE