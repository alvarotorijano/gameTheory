# Technical Requirements & Specifications

This document specifies the technical requirements and deliverables for the Iterated Prisoner's Dilemma project.

---

## Game Mechanics (Locked)

### Payoff Matrix
- Both cooperate: 3 points each
- Both defect: 1 point each
- Betrayed cooperator: 0 points
- Betrayer reward: 5 points
- **Configuration:** Externalized to `config.json` (values editable, structure fixed)

### Round Structure
- **Default rounds:** 100
- **Unknown horizon range:** 50–200 rounds (randomly chosen per match)
- **Configuration:** In `config.json` under `rounds` section

### Match Structure
- **Ida:** Agent A as Player 1, Agent B as Player 2
- **Vuelta:** Agent B as Player 1, Agent A as Player 2
- **Winner:** Agent with higher average score across both legs
- **Simultaneous moves:** Agents decide without knowing opponent's current-round move

### Tournament Structure
- **Round-robin:** Every agent plays every other agent (both orderings)
- **Self-play:** Included by default (optional flag to exclude)
- **Results:** One CSV row per `(agent, leg)` with detailed statistics

---

## Core Components to Implement

### 1. Game Core Library (`utils/game_core/`)

#### `moves.py`
- **COOPERATE** constant: `"C"`
- **DEFECT** constant: `"D"`

#### `agent_base.py`
Abstract base class:
```python
class Agent(ABC):
    def __init__(self, num_rounds: Optional[int] = None)
    @abstractmethod
    def play(self, own_history: List[str], opponent_history: List[str]) -> str
```
- Must be subclassed by all agents
- `play()` returns `"C"` or `"D"`
- `num_rounds` can be `None` (unknown horizon)

#### `payoff.py`
- Load `config.json` at module initialization
- Function: `score_round(move_a: str, move_b: str) -> Tuple[int, int]`
- Return points for both players based on payoff matrix

#### `engine.py`
- Function: `run_leg(agent_a: Agent, agent_b: Agent, num_rounds: int, verbose: bool = False) -> MatchResult`
- Execute one complete leg (full match) between two agents
- Track move histories and statistics
- Return `MatchResult` dataclass with:
  - `agent_a_name`, `agent_b_name`: Agent identifiers
  - `agent_a_score`, `agent_b_score`: Total points
  - `agent_a_history`, `agent_b_history`: Lists of moves (strings)
  - `num_rounds`: Rounds actually played
  - Statistics (cooperation counts, conditional cooperation/defection counts)

#### `agent_loader.py`
- Function: `discover_agents(agents_dir: str) -> Dict[str, Type[Agent]]`
- Use AST parsing to find all classes inheriting from `Agent`
- Return dictionary: agent name → agent class
- Robust to non-standard file/folder names

#### `README.md` (for game_core)
- Explain the library's purpose
- Document how to use the base Agent class
- Examples of payoff scoring

---

### 2. Example Agents (`agents/`)

Each agent in its own folder: `<agent_name>/agent.py` + `<agent_name>/README.md`

#### `random_agent/`
- **Strategy:** Play random move each round
- **Class name:** `RandomAgent` (or similar)
- **Purpose:** Baseline fictitious opponent for testing

