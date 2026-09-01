# Student Guide: Writing Your First Prisoner's Dilemma Agent

Welcome! This guide walks you through writing your first agent step by step.

## What Is an Agent?

An **agent** is a Python class that decides how to play the Iterated Prisoner's Dilemma. Each
round, your agent sees the history of moves and decides: cooperate or defect?

You'll write a class that inherits from `Agent` and implements a single method: `play()`.

---

## Step 1: Copy the Copycat Agent (Template)

The **copycat agent** is provided as a reference implementation. It plays tit-for-tat
(copies the opponent's last move).

1. Navigate to the `agents/` folder.
2. **Copy** the entire `copycat_agent` folder.
3. **Rename** your copy to something meaningful, e.g., `my_strategy` or `my_agent`.

Your folder should look like this:

```
agents/
├── random_agent/
├── copycat_agent/          ← the template
└── my_strategy/            ← your copy
    ├── agent.py            ← you'll edit this
    └── README.md           ← update this with your strategy
```

---

## Step 2: Understand the Agent Interface

Open `agents/copycat_agent/agent.py` and read it carefully:

```python
from utils.game_core.agent_base import Agent
from utils.game_core.moves import COOPERATE, DEFECT

class CopycatAgent(Agent):
    """
    Tit-for-tat strategy: cooperate on round 1, then play the opponent's last move.
    """

    def play(self, own_history, opponent_history):
        """
        Decide the agent's move.
        
        Parameters:
            own_history: List of your moves in all prior rounds (empty on round 1).
            opponent_history: List of the opponent's moves in all prior rounds (empty on round 1).
        
        Returns:
            "C" (cooperate) or "D" (defect).
        """
        if not opponent_history:
            # Round 1: no history yet, cooperate
            return COOPERATE
        # Copy the opponent's last move
        return opponent_history[-1]
```

### Key Points

- Your agent **always** has access to the full history of both players.
- `own_history` and `opponent_history` are **lists of strings** (`["C", "D", "C", ...]`).
- You **must return either `"C"` or `"D"`** (use the constants `COOPERATE` and `DEFECT`).
- Your agent does **not** know how many rounds remain (unless the instructor tells you via
  `self.num_rounds`).

---

## Step 3: Create Your Strategy

Edit `my_strategy/agent.py`:

1. **Rename the class** from `CopycatAgent` to something unique (e.g., `MyStrategy`).
2. **Update the docstring** to describe your strategy.
3. **Modify the `play()` method** to implement your logic.

### Example: Simple Tit-for-Tat with Forgiveness

```python
from utils.game_core.agent_base import Agent
from utils.game_core.moves import COOPERATE, DEFECT

class MyForgiveStrategy(Agent):
    """
    Tit-for-tat with occasional forgiveness:
    - Cooperate by default.
    - If the opponent defects, defect once, then go back to cooperating.
    - (More forgiving than pure tit-for-tat.)
    """

    def play(self, own_history, opponent_history):
        if not opponent_history:
            # Round 1: cooperate
            return COOPERATE
        
        # If the opponent defected in the last round, defect now
        if opponent_history[-1] == DEFECT:
            return DEFECT
        
        # Otherwise, cooperate
        return COOPERATE
```

### Tips for Strategy Design

1. **Read the history:** Use `own_history` and `opponent_history` to detect patterns.
   - Example: `opponent_history.count(DEFECT)` to count defections.
   - Example: `opponent_history[-2:]` to see the last two moves.

2. **Keep track of state:** You can store instance variables (set in `__init__`).
   ```python
   def __init__(self, num_rounds=None):
       super().__init__(num_rounds)
       self.defection_count = 0  # track something across rounds
   ```

3. **Simple is often better:** Strategies that are easy to understand usually perform well.
   - Pure cooperation (always `"C"`).
   - Pure defection (always `"D"`).
   - Tit-for-tat (copy opponent).
   - Tit-for-tat with forgiveness.

4. **Avoid assuming the opponent is rational:** The game is open to all strategies, including
   random ones.

---

## Step 4: Test Your Agent Locally

Once you've written your strategy, test it against the **random agent**:

```bash
cd gameTheory
python utils/match_runner/run_match.py my_strategy random_agent --rounds 50
```

**Output example:**
```
Ida (my_strategy vs random_agent):
  my_strategy: 145 points
  random_agent: 60 points

Vuelta (random_agent vs my_strategy):
  random_agent: 65 points
  my_strategy: 140 points

Average:
  my_strategy: 142.5 points (WINNER)
  random_agent: 62.5 points
```

If you see an error, check:
- Did you **rename the class** in your `agent.py`?
- Did you **import the constants** (`COOPERATE`, `DEFECT`)?
- Does your `play()` method **always return a string** (`"C"` or `"D"`)?

---

## Step 5: Update Your README

Edit `my_strategy/README.md` with:

1. **Strategy name and description:** What does your agent do?
2. **Decision tree (Mermaid diagram):** A flowchart of your logic.

### Example README

```markdown
# My Forgive Strategy

## Description

A tit-for-tat strategy with forgiveness. The agent cooperates by default but defects
once after the opponent defects, then immediately returns to cooperation.

## Decision Tree

\`\`\`mermaid
graph TD
    A["Round 1?"] -->|Yes| B["Cooperate"]
    A -->|No| C["Opponent defected<br/>last round?"]
    C -->|Yes| D["Defect once"]
    C -->|No| E["Cooperate"]
\`\`\`

## Why This Strategy?

Tit-for-tat is a proven strategy in tournament play, but it can get stuck in mutual defection.
By forgiving once, we allow the opponent a chance to return to cooperation.
```

---

## Step 6: Submit Your Agent

Once you're happy with your agent:

1. **Commit your changes** to your own fork or repo.
2. **Push to GitHub** (or provide the file to your instructor).
3. Your instructor will run the **tournament** to compare all student agents.

---

## Common Mistakes

### Mistake 1: Returning the wrong type
❌ `return 0` (should be `"C"`)
✅ `return COOPERATE` or `return "C"`

### Mistake 2: Accessing moves incorrectly
❌ `opponent_history[0]` when the list might be empty
✅ `if opponent_history: return opponent_history[-1]`

### Mistake 3: Forgetting to inherit from `Agent`
❌ `class MyStrategy: ...`
✅ `class MyStrategy(Agent): ...`

### Mistake 4: Not implementing `play()`
❌ Forgetting to define the `play()` method
✅ Always define `play(self, own_history, opponent_history)`

---

## Next Steps

- Read `docs/game_rules.md` to understand payoff scoring and tournaments.
- Look at `agents/copycat_agent/` and `agents/second_chance_agent/` for more examples.
- Test your agent against other example agents:
  ```bash
  python utils/match_runner/run_match.py my_strategy copycat_agent --rounds 100
  ```
- Once all students submit, your instructor will run:
  ```bash
  python utils/tournament_runner/run_tournament.py
  ```
  And you'll see how your strategy compares to everyone else's!

---

## Questions?

Refer to:
- `docs/game_rules.md` — payoff matrix and game mechanics.
- `docs/architecture.md` — technical details about agents and the game engine.
- The `README.md` in the project root for setup and usage examples.
