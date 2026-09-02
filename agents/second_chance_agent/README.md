# Second Chance Agent

**Strategy:** Cooperate by default. Forgive the first defection. On the second defection, retaliate once, then forgive and reset.

## Description

The Second Chance Agent implements a more forgiving strategy than Tit-for-Tat. It believes everyone deserves a second chance.

**Philosophy:**
- **Default:** Cooperate always
- **First defection:** No retaliation—forgive and move forward
- **Second defection:** Issue a single punishment (defect once)
- **After punishment:** Reset counter and return to cooperation
- **Memory:** Only "remembers" the last two interactions with the opponent

**Rationale:** This strategy assumes opponents may make mistakes. Rather than immediately punishing each defection, it only retaliates when the pattern of defection becomes clear. This can be effective against:
- Agents that make occasional mistakes
- Agents that are learning or testing
- Agents that appreciate forgiveness

But it can be exploited by serial defectors who see forgiveness as weakness.

## Decision Tree & State Machine

```mermaid
graph TD
    A["Start Round"] --> B{"First Round?"}
    B -->|Yes| C["Cooperate (C)<br/>defection_count = 0"]
    B -->|No| D{"Opponent's<br/>Last Move?"}
    D -->|Cooperated (C)| E["Cooperate (C)"]
    D -->|Defected (D)| F["Increment<br/>defection_count"]
    F --> G{"defection_count<br/>= 2?"}
    G -->|No| H["Cooperate (C)<br/>Forgive"]
    G -->|Yes| I["Defect (D)<br/>Retaliate"]
    I --> J["Reset<br/>defection_count = 0"]
    E --> K["Next Round"]
    H --> K
    J --> K
```

## Behavior Examples

### vs. Cooperative Agent
```
Round 1: Me=C, They=C  (mutual cooperation)
Round 2: Me=C, They=C  (stay cooperative)
Round 3: Me=C, They=C  (continue)
Count: 0 defections observed
Average: 3 points/round (perfect mutual cooperation)
```

### vs. One-Time Defector
```
Round 1: Me=C, They=C
Round 2: Me=C, They=D  (count=1: first defection)
Round 3: Me=C, They=C  (forgive, count stays 1)
Round 4: Me=C, They=C  (back to normal)
Count: 1 defection observed (forgiven)
Average: ~2.75 points/round (lose once, then recover)
```

### vs. Two-Time Defector
```
Round 1: Me=C, They=C
Round 2: Me=C, They=D  (count=1: first defection, forgive)
Round 3: Me=C, They=D  (count=2: second defection detected)
Round 4: Me=D, They=?  (retaliate! count reset to 0)
Round 5: Me=C, They=?  (back to cooperation)
Pattern: Forgive once, then punish once, then forgive again
```

### vs. Serial Defector
```
Round 1: Me=C, They=D  (count=1)
Round 2: Me=C, They=D  (count=2)
Round 3: Me=D, They=D  (retaliate, count=0)
Round 4: Me=C, They=D  (count=1)
Round 5: Me=C, They=D  (count=2)
Round 6: Me=D, They=D  (retaliate again, count=0)
Pattern: Cycle of forgive-forgive-punish repeats
Average: ~1.5 points/round (exploited by serial defector)
```

## Key Characteristics

- **Forgiving:** Tolerates one defection without retaliation
- **Fair:** Issues exactly one retaliation for pattern defection
- **Resetting:** Starts fresh after punishing
- **Trusting:** Assumes defections might be mistakes
- **Vulnerable:** Can be exploited by agents that always defect

## Strengths & Weaknesses

| For | Against |
|---|---|
| Cooperative agents ✓ | Always-Defect agents ✗ |
| Mistake-prone agents ✓ | Serial defectors ✗ |
| Learning agents ✓ | Exploiters ✗ |
| Creates goodwill ✓ | Loses too many points early ✗ |

## Memory

This agent "remembers" roughly two rounds:
- It tracks `opponent_defection_count`
- When count reaches 2, it retaliattes and resets
- This creates a forgiving cycle

(Technically, it maintains state across rounds, but the defection counter is the only memory.)

## Usage

```bash
# Play against random:
python utils/match_runner/run_match.py second_chance_agent random_agent --rounds 100

# Play against copycat:
python utils/match_runner/run_match.py second_chance_agent copycat_agent --rounds 100
# (Should do well—copycat will cooperate back)

# Include in tournament:
python utils/tournament_runner/run_tournament.py
```

## Comparison with Copycat (Tit-for-Tat)

| Aspect | Copycat | Second Chance |
|---|---|---|
| Strategy | Immediate retaliation | Forgiving until pattern |
| vs. Cooperator | Perfect mutual cooperation | Perfect mutual cooperation |
| vs. Defector | Stuck in retaliation cycle | Cycle: forgive-forgive-punish |
| Complexity | Simpler (no state) | Slightly complex (maintains counter) |
| Tournament success | Very high | Good (depends on opponent mix) |

---

**Expected Performance:**
- vs. Cooperative: ~3 points/round (great!)
- vs. Copycat: ~3 points/round (mutual forgiveness/cooperation)
- vs. Random: ~2 points/round (average)
- vs. Always-Defect: ~1 point/round (exploited)
