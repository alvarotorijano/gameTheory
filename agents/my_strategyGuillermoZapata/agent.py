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

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        To try and beat a one on one just by returning DEFEAT the agent would always win. When trying to achieve the highest amount of
        points against the current 3 other agents, going tit for tat is the most likely strategy to score the most points over all. However there
        would always be a tie against a Copycat agent. 

        When playing against the second chance agent, Copycat would lose to it in the overall point system when paired up against the Random
        agent.

        The idea is to mix the second chance agent with the copycat agent, trying to achieve the best of both worlds.

        Parameters:
            own_history: This agent's past moves (unused in tit-for-tat).
            opponent_history: Opponent's past moves.

        """
        if not opponent_history:
                    # Round 1: start with cooperation
                    return COOPERATE
        
                # Check if opponent defected last round
        if opponent_history[-1] == DEFECT:
                    self.opponent_defection_count += 1
        
                # Retaliate only if we've seen two defections
        if self.opponent_defection_count >= 2:
                    # Retaliate once
                    self.opponent_defection_count = 0  # Reset for forgiveness
                    return DEFECT
        
                
        if self.opponent_defection_count <2:
                return opponent_history[-1]

