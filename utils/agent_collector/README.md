# Agent Collector

Import student agents from GitHub repositories or local files into the main agents folder.

## Purpose

When students submit their agents via git repos or files, Agent Collector:
- Clones git repositories
- Discovers Agent subclasses using AST parsing
- Copies new agents to the main `agents/` folder
- Avoids overwriting example agents
- Prevents duplicate imports

## Usage

**Run from the project root directory:**

```bash
python utils/agent_collector/collect_agents.py --sources <JSON_FILE> [OPTIONS]
```

## Options

- `--sources FILE` — JSON file listing student submissions (required)
- `--dry-run` — Show what would happen without actually copying
- `--verbose` — Print detailed progress

## Sources JSON Format

Create a JSON file with an array of student submissions:

```json
[
  {
    "student": "juan_perez",
    "source": "https://github.com/juan_perez/prisoner-dilemma-agent.git"
  },
  {
    "student": "maria_lopez",
    "source": "https://github.com/maria_lopez/my_strategy.git"
  },
  {
    "student": "carlos_sanchez",
    "source": "/home/prof/submissions/carlos_agent.py"
  }
]
```

## Examples

### Dry Run (preview without importing)
```bash
python utils/agent_collector/collect_agents.py --sources sources.json --dry-run
```

Output:
```
[juan_perez] https://github.com/juan_perez/prisoner-dilemma-agent.git
  Cloning https://github.com/juan_perez/prisoner-dilemma-agent.git...
  [DRY RUN] Would copy: my_agent -> juan_perez_my_agent

[maria_lopez] https://github.com/maria_lopez/my_strategy.git
  Cloning https://github.com/maria_lopez/my_strategy.git...
  [DRY RUN] Would copy: strategy -> maria_lopez_strategy

============================================================
Collection complete!
  Total agents imported: 2
  Dry run: True
============================================================
```

### Actual Import
```bash
python utils/agent_collector/collect_agents.py --sources sources.json
```

## Agent Discovery

Collector uses AST parsing to find agents, so it's robust to:
- Non-standard folder/file names
- Multiple agents in one submission
- Different file organization

It automatically:
- Finds all classes inheriting from `Agent`
- Excludes example agents (random_agent, copycat_agent, second_chance_agent)
- Renames imported agents to avoid collisions: `<student_name>_<agent_name>`

## Example: After Importing

Before:
```
agents/
├── random_agent/
├── copycat_agent/
└── second_chance_agent/
```

After collecting from Juan and Maria:
```
agents/
├── random_agent/
├── copycat_agent/
├── second_chance_agent/
├── juan_perez_my_agent/
└── maria_lopez_strategy/
```

## Caching

For git repositories, Collector caches clones in `._cache/` to avoid re-downloading. If a repo is already cached, you'll be asked whether to reuse it.

## Integration with Tournament

Once agents are imported, use Tournament Runner to include them:

```bash
python utils/agent_collector/collect_agents.py --sources sources.json
python utils/tournament_runner/run_tournament.py
```

The tournament will automatically discover and include all imported agents.

## Troubleshooting

**"No agents found in [path]"**
- Verify the student's submission contains a valid `agent.py` file
- Check that the Agent class is properly named and inherits from `Agent`

**"Repo already cached at ... Reuse?"**
- Choose `y` to reuse or `n` to re-download
- Useful if the student updated their repo

**"[student] already exists, skipping"**
- That agent is already in the `agents/` folder
- Delete it if you want to re-import

## Student Submission Guidelines

Students should submit:
- A git repository URL, OR
- A local file/folder path

Structure (recommended):
```
submission/
├── agent.py      (contains Agent subclass)
└── README.md     (optional strategy description)
```

Example `agent.py`:
```python
from utils.game_core import Agent, COOPERATE, DEFECT

class MyStrategy(Agent):
    def play(self, own_history, opponent_history):
        if not opponent_history:
            return COOPERATE
        return opponent_history[-1]
```

## See Also

- `match_runner/` — Test individual agents
- `tournament_runner/` — Run tournament with all agents
- `docs/student_guide.md` — Student submission guide
