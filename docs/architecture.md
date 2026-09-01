# Architecture & Technical Design

## Folder Layout

```
gameTheory/
├── CLAUDE.md                     # Project rules and constraints
├── README.md                     # Overview, quick start, usage examples
├── config.json                   # Payoff matrix and round-count settings
├── requirements.txt              # Python dependencies (pytest only)
├── .gitignore                    # Excludes results/, .venv, cache, student source lists
├── agents/
│   ├── random_agent/
│   │   ├── agent.py              # RandomAgent class implementation
│   │   └── README.md             # Decision tree (Mermaid diagram)
│   ├── copycat_agent/
│   │   ├── agent.py              # CopycatAgent (tit-for-tat) implementation
│   │   └── README.md             # Decision tree (Mermaid diagram)
│   ├── second_chance_agent/
│   │   ├── agent.py              # SecondChanceAgent implementation
│   │   └── README.md             # Decision tree (Mermaid diagram)
│   └── <student_agents>/         # Students add folders here
├── utils/
│   ├── game_core/                # Shared game engine library
│   │   ├── __init__.py
│   │   ├── moves.py              # COOPERATE, DEFECT constants
│   │   ├── agent_base.py         # Abstract Agent base class
│   │   ├── payoff.py             # Loads config.json, scores rounds
│   │   ├── engine.py             # Runs a single leg (match) between agents
│   │   ├── agent_loader.py       # AST-based discovery of Agent subclasses
│   │   └── README.md             # Library documentation
│   ├── match_runner/
│   │   ├── run_match.py          # CLI: play two agents (ida + vuelta)
│   │   └── README.md             # Usage examples
│   ├── tournament_runner/
│   │   ├── run_tournament.py     # CLI: round-robin all agents -> CSV
│   │   └── README.md             # Usage examples
│   └── agent_collector/
│       ├── collect_agents.py     # CLI: import student agents from repos/files
│       └── README.md             # Usage examples
├── docs/
│   ├── original_prompt.md        # Original user prompt (Spanish)
│   ├── implementation_plan.md    # This project's development plan
│   ├── game_rules.md             # Game mechanics and scoring
│   ├── architecture.md           # This file
│   ├── student_guide.md          # Step-by-step: how to write your first agent
│   └── installation.md           # Python environment setup (pyenv, venv)
├── tests/
│   ├── __init__.py
│   ├── test_game_core.py         # Tests for payoff, engine, agent_base
│   ├── test_agents.py            # Tests for the three example agents
│   ├── test_match_runner.py      # Tests for match output and averaging
│   ├── test_tournament_runner.py # Tests for tournament CSV logic
│   ├── test_agent_collector.py   # Tests for agent discovery and import
│   ├── run_tests.py              # Convenience pytest wrapper
│   └── README.md                 # Testing documentation
└── results/                      # Generated tournament CSVs (gitignored)
```

---

## Core Components

### 1. `utils/game_core/` — Shared Library

This folder contains the **game engine** and **interfaces** that everything else depends on.
It is **not** a standalone script.

#### `moves.py`
Defines move constants for clarity:
```python
COOPERATE = "C"
DEFECT = "D"
```

#### `agent_base.py`
Defines the **abstract base class** that all agents must inherit from:

```python
from abc import ABC, abstractmethod
from typing import List, Optional

class Agent(ABC):
    """
    Abstract base class for all Prisoner's Dilemma agents.
    """

    def __init__(self, num_rounds: Optional[int] = None):
        """
        Initialize the agent.
        
        Parameters:
            num_rounds: Number of rounds this agent will play.
                       None if the horizon is unknown (random rounds in a configured range).
        """
        self.num_rounds = num_rounds

    @abstractmethod
    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        """
        Decide the agent's move for this round.
        
        Parameters:
            own_history: List of this agent's moves in all prior rounds.
                        Empty list on round 1.
            opponent_history: List of the opponent's moves in all prior rounds.
                             Empty list on round 1.
        
        Returns:
            A single move: "C" (cooperate) or "D" (defect).
        """
        pass
```

**Students write agents by**:
1. Subclassing `Agent`.
2. Implementing the `play()` method.

#### `payoff.py`
Loads `config.json` at initialization and provides a function to score a single round:

