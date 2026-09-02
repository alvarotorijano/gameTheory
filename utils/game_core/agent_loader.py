"""
Agent discovery and loading using AST parsing.

Scans agent files to find all classes that inherit from Agent.
"""

import ast
import importlib.util
from pathlib import Path
from typing import Dict, Type

# ANSI color codes
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

from .agent_base import Agent


def discover_agents(agents_dir: str | Path) -> Dict[str, Type[Agent]]:
    """
    Discover all Agent subclasses in the agents directory.

    Uses AST parsing to find classes that inherit from Agent, then dynamically
    loads them. Robust to non-standard file/folder names and multiple agents per file.

    Parameters:
        agents_dir: Path to the agents directory.

    Returns:
        Dictionary mapping agent names (folder/file-based) to Agent classes.
        Agent name is derived from folder name or file name (whichever is used).
    """
    agents_dir = Path(agents_dir)
    agents = {}

    if not agents_dir.exists():
        return agents

    for agent_folder in agents_dir.iterdir():
        if not agent_folder.is_dir():
            continue

        agent_py = agent_folder / "agent.py"
        if not agent_py.exists():
            continue

        agent_name = agent_folder.name

        try:
            found_classes = _find_agent_classes_in_file(agent_py)
            if found_classes:
                loaded_class = _load_agent_class(agent_py, found_classes[0])
                if loaded_class:
                    agents[agent_name] = loaded_class
        except Exception as e:
            print(f"{YELLOW}Warning: Failed to load agent from {agent_folder}: {e}{RESET}")

    return agents


def _find_agent_classes_in_file(file_path: Path) -> list[str]:
    """
    Parse a Python file and find all class names that inherit from Agent.

    Parameters:
        file_path: Path to the Python file to parse.

    Returns:
        List of class names that inherit from Agent.
    """
    class_names = []

    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    base_name = None
                    if isinstance(base, ast.Name):
                        base_name = base.id
                    elif isinstance(base, ast.Attribute):
                        base_name = base.attr

                    if base_name == "Agent":
                        class_names.append(node.name)
                        break
    except SyntaxError as e:
        print(f"{RED}Syntax error in {file_path}: {e}{RESET}")

    return class_names


def _load_agent_class(file_path: Path, class_name: str) -> Type[Agent] | None:
    """
    Dynamically load an Agent class from a Python file.

    Parameters:
        file_path: Path to the Python file.
        class_name: Name of the class to load.

    Returns:
        The Agent class, or None if loading failed.
    """
    try:
        spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
        if spec is None or spec.loader is None:
            return None

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        agent_class = getattr(module, class_name)
        if issubclass(agent_class, Agent):
            return agent_class
    except Exception as e:
        print(f"{RED}Failed to load {class_name} from {file_path}: {e}{RESET}")

    return None
