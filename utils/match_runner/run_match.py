"""
Match Runner: Play two agents against each other (simultaneous moves).

CLI tool to execute a match between two agents and display results.
"""

import argparse
import sys
import time
from pathlib import Path

# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
RESET = "\033[0m"

# Calculate project root from this script's location
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

try:
    from utils.game_core import (
        COOPERATE,
        DEFECT,
        discover_agents,
        get_config,
        get_effective_rounds,
        run_leg,
    )
except ImportError as e:
    print(f"{RED}Error: Could not import game core modules.{RESET}", file=sys.stderr)
    print(f"{WHITE}   Details: {e}{RESET}", file=sys.stderr)
    print(f"\n{YELLOW}Project root: {project_root}{RESET}", file=sys.stderr)
    print(f"{WHITE}   Expected location: {project_root}/utils/game_core/{RESET}", file=sys.stderr)
    print(f"\n{YELLOW}Verify that utils/game_core/ contains:{RESET}", file=sys.stderr)
    print(f"{WHITE}   - agent_base.py", file=sys.stderr)
    print(f"   - agent_loader.py", file=sys.stderr)
    print(f"   - engine.py", file=sys.stderr)
    print(f"   - payoff.py{RESET}", file=sys.stderr)
    sys.exit(1)


def visualize_leg(agent_a_name: str, agent_b_name: str, agent_a_moves: list, agent_b_moves: list, delay: float = 0.8):
    """
    Visualize a leg move-by-move with delays between rounds.

    Parameters:
        agent_a_name: Name of first agent.
        agent_b_name: Name of second agent.
        agent_a_moves: List of moves for agent A.
        agent_b_moves: List of moves for agent B.
        delay: Delay in seconds between rounds.
    """
    print(f"\n{GREEN}Live replay:{RESET}\n")

    for round_num, (move_a, move_b) in enumerate(zip(agent_a_moves, agent_b_moves), start=1):
        # Move display
        move_a_display = "COOPERATE" if move_a == "C" else "DEFECT"
        move_b_display = "COOPERATE" if move_b == "C" else "DEFECT"

        # Color based on move (green for cooperation, red for defection)
        move_a_color = GREEN if move_a == "C" else RED
        move_b_color = GREEN if move_b == "C" else RED

        print(f"  Round {round_num}: {agent_a_name} → {move_a_color}{move_a_display}{RESET}  |  {agent_b_name} → {move_b_color}{move_b_display}{RESET}")
        time.sleep(delay)

    print()


