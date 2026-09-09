# Win-Stay, Lose-Shift Agent implemented by Gonzalo Carrasco

**Strategy:** Cooperate on round 1, then repeat last movement if succesfully defected or both cooperated, otherwise shift strategy.

## Description

This agent implements the Pavlov strategy.

**Philosophy:**
- **Round 1:** Be nice—start with cooperation
- **Subsequent rounds:** Repeat winning decisions, switch decision after losing
- **Effect:** Encourages mutual cooperation and can win against complex agents who switch strategy often

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
Round 2: Me=(stay or change), They=? (random)
...varies based on random opponent
Average: ~2 points/round (sometimes punishes, sometimes cooperates)
```

### vs. Always-Defect
```
Round 1: Me=C, They=D  (I cooperate, they defect → I get 0)
Round 2: Me=D, They=D  (I retaliate, they keep defecting)
Round 3: Me=C, They=D  (I cooperate, they defect -> I get 0)
Average: ~0.5 point/round (trapped)
```

## Key Characteristics

- **Nice:** Starts with cooperation
- **Hard to predict:** If an agent tries to exploit WSLS agent it won't stop changing decisions
- **Easily beaten by Defector:** If WSLS agent loses a round it will change the action, meaning Defector
gets free 5 points every other round.


**Expected Performance:** 
- vs. Copycat: ~3 points/round (mutual cooperation)
- vs. Random: ~2 points/round (average)
- vs. Defector: ~0.5 points/round (1 point every other turn)
