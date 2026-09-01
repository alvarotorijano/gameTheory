# Game Rules & Mechanics

## The Iterated Prisoner's Dilemma

In each round, two players simultaneously choose to either **cooperate (C)** or **defect (D)**.
Based on both choices, they each receive points according to this payoff matrix:

| Both Players | Payoff | Rationale |
|---|---|---|
| Both Cooperate | 3 points each | Mutual cooperation — the "happy" outcome |
| Both Defect | 1 point each | Mutual betrayal — poor outcome for both |
| One Cooperates, One Defects | Cooperator: 0, Defector: 5 | The defector exploits cooperation |

This is configurable in `config.json`:
```json
{
  "payoff": {
    "both_cooperate": 3,
    "both_defect": 1,
    "betrayed_cooperator": 0,
    "betrayer_reward": 5
  }
}
```

## Match Structure: Ida and Vuelta

A complete match between two agents consists of **two legs**:

### Ida (First Leg)
- **Agent A** is designated **Player 1**.
- **Agent B** is designated **Player 2**.
- They play for a fixed number of rounds.

### Vuelta (Second Leg)
- **Agent B** is designated **Player 1**.
- **Agent A** is designated **Player 2**.
- The roles reverse, but the agents are the same.
- They play for the same number of rounds (or a newly random horizon if unknown).

### Why Two Legs?

In the Iterated Prisoner's Dilemma, **the order in which agents are listed can affect outcome**
(for example, if one agent always copies the opponent's *first* move, being the first mover
matters). By playing both "A vs B" and "B vs A," we fairly account for any such asymmetries
and compute a more representative average score for each agent.

### Example
If Agent A scores 150 total points in Ida and Agent B scores 50, then:
- A's Ida score: 150
- B's Ida score: 50

Then in Vuelta, the roles swap:
- B's Vuelta score: 120 (as Player 1 this time)
- A's Vuelta score: 80 (as Player 2 this time)

Final averages:
- A: (150 + 80) / 2 = 115 average
- B: (50 + 120) / 2 = 85 average
- A wins the match.

---

## Round Dynamics

Each round proceeds as follows:

1. **Agent A's `play()` is called** with:
   - `own_history`: List of A's moves in all prior rounds (empty on round 1).
   - `opponent_history`: List of B's moves in all prior rounds (empty on round 1).

2. **Agent B's `play()` is called** with:
   - `own_history`: List of B's moves in all prior rounds.
   - `opponent_history`: List of A's moves in all prior rounds.

3. **Both moves are recorded** simultaneously (the agents don't see each other's choice until
   the round ends).

4. **Payoff is calculated** using the matrix above.

5. **History is updated** for the next round.

### Simultaneity

The game is **genuinely simultaneous** — agents decide without knowing the opponent's current-round
choice. This is why both `play()` calls happen "in parallel" (from each agent's perspective) before
any payoff is calculated. Each agent can only react to what the opponent *did*, not what they
*will* do.

---

## Rounds: Known vs. Unknown Horizon

### Known Horizon
When an agent is instantiated with `num_rounds=100` (a concrete number), the agent:
- Knows it will play exactly 100 rounds.
- Can adopt strategies that depend on "how many rounds are left."

### Unknown Horizon
When an agent is instantiated with `num_rounds=None`, the agent:
- Does **not** know how many rounds it will play.
- The engine still plays a **finite** number of rounds (randomly chosen at the start of the
  match from the range in `config.json`), but the agent is never told this number.
- Encourages agents to adopt "stateless" or "reactive" strategies that don't rely on knowing
  the end of the game.

### Configuration
In `config.json`:
```json
{
  "rounds": {
    "default": 100,
    "unknown_horizon_min": 50,
    "unknown_horizon_max": 200
  }
}
```

- `default`: Used if neither the CLI nor the API specifies a round count.
- `unknown_horizon_min` / `unknown_horizon_max`: The range from which the engine randomly
  picks a round count when `num_rounds=None`.

---

## Tournament Structure

The **Tournament Runner** plays every agent against every other agent in the discovery set:
- For each pair of agents (A, B), it runs both Ida (A vs B) and Vuelta (B vs A).
- By default, agents also play against themselves (self-play enabled).
- Results are recorded in a CSV with one row per `(agent, leg)`.

This creates a **complete round-robin tournament**. With *n* agents, there are *n² × 2* total
legs (each agent pair, both orderings, both legs).

---

## Scoring Summary for a Match

After Ida and Vuelta, the instructor examines:
1. **Points per leg** (how many points each agent scored in each leg).
2. **Average points** across both legs (which agent won the match overall).
3. **Statistical columns** (cooperations, defections, conditional behavior), which reveal
   *why* one agent beat another (e.g., "A cooperated more often and was exploited" vs.
   "A was selective and only defected when necessary").

---

## Move Representation

Moves are represented as **single-character strings**:
- `"C"` = Cooperate
- `"D"` = Defect

These are available as constants in `utils/game_core/moves.py`:
```python
COOPERATE = "C"
DEFECT = "D"
```

This is deliberately simple (not an enum) to lower the barrier for student programmers.
