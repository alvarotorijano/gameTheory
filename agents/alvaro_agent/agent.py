"""
Copycat Agent (Tit-for-Tat) for the Iterated Prisoner's Dilemma.

Cooperates on round 1, then plays the opponent's previous move.
This is a template for student agents to study and modify.
"""

from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class AlvaroAgent(Agent):
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
        Cooperate first and forgive one defection.
        Defect if the opponent defects twice in a row.
        """
        if not opponent_history:
            # Round 1: start with cooperation (nice)
            return COOPERATE

        #*el -1 significa el ultimo movimiento del oponente

        if opponent_history[-1] == COOPERATE:
            return COOPERATE # Si coopera, nosotros cooperamos

        #Con len forzamos a tener las ultimas dos jugadas del rival

        if len(opponent_history) >= 2 and opponent_history[-1] == DEFECT and opponent_history[-2] == DEFECT:
            return DEFECT # sI nos la lia dos veces, (dos Defects), hacemos D

        # Si solo hace una liada, se perdona, *2 o mas ya no
        return COOPERATE
