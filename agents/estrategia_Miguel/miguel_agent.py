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

    def play(my_history, opponent_history, round_number, total_rounds=None):
        if not opponent_history:
            return "C"

        if len(opponent_history) >= 2:
            if opponent_history[-1] == "C" and opponent_history[-2] == "C":
                return "C"

        if len(opponent_history) >= 2:
            if opponent_history[-1] == "D" and opponent_history[-2] == "C":
                return "C"

        if len(opponent_history) >= 2:
            if opponent_history[-1] == "D" and opponent_history[-2] == "D":
                return "D"

        return opponent_history[-1]
