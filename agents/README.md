# Agents Folder

This folder contains all game agents (strategies for the Iterated Prisoner's Dilemma).

## Structure

Each agent is in its own subfolder:

```
agents/
├── random_agent/
│   ├── agent.py       # Agent implementation
│   └── README.md      # Strategy description & decision tree
├── copycat_agent/     # Template for student agents
│   ├── agent.py
│   └── README.md
├── second_chance_agent/
│   ├── agent.py
│   └── README.md
└── <student_agents>/  # Students add their own agents here
```

## For Students

1. **Copy** one of the example agents (e.g., `copycat_agent/`)
2. **Rename** the folder to your strategy name (e.g., `my_strategy/`)
3. **Edit** `agent.py` to implement your logic
4. **Test** locally: `python utils/match_runner/run_match.py my_strategy random_agent --rounds 50`
5. **Update** `README.md` with your strategy description

## Example Agents

- **`random_agent/`** — Plays random moves (baseline fictitious opponent)
- **`copycat_agent/`** — Tit-for-tat (template for students)
- **`second_chance_agent/`** — Forgiving strategy with defection counter

## Requirements

Each agent must:
- Contain a Python class that inherits from `Agent` (from `utils.game_core.agent_base`)
- Implement the `play(own_history, opponent_history)` method
- Return either `"C"` (cooperate) or `"D"` (defect)

See [`../docs/student_guide.md`](../docs/student_guide.md) for complete instructions.
