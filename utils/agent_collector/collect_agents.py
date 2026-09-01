"""
Agent Collector: Import student agents from repositories or local files.

Discovers agents in student submissions and copies them into the main agents/ folder.
Handles both git repos and local files, with AST-based agent discovery.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

from utils.game_core import discover_agents


# Names of example agents to exclude from import (never overwrite examples)
EXAMPLE_AGENT_NAMES = {"random_agent", "copycat_agent", "second_chance_agent"}


def clone_repo(repo_url: str, cache_dir: Path) -> Path | None:
    """
    Clone a git repository into the cache directory.

    Parameters:
        repo_url: Git repository URL.
        cache_dir: Directory to clone into.

    Returns:
        Path to the cloned directory, or None if cloning failed.
    """
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = cache_dir / repo_name

    if repo_path.exists():
        if input(f"  Repo already cached at {repo_path}. Reuse? (y/n): ").lower() != "y":
            shutil.rmtree(repo_path)
            print(f"  Cloning {repo_url}...")
            try:
                subprocess.run(
                    ["git", "clone", repo_url, str(repo_path)],
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError as e:
                print(f"  Error: Failed to clone {repo_url}", file=sys.stderr)
                return None
        else:
            print(f"  Using cached repo")
        return repo_path

    print(f"  Cloning {repo_url}...")
    try:
        subprocess.run(
            ["git", "clone", repo_url, str(repo_path)],
            check=True,
            capture_output=True,
        )
        return repo_path
    except subprocess.CalledProcessError as e:
        print(f"  Error: Failed to clone {repo_url}", file=sys.stderr)
        return None


def import_agents_from_source(
    source: str | Path, student_name: str, agents_dir: Path, dry_run: bool = False
) -> int:
    """
    Import agents from a source (git repo or local path).

    Parameters:
        source: Git URL or local file/folder path.
        student_name: Name of the student (for namespacing).
        agents_dir: Destination agents directory.
        dry_run: If True, don't actually copy files.

    Returns:
        Number of agents imported.
    """
    source_path = None

    # Determine if source is git URL or local path
    if isinstance(source, str) and (source.startswith("http") or source.startswith("git")):
        # Git repository
        cache_dir = agents_dir.parent / "._cache"
        cache_dir.mkdir(exist_ok=True)
        source_path = clone_repo(source, cache_dir)
        if not source_path:
            return 0
    else:
        # Local path
        source_path = Path(source)
        if not source_path.exists():
            print(f"  Error: Local path does not exist: {source}", file=sys.stderr)
            return 0

    if not source_path:
        return 0

    # Discover agents in source
    discovered = discover_agents(source_path)

    if not discovered:
        print(f"  No agents found in {source_path}")
        return 0

    # Import each discovered agent
    imported_count = 0

    for agent_folder_name in source_path.glob("**"):
        if not agent_folder_name.is_dir():
            continue

        agent_py = agent_folder_name / "agent.py"
        if not agent_py.exists():
            continue

        # Skip example agents
        if agent_folder_name.name in EXAMPLE_AGENT_NAMES:
            print(f"  Skipping example agent: {agent_folder_name.name}")
            continue

        # Create destination folder name (avoid collisions)
        dest_folder_name = f"{student_name}_{agent_folder_name.name}"
        dest_folder = agents_dir / dest_folder_name

        if dest_folder.exists():
            print(f"  Warning: {dest_folder_name} already exists, skipping")
            continue

        # Copy agent folder
        if dry_run:
            print(f"  [DRY RUN] Would copy: {agent_folder_name} -> {dest_folder_name}")
        else:
            print(f"  Copying: {agent_folder_name.name} -> {dest_folder_name}")
            shutil.copytree(agent_folder_name, dest_folder)

        imported_count += 1

    return imported_count


def main():
    """
    Main entry point for agent collector.

    Reads sources from JSON file and imports all agents.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Collect agents from student repositories or files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example sources.json:
[
  {"student": "juan_perez", "source": "https://github.com/juan_perez/pd-agent.git"},
  {"student": "maria_lopez", "source": "/home/prof/submissions/maria_strategy.py"}
]

Examples:
  python collect_agents.py --sources sources.json
  python collect_agents.py --sources sources.json --dry-run
  python collect_agents.py --sources sources.json --verbose
        """,
    )

    parser.add_argument(
        "--sources",
        required=True,
        help="JSON file with list of {student, source} objects",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually copying",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed progress information",
    )

    args = parser.parse_args()

    # Load sources
    sources_path = Path(args.sources)
    if not sources_path.exists():
        print(f"Error: Sources file not found: {sources_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sources_path, "r") as f:
            sources = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {sources_path}: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(sources, list):
        print(f"Error: JSON must be an array of {{student, source}} objects", file=sys.stderr)
        sys.exit(1)

    # Get agents directory
    agents_dir = Path(__file__).parent.parent.parent / "agents"
    agents_dir.mkdir(exist_ok=True)

    # Import agents from each source
    total_imported = 0

    for item in sources:
        if not isinstance(item, dict) or "student" not in item or "source" not in item:
            print(f"Warning: Skipping invalid entry (missing student/source): {item}")
            continue

        student_name = item["student"]
        source = item["source"]

        print(f"\n[{student_name}] {source}")
        imported = import_agents_from_source(source, student_name, agents_dir, dry_run=args.dry_run)
        total_imported += imported

    # Summary
    print(f"\n{'='*60}")
    print(f"Collection complete!")
    print(f"  Total agents imported: {total_imported}")
    print(f"  Dry run: {args.dry_run}")
    if not args.dry_run:
        print(f"  Agents directory: {agents_dir}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
