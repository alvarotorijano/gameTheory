# Copycat Agent (Tit-for-Tat)

**Strategy:** Cooperate on round 1, then play whatever the opponent played last round.

## Description

The Copycat Agent implements **Tit-for-Tat**, one of the most famous and effective strategies in game theory. It won the first computer tournament for the Iterated Prisoner's Dilemma.

**Philosophy:**
- **Round 1:** Be nice—start with cooperation
- **Subsequent rounds:** Punish defection immediately (retaliate), but forgive the next round if opponent returns to cooperation
- **Effect:** Encourages mutual cooperation while defending against exploitation

**This agent is provided as a template.** Students should copy this folder, rename it, and modify the `play()` method to experiment with variations.

## Decision Tree

```mermaid
graph TD
    A["Start Round"] --> B{"First Round?"}
    B -->|Yes| C["Cooperate (C)"]
    B -->|No| D{"What did opponent<br/>play last round?"}
    D -->|Cooperated (C)| E["Cooperate (C)"]
    D -->|Defected (D)| F["Defect (D)"]
    C --> G["Next Round"]
    E --> G
    F --> G
```

## Behavior Examples

### vs. Another Copycat
```
Round 1: Me=C, They=C  (mutual cooperation)
Round 2: Me=C, They=C  (stay cooperative)
Round 3: Me=C, They=C  (and so on...)
Average: 3 points/round (perfect mutual cooperation)
```

### vs. Random Agent
```
Round 1: Me=C, They=? (random)
Round 2: Me=(copy last), They=? (random)
...varies based on random opponent
Average: ~2 points/round (sometimes punishes, sometimes cooperates)
```

### vs. Always-Defect
```
Round 1: Me=C, They=D  (I cooperate, they defect → I get 0)
Round 2: Me=D, They=D  (I retaliate, they keep defecting)
Round 3: Me=D, They=D  (locked in mutual defection)
Average: ~1 point/round (trapped)
```

## Key Characteristics

- **Nice:** Starts with cooperation
- **Retaliatory:** Punishes defection immediately
- **Forgiving:** Stops punishing if opponent stops defecting
- **Effective:** Ranked among the best strategies in tournaments
- **Simple:** Easy to understand and modify

## Why This Works

1. **Mutual cooperation** is a stable equilibrium (both agents stay cooperative)
2. **Immediate retaliation** deters exploitation
3. **Forgiveness** prevents endless defection spirals
4. **Simplicity** is hard to exploit

## How to Modify (For Students)

This is a great starting point for experiments:

```python
# Variant: Tit-for-Two-Tats (retaliate only after 2 defections)
# Variant: Generous Tit-for-Tat (forgive 10% of defections)
# Variant: Tit-for-Tat with Noise (add random forgiveness)
```

## Usage

```bash
# Play against random agent:
python utils/match_runner/run_match.py copycat_agent random_agent --rounds 100

# Include in tournament:
python utils/tournament_runner/run_tournament.py
# (copycat_agent will be discovered automatically)
```

## Historical Context

Tit-for-Tat was submitted by Anatol Rapoport to Robert Axelrod's famous 1984 tournament. It won with just 4 lines of code, proving that simple strategies can outperform complex ones in game theory.

---

**Expected Performance:** 
- vs. Copycat: ~3 points/round (mutual cooperation)
- vs. Random: ~2 points/round (average)
- vs. Defector: ~1 point/round (stuck in retaliation)
