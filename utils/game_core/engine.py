"""
Match engine for the Iterated Prisoner's Dilemma.

Orchestrates complete matches (legs) between two agents.
"""

import random
from dataclasses import dataclass, field
from typing import List

from .agent_base import Agent
from .moves import COOPERATE, DEFECT
from .payoff import score_round, get_config


@dataclass
class MatchResult:
    """
    Result of a completed leg (match) between two agents.

    Attributes:
        agent_a_name: Identifier for agent A (Player 1).
        agent_b_name: Identifier for agent B (Player 2).
        agent_a_score: Total points scored by agent A.
        agent_b_score: Total points scored by agent B.
        agent_a_history: List of agent A's moves.
        agent_b_history: List of agent B's moves.
        num_rounds: Number of rounds actually played.
        first_move_a_cooperate: True if agent A played "C" on round 1.
        first_move_b_cooperate: True if agent B played "C" on round 1.
    """

    agent_a_name: str
    agent_b_name: str
    agent_a_score: int
    agent_b_score: int
    agent_a_history: List[str] = field(default_factory=list)
    agent_b_history: List[str] = field(default_factory=list)
    num_rounds: int = 0
    first_move_a_cooperate: bool = False
    first_move_b_cooperate: bool = False


def run_leg(
    agent_a: Agent, agent_b: Agent, num_rounds: int, agent_a_name: str = "AgentA", agent_b_name: str = "AgentB", verbose: bool = False
) -> MatchResult:
    """
    Run a single leg (complete match) between two agents.

    Both agents are called each round to decide their moves. Moves are simultaneous
    (neither agent knows the opponent's current-round choice).

    Parameters:
        agent_a: First agent (Player 1).
        agent_b: Second agent (Player 2).
        num_rounds: Number of rounds to play.
        agent_a_name: Display name for agent A (used in output).
        agent_b_name: Display name for agent B (used in output).
        verbose: If True, print each round's result.

    Returns:
        MatchResult object with scores, histories, and statistics.
    """
    agent_a_history = []
    agent_b_history = []
    agent_a_score = 0
    agent_b_score = 0

    for round_num in range(num_rounds):
        move_a = agent_a.play(agent_a_history[:], agent_b_history[:])
        move_b = agent_b.play(agent_b_history[:], agent_a_history[:])

        if move_a not in [COOPERATE, DEFECT] or move_b not in [COOPERATE, DEFECT]:
            raise ValueError(f"Invalid move: {move_a} or {move_b}. Must be 'C' or 'D'.")

        points_a, points_b = score_round(move_a, move_b)
        agent_a_score += points_a
        agent_b_score += points_b

        agent_a_history.append(move_a)
        agent_b_history.append(move_b)

        if verbose:
            print(f"Round {round_num + 1}: {agent_a_name}={move_a} {agent_b_name}={move_b} | Points: {points_a}, {points_b}")

    result = MatchResult(
        agent_a_name=agent_a_name,
        agent_b_name=agent_b_name,
        agent_a_score=agent_a_score,
        agent_b_score=agent_b_score,
        agent_a_history=agent_a_history,
        agent_b_history=agent_b_history,
        num_rounds=num_rounds,
        first_move_a_cooperate=(agent_a_history[0] == COOPERATE) if agent_a_history else False,
        first_move_b_cooperate=(agent_b_history[0] == COOPERATE) if agent_b_history else False,
    )

    return result


def get_effective_rounds(num_rounds: int | None) -> int:
    """
    Determine the actual number of rounds to play.

    If num_rounds is None (unknown horizon), randomly pick a number from the configured range.
    Otherwise, return num_rounds as-is.

    Parameters:
        num_rounds: Requested number of rounds, or None for unknown horizon.

    Returns:
        The actual number of rounds to play.
    """
    if num_rounds is None:
        config = get_config()
        return random.randint(config.unknown_horizon_min, config.unknown_horizon_max)
    return num_rounds
