"""
Tournament Runner: Execute a complete round-robin tournament.

Discovers all agents, plays every pairing (both directions), and outputs CSV results.
"""

import argparse
import csv
import random
import sys
from pathlib import Path
from typing import List

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


def calculate_statistics(agent_history: List[str], opponent_history: List[str]):
    """
    Calculate behavioral statistics for an agent in one leg.

    Parameters:
        agent_history: List of agent's moves.
        opponent_history: List of opponent's moves.

    Returns:
        Dict with cooperation/defection statistics.
    """
    total_cooperations = agent_history.count(COOPERATE)
    total_defections = agent_history.count(DEFECT)

    cooperate_after_opponent_cooperate = 0
    cooperate_after_opponent_defect = 0
    defect_after_opponent_cooperate = 0
    defect_after_opponent_defect = 0

    for i in range(1, len(agent_history)):
        prev_opponent_move = opponent_history[i - 1]
        current_agent_move = agent_history[i]

        if prev_opponent_move == COOPERATE:
            if current_agent_move == COOPERATE:
                cooperate_after_opponent_cooperate += 1
            else:
                defect_after_opponent_cooperate += 1
        else:  # prev_opponent_move == DEFECT
            if current_agent_move == COOPERATE:
                cooperate_after_opponent_defect += 1
            else:
                defect_after_opponent_defect += 1

    first_move_cooperate = agent_history[0] == COOPERATE if agent_history else False

    return {
        "total_cooperations": total_cooperations,
        "total_defections": total_defections,
        "first_move_cooperate": first_move_cooperate,
        "cooperate_after_opponent_cooperate": cooperate_after_opponent_cooperate,
        "defect_after_opponent_cooperate": defect_after_opponent_cooperate,
        "cooperate_after_opponent_defect": cooperate_after_opponent_defect,
        "defect_after_opponent_defect": defect_after_opponent_defect,
    }


