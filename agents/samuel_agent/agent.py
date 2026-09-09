"""
Copycat Agent (Tit-for-Tat) for the Iterated Prisoner's Dilemma.

Cooperates on round 1, then plays the opponent's previous move.
This is a template for student agents to study and modify.
"""

from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class MyStrategy(Agent):


    # def play(self, own_history, opponent_history):
    #     """
    #     Contrary to what the opponent did in the last round, this agent will do the opposite.
    #     If the opponent cooperated, this agent will defect. If the opponent defected, this agent will cooperate.
    #     """
        
    #     if not opponent_history:
    #         # Round 1: cooperate
    #         return COOPERATE
        
    #     # If the opponent cooperated in the last round, defect now
    #     if opponent_history[-1] == COOPERATE:
    #         return DEFECT

    #     # If the opponent defected in the last round, cooperate now
    #     if opponent_history[-1] == DEFECT:
    #         return COOPERATE
        
    #     # Otherwise, cooperate
    #     return DEFECT

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Cooperates on round 1, then always defects independently of the opponent's previous move.
        """

        if not opponent_history:
            # Round 1, cooperate
            return COOPERATE
        
        # Otherwise, defect regardless of the opponent's previous move
        return DEFECT