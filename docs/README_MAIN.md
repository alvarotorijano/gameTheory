# Iterated Prisoner's Dilemma: Course Project

Welcome to the Iterated Prisoner's Dilemma tournament platform! This project is designed as a
teaching tool where students implement their own strategies for the classic game theory problem
and compete against each other.

---

## Project Overview

The **Iterated Prisoner's Dilemma** is a two-player game where each player repeatedly chooses
to either **cooperate** or **defect**. Based on both players' simultaneous choices, they
receive points according to this payoff matrix:

| Both Players | Payoff |
|---|---|
| Both Cooperate | 3 points each |
| Both Defect | 1 point each |
| One Cooperates, One Defects | Cooperator: 0, Defector: 5 |

The challenge: **What strategy maximizes your score without knowing what your opponent will do?**

---

## Quick Start

### 1. Install Dependencies

See [`installation.md`](installation.md) for detailed instructions. Quick version:

```bash
python -m venv .venv

# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# macOS/Linux:
source .venv/bin/activate

# Install dependencies:
pip install -r requirements.txt
```

### 2. Run a Single Match

Test the example agents against each other:

```bash
python utils/match_runner/run_match.py copycat_agent random_agent --rounds 50
```

**Output:**
```
First Leg (copycat_agent vs random_agent):
  copycat_agent: 145 points
  random_agent: 68 points

Second Leg (random_agent vs copycat_agent):
  random_agent: 72 points
  copycat_agent: 143 points

Average:
  copycat_agent: 144.0 points (WINNER)
  random_agent: 70.0 points
```

### 3. Run the Full Tournament

Discover all agents and play every matchup:

```bash
python utils/tournament_runner/run_tournament.py
```

Results are saved to `results/tournament.csv`. Open it in Excel or a spreadsheet viewer to
analyze performance.

### 4. Write Your First Agent

See [`student_guide.md`](student_guide.md) for a step-by-step walkthrough:

1. Copy `agents/copycat_agent/` to `agents/my_strategy/`.
2. Edit `agent.py` to implement your logic.
3. Test: `python utils/match_runner/run_match.py my_strategy random_agent --rounds 50`
4. Update `README.md` with your strategy description.

---

## How the Game Works

### Simultaneous Moves

Each round, both agents decide their move **without knowing** what the opponent will do:

1. Agent A's `play()` is called.
2. Agent B's `play()` is called.
3. Both moves are revealed simultaneously.
4. Points are awarded.
5. History is updated for the next round.

### First Leg and Second Leg (Two Legs)

A complete match consists of **two legs** to ensure fairness:

- **First Leg:** Agent A plays first (is designated "Player 1"), Agent B is "Player 2".
- **Second Leg:** Roles reverse — Agent B is "Player 1", Agent A is "Player 2".

Both legs use the same number of rounds. The **average score** across both legs determines
the match winner.

### Tournament Structure

The tournament runner plays **every agent against every other agent**, both orderings:
- With *n* agents, there are *n²* matches (including self-play by default).
- Each match includes both ida and vuelta, so *2n²* total legs.
- Results are recorded in a CSV with detailed statistics per agent per leg.

---

## Available Scripts

### Match Runner (`utils/match_runner/run_match.py`)

Play two agents against each other and see the result (ida + vuelta + average).

**Usage:**
```bash
python utils/match_runner/run_match.py <agent_a> <agent_b> [--rounds N] [--unknown-horizon]
```

**Examples:**
```bash
# Play copycat against random, 50 rounds
python utils/match_runner/run_match.py copycat_agent random_agent --rounds 50

# Play with unknown horizon (random rounds, agent doesn't know the count)
python utils/match_runner/run_match.py copycat_agent random_agent --unknown-horizon

# Use default 100 rounds
python utils/match_runner/run_match.py copycat_agent random_agent
```

**Output:** First Leg score, Second Leg score, averages, and the winner.

---

### Tournament Runner (`utils/tournament_runner/run_tournament.py`)

Discover all agents and run a complete round-robin tournament, output CSV.

**Usage:**
```bash
python utils/tournament_runner/run_tournament.py [--rounds N] [--unknown-horizon] [--no-self-play] [--output PATH]
```

**Examples:**
```bash
# Run tournament with default 100 rounds
python utils/tournament_runner/run_tournament.py

# Run tournament with 50 rounds per match
python utils/tournament_runner/run_tournament.py --rounds 50

# Exclude self-play (agents only play different agents)
python utils/tournament_runner/run_tournament.py --no-self-play

# Custom output file
python utils/tournament_runner/run_tournament.py --output results/my_tournament.csv
```

**Output:** A CSV file (`results/tournament.csv` by default) with one row per `(agent, leg)`.

**CSV Columns:**
- `pairing_id`, `leg`, `num_rounds`
- `agent_name`, `opponent_name`, `points_scored`, `opponent_points`
- `first_move_cooperate`
- `total_cooperations`, `total_defections`
- `cooperate_after_opponent_defect`, `defect_after_opponent_defect`
- `cooperate_after_opponent_cooperate`, `defect_after_opponent_cooperate`

---

### Agent Collector (`utils/agent_collector/collect_agents.py`)

