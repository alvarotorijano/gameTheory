# Tests Folder

This folder contains the test suite for the Iterated Prisoner's Dilemma project.

## Structure

```
tests/
├── README.md                      # This file
├── run_tests.py                   # Convenience wrapper to run all tests
│
├── test_game_core.py              # Tests for game engine & scoring
├── test_agents.py                 # Tests for example agents
├── test_match_runner.py           # Tests for match runner CLI
├── test_tournament_runner.py      # Tests for tournament runner CLI
└── test_agent_collector.py        # Tests for agent discovery & import
```

## Running Tests

### Run All Tests
```bash
python run_tests.py
```

### Run with Pytest Directly
```bash
pytest tests/ -v
pytest tests/test_agents.py -v    # Run specific test file
pytest tests/test_agents.py::TestCopycatAgent -v  # Run specific test class
```

## Test Coverage

| File | Coverage |
|---|---|
| `test_game_core.py` | Payoff scoring, engine, agent base class |
| `test_agents.py` | Example agent behavior (random, copycat, second_chance) |
| `test_match_runner.py` | CLI output, ida/vuelta/average calculations |
| `test_tournament_runner.py` | CSV schema, column types, value correctness |
| `test_agent_collector.py` | Agent discovery, file copying, exclusion logic |

## Requirements

- **pytest** (specified in `requirements.txt`)
- Python 3.7+
- Virtual environment activated

## Implementation Status

- [ ] `test_game_core.py` — To be implemented
- [ ] `test_agents.py` — To be implemented
- [ ] `test_match_runner.py` — To be implemented
- [ ] `test_tournament_runner.py` — To be implemented
- [ ] `test_agent_collector.py` — To be implemented
- [ ] `run_tests.py` — To be implemented

## Test Philosophy

- **Comprehensive:** All major functionality tested
- **Isolated:** Each test is independent
- **Fast:** Tests run quickly for fast feedback
- **Readable:** Test names describe what they test

See [`../docs/requirements.md`](../docs/requirements.md) for complete test specifications.
