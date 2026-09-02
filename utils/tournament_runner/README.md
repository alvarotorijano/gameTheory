# Tournament Runner

Execute a complete round-robin tournament with all discovered agents.

## Usage

Run from the project root directory:

```bash
python utils/tournament_runner/run_tournament.py --rounds N [OPTIONS]
```

## Options

- `--rounds N` — Rounds per match **(required)**
- `--unknown-horizon` — Agents don't know the round count (cannot plan strategy ahead)
- `--no-self-play` — Exclude self-play matches (agents only play different agents)
- `--output FILE` — Output CSV file (default: auto-generated with timestamp + flags)
- `--verbose` — Show progress information

## Examples

### Tournament with 100 rounds per match
```bash
python utils/tournament_runner/run_tournament.py --rounds 100
```

### Tournament with unknown horizon (agents don't know round count)
```bash
python utils/tournament_runner/run_tournament.py --rounds 100 --unknown-horizon
# Output: results/tournament_02092026-143120_rounds100_unknown-horizon.csv
```

### Tournament without self-play
```bash
python utils/tournament_runner/run_tournament.py --rounds 100 --no-self-play
# Output: results/tournament_02092026-143135_rounds100_no-self-play.csv
```

### Verbose output with multiple flags
```bash
python utils/tournament_runner/run_tournament.py --rounds 50 --unknown-horizon --no-self-play --verbose
# Output: results/tournament_02092026-143150_rounds50_unknown-horizon_no-self-play.csv
```

### Custom output filename
```bash
python utils/tournament_runner/run_tournament.py --rounds 100 --output results/my_tournament.csv
# Output: results/my_tournament.csv
```

## Output File

### Auto-Generated Filenames

By default, tournament results are saved with a timestamp and flags in the filename:

**Format:** `tournament_DDMMYYYY-HHMMSS_<flags>.csv`

**Examples:**
- `tournament_02092026-143052_rounds100.csv` — 100 rounds, known horizon, with self-play
- `tournament_02092026-143105_rounds50_unknown-horizon.csv` — 50 rounds, unknown horizon
- `tournament_02092026-143120_rounds100_no-self-play.csv` — 100 rounds, no self-play
- `tournament_02092026-143135_rounds50_unknown-horizon_no-self-play.csv` — All flags combined

This allows **multiple tournaments to run without overwriting** previous results.

### Custom Filename

To use a custom filename instead:
```bash
python utils/tournament_runner/run_tournament.py --rounds 100 --output results/my_custom_name.csv
```

## Output CSV

Generates a CSV with one row per agent per match (two rows per unique pairing: one for each agent's perspective).

**Columns:**

| Column | Type | Meaning |
|---|---|---|
| `pairing_id` | int | Unique identifier for this match |
| `num_rounds` | int | Rounds played in this match |
| `agent_name` | str | Agent this row describes |
| `opponent_name` | str | Opponent agent |
| `points_scored` | int | Points this agent earned |
| `opponent_points` | int | Points opponent earned |
| `first_move_cooperate` | bool | True if agent played "C" on round 1 |
| `total_cooperations` | int | Count of "C" moves |
| `total_defections` | int | Count of "D" moves |
| `cooperate_after_opponent_cooperate` | int | Times agent cooperated after opponent cooperated |
| `defect_after_opponent_cooperate` | int | Times agent defected after opponent cooperated |
| `cooperate_after_opponent_defect` | int | Times agent cooperated after opponent defected |
| `defect_after_opponent_defect` | int | Times agent defected after opponent defected |

## Example Output (CSV)

```
pairing_id,num_rounds,agent_name,opponent_name,points_scored,opponent_points,first_move_cooperate,total_cooperations,total_defections,...
0,100,random_agent,copycat_agent,150,250,true,51,49,...
0,100,copycat_agent,random_agent,250,150,true,99,1,...
1,100,copycat_agent,second_chance_agent,275,225,true,97,3,...
1,100,second_chance_agent,copycat_agent,225,275,true,96,4,...
```

## Analysis

After the tournament completes:

1. **Open the CSV in Excel or Google Sheets**
2. **Sort by `points_scored` (descending)** to see which agents scored most
3. **Filter by agent name** to see how that agent performed overall
4. **Compare statistics** (cooperation counts, conditional behavior) to understand strategy differences

## Discovering Agents

The tournament automatically discovers all agents in `agents/` folder. Each agent must:
- Be in a subfolder under `agents/`
- Contain a file named `agent.py`
- Define a class that inherits from `Agent`

Example structure:
```
agents/
├── random_agent/
│   ├── agent.py      (contains RandomAgent class)
│   └── README.md
├── copycat_agent/
│   ├── agent.py      (contains CopycatAgent class)
│   └── README.md
└── my_agent/
    ├── agent.py      (contains MyAgent class)
    └── README.md
```

## Performance Notes

- **With N agents and self-play:** N² total matches (each agent plays each other plus itself)
- **With N agents and no self-play:** N×(N-1)/2 total matches (each unique pairing once)
- With 3 agents: 9 matches (with self-play) or 3 matches (without)
- With 5 agents: 25 matches (with self-play) or 10 matches (without)
- With 10 agents: 100 matches (with self-play) or 45 matches (without)

Each match runs for `--rounds` iterations, so total computation time scales with N² or N×(N-1)/2.

## See Also

- `match_runner/` — Play two agents (useful for debugging)
- `agent_collector/` — Import student agents from repos
- `docs/game_rules.md` — Game mechanics
