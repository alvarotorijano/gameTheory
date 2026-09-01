# Implementation Plan: Iterated Prisoner's Dilemma Course Project

This document is a copy of the approved implementation plan for the Iterated Prisoner's Dilemma
course project. It serves as the blueprint for all code and tooling development.

---

## Context

This is a brand-new, empty repository (`gameTheory`, only `.git` exists) that will host a
teaching exercise for an ICAI course. Students each write their own strategy ("agent") for
the Iterated Prisoner's Dilemma, submit it (via git fork or a raw file), and the instructor
runs a round-robin tournament to score every agent against every other agent.

### Global Rules

- All code (identifiers, comments, docstrings, CLI/log output) is written in English.
- Claude must never perform git write operations (no commit/add/push) in this repo — the user
  handles all git operations.
- Every function/method must have a docstring.
- Always produce an implementation plan before writing code (this workflow itself).
- Everything runs locally; no external services.

---

## Folder Structure

```
gameTheory/
├── CLAUDE.md
├── README.md
├── config.json                  # payoff matrix + round-count settings, editable by instructor
├── requirements.txt              # pytest only; everything else is stdlib
├── .gitignore                    # results/, __pycache__, .venv, collected-repo cache, student source lists
├── agents/
│   ├── random_agent/{agent.py, README.md}
│   ├── copycat_agent/{agent.py, README.md}      # the "first code" template (tit-for-tat)
│   ├── second_chance_agent/{agent.py, README.md}
│   └── <students add one subfolder per agent here>
├── utils/
│   ├── game_core/                # shared library, not a standalone script
│   │   ├── moves.py              # COOPERATE = "C", DEFECT = "D"
│   │   ├── agent_base.py         # abstract Agent base class
│   │   ├── payoff.py             # loads config.json, scores one round
│   │   ├── engine.py             # runs one leg (a full match) between two agent instances
│   │   ├── agent_loader.py       # discovers agent subclasses under agents/ via AST scan
│   │   └── README.md
│   ├── match_runner/{run_match.py, README.md}          # agent vs agent, ida+vuelta+average
│   ├── tournament_runner/{run_tournament.py, README.md} # round robin -> CSV
│   └── agent_collector/{collect_agents.py, README.md}   # clone/copy student agents into agents/
├── docs/  (from documentation phase, plus this plan)
├── tests/
│   ├── test_game_core.py
│   ├── test_agents.py
│   ├── test_match_runner.py
│   ├── test_tournament_runner.py
│   ├── test_agent_collector.py
│   ├── run_tests.py              # convenience wrapper around pytest
│   └── README.md
└── results/                      # generated CSVs land here, gitignored
```

---

## Payoff Configuration (`config.json`)

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

`utils/game_core/payoff.py` loads this and scores a round from the two simultaneous moves.

---

## Agent Interface (`utils/game_core/agent_base.py`)

```python
class Agent(ABC):
    def __init__(self, num_rounds: Optional[int] = None): ...
    @abstractmethod
    def play(self, own_history: List[str], opponent_history: List[str]) -> str: ...
```

### Key Points

- `num_rounds` is the length told to the agent — it can be `None` ("unknown horizon"), even
  when the engine internally still runs a concrete number of rounds. When the CLI requests
  `--rounds unknown`, the engine privately picks a length from `rounds.unknown_horizon_min/max`
  in `config.json` and passes `num_rounds=None` to both agents.
- Moves are plain strings `"C"`/`"D"` (constants `COOPERATE`/`DEFECT`) — simplest for
  first-time students, no enum ceremony.
- Both agents' `play()` is called each round with only history (no access to the opponent's
  current-round move) — genuinely simultaneous, so there is no informational first-mover
  advantage. "Ida: A empieza primero / vuelta: B empieza primero" is implemented as which
  agent is recorded as *Player 1* for that leg (bookkeeping/labeling only, e.g., who appears
  first in the CSV and console output).

---

## Three Example Agents

### 1. `random_agent`
The default "fictitious adversary" for a student's first test run:
- Plays `random.choice([COOPERATE, DEFECT])` each round.

### 2. `copycat_agent`
The worked example students copy to write their first strategy (tit-for-tat):
- Cooperates on round 1.
- Then plays the opponent's previous move.

### 3. `second_chance_agent`
A stateful strategy matching the user's description exactly:
- Keeps an internal `defection_count`.
- Cooperates by default.
- Each time the opponent's last move was `D`, increments the counter.
- On reaching 2, it defects once and resets the counter to 0 (so the very next round it
  is back to forgiving).
