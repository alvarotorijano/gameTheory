"""
Match Runner: Play two agents against each other (ida + vuelta).

CLI tool to execute a complete match (two legs) between two agents and display results.
"""

import argparse
import sys
from pathlib import Path

from utils.game_core import (
    COOPERATE,
    DEFECT,
    discover_agents,
    get_config,
    get_effective_rounds,
    run_leg,
)


def main():
    """
    Main entry point for match runner.

    Parses command-line arguments, discovers agents, runs both legs, and displays results.
    """
    parser = argparse.ArgumentParser(
        description="Play two agents in the Iterated Prisoner's Dilemma (ida + vuelta)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_match.py copycat_agent random_agent --rounds 50
  python run_match.py copycat_agent random_agent --unknown-horizon
  python run_match.py my_agent opponent_agent
        """,
    )

    parser.add_argument("agent_a", help="Name of first agent (Player 1 in ida)")
    parser.add_argument("agent_b", help="Name of second agent (Player 2 in ida)")
    parser.add_argument(
        "--rounds",
        type=int,
        default=None,
        help="Number of rounds per leg (default: from config.json)",
    )
    parser.add_argument(
        "--unknown-horizon",
        action="store_true",
        help="Use unknown horizon (random rounds, agent sees num_rounds=None)",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print each round's result"
    )

    args = parser.parse_args()

    # Determine effective rounds
    config = get_config()
    if args.unknown_horizon:
        num_rounds_ida = get_effective_rounds(None)
        num_rounds_vuelta = get_effective_rounds(None)
        print(f"[Unknown Horizon Mode]")
        print(f"  Ida will run: {num_rounds_ida} rounds")
        print(f"  Vuelta will run: {num_rounds_vuelta} rounds")
        print()
    else:
        num_rounds_ida = args.rounds or config.default_rounds
        num_rounds_vuelta = num_rounds_ida

    # Discover agents
    agents_dir = Path(__file__).parent.parent.parent / "agents"
    agents = discover_agents(agents_dir)

    if args.agent_a not in agents:
        print(f"Error: Agent '{args.agent_a}' not found.", file=sys.stderr)
        print(f"Available agents: {', '.join(agents.keys())}", file=sys.stderr)
        sys.exit(1)

    if args.agent_b not in agents:
        print(f"Error: Agent '{args.agent_b}' not found.", file=sys.stderr)
        print(f"Available agents: {', '.join(agents.keys())}", file=sys.stderr)
        sys.exit(1)

    # Run Ida (A vs B)
    print(f"{'='*60}")
    print(f"IDA: {args.agent_a} (Player 1) vs {args.agent_b} (Player 2)")
    print(f"Rounds: {num_rounds_ida}")
    print(f"{'='*60}")

    agent_a_ida = agents[args.agent_a](num_rounds=(None if args.unknown_horizon else num_rounds_ida))
    agent_b_ida = agents[args.agent_b](num_rounds=(None if args.unknown_horizon else num_rounds_ida))

    result_ida = run_leg(
        agent_a_ida,
        agent_b_ida,
        num_rounds_ida,
        agent_a_name=args.agent_a,
        agent_b_name=args.agent_b,
        verbose=args.verbose,
    )

    print(f"\nIDA Results:")
    print(f"  {args.agent_a}: {result_ida.agent_a_score} points")
    print(f"  {args.agent_b}: {result_ida.agent_b_score} points")
    print()

    # Run Vuelta (B vs A)
    print(f"{'='*60}")
    print(f"VUELTA: {args.agent_b} (Player 1) vs {args.agent_a} (Player 2)")
    print(f"Rounds: {num_rounds_vuelta}")
    print(f"{'='*60}")

    agent_a_vuelta = agents[args.agent_a](num_rounds=(None if args.unknown_horizon else num_rounds_vuelta))
    agent_b_vuelta = agents[args.agent_b](num_rounds=(None if args.unknown_horizon else num_rounds_vuelta))

    result_vuelta = run_leg(
        agent_b_vuelta,
        agent_a_vuelta,
        num_rounds_vuelta,
        agent_a_name=args.agent_b,
        agent_b_name=args.agent_a,
        verbose=args.verbose,
    )

    print(f"\nVUELTA Results:")
    print(f"  {args.agent_b}: {result_vuelta.agent_a_score} points")
    print(f"  {args.agent_a}: {result_vuelta.agent_b_score} points")
    print()

    # Calculate averages
    total_ida_a = result_ida.agent_a_score
    total_ida_b = result_ida.agent_b_score
    total_vuelta_a = result_vuelta.agent_b_score  # Note: roles reversed in vuelta
    total_vuelta_b = result_vuelta.agent_a_score

    avg_a = (total_ida_a + total_vuelta_a) / 2
    avg_b = (total_ida_b + total_vuelta_b) / 2

    # Display summary
    print(f"{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"\n{args.agent_a}:")
    print(f"  Ida:    {total_ida_a} points")
    print(f"  Vuelta: {total_vuelta_a} points")
    print(f"  Average: {avg_a:.1f} points")

    print(f"\n{args.agent_b}:")
    print(f"  Ida:    {total_ida_b} points")
    print(f"  Vuelta: {total_vuelta_b} points")
    print(f"  Average: {avg_b:.1f} points")

    print(f"\n{'='*60}")
    if avg_a > avg_b:
        winner = args.agent_a
        margin = avg_a - avg_b
    elif avg_b > avg_a:
        winner = args.agent_b
        margin = avg_b - avg_a
    else:
        winner = "TIE"
        margin = 0

    if winner == "TIE":
        print(f"RESULT: TIE - Both agents scored {avg_a:.1f} points on average")
    else:
        print(f"RESULT: {winner} WINS by {margin:.1f} points on average")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
