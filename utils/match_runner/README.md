# Match Runner

Play two agents against each other in the Iterated Prisoner's Dilemma.

## Usage

Run from the project root directory:

```bash
python utils/match_runner/run_match.py <agent_a> <agent_b> --rounds N
```

## Options

- `--rounds N` — Number of rounds **(required)**
- `--unknown-horizon` — Agents don't know the round count (cannot plan strategy ahead)
- `--verbose` — Print each round's result
- `--visualize` — Show live replay of moves with delays (great for learning how agents play)

## Examples

### Basic Match
```bash
python utils/match_runner/run_match.py copycat_agent random_agent --rounds 50
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
python utils/match_runner/run_match.py copycat_agent random_agent --rounds 10 --visualize
```

Shows each move with a 0.8 second delay between rounds. Cooperation shown in green, defection in red.

## Output

The script displays:

1. **Match header** — agent A vs agent B, round count
2. **Move sequence** (if `--verbose`) — each round's choices
3. **Live replay** (if `--visualize`) — animated playback with color
4. **Summary** — final scores and winner

Example output:
```
============================================================
MATCH: copycat_agent vs random_agent
Rounds: 50
============================================================

Results:
  copycat_agent: 250 points
  random_agent: 150 points

============================================================
SUMMARY
============================================================

copycat_agent: 250 points
random_agent: 150 points

============================================================
RESULT: copycat_agent WINS by 100 points
============================================================
```

## Strategies

- **copycat_agent** — Tit-for-tat: cooperate first, then play opponent's last move
- **random_agent** — Play random moves (50% cooperate, 50% defect)
- **second_chance_agent** — Forgive first defection, retaliate on the second

## See Also

- `tournament_runner/` — Run round-robin tournament with all agents
- `agent_collector/` — Import student agents from repos
- `docs/game_rules.md` — Game mechanics explained
