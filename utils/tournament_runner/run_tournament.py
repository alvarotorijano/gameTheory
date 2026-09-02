"""
Tournament Runner: Execute a complete round-robin tournament.

Discovers all agents, plays every unique pairing once (simultaneous moves), and outputs CSV results.
"""

import argparse
import csv
import random
import sys
from datetime import datetime
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


def generate_output_filename(args) -> str:
    """
    Generate output filename with timestamp and flags.

    Format: tournament_DDMMYYYY-HHMMSS_<flags>.csv
    """
    now = datetime.now()
    timestamp = now.strftime("%d%m%Y-%H%M%S")

    flags = [f"rounds{args.rounds}"]
    if args.unknown_horizon:
        flags.append("unknown-horizon")
    if args.no_self_play:
        flags.append("no-self-play")

    flags_str = "_".join(flags)
    return f"tournament_{timestamp}_{flags_str}.csv"


def calculate_statistics(agent_history: List[str], opponent_history: List[str]):
    """
    Calculate behavioral statistics for an agent in one match.
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
        else:
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
    """
    parser = argparse.ArgumentParser(
        description="Run a complete round-robin tournament with all agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python utils/tournament_runner/run_tournament.py --rounds 100
  python utils/tournament_runner/run_tournament.py --rounds 50 --no-self-play
  python utils/tournament_runner/run_tournament.py --rounds 100 --unknown-horizon
        """,
    )

    parser.add_argument(
        "--rounds",
        type=int,
        required=True,
        help="Number of rounds per match (required)",
    )
    parser.add_argument(
        "--unknown-horizon",
        action="store_true",
        help="Agents don't know the round count (cannot plan strategy)",
    )
    parser.add_argument(
        "--no-self-play",
        action="store_true",
        help="Exclude self-play (agents only play different agents)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output CSV file (default: auto-generated with timestamp and flags)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress information",
    )

    args = parser.parse_args()

    # Determine output file
    if args.output is None:
        filename = generate_output_filename(args)
        output_path = Path("results") / filename
    else:
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

    num_rounds = args.rounds

    # Generate unique pairings (A vs B only, not B vs A)
    agent_names = sorted(agents.keys())
    if args.no_self_play:
        pairings = [(a, b) for i, a in enumerate(agent_names) for b in agent_names[i+1:]]
    else:
        pairings = [(a, b) for i, a in enumerate(agent_names) for b in agent_names[i:]]

    results = []
    total_pairings = len(pairings)

    for idx, (agent_a_name, agent_b_name) in enumerate(pairings, 1):
        if args.verbose:
            print(f"[{idx}/{total_pairings}] {agent_a_name} vs {agent_b_name}...", end=" ", flush=True)

        # Agents get num_rounds only if horizon is known
        agent_rounds = None if args.unknown_horizon else num_rounds

        # Execute match (simultaneous moves)
        agent_a = agents[agent_a_name](num_rounds=agent_rounds)
        agent_b = agents[agent_b_name](num_rounds=agent_rounds)

        result = run_leg(
            agent_a,
            agent_b,
            num_rounds,
            agent_a_name=agent_a_name,
            agent_b_name=agent_b_name,
            verbose=False,
        )

        stats_a = calculate_statistics(result.agent_a_history, result.agent_b_history)
        stats_b = calculate_statistics(result.agent_b_history, result.agent_a_history)

        # Record both perspectives (same match, different perspectives)
        results.append({
            "pairing_id": idx - 1,
            "num_rounds": result.num_rounds,
            "agent_name": agent_a_name,
            "opponent_name": agent_b_name,
            "points_scored": result.agent_a_score,
            "opponent_points": result.agent_b_score,
            "first_move_cooperate": stats_a["first_move_cooperate"],
            "total_cooperations": stats_a["total_cooperations"],
            "total_defections": stats_a["total_defections"],
            "cooperate_after_opponent_cooperate": stats_a["cooperate_after_opponent_cooperate"],
            "defect_after_opponent_cooperate": stats_a["defect_after_opponent_cooperate"],
            "cooperate_after_opponent_defect": stats_a["cooperate_after_opponent_defect"],
            "defect_after_opponent_defect": stats_a["defect_after_opponent_defect"],
        })

        results.append({
            "pairing_id": idx - 1,
            "num_rounds": result.num_rounds,
            "agent_name": agent_b_name,
            "opponent_name": agent_a_name,
            "points_scored": result.agent_b_score,
            "opponent_points": result.agent_a_score,
            "first_move_cooperate": stats_b["first_move_cooperate"],
            "total_cooperations": stats_b["total_cooperations"],
            "total_defections": stats_b["total_defections"],
            "cooperate_after_opponent_cooperate": stats_b["cooperate_after_opponent_cooperate"],
            "defect_after_opponent_cooperate": stats_b["defect_after_opponent_cooperate"],
            "cooperate_after_opponent_defect": stats_b["cooperate_after_opponent_defect"],
            "defect_after_opponent_defect": stats_b["defect_after_opponent_defect"],
        })

        if args.verbose:
            print("Done")

    # Write CSV
    if results:
        keys = results[0].keys()
        with open(output_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)

    print(f"\n{GREEN}Tournament complete!{RESET}")
    print(f"  {WHITE}Agents: {len(agents)}{RESET}")
    print(f"  {WHITE}Unique pairings: {len(pairings)}{RESET}")
    print(f"  {WHITE}Results rows: {len(results)}{RESET}")
    print(f"  {WHITE}Output: {output_path}{RESET}")


if __name__ == "__main__":
    main()