#### `copycat_agent/`
- **Strategy:** Tit-for-tat (cooperate round 1, then copy opponent's last move)
- **Class name:** `CopycatAgent` (or similar)
- **Purpose:** Template for student assignments

#### `second_chance_agent/`
- **Strategy:**
  - Default: cooperate
  - Track opponent defections with internal counter
  - On 1st defection: forgive (cooperate next round)
  - On 2nd defection: retaliate once (defect), then reset counter
  - "Remembers" only the last two rounds conceptually
- **Class name:** `SecondChanceAgent` (or similar)
- **State:** Internal `defection_count` variable
- **README:** Include Mermaid state diagram

#### Agent README Requirements
Each agent's `README.md` must include:
- Strategy description
- Decision tree (Mermaid diagram)
- Rationale for the strategy

---

### 3. CLI Scripts

#### Match Runner (`utils/match_runner/run_match.py`)
**CLI:** `python run_match.py <agent_a> <agent_b> [--rounds N] [--unknown-horizon]`
- Run two agents in both legs (ida + vuelta)
- Display:
  - Ida: agent A score vs agent B score
  - Vuelta: agent B score vs agent A score
  - Average: (sum per agent) / 2 for each
  - Winner: agent with higher average
- **Default rounds:** From `config.json['rounds']['default']`
- **Unknown horizon:** Randomly pick rounds from config range, pass `num_rounds=None` to agents

**README.md:** Include usage examples

#### Tournament Runner (`utils/tournament_runner/run_tournament.py`)
**CLI:** `python run_tournament.py [--rounds N] [--unknown-horizon] [--no-self-play] [--output PATH]`
- Discover all agents under `agents/` using `agent_loader.py`
- Play every ordered pair (both ida and vuelta)
- Output CSV to `results/tournament.csv` (or custom path)
- **Default:** Include self-play; `--no-self-play` to exclude

**CSV Schema** (one row per agent per leg):
| Column | Type | Notes |
|---|---|---|
| `pairing_id` | string | Unique ID for this (A, B) pair |
| `leg` | string | `"ida"` or `"vuelta"` |
| `num_rounds` | int | Rounds actually played |
| `agent_name` | string | Agent this row describes |
| `opponent_name` | string | Opponent agent |
| `points_scored` | int | Points for this agent |
| `opponent_points` | int | Points for opponent |
| `first_move_cooperate` | bool | `true` if round 1 was "C" |
| `total_cooperations` | int | Count of "C" moves |
| `total_defections` | int | Count of "D" moves |
| `cooperate_after_opponent_defect` | int | Conditional count |
| `defect_after_opponent_defect` | int | Conditional count |
| `cooperate_after_opponent_cooperate` | int | Conditional count |
| `defect_after_opponent_cooperate` | int | Conditional count |

**README.md:** Include usage examples, output interpretation

#### Agent Collector (`utils/agent_collector/collect_agents.py`)
**CLI:** `python collect_agents.py --sources sources.json [--dry-run]`
- Input: JSON file with student submissions
- For each source:
  - If git URL: clone to `._cache/` (gitignored)
  - If local path: use directly
- AST-scan for `Agent` subclasses
- Exclude the three example agents (by known names)
- Copy new agents to `agents/<student>_<filename>/`
- If `--dry-run`: print without copying

**Input Format** (`sources.json`):
```json
[
  {"student": "name", "source": "https://github.com/...git"},
  {"student": "name", "source": "/local/path/file.py"}
]
```

**Template:** `sources_example.json` (committed to repo; per-cohort list goes in `.gitignore`)

**README.md:** Include usage examples, source format explanation

---

### 4. Test Suite (`tests/`)

Use `pytest`. All tests must pass before implementation is considered complete.

#### `test_game_core.py`
- Payoff scoring: verify all four cases (both cooperate, both defect, betrayal)
- Engine: verify single leg execution, move recording, score calculation
- Agent base: verify instantiation, abstract method requirement

#### `test_agents.py`
- **RandomAgent:** verify non-zero cooperations and defections (statistical test)
- **CopycatAgent:** verify tit-for-tat behavior against scripted histories
- **SecondChanceAgent:** verify defection counter logic and reset behavior

#### `test_match_runner.py`
- Verify ida/vuelta/average calculations
- Verify winner determination
- Verify output formatting

#### `test_tournament_runner.py`
- Verify CSV headers and schema
- Verify CSV values for small fixture set
- Verify pairing_id grouping (ida/vuelta pairs)

#### `test_agent_collector.py`
- Verify agent discovery (AST-based)
- Verify exclusion of example agents
- Verify file copying logic
- Note: Git clone not tested (local-path branch only)

#### `run_tests.py`
- Thin wrapper around `pytest` with readable summary
- Invoke with `python tests/run_tests.py`

#### `README.md` (for tests)
- Testing strategy and coverage
- How to run tests
- Common test failures and fixes

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

**Constraints:**
- Structure is fixed (keys must match exactly)
- Values are editable by instructors
- Loaded by `utils/game_core/payoff.py` at module init

---

## Dependencies

**Only external dependency:** `pytest` (in `requirements.txt`)

**Standard library only:**
- `random` — random choice
- `json` — config loading
- `csv` — tournament output
- `argparse` — CLI parsing
- `ast` — agent discovery
- `subprocess` — git clone in agent_collector
- `importlib` — dynamic loading
- `dataclasses` — MatchResult, etc.
- `abc` — abstract base class

---

## Folder Structure (Final)

```
gameTheory/
├── CLAUDE.md
├── README.md
├── config.json
├── requirements.txt
├── .gitignore
├── agents/
│   ├── random_agent/
│   │   ├── agent.py
│   │   └── README.md
│   ├── copycat_agent/
│   │   ├── agent.py
│   │   └── README.md
│   └── second_chance_agent/
│       ├── agent.py
│       └── README.md
├── utils/
│   ├── game_core/
│   │   ├── __init__.py
│   │   ├── moves.py
│   │   ├── agent_base.py
│   │   ├── payoff.py
│   │   ├── engine.py
│   │   ├── agent_loader.py
│   │   └── README.md
│   ├── match_runner/
│   │   ├── run_match.py
│   │   └── README.md
│   ├── tournament_runner/
│   │   ├── run_tournament.py
│   │   └── README.md
│   └── agent_collector/
│       ├── collect_agents.py
│       └── README.md
├── docs/
│   ├── README.md
│   ├── original_prompt.md
│   ├── implementation_plan.md
│   ├── game_rules.md
│   ├── architecture.md
│   ├── student_guide.md
│   ├── installation.md
│   ├── requirements.md (this file)
│   ├── CLAUDE.md (or equivalent)
│   └── prompts.md
├── tests/
│   ├── __init__.py
│   ├── test_game_core.py
│   ├── test_agents.py
│   ├── test_match_runner.py
│   ├── test_tournament_runner.py
│   ├── test_agent_collector.py
│   ├── run_tests.py
│   └── README.md
└── results/ (empty, gitignored)
```

---

## Verification Steps (Post-Implementation)

- [ ] `python tests/run_tests.py` passes all tests
- [ ] `python utils/match_runner/run_match.py copycat_agent random_agent --rounds 50` runs without error
- [ ] CSV from tournament_runner has correct headers and plausible values
- [ ] Agent discovery correctly identifies all agents under `agents/`
- [ ] `--unknown-horizon` flag works (agents see `num_rounds=None`)
- [ ] Ida/vuelta pairs are correctly labeled in CSV (`pairing_id` groups them)

---

## Notes

- All code must be in English (see `CLAUDE.md` for project rules).
- Every function must have a docstring.
- No local/absolute machine paths in any file (use relative paths only).
- Project must be portable (works on any machine without modification).
