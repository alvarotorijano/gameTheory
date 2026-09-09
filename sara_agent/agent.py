"""
Earn My Trust Strategy: 
Defect in the first round. In subsequent rounds, cooperate if the opponent has cooperated at least once; otherwise, defect.
"""

from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class EarnMyTrustAgent(Agent):
    """
    Strategy: Defect in the first round. 
    In subsequent rounds, cooperate if the opponent has cooperated at least once; 
    otherwise, defect

    """

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        #Primera ronda: traicionar
        if not opponent_history:   
            return DEFECT
        #Si el rival a coperado alguna vez
        if COOPERATE in opponent_history:
            return COOPERATE
        #Si nunca ha coperado 
        return DEFECT
