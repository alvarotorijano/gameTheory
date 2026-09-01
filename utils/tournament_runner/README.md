# Tournament Runner

Execute a complete round-robin tournament with all discovered agents.

## Usage

```bash
python run_tournament.py [OPTIONS]
```

## Options

- `--rounds N` — Rounds per leg (default: 100 from config.json)
- `--unknown-horizon` — Use unknown horizon (random rounds per leg)
- `--no-self-play` — Exclude self-play matches
- `--output FILE` — Output CSV file (default: `results/tournament.csv`)
- `--verbose` — Show progress information

## Examples

### Default Tournament (100 rounds, all agents)
```bash
python run_tournament.py
```

### Custom Rounds
```bash
python run_tournament.py --rounds 50
```

### Unknown Horizon
```bash
python run_tournament.py --unknown-horizon
```

### No Self-Play (agents don't play themselves)
```bash
python run_tournament.py --no-self-play
```

### Verbose Output (see progress)
```bash
python run_tournament.py --verbose
```

### Custom Output File
```bash
python run_tournament.py --output results/tournament_custom.csv
```

## Output CSV

Generates a CSV with one row per agent per leg (ida/vuelta).

**Columns:**

| Column | Type | Meaning |
|---|---|---|
| `pairing_id` | int | Groups ida+vuelta pairs together |
| `leg` | str | `"ida"` or `"vuelta"` |
| `num_rounds` | int | Rounds played that leg |
| `agent_name` | str | Agent this row describes |
| `opponent_name` | str | Opponent agent |
| `points_scored` | int | Points this agent earned |
| `opponent_points` | int | Points opponent earned |
| `first_move_cooperate` | bool | True if agent played "C" on round 1 |
| `total_cooperations` | int | Count of "C" moves |
| `total_defections` | int | Count of "D" moves |
| `cooperate_after_opponent_cooperate` | int | Conditional count |
| `defect_after_opponent_cooperate` | int | Conditional count |
| `cooperate_after_opponent_defect` | int | Conditional count |
| `defect_after_opponent_defect` | int | Conditional count |

## Example Output (CSV)

```
pairing_id,leg,num_rounds,agent_name,opponent_name,points_scored,opponent_points,first_move_cooperate,total_cooperations,total_defections,...
0,ida,100,random_agent,copycat_agent,150,250,true,51,49,...
0,ida,100,copycat_agent,random_agent,250,150,true,99,1,...
0,vuelta,100,copycat_agent,random_agent,240,160,true,98,2,...
0,vuelta,100,random_agent,copycat_agent,160,240,false,48,52,...
```

## Analysis

After the tournament completes:

1. **Open the CSV in Excel or Google Sheets**
2. **Sort by `points_scored` (descending)** to see which agents scored most
3. **Filter by agent name** to see how that agent performed overall
4. **Compare statistics** (cooperation counts, conditional behavior) to understand strategy differences

### Sample Analysis Query (SQL-like)

```
SELECT agent_name, AVG(points_scored) as avg_score, COUNT(*) as matches
GROUP BY agent_name
ORDER BY avg_score DESC
```

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

- **With N agents:** N² × 2 total legs (each agent plays each other in both directions)
- With 3 agents: 18 legs total
- With 5 agents: 50 legs total
- With 10 agents: 200 legs total

Each leg runs for `--rounds` iterations (default 100), so total computation time scales quickly.

## See Also

- `match_runner/` — Play two agents (useful for debugging)
- `agent_collector/` — Import student agents from repos
- `docs/game_rules.md` — Game mechanics
