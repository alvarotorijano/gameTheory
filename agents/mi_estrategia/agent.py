"""
Grudger Agent (Rencorosa) for the Iterated Prisoner's Dilemma.

Cooperates always, until the opponent defects once.
From that point on, this agent defects forever - it never forgives.
"""

from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class GrudgerAgent(Agent):
    """
    Grudger strategy: cooperate until betrayed once, then never forgive.
    """

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Cooperate unless the opponent has ever defected before.
        """
        if DEFECT in opponent_history:
            # El rival nos ha traicionado alguna vez en el pasado: no perdonamos.
            return DEFECT

        # El rival nunca ha traicionado (o es la ronda 1): seguimos cooperando.
        return COOPERATE