- Net effect: a single defection is forgiven, a second defection triggers exactly one
  retaliatory defection, then it resets — "remembers only two plays back."
- Each agent's README will include a Mermaid state diagram of this exact logic for review.

---

## Match Runner (`utils/match_runner/run_match.py`)

**CLI:** `python run_match.py <agent_a> <agent_b> [--rounds N|unknown]`

Runs two legs:
- **Ida:** agent A as Player 1, agent B as Player 2.
- **Vuelta:** agent B as Player 1, agent A as Player 2.

**Output:** Prints ida score, vuelta score, and the per-agent average across both legs,
declaring whoever has the higher average.

---

## Tournament Runner (`utils/tournament_runner/run_tournament.py`)

Discovers every agent under `agents/` (via `agent_loader.py`, which AST-scans each `.py` file
for classes subclassing `Agent` — robust to non-standard file/folder names from student
submissions), then plays every ordered pairing as ida+vuelta (self-play included by default,
flag to exclude it), and writes one CSV row per `(agent, leg)`.

### CSV Schema

| Column | Meaning |
|---|---|
| `pairing_id` | Groups an ida+vuelta pair together |
| `leg` | `ida` / `vuelta` |
| `num_rounds` | Actual rounds played that leg |
| `agent_name` / `opponent_name` | Agent identifiers |
| `points_scored` / `opponent_points` | Points in that leg |
| `first_move_cooperate` | Boolean |
| `total_cooperations` / `total_defections` | Totals per agent per leg |
| `cooperate_after_opponent_defect` | Count |
| `defect_after_opponent_defect` | Count |
| `cooperate_after_opponent_cooperate` | Count |
| `defect_after_opponent_cooperate` | Count |

This covers every statistic the user listed (points per match, conditional cooperation/defection
counts in all four combinations, first-move flag, total cooperations/defections per player per
match).

---

## Agent Collector (`utils/agent_collector/collect_agents.py`)

**Input:** A JSON list of sources, e.g.
```json
[
  {"student": "juan_perez", "source": "https://github.com/.../pd-agent.git"},
  {"student": "maria_lopez", "source": "C:/entregas/maria_agent.py"}
]
```

### Behavior

For each entry:
- If `source` looks like a git URL, `git clone` it into a gitignored cache folder.
- If it's a local path (file or folder), use it directly — covers students who just hand in
  a loose `.py` file instead of a repo.
- AST-scans the result for every class subclassing `Agent`, **excluding** the three example
  agent files (matched by known example filenames/paths, so they're never re-copied), and
  copies each match into its own new folder under `agents/` (named
  `<student>_<original_filename>` to avoid collisions when one student submits multiple agents).

A template `sources_example.json` will be committed; the real per-cohort source list is
instructor data and goes in `.gitignore`.

---

## Tests (`tests/`)

`pytest`-based (added to `requirements.txt`), covering:
- Payoff scoring correctness.
- The three example agents' move sequences against scripted histories (especially the
  second-chance counter/reset state machine).
- Match runner's ida/vuelta/average computation.
- Tournament runner's CSV schema and values on a small fixture set of agents.
- Agent collector's discovery/copy logic against a fixture directory (git clone itself
  not exercised in unit tests — only the local-path branch and the AST-based discovery,
  to keep tests hermetic).

`tests/run_tests.py` is a thin wrapper that invokes `pytest` with a readable summary.

---

## Installation & Dependencies

### Requirements

Only dependency is `pytest` — everything else (`random`, `json`, `csv`, `argparse`, `ast`,
`subprocess`, `importlib`, `dataclasses`) is standard library.

### Guide Contents (in `docs/installation.md`)

- **Windows (pyenv-win):** Download, install, create venv, activate, install requirements.
- **Unix (pyenv):** Download, install, create venv, activate, install requirements.
- PowerShell and bash activation instructions.
- `pip install -r requirements.txt` summary.

---

## Verification (once implementation phase happens)

- `python tests/run_tests.py` (or `pytest`) green across all suites.
- Manual run: `python utils/match_runner/run_match.py copycat_agent random_agent --rounds 50`
  and eyeball the ida/vuelta/average output.
- Manual run: `python utils/tournament_runner/run_tournament.py` and inspect the generated CSV
  in `results/` for correct headers and plausible values (e.g., `copycat_agent` should show 0
  `defect_after_opponent_cooperate` against another always-cooperating strategy).
- `python utils/agent_collector/collect_agents.py --sources sources_example.json --dry-run`
  against a small fixture folder to confirm discovery/copy logic before ever pointing it at
  real student repos.
