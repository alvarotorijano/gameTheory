# Iterated Prisoner's Dilemma Tournament

A tournament platform where students implement strategies for the Iterated Prisoner's Dilemma and compete against each other.

---

## Quick Start

Get started in two commands:

```bash
# 1. Run your first match
python utils/match_runner/run_match.py copycat_agent random_agent --rounds 50

# 2. Run a full tournament
python utils/tournament_runner/run_tournament.py --rounds 50
```

That's it. You'll see a match between two example agents, and a tournament with all agents.

---

## Next Steps

After running your first commands:

1. **Write your first agent:** Copy `agents/copycat_agent/` to `agents/my_strategy/` and edit `agent.py`
2. **Test your agent:** `python utils/match_runner/run_match.py my_strategy random_agent --rounds 50`
3. **Run a full tournament:** `python utils/tournament_runner/run_tournament.py --rounds 50`

---

## Documentation

Full guides and technical details:

- **[Game Rules](docs/game_rules.md)** — How the game works, payoff matrix, match structure
- **[Student Guide](docs/student_guide.md)** — Step-by-step walkthrough to write your first agent
- **[Installation](docs/installation.md)** — Environment setup with virtual environments and pyenv (optional)
- **[Architecture](docs/architecture.md)** — Technical design and component descriptions
- **[Technical Requirements](docs/requirements.md)** — Complete specifications

## Command Reference

### Match Runner
Play two agents against each other:

```bash
python utils/match_runner/run_match.py <agent1> <agent2> --rounds 50
python utils/match_runner/run_match.py copycat_agent random_agent --rounds 50 --visualize
python utils/match_runner/run_match.py copycat_agent random_agent --rounds 50 --unknown-horizon
```

### Tournament Runner
Run round-robin tournament with all agents:

```bash
python utils/tournament_runner/run_tournament.py --rounds 100
python utils/tournament_runner/run_tournament.py --rounds 50 --no-self-play
python utils/tournament_runner/run_tournament.py --rounds 100 --unknown-horizon
```

Results are saved to `results/tournament_<timestamp>_<flags>.csv`

### Agent Collector
Import student agents from repositories or files:

```bash
python utils/agent_collector/collect_agents.py --sources sources.json
python utils/agent_collector/collect_agents.py --sources sources.json --dry-run
```

---

## Example Agents

Three example agents are provided:

- **random_agent** — Plays random moves (50% cooperate, 50% defect)
- **copycat_agent** — Tit-for-tat: cooperate first, then copy opponent's last move
- **second_chance_agent** — Forgives one defection, retaliates on the second

---

## Project Status

- Complete: Core game engine, example agents, CLI tools, documentation
- In progress: Test suite

---

## Key Concepts

- **Simultaneous moves**: Agents decide without knowing the opponent's choice in that round
- **Known vs unknown horizon**: Agents can know or not know the round count
- **Unique pairings**: Each agent plays each other agent once (order doesn't matter)
- **Tournament results**: CSV with statistics per agent per matchup

See [docs/README.md](docs/README.md) for a complete documentation index.
