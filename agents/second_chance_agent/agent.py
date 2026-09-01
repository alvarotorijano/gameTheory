"""
Second Chance Agent for the Iterated Prisoner's Dilemma.

A forgiving strategy that only retaliates after two defections, then resets.
Remembers roughly the last two rounds of opponent behavior.
"""

from typing import List

from utils.game_core import Agent, COOPERATE, DEFECT


class SecondChanceAgent(Agent):
    """
    Forgiving strategy with two-strike retaliation.

    This agent cooperates by default and forgives the opponent's first defection.
    Only on the second consecutive defection (or second defection pattern) does it
    retaliate once, then immediately forgives and returns to cooperation.

    Philosophy:
    - Everyone deserves a second chance
    - After two mistakes, a single retaliation is fair warning
    - Then forgive and move forward

    This demonstrates a "softer" strategy than pure tit-for-tat.
    """

    def __init__(self, num_rounds=None):
        """
        Initialize the agent with defection counter.

        Parameters:
            num_rounds: Number of rounds (or None for unknown horizon).
        """
        super().__init__(num_rounds)
        self.opponent_defection_count = 0

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Cooperate by default. Retaliate only after seeing two defections.

        Logic:
        1. If opponent's last move was DEFECT: increment defection counter
        2. If defection_count reaches 2: defect once (retaliation), then reset counter
        3. Otherwise: cooperate

        This creates a pattern:
        - 1st defection from opponent: we cooperate (forgive)
        - 2nd defection from opponent: we defect once (retaliate)
        - Then: counter resets, we cooperate again

        Parameters:
            own_history: This agent's past moves (unused).
            opponent_history: Opponent's past moves.

        Returns:
            "D" (defect) if opponent just triggered second-strike retaliation,
            "C" (cooperate) otherwise.
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

        # Default: be cooperative (even after the first defection)
        return COOPERATE