def main():
    """
    Main entry point for tournament runner.

    Discovers all agents, runs round-robin tournament, outputs CSV.
    """
    parser = argparse.ArgumentParser(
        description="Run a complete round-robin tournament with all agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tournament.py
  python run_tournament.py --rounds 50
  python run_tournament.py --unknown-horizon
  python run_tournament.py --no-self-play
  python run_tournament.py --output results/my_tournament.csv
        """,
    )

    parser.add_argument(
        "--rounds",
        type=int,
        default=None,
        help="Number of rounds per leg (default: from config.json)",
    )
    parser.add_argument(
        "--unknown-horizon",
        action="store_true",
        help="Use unknown horizon (random rounds per leg)",
    )
    parser.add_argument(
        "--no-self-play",
        action="store_true",
        help="Exclude self-play (agents only play different agents)",
    )
    parser.add_argument(
        "--output",
        default="results/tournament.csv",
        help="Output CSV file (default: results/tournament.csv)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress information",
    )

    args = parser.parse_args()

    # Create output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Discover agents
    agents_dir = project_root / "agents"
    agents = discover_agents(agents_dir)

    if not agents:
        print(f"{RED}Error: No agents found in agents/ folder.{RESET}", file=sys.stderr)
        print(f"\n{YELLOW}To add agents:{RESET}", file=sys.stderr)
        print(f"{WHITE}   1. Create a folder: agents/<agent_name>/", file=sys.stderr)
        print(f"   2. Add agent.py with an Agent subclass", file=sys.stderr)
        print(f"   3. Example: agents/random_agent/agent.py{RESET}", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"Discovered {len(agents)} agents: {', '.join(agents.keys())}")

    # Get configuration
    config = get_config()
    num_rounds = args.rounds or config.default_rounds

    # Run tournament
    results = []
    pairing_id = 0

    agent_names = sorted(agents.keys())
    total_pairings = len(agent_names) ** 2 if not args.no_self_play else len(agent_names) * (len(agent_names) - 1)
    current_pairing = 0

    for agent_a_name in agent_names:
        for agent_b_name in agent_names:
            if args.no_self_play and agent_a_name == agent_b_name:
                continue

            current_pairing += 1

            if args.verbose:
                print(f"[{current_pairing}/{total_pairings}] {agent_a_name} vs {agent_b_name}...", end=" ", flush=True)

            # Determine rounds for this leg
            num_rounds_first_leg = get_effective_rounds(None) if args.unknown_horizon else num_rounds
            num_rounds_second_leg = get_effective_rounds(None) if args.unknown_horizon else num_rounds

            # IDA
            agent_a_first_leg = agents[agent_a_name](num_rounds=(None if args.unknown_horizon else num_rounds_first_leg))
            agent_b_first_leg = agents[agent_b_name](num_rounds=(None if args.unknown_horizon else num_rounds_first_leg))

            result_first_leg = run_leg(
                agent_a_first_leg,
                agent_b_first_leg,
                num_rounds_first_leg,
                agent_a_name=agent_a_name,
                agent_b_name=agent_b_name,
                verbose=False,
            )

            stats_first_leg_a = calculate_statistics(result_first_leg.agent_a_history, result_first_leg.agent_b_history)
            stats_first_leg_b = calculate_statistics(result_first_leg.agent_b_history, result_first_leg.agent_a_history)

            # VUELTA
            agent_a_second_leg = agents[agent_a_name](num_rounds=(None if args.unknown_horizon else num_rounds_second_leg))
            agent_b_second_leg = agents[agent_b_name](num_rounds=(None if args.unknown_horizon else num_rounds_second_leg))

            result_second_leg = run_leg(
                agent_b_second_leg,
                agent_a_second_leg,
                num_rounds_second_leg,
                agent_a_name=agent_b_name,
                agent_b_name=agent_a_name,
                verbose=False,
            )

            stats_second_leg_a = calculate_statistics(result_second_leg.agent_a_history, result_second_leg.agent_b_history)
            stats_second_leg_b = calculate_statistics(result_second_leg.agent_b_history, result_second_leg.agent_a_history)

            # Record IDA row (agent_a perspective)
            results.append({
                "pairing_id": pairing_id,
                "leg": "first_leg",
                "num_rounds": result_first_leg.num_rounds,
                "agent_name": agent_a_name,
                "opponent_name": agent_b_name,
                "points_scored": result_first_leg.agent_a_score,
                "opponent_points": result_first_leg.agent_b_score,
                "first_move_cooperate": stats_first_leg_a["first_move_cooperate"],
                "total_cooperations": stats_first_leg_a["total_cooperations"],
                "total_defections": stats_first_leg_a["total_defections"],
                "cooperate_after_opponent_cooperate": stats_first_leg_a["cooperate_after_opponent_cooperate"],
                "defect_after_opponent_cooperate": stats_first_leg_a["defect_after_opponent_cooperate"],
                "cooperate_after_opponent_defect": stats_first_leg_a["cooperate_after_opponent_defect"],
                "defect_after_opponent_defect": stats_first_leg_a["defect_after_opponent_defect"],
            })

            # Record IDA row (agent_b perspective)
            results.append({
                "pairing_id": pairing_id,
                "leg": "first_leg",
                "num_rounds": result_first_leg.num_rounds,
                "agent_name": agent_b_name,
                "opponent_name": agent_a_name,
                "points_scored": result_first_leg.agent_b_score,
                "opponent_points": result_first_leg.agent_a_score,
                "first_move_cooperate": stats_first_leg_b["first_move_cooperate"],
                "total_cooperations": stats_first_leg_b["total_cooperations"],
                "total_defections": stats_first_leg_b["total_defections"],
                "cooperate_after_opponent_cooperate": stats_first_leg_b["cooperate_after_opponent_cooperate"],
                "defect_after_opponent_cooperate": stats_first_leg_b["defect_after_opponent_cooperate"],
                "cooperate_after_opponent_defect": stats_first_leg_b["cooperate_after_opponent_defect"],
                "defect_after_opponent_defect": stats_first_leg_b["defect_after_opponent_defect"],
            })

            # Record VUELTA row (agent_b perspective, now Player 1)
            results.append({
                "pairing_id": pairing_id,
                "leg": "second_leg",
                "num_rounds": result_second_leg.num_rounds,
                "agent_name": agent_b_name,
                "opponent_name": agent_a_name,
                "points_scored": result_second_leg.agent_a_score,
                "opponent_points": result_second_leg.agent_b_score,
                "first_move_cooperate": stats_second_leg_a["first_move_cooperate"],
                "total_cooperations": stats_second_leg_a["total_cooperations"],
                "total_defections": stats_second_leg_a["total_defections"],
                "cooperate_after_opponent_cooperate": stats_second_leg_a["cooperate_after_opponent_cooperate"],
                "defect_after_opponent_cooperate": stats_second_leg_a["defect_after_opponent_cooperate"],
                "cooperate_after_opponent_defect": stats_second_leg_a["cooperate_after_opponent_defect"],
                "defect_after_opponent_defect": stats_second_leg_a["defect_after_opponent_defect"],
            })

            # Record VUELTA row (agent_a perspective, now Player 2)
            results.append({
                "pairing_id": pairing_id,
                "leg": "second_leg",
                "num_rounds": result_second_leg.num_rounds,
                "agent_name": agent_a_name,
                "opponent_name": agent_b_name,
                "points_scored": result_second_leg.agent_b_score,
                "opponent_points": result_second_leg.agent_a_score,
                "first_move_cooperate": stats_second_leg_b["first_move_cooperate"],
                "total_cooperations": stats_second_leg_b["total_cooperations"],
                "total_defections": stats_second_leg_b["total_defections"],
                "cooperate_after_opponent_cooperate": stats_second_leg_b["cooperate_after_opponent_cooperate"],
                "defect_after_opponent_cooperate": stats_second_leg_b["defect_after_opponent_cooperate"],
                "cooperate_after_opponent_defect": stats_second_leg_b["cooperate_after_opponent_defect"],
                "defect_after_opponent_defect": stats_second_leg_b["defect_after_opponent_defect"],
            })

            pairing_id += 1

            if args.verbose:
                print("Done")

    # Write CSV
    if results:
        keys = results[0].keys()
        with open(output_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)

    print(f"\nTournament complete!")
    print(f"  Agents: {len(agents)}")
    print(f"  Pairings: {pairing_id}")
    print(f"  Results rows: {len(results)}")
    print(f"  Output: {output_path}")


if __name__ == "__main__":
    main()
