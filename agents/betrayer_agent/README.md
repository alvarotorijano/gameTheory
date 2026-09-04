# Betrayer Agent

**Strategy:** Cooperate by default, but periodically betray a fully trusting opponent to test their reaction — forgive a single provoked exchange of defections, hold a permanent grudge after a second unprovoked defection, and always defect on a known final round.

## Description

The Betrayer Agent starts out cooperative but never lets an opponent get too comfortable. Against an opponent with a clean record, it will defect unprovoked just to see how they respond, then decides how to treat them.

**Philosophy (from the agent's own notes):**
- Opens with `COOPERATE`. If the opponent defects in round 1, punish immediately in round 2.
- If the opponent has defected more than once (ever), defect always — trust is gone for the rest of the match.
- If the opponent cooperates, cooperate back.
- Betray (defect) an opponent with a clean record from time to time: if the opponent then punishes the betrayal, cooperate for the rest of the match; if the opponent doesn't punish it, betray again.

## Behavior Examples

### vs. Always-Cooperate Agent
```
Round 1: Me=C, They=C
Round 2: Me=C, They=C   (they didn't defect in round 1)
Round 3: Me=D, They=C   (clean record + our last move was C -> betray)
Round 4: Me=C, They=C   (our last move was D, so the betray-check doesn't fire)
Round 5: Me=D, They=C   (clean record again -> betray again)
Round 6: Me=C, They=C
...
Never punished, so it keeps exploiting: cooperate, betray, cooperate, betray...
```

### vs. Copycat (Tit-for-Tat) — betrayal gets punished once, then forgiven
```
Round 1: Me=C, They=C
Round 2: Me=C, They=C
Round 3: Me=D, They=C   (clean record + our last move was C -> betray)
Round 4: Me=C, They=D   (they mirror our round-3 defection; our own last move was D, so no re-betray)
Round 5: Me=C, They=C   (their defection was provoked by our round-3 move -> forgive)
Round 6: Me=C, They=C   (one defection each, settled -> lock into cooperation)
...
Converges to permanent mutual cooperation after a single betray-and-forgive exchange.
```

### vs. One-Time Early Defector
```
Round 1: Me=C, They=D
Round 2: Me=D, They=C   (punish the round-1 defection)
Round 3: Me=C, They=C   (one defection each so far, opponent's record is otherwise clean -> settled)
Round 4: Me=C, They=C
...
Quick reconciliation: a single early defection from either side is forgiven.
```

### vs. Serial Defector
```
Round 1: Me=C, They=D
Round 2: Me=D, They=D   (punish the round-1 defection)
Round 3: Me=D, They=D   (opponent has now defected twice -> permanent grudge)
Round 4: Me=D, They=D
...
Locks into permanent mutual defection once the opponent defects a second time.
```

## Key Characteristics

- **Cooperative opener:** always cooperates round 1, and only reacts to a round-1 defection (immediate punish-or-continue) when deciding round 2.
- **Self-testing:** against an opponent with a completely clean record, periodically defects unprovoked just to probe their reaction, as long as its own previous move was cooperation.
- **Provoked vs. unprovoked:** when the opponent defects, checks whether *our* move two rounds earlier was a cooperation (unprovoked defection -> retaliate) or a defection (provoked defection -> forgive).
- **One-strike forgiveness:** once each side has defected exactly once, resets to permanent cooperation for the rest of the match.
- **Zero tolerance beyond that:** a second defection from the opponent, anywhere in the match history, triggers permanent unconditional defection from then on.
- **Endgame defection:** on a known final round, defects regardless of any other state — there's no future round left to be punished for it.
- **Stateful:** unlike plain tit-for-tat, decisions depend on cumulative defection counts and on the move from two rounds back, not just the opponent's last move.

## Usage

```bash
python utils/match_runner/run_match.py betrayer_agent copycat_agent --rounds 20 --verbose
python utils/match_runner/run_match.py betrayer_agent random_agent --rounds 100
python utils/tournament_runner/run_tournament.py --rounds 100
```
