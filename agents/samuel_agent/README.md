# My Agent

**Strategy:** Cooperate on round 1, then deflect independently of what the opponent does.

## Description

The Copycat Agent implements **Tit-for-Tat**, one of the most famous and effective strategies in game theory. It won the first computer tournament for the Iterated Prisoner's Dilemma.

However, my agent implements an always-deflect strategy.

**Philosophy:**
- **Round 1:** Be nice—start with cooperation
- **Subsequent rounds:** Defect immediately to ensure some kind of point is awarded
- **Effect:** Awards point regardless of what the opponent does.


## Decision Tree

```mermaid
graph TD
    A["Start Round"] --> B{"First Round?"}
    B -->|Yes| C["Cooperate (C)"]
    B -->|No| D["Defect (D)"}
    C --> F["Next Round"]
    D --> F
    E --> F
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
