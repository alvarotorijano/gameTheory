# myAlternate Agent (Tit-for-Tat)

**Strategy:** Round one will be a random answer. The following rounds it will alternate the answers

## Description

myAlternate Agent follows an easy strategy. It will alternate its answers depending on its previous answer.

**Philosophy:**
- **Round 1:** Star with a random choice
- **Subsequent rounds:** IT will alternate its answer, which means that it will choose the oposite answer to its previous round

## Decision Tree

```mermaid
graph TD
    A["Start Round"] --> B{"First Round?"}
    B -->|Yes| C[random choice]
    B -->|No| D{"What did I<br/>play last round?"}
    D -->|Cooperated (C)| E["Defected (D)"]
    D -->|Defected (D)| F["Cooperated (C)"]
    C --> G["Next Round"]
    E --> G
    F --> G
```

## Usage

```bash
# Play against random agent:
python utils/match_runner/run_match.py myAlternateAgent random_agent --rounds 100

# Include in tournament:
python utils/tournament_runner/run_tournament.py
# (copycat_agent will be discovered automatically)
```