Import student agents from GitHub repos or local files.

**Usage:**
```bash
python utils/agent_collector/collect_agents.py --sources sources.json [--dry-run]
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
    "source": "./submissions/maria_agent.py"
  }
]
```

**Behavior:**
- Clones git repos or uses local paths.
- Discovers all `Agent` subclasses (excluding the three examples).
- Copies each agent to a new folder under `agents/`.
- Renames to avoid collisions: `<student>_<filename>` if multiple agents per student.
- `--dry-run` shows what would be imported without actually copying.

A template `sources_example.json` is provided for reference.

---

## Example Agents

Three example agents are provided in the `agents/` folder:

### `random_agent`
Plays a random move each round. The baseline "fictitious opponent" for testing your strategy.

### `copycat_agent`
Classic tit-for-tat: cooperate on round 1, then play the opponent's last move.

### `second_chance_agent`
More sophisticated: forgives a single defection but retaliates if the opponent defects twice.
See `agents/second_chance_agent/README.md` for details.

---

## Configuration

Game parameters are stored in `config.json`:

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

- **Payoff values:** Instructors can adjust these to explore different game dynamics.
- **Round counts:**
  - `default`: Used if no `--rounds` flag is passed.
  - `unknown_horizon_min/max`: Range for random round counts (when `--unknown-horizon` is used).

---

## Testing

Run all tests to verify the system:

```bash
python tests/run_tests.py
```

Or with pytest directly:

```bash
pytest tests/ -v
```

Tests cover:
- Payoff scoring.
- Example agents' behavior.
- Match runner output.
- Tournament CSV generation.
- Agent discovery and import logic.

---

## Project Structure

```
gameTheory/
├── config.json                            # Game parameters (editable)
├── requirements.txt                       # Python dependencies (pytest only)
├── agents/                                # Agent implementations
│   ├── random_agent/
│   ├── copycat_agent/
│   ├── second_chance_agent/
│   └── <your_agent>/
├── utils/
│   ├── game_core/                         # Game engine and interfaces
│   ├── match_runner/                      # CLI: play two agents
│   ├── tournament_runner/                 # CLI: round-robin all agents
│   └── agent_collector/                   # CLI: import student agents
├── docs/
│   ├── README_MAIN.md                     # This file (main project overview)
│   ├── CLAUDE.md                          # Project constraints and rules
│   ├── requirements.md                    # Technical specifications
│   ├── prompts.md                         # User prompts (historical record)
│   ├── game_rules.md                      # Game mechanics and scoring
│   ├── architecture.md                    # Technical design
│   ├── student_guide.md                   # How to write an agent
│   ├── installation.md                    # Setup instructions
│   └── implementation_plan.md             # Development plan
├── tests/                                 # Unit tests (pytest)
│   ├── run_tests.py                       # Convenience wrapper
│   ├── test_game_core.py
│   ├── test_agents.py
│   ├── test_match_runner.py
│   ├── test_tournament_runner.py
│   └── test_agent_collector.py
└── results/                               # Generated CSVs (gitignored)
```

---

## Documentation

- **[Game Rules](game_rules.md)** — Detailed rules, payoff matrix, ida/vuelta structure.
- **[Architecture](architecture.md)** — Technical design, folder layout, component descriptions.
- **[Student Guide](student_guide.md)** — Step-by-step: write and test your first agent.
- **[Installation](installation.md)** — Python setup, virtual environments, pyenv (optional).
- **[Technical Requirements](requirements.md)** — What needs to be implemented.
- **[Project Rules](CLAUDE.md)** — Constraints, style guidelines, best practices.
- **[User Prompts](prompts.md)** — Historical record of all project instructions.

---

## Common Workflows

### As a Student

1. Follow [Student Guide](student_guide.md) to implement your agent.
2. Test locally: `python utils/match_runner/run_match.py my_agent random_agent --rounds 50`
3. Push your agent to GitHub or give the file to the instructor.

### As an Instructor

1. Collect student submissions via `collect_agents.py` (GitHub links or files).
2. Run tournament: `python utils/tournament_runner/run_tournament.py`
3. Open the CSV in Excel to analyze results.
4. (Optional) Debug individual matchups: `python utils/match_runner/run_match.py agent1 agent2 --rounds 100`

---

## Troubleshooting

**"ModuleNotFoundError: No module named utils"**
- Make sure you're running scripts from the project root directory.
- Check that `utils/` exists and contains `__init__.py` files.

**"Agent not found"**
- Verify the agent folder exists under `agents/`.
- Check the class name matches the folder name (lowercased, underscored).
- Run `python utils/tournament_runner/run_tournament.py --dry-run` (if implemented) to list discovered agents.

**Tests failing**
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version: `python --version` (3.7+ required).

---

## Questions or Issues?

Refer to:
- [`student_guide.md`](student_guide.md) — to write your first agent.
- [`game_rules.md`](game_rules.md) — to understand the game.
- [`architecture.md`](architecture.md) — for technical details.
- [`CLAUDE.md`](CLAUDE.md) — for project rules and constraints.
- Individual script READMEs in `utils/*/` for usage examples.

Good luck with your strategies!
