"""
Game core library for the Iterated Prisoner's Dilemma.

Provides the game engine, agent base class, and utilities for scoring and discovery.
"""

from .agent_base import Agent
from .agent_loader import discover_agents
from .engine import MatchResult, run_leg, get_effective_rounds
from .moves import COOPERATE, DEFECT
from .payoff import score_round, get_config, PayoffConfig

__all__ = [
    "Agent",
    "COOPERATE",
    "DEFECT",
    "MatchResult",
    "PayoffConfig",
    "discover_agents",
    "get_config",
    "get_effective_rounds",
    "run_leg",
    "score_round",
]