```python
def score_round(move_a: str, move_b: str) -> Tuple[int, int]:
    """
    Score one round of the Prisoner's Dilemma given both players' moves.
    
    Parameters:
        move_a: Move by player A ("C" or "D").
        move_b: Move by player B ("C" or "D").
    
    Returns:
        Tuple of (points_for_a, points_for_b).
    """
```

#### `engine.py`
The **match engine**: orchestrates one complete leg (ida or vuelta) between two agent instances.

```python
def run_leg(
    agent_a: Agent,
    agent_b: Agent,
    num_rounds: int,
    verbose: bool = False
) -> MatchResult:
    """
    Run a single leg of the match.
    
    Parameters:
        agent_a: First agent (Player 1).
        agent_b: Second agent (Player 2).
        num_rounds: Number of rounds to play.
        verbose: Whether to print each round's result.
    
    Returns:
        MatchResult containing scores, histories, and statistics.
    """
```

`MatchResult` is a dataclass containing:
- `agent_a_name`, `agent_b_name`: Agent identifiers.
- `agent_a_score`, `agent_b_score`: Total points.
- `agent_a_history`, `agent_b_history`: Lists of moves.
- `num_rounds`: Rounds actually played.
- Statistics (cooperation counts, conditional counts).

#### `agent_loader.py`
Uses Python's `ast` module to **discover all Agent subclasses** in the `agents/` folder:

```python
def discover_agents(agents_dir: str) -> Dict[str, Type[Agent]]:
    """
    Discover all Agent subclasses in the agents directory.
    
    Parameters:
        agents_dir: Path to the agents folder.
    
    Returns:
        Dictionary mapping agent names (e.g., "random_agent") to Agent classes.
    """
```

**Why AST?** AST parsing is robust to:
- Non-standard file/folder names (students might name things oddly).
- Multiple agents in one file or folder.
- Student code that doesn't follow conventions.

It scans for any class that inherits from `Agent`, no matter where it's defined.

---

### 2. `utils/match_runner/` — CLI Script

**Purpose:** Play one match (ida + vuelta) between two agents and show results.

**Usage:**
```bash
python run_match.py <agent_a> <agent_b> [--rounds N] [--unknown-horizon]
```

**Example:**
```bash
python run_match.py copycat_agent random_agent --rounds 50
```

**Output:**
```
Ida (copycat_agent vs random_agent):
  copycat_agent: 123 points
  random_agent: 87 points

Vuelta (random_agent vs copycat_agent):
  random_agent: 95 points
  copycat_agent: 110 points

Average:
  copycat_agent: 116.5 points (WINNER)
  random_agent: 91.0 points
```

---

### 3. `utils/tournament_runner/` — CLI Script

**Purpose:** Discover all agents and play a round-robin tournament, output CSV.

**Usage:**
```bash
python run_tournament.py [--rounds N] [--unknown-horizon] [--no-self-play] [--output results/tournament.csv]
```

**Logic:**
1. Discover all agents under `agents/` using `agent_loader.py`.
2. For each ordered pair (A, B):
   - Run Ida (A vs B).
   - Run Vuelta (B vs A).
   - Record all statistics.
3. Write a CSV to `results/` (or user-specified output).

**CSV Schema:** (one row per `(agent, leg)`)

| Column | Type | Notes |
|---|---|---|
| `pairing_id` | string | Unique ID for this (A, B) pair |
| `leg` | string | `"ida"` or `"vuelta"` |
| `num_rounds` | int | Rounds actually played |
| `agent_name` | string | Name of the agent this row describes |
| `opponent_name` | string | Name of the opponent |
| `points_scored` | int | Points this agent scored |
| `opponent_points` | int | Points the opponent scored |
| `first_move_cooperate` | bool | True if agent played "C" in round 1 |
| `total_cooperations` | int | Total "C" moves across all rounds |
| `total_defections` | int | Total "D" moves across all rounds |
| `cooperate_after_opponent_defect` | int | Count of "C" after opponent played "D" |
| `defect_after_opponent_defect` | int | Count of "D" after opponent played "D" |
| `cooperate_after_opponent_cooperate` | int | Count of "C" after opponent played "C" |
| `defect_after_opponent_cooperate` | int | Count of "D" after opponent played "C" |

