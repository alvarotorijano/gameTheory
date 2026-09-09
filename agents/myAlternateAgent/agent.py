"""
Alternate Agent for the Iterated Prisoner's Dilemma.

"""
import random

from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class myAlternateAgent(Agent):
    """
    
    """

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Random on round 1, alternate answers on the following rounds, .....
        It will alternate its answer depending on its previous answer

        Parameters:
            own_history: This agent's past moves ).
            opponent_history: Opponent's past moves.

        Returns:
            It will alternate its answer depending on its previous answer
            First answer is random
        """
        if not own_history:
            # Round 1: start random choice
            return random.choice([COOPERATE, DEFECT])

        if own_history:
            #next rounds it will alternate the answer depending on its previous answer
            answer = own_history[-1]
            if answer == DEFECT:
                return COOPERATE
            return DEFECT
            
