# Match Runner

Play two agents against each other in the Iterated Prisoner's Dilemma (first leg + second leg).

## Usage

**Run from the project root directory:**

```bash
python utils/match_runner/run_match.py <agent_a> <agent_b> [OPTIONS]
```

## Options

- `--rounds N` — Number of rounds per leg **(required)**
- `--unknown-horizon` — Agents don't know the round count (cannot plan strategy ahead)
- `--verbose` — Print each round's result
- `--visualize` — Show live replay of moves with delays (great for learning how agents play)

## Examples

### Basic Match (100 rounds)
```bash
python utils/match_runner/run_match.py copycat_agent random_agent
```

### Custom Round Count
```bash
python utils/match_runner/run_match.py copycat_agent second_chance_agent --rounds 50
```

### Unknown Horizon (agents don't know how many rounds)
```bash
python utils/match_runner/run_match.py copycat_agent random_agent --rounds 50 --unknown-horizon
```

### Verbose Output (see each round)
```bash
python utils/match_runner/run_match.py copycat_agent random_agent --rounds 10 --verbose
```

### Live Visualization (see moves in real-time)
```bash
python utils/match_runner/run_match.py copycat_agent random_agent --visualize --rounds 10
```
Shows each move with a 0.8 second delay between rounds. Cooperation shown in green, defection in red.

## Output

The script displays:

1. **FIRST LEG Results** — Agent A vs Agent B (A as Player 1)
2. **SECOND LEG Results** — Agent B vs Agent A (B as Player 1)
3. **SUMMARY** — Average scores and winner

Example output:
```
============================================================
FIRST LEG: copycat_agent (Player 1) vs random_agent (Player 2)
Rounds: 100
============================================================

FIRST LEG Results:
  copycat_agent: 250 points
  random_agent: 150 points

============================================================
SECOND LEG: random_agent (Player 1) vs copycat_agent (Player 2)
Rounds: 100
============================================================

SECOND LEG Results:
  random_agent: 160 points
  copycat_agent: 240 points

============================================================
SUMMARY
============================================================

copycat_agent:
  First Leg:    250 points
  Second Leg: 240 points
  Average: 245.0 points

random_agent:
  First Leg:    150 points
  Second Leg: 160 points
  Average: 155.0 points

============================================================
RESULT: copycat_agent WINS by 90.0 points on average
============================================================
```

## What is First Leg/Second Leg?

- **First Leg (First Leg):** Agent A plays as Player 1, Agent B as Player 2
- **Second Leg (Second Leg):** Roles reverse — Agent B as Player 1, Agent A as Player 2

This fairness mechanism accounts for any first-mover advantages.

## See Also

- `tournament_runner/` — Run round-robin tournament with all agents
- `agent_collector/` — Import student agents from repos
- `docs/game_rules.md` — Game mechanics explained
