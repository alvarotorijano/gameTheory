"""
Betrayer Agent for the Iterated Prisoner's Dilemma.

Cooperates by default. From time to time, tries to betray his opponent and measure their reaction, in order to act accordingly.
"""

from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class BetrayerAgent(Agent):
    """
    Cooperates by default.

    Philosophy:
    - Opens with COOPERATE. If the opponent DEFECT in the first round, punish him.
    - If the opponent DEFECT more than 1 time, DEFECT always.
    - If the opponent COOPERATE, COOPERATE also.
    - DEFECT (betray) the opponent: If the opponent punish the agent, COOPERATE in the whole match. If not, DEFECT him again. 
    """

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:

        round_number = len(own_history)+1

        # If we know that we are in the last round, always DEFECT. 
        if self.num_rounds != None and self.num_rounds == round_number:
            return DEFECT

        # The first round COOPERATE
        if round_number == 1:
            return COOPERATE
        if round_number == 2:
            # If the opponent DEFECT in the first round, we will punish him 
            if opponent_history[-1] == DEFECT:
                return DEFECT
            else:
                return COOPERATE


        # If the opponent has DEFECTED more that one time, DEFECT always. We don't trust him
        if opponent_history.count(DEFECT) > 1:
            return DEFECT
        else:
            # If the oponent DEFECT without a reason, DEFECT also
            if opponent_history[-1] == DEFECT and own_history[-2] == COOPERATE:
                return DEFECT
            # If the opponent DEFECT with a reason (a previous DEFECT from us), COOPERATE
            if opponent_history[-1] == DEFECT and own_history[-2] == DEFECT:
                return COOPERATE
            # If we both have already DEFECT, try to COOPERATE. We are forced to be good guys :)
            if opponent_history.count(DEFECT) == 1 and own_history.count(DEFECT) == 1:
                return COOPERATE
            # If the opponent has not betrayed us, try to DEFECT to see his response 
            if opponent_history.count(DEFECT) == 0 and own_history[-1] == COOPERATE:
                return DEFECT
            return COOPERATE

