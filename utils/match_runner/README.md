# Match Runner

Play two agents against each other in the Iterated Prisoner's Dilemma (ida + vuelta).

## Usage

```bash
python run_match.py <agent_a> <agent_b> [OPTIONS]
```

## Options

- `--rounds N` — Number of rounds per leg (default: 100 from config.json)
- `--unknown-horizon` — Use unknown horizon (agents see `num_rounds=None`, actual rounds randomized)
- `--verbose` — Print each round's result

## Examples

### Basic Match (100 rounds)
```bash
python run_match.py copycat_agent random_agent
```

### Custom Round Count
```bash
python run_match.py copycat_agent second_chance_agent --rounds 50
```

### Unknown Horizon
```bash
python run_match.py copycat_agent random_agent --unknown-horizon
```

### Verbose Output (see each round)
```bash
python run_match.py copycat_agent random_agent --rounds 10 --verbose
```

## Output

The script displays:

1. **IDA Results** — Agent A vs Agent B (A as Player 1)
2. **VUELTA Results** — Agent B vs Agent A (B as Player 1)
3. **SUMMARY** — Average scores and winner

Example output:
```
============================================================
IDA: copycat_agent (Player 1) vs random_agent (Player 2)
Rounds: 100
============================================================

IDA Results:
  copycat_agent: 250 points
  random_agent: 150 points

============================================================
VUELTA: random_agent (Player 1) vs copycat_agent (Player 2)
Rounds: 100
============================================================

VUELTA Results:
  random_agent: 160 points
  copycat_agent: 240 points

============================================================
SUMMARY
============================================================

copycat_agent:
  Ida:    250 points
  Vuelta: 240 points
  Average: 245.0 points

random_agent:
  Ida:    150 points
  Vuelta: 160 points
  Average: 155.0 points

============================================================
RESULT: copycat_agent WINS by 90.0 points on average
============================================================
```

## What is Ida/Vuelta?

- **Ida (First Leg):** Agent A plays as Player 1, Agent B as Player 2
- **Vuelta (Second Leg):** Roles reverse — Agent B as Player 1, Agent A as Player 2

This fairness mechanism accounts for any first-mover advantages.

## See Also

- `tournament_runner/` — Run round-robin tournament with all agents
- `agent_collector/` — Import student agents from repos
- `docs/game_rules.md` — Game mechanics explained