def main():
    """
    Main entry point for match runner.

    Parses command-line arguments, discovers agents, runs both legs, and displays results.
    """
    parser = argparse.ArgumentParser(
        description="Play two agents in the Iterated Prisoner's Dilemma (simultaneous moves)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python utils/match_runner/run_match.py copycat_agent random_agent --rounds 50
  python utils/match_runner/run_match.py copycat_agent random_agent --rounds 50 --unknown-horizon
  python utils/match_runner/run_match.py copycat_agent random_agent --rounds 10 --visualize
  python utils/match_runner/run_match.py my_agent opponent_agent --rounds 100
        """,
    )

    parser.add_argument("agent_a", help="Name of first agent")
    parser.add_argument("agent_b", help="Name of second agent")
    parser.add_argument(
        "--rounds",
        type=int,
        required=True,
        help="Number of rounds per leg (required)",
    )
    parser.add_argument(
        "--unknown-horizon",
        action="store_true",
        help="Use unknown horizon (random rounds, agent sees num_rounds=None)",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print each round's result"
    )
    parser.add_argument(
        "--visualize", action="store_true", help="Show each move with delay (visual mode)"
    )

    args = parser.parse_args()

    # Determine effective rounds
    num_rounds_first_leg = args.rounds
    num_rounds_second_leg = args.rounds

    if args.unknown_horizon:
        print(f"{YELLOW}[Unknown Horizon Mode]{RESET}")
        print(f"{WHITE}  Agents will NOT know the round count")
        print(f"  Engine will play: {num_rounds_first_leg} rounds per leg{RESET}")
        print()
    else:
        print(f"{YELLOW}[Known Horizon Mode]{RESET}")
        print(f"{WHITE}  Agents know they will play: {num_rounds_first_leg} rounds per leg{RESET}")
        print()

    # Discover agents
    agents_dir = project_root / "agents"

    if not agents_dir.exists():
        print(f"{RED}Error: Agents directory not found.{RESET}", file=sys.stderr)
        print(f"{WHITE}   Expected at: {agents_dir}{RESET}", file=sys.stderr)
        sys.exit(1)

    agents = discover_agents(agents_dir)

    if not agents:
        print(f"{RED}Error: No agents found in {agents_dir}{RESET}", file=sys.stderr)
        print(f"\n{YELLOW}Make sure agents are placed in:{RESET}", file=sys.stderr)
        print(f"{WHITE}   {agents_dir}/{RESET}", file=sys.stderr)
        print(f"\n{YELLOW}Expected structure:{RESET}", file=sys.stderr)
        print(f"{WHITE}   agents/", file=sys.stderr)
        print(f"   ├── random_agent/", file=sys.stderr)
        print(f"   ├── copycat_agent/", file=sys.stderr)
        print(f"   └── <your_agent>/{RESET}", file=sys.stderr)
        sys.exit(1)

    # Check if requested agents exist
    missing_agents = []
    if args.agent_a not in agents:
        missing_agents.append(args.agent_a)
    if args.agent_b not in agents:
        missing_agents.append(args.agent_b)

    if missing_agents:
        print(f"{RED}Error: Agent(s) not found: {', '.join(missing_agents)}{RESET}", file=sys.stderr)
        print(f"\n{YELLOW}Searched in: {agents_dir}{RESET}", file=sys.stderr)
        print(f"\n{GREEN}Available agents ({len(agents)} found):{RESET}", file=sys.stderr)
        for agent_name in sorted(agents.keys()):
            print(f"{WHITE}   - {agent_name}{RESET}", file=sys.stderr)
        sys.exit(1)

    # Run match (agents make simultaneous moves)
    print(f"{'='*60}")
    print(f"MATCH: {args.agent_a} vs {args.agent_b}")
    print(f"Rounds: {num_rounds_first_leg}")
    print(f"{'='*60}")

    # Agents get num_rounds only if horizon is known
    agent_rounds = None if args.unknown_horizon else num_rounds_first_leg
    agent_a = agents[args.agent_a](num_rounds=agent_rounds)
    agent_b = agents[args.agent_b](num_rounds=agent_rounds)

    result = run_leg(
        agent_a,
        agent_b,
        num_rounds_first_leg,
        agent_a_name=args.agent_a,
        agent_b_name=args.agent_b,
        verbose=args.verbose,
    )

    print(f"\nResults:")
    print(f"  {args.agent_a}: {result.agent_a_score} points")
    print(f"  {args.agent_b}: {result.agent_b_score} points")
    print()

    if args.visualize:
        visualize_leg(args.agent_a, args.agent_b, result.agent_a_history, result.agent_b_history)

    # Display summary
    print(f"{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"\n{args.agent_a}: {result.agent_a_score} points")
    print(f"{args.agent_b}: {result.agent_b_score} points")

    print(f"\n{'='*60}")
    if result.agent_a_score > result.agent_b_score:
        winner = args.agent_a
        margin = result.agent_a_score - result.agent_b_score
    elif result.agent_b_score > result.agent_a_score:
        winner = args.agent_b
        margin = result.agent_b_score - result.agent_a_score
    else:
        winner = "TIE"
        margin = 0

    if winner == "TIE":
        print(f"RESULT: TIE - Both agents scored {result.agent_a_score} points")
    else:
        print(f"RESULT: {winner} WINS by {margin} points")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
