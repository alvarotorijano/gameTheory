"""
My strategy for prisoner's dilemma. Tit-for-tat modification.

"""

from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class MyStrategy(Agent):
    """
    Tit-for-Tat with final defect

    Sigue el Tit-for-tat clásico pero cuando el agente SÍ conoce el número de rondas, este traiciona
    en la última ronda para obtener así un beneficio final de condena sin un posterior castigo del contrincante.
    """
    def __init__(self, num_rounds=None):
      """
      Initialize the agent with defection counter.
      Parameters:
        num_rounds: Number of rounds (or None for unknown horizon).
      """
      super().__init__(num_rounds)

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Coopera ronda 1, copia último movimiento en las siguientes. Si conoce el número de rondas, traiciona en
        la última.

        Parameters:
            own_history: This agent's past moves (unused in tit-for-tat).
            opponent_history: Opponent's past moves.

        Returns:
            "C" (cooperate) on round 1, otherwise opponent's last move.
        """

        if self.num_rounds is not None and len(opponent_history) == self.num_rounds -1:
            return DEFECT
             
        else:
            if not opponent_history:
                # Round 1: start with cooperation (nice)
                return COOPERATE

            else:
                # Copy opponent's last move (tit-for-tat)
                return opponent_history[-1]
