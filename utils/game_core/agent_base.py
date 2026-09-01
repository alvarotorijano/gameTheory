"""
Abstract base class for all Prisoner's Dilemma agents.

All agents must inherit from this class and implement the play() method.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class Agent(ABC):
    """
    Abstract base class for Iterated Prisoner's Dilemma agents.

    Subclasses must implement the play() method to define their strategy.
    """

    def __init__(self, num_rounds: Optional[int] = None):
        """
        Initialize the agent.

        Parameters:
            num_rounds: The number of rounds this agent will play, or None if unknown.
                       When None, the agent does not know how many rounds it will play
                       (unknown horizon). The game still runs for a finite number of rounds,
                       but the agent is not told this number.
        """
        self.num_rounds = num_rounds

    @abstractmethod
    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Decide the agent's move for this round.

        This method is called once per round. Both agents' play() methods are called
        simultaneously (the agent does not know the opponent's current-round move).

        Parameters:
            own_history: List of this agent's moves in all prior rounds.
                        Empty list on round 1.
                        Each move is either "C" (cooperate) or "D" (defect).
            opponent_history: List of the opponent's moves in all prior rounds.
                             Empty list on round 1.
                             Each move is either "C" (cooperate) or "D" (defect).

        Returns:
            A single move: "C" (cooperate) or "D" (defect).
        """
        pass
