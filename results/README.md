# Results Folder

This folder contains tournament result files (CSV format).

## What Goes Here

When you run the tournament runner:

```bash
python utils/tournament_runner/run_tournament.py --rounds 100
```

It generates a CSV file here:

```
results/tournament_02092026-143052_rounds100.csv
```

## CSV Format

One row per agent per match, with these columns:

| Column | Meaning |
|---|---|
| `pairing_id` | Unique identifier for this match |
| `num_rounds` | Rounds actually played |
| `agent_name` | Agent identifier |
| `opponent_name` | Opponent identifier |
| `points_scored` | Points this agent earned |
| `opponent_points` | Points the opponent earned |
| `first_move_cooperate` | `true` if agent played "C" on round 1 |
| `total_cooperations` | Count of "C" moves |
| `total_defections` | Count of "D" moves |
| `cooperate_after_opponent_defect` | Conditional count |
| `defect_after_opponent_defect` | Conditional count |
| `cooperate_after_opponent_cooperate` | Conditional count |
| `defect_after_opponent_cooperate` | Conditional count |

## Filename Format

Tournament files are auto-named with timestamp and flags:

**Format:** `tournament_DDMMYYYY-HHMMSS_<flags>.csv`

**Examples:**
- `tournament_02092026-143052_rounds100.csv` — 100 rounds, known horizon, with self-play
- `tournament_02092026-143105_rounds50_unknown-horizon.csv` — Unknown horizon mode
- `tournament_02092026-143120_rounds100_no-self-play.csv` — No self-play
- `tournament_02092026-143135_rounds50_unknown-horizon_no-self-play.csv` — All flags

This allows multiple tournaments to run without overwriting previous results.

## Using Results

1. **Open in Excel:** Double-click the CSV file to open in your spreadsheet app
2. **Analyze:** Sort by `points_scored` to see which agents won
3. **Compare:** Use conditional counts to understand agent behavior
4. **Archive:** Rename files to keep historical results (e.g., `tournament_cohort_2024.csv`)

## Git Notes

This folder is in `.gitignore` — tournament results are not committed to git. Generate them locally as needed.

See [../docs/requirements.md](../docs/requirements.md) for CSV schema details.
