# Game Core Library

The core game engine and interfaces for the Iterated Prisoner's Dilemma.

## Modules

### `moves.py`
Constants for player moves:
- `COOPERATE = "C"` — Cooperate move
- `DEFECT = "D"` — Defect move

### `agent_base.py`
Abstract base class that all agents must inherit from.

**Key Class:** `Agent`
- `__init__(num_rounds: Optional[int])` — Initialize with optional round count
- `play(own_history: List[str], opponent_history: List[str]) -> str` — Decide the agent's move (must be implemented by subclasses)

### `payoff.py`
Scoring logic and configuration management.

**Key Functions:**
- `score_round(move_a: str, move_b: str) -> Tuple[int, int]` — Score one round
- `get_config() -> PayoffConfig` — Get current game configuration

**Configuration is loaded from `config.json`:**
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

### `engine.py`
Match orchestration between two agents.

**Key Functions:**
- `run_leg(agent_a: Agent, agent_b: Agent, num_rounds: int, ...) -> MatchResult` — Execute one complete match
- `get_effective_rounds(num_rounds: Optional[int]) -> int` — Resolve the actual round count

**MatchResult Dataclass:** Contains scores, histories, and statistics from a completed leg.

### `agent_loader.py`
Agent discovery using AST parsing.

**Key Functions:**
- `discover_agents(agents_dir: str | Path) -> Dict[str, Type[Agent]]` — Find all Agent subclasses in a directory

---

## Usage Example

```python
from utils.game_core import Agent, COOPERATE, DEFECT, run_leg, discover_agents

# Define a simple agent
class MyAgent(Agent):
    def play(self, own_history, opponent_history):
        if not opponent_history:
            return COOPERATE
        return opponent_history[-1]  # Tit-for-tat

# Discover all agents
agents = discover_agents("agents/")

# Run a match
agent1 = MyAgent(num_rounds=100)
agent2 = agents["random_agent"](num_rounds=100)
result = run_leg(agent1, agent2, 100, "my_agent", "random_agent", verbose=True)

print(f"Score: {result.agent_a_score} vs {result.agent_b_score}")
```

---

## Architecture

```
game_core/
├── moves.py           # Constants
├── agent_base.py      # Agent interface
├── payoff.py          # Scoring & config
├── engine.py          # Match engine
├── agent_loader.py    # Agent discovery
├── __init__.py        # Package exports
└── README.md          # This file
```

---

## Design Notes

- **Configuration externalized:** All scoring and round-count settings come from `config.json`
- **AST-based discovery:** Robust to non-standard agent file/folder names
- **Simultaneous moves:** Both agents' `play()` methods are called before evaluating the round
- **Unknown horizon support:** Agents can be told `num_rounds=None` and game engine handles randomization

---

See [`../../docs/architecture.md`](../../docs/architecture.md) for full technical design.