---

### 4. `utils/agent_collector/` — CLI Script

**Purpose:** Import student agents from repos or loose files into the local `agents/` folder.

**Usage:**
```bash
python collect_agents.py --sources sources.json [--dry-run]
```

**Input Format** (`sources.json`):
```json
[
  {
    "student": "juan_perez",
    "source": "https://github.com/juan_perez/pd-agent.git"
  },
  {
    "student": "maria_lopez",
    "source": "/home/professor/submissions/maria_agent.py"
  }
]
```

**Behavior:**
1. For each source:
   - If it's a git URL, clone into a gitignored cache (`._cache/`).
   - If it's a local path, use it directly.
2. AST-scan the result for all `Agent` subclasses.
3. **Exclude** the three example agents by name (matched against known example filenames).
4. Copy each discovered agent to a new folder under `agents/`:
   - Folder name: `<student>_<original_filename>` (e.g., `juan_perez_strategy.py` from
     `strategy.py` in Juan's repo).
   - Avoids collisions if a student submits multiple agents.
5. If `--dry-run`, print what *would* be imported without actually copying.

**Template** (`sources_example.json`) is committed to the repo for reference; the real
per-cohort list is instructor data and goes in `.gitignore`.

---

## Agent Naming Convention

Agents are discovered by their **class name** (lowercased and underscored) or by folder name
(if it's the only agent in that folder):

- Folder `random_agent/` containing a class `RandomAgent` → agent name: `random_agent`.
- Folder `student_pedro_agent/` containing a class `PedroStrategy` → agent name: `student_pedro_agent`.

For CLI purposes, you refer to agents by **folder name** (which becomes the `agent_name` in CSVs).

---

## Configuration (`config.json`)

```json
{
  "payoff": {
    "both_cooperate": 3,
    "both_defect": 1,
    "betrayed_cooperator": 0,
    "betrayer_reward": 5
  },
  "rounds": {
    "default": 100,
    "unknown_horizon_min": 50,
    "unknown_horizon_max": 200
  }
}
```

- **Payoffs:** All scoring values. Instructors can adjust these to explore different game dynamics.
- **Rounds:**
  - `default`: Used if no `--rounds` flag is passed to match_runner or tournament_runner.
  - `unknown_horizon_min/max`: The range from which a random number of rounds is chosen when
    `--unknown-horizon` is passed (agents see `num_rounds=None`).

---

## Testing Strategy

Tests are in `tests/` and use `pytest`:

- **`test_game_core.py`:** Tests for payoff scoring, engine execution, and base class behavior.
- **`test_agents.py`:** Tests for each of the three example agents, verifying their move sequences
  against scripted opponent histories.
- **`test_match_runner.py`:** Tests the CLI and output formatting (ida/vuelta/average).
- **`test_tournament_runner.py`:** Tests CSV generation, column headers, and value correctness
  against a small fixture set.
- **`test_agent_collector.py`:** Tests AST-based discovery and file-copy logic (git clone
  not exercised in tests to keep them hermetic).

`tests/run_tests.py` wraps `pytest` for easy invocation.

---

## Dependencies

**Only one external dependency:** `pytest` (for testing).

Everything else uses Python standard library:
- `random` — random choice for random_agent.
- `json` — load config.json.
- `csv` — write tournament results.
- `argparse` — CLI argument parsing.
- `ast` — agent discovery.
- `subprocess` — git clone in agent_collector.
- `importlib` — dynamic agent loading.
- `dataclasses` — MatchResult and other data structures.

---

## Deployment & Instructor Workflow

1. **Setup:** Instructor runs `python -m venv .venv && pip install -r requirements.txt`.
2. **Per Cohort:**
   - Prepare a `sources.json` with student submission URLs/paths.
   - Run `python utils/agent_collector/collect_agents.py --sources sources.json`.
   - Run `python utils/tournament_runner/run_tournament.py`.
   - Results CSV appears in `results/`.
   - Open CSV in Excel or Google Sheets to inspect agent performance.
3. **Optional:** Run `python utils/match_runner/run_match.py <agent1> <agent2>` to debug
   individual matchups.
