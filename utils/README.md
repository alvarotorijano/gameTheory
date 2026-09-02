# Utils Folder

This folder contains the core game library and CLI tools for the tournament.

## Structure

```
utils/
├── README.md              # This file
├── game_core/             # Shared game engine library
│   ├── __init__.py
│   ├── moves.py           # Move constants (COOPERATE, DEFECT)
│   ├── agent_base.py      # Abstract Agent base class
│   ├── payoff.py          # Payoff scoring logic
│   ├── engine.py          # Match engine (runs one match)
│   ├── agent_loader.py    # Agent discovery (AST-based)
│   └── README.md          # Library documentation
│
├── match_runner/          # Play two agents
│   ├── run_match.py       # CLI script
│   └── README.md          # Usage instructions
│
├── tournament_runner/     # Run round-robin tournament
│   ├── run_tournament.py  # CLI script
│   └── README.md          # Usage instructions
│
└── agent_collector/       # Import student agents
    ├── collect_agents.py  # CLI script
    └── README.md          # Usage instructions
```

## Core Library (`game_core/`)

Provides the game engine and base classes for agents.

**Key Components:**
- `Agent` — Base class for all agents
- `play()` — Method agents must implement
- `score_round()` — Payoff scoring
- `run_leg()` — Execute one match
- `discover_agents()` — Find agents (AST-based)

## CLI Tools

Each tool has its own folder with a Python script and README:

### Match Runner
```bash
python match_runner/run_match.py <agent_a> <agent_b> --rounds N
```
Play two agents against each other and show results.

### Tournament Runner
```bash
python tournament_runner/run_tournament.py --rounds N [--no-self-play]
```
Run round-robin tournament with all agents, output CSV.

### Agent Collector
```bash
python agent_collector/collect_agents.py --sources sources.json [--dry-run]
```
Import student agents from repos or files.

## Implementation Status

- [x] `game_core/` — Implemented
- [x] `match_runner/` — Implemented
- [x] `tournament_runner/` — Implemented
- [ ] `agent_collector/` — To be implemented

See [../docs/requirements.md](../docs/requirements.md) for complete specifications.
