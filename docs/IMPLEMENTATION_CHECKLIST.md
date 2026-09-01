# Implementation Phase Checklist

This checklist tracks the implementation of the Iterated Prisoner's Dilemma project.

---

## Phase 1: Core Library (`utils/game_core/`) - FOUNDATION

**Status:** ⏳ Pending  
**Commits:** Should be 1-2 commits (one per module or all together)

- [ ] `__init__.py` — Package initialization
- [ ] `moves.py` — COOPERATE and DEFECT constants
- [ ] `agent_base.py` — Abstract Agent base class
- [ ] `payoff.py` — Config loader and score_round() function
- [ ] `engine.py` — Match engine (run_leg function)
- [ ] `agent_loader.py` — AST-based agent discovery
- [ ] `README.md` — Library documentation

**Depends on:** None  
**Required by:** Agents, CLI scripts, tests  
**Verification:**
```bash
python -c "from utils.game_core import Agent, COOPERATE, DEFECT"
```

---

## Phase 2: Example Agents (`agents/`) - TEMPLATES

**Status:** ⏳ Pending  
**Commits:** 1 commit per agent (3 commits total)

### 2.1 Random Agent
- [ ] `agents/random_agent/agent.py`
- [ ] `agents/random_agent/README.md` (with Mermaid diagram)

### 2.2 Copycat Agent (Tit-for-Tat)
- [ ] `agents/copycat_agent/agent.py`
- [ ] `agents/copycat_agent/README.md` (with Mermaid diagram)

### 2.3 Second Chance Agent
- [ ] `agents/second_chance_agent/agent.py`
- [ ] `agents/second_chance_agent/README.md` (with Mermaid diagram)

**Depends on:** Phase 1 (core library)  
**Required by:** CLI scripts, tests  
**Verification:**
```bash
python utils/match_runner/run_match.py random_agent copycat_agent --rounds 50
```

---

## Phase 3: CLI Scripts (`utils/`) - TOOLS

**Status:** ⏳ Pending  
**Commits:** 1 commit per tool (3 commits total)

### 3.1 Match Runner
- [ ] `utils/match_runner/run_match.py`
- [ ] `utils/match_runner/README.md`

### 3.2 Tournament Runner
- [ ] `utils/tournament_runner/run_tournament.py`
- [ ] `utils/tournament_runner/README.md`

### 3.3 Agent Collector
- [ ] `utils/agent_collector/collect_agents.py`
- [ ] `utils/agent_collector/README.md`
- [ ] `utils/agent_collector/sources_example.json`

**Depends on:** Phase 1 (core library), Phase 2 (agents to test with)  
**Required by:** Tests, manual verification  
**Verification:**
```bash
python utils/match_runner/run_match.py random_agent copycat_agent --rounds 50
python utils/tournament_runner/run_tournament.py
```

---

## Phase 4: Test Suite (`tests/`) - VERIFICATION

**Status:** ⏳ Pending  
**Commits:** 1-2 commits (can group related tests or split by module)

- [ ] `test_game_core.py` — Payoff, engine, agent base
- [ ] `test_agents.py` — Random, copycat, second_chance agents
- [ ] `test_match_runner.py` — Match runner CLI & math
- [ ] `test_tournament_runner.py` — Tournament CSV & logic
- [ ] `test_agent_collector.py` — Agent discovery & import
- [ ] `run_tests.py` — Pytest wrapper
- [ ] `README.md` — Testing guide

**Depends on:** Phase 1, 2, 3 (all components to test)  
**Verification:**
```bash
python tests/run_tests.py
pytest tests/ -v
```

---

## Phase 5: Manual Testing & Verification

**Status:** ⏳ Pending

- [ ] Run all tests: `python tests/run_tests.py` (all pass)
- [ ] Single match: `python utils/match_runner/run_match.py copycat_agent random_agent --rounds 50`
- [ ] Tournament: `python utils/tournament_runner/run_tournament.py` (CSV generated)
- [ ] Check CSV output in `results/tournament.csv`
- [ ] Verify unknown horizon: `python utils/match_runner/run_match.py copycat_agent random_agent --unknown-horizon`

---

## Commit Strategy

**Recommended commit messages:**

```
Phase 1: Core game library (moves, agent_base, payoff, engine, agent_loader)
Phase 2.1: Random agent (example & baseline)
Phase 2.2: Copycat agent (tit-for-tat template)
Phase 2.3: Second chance agent (forgiving strategy)
Phase 3.1: Match runner CLI tool
Phase 3.2: Tournament runner CLI tool
Phase 3.3: Agent collector CLI tool
Phase 4: Test suite (all test files)
```

Or combine into fewer commits if preferred:
```
Phase 1: Core game library
Phase 2: All example agents
Phase 3: All CLI tools
Phase 4: All tests
```

---

## Implementation Order

**Strictly follow this order** (each phase depends on previous phases):

1. ✅ **Phase 1** (core library) — Foundation for everything
2. **Phase 2** (agents) — Can test core library
3. **Phase 3** (CLI tools) — Uses core library + agents
4. **Phase 4** (tests) — Verifies everything
5. **Phase 5** (manual testing) — End-to-end validation

---

## Notes

- Each phase should be committed separately (or as specified above)
- Tests should pass after each phase
- Documentation (README.md files) included with each component
- All code must follow `CLAUDE.md` style guidelines
- Every function must have a docstring

---

**Status:** Ready to begin Phase 1 implementation

See `docs/requirements.md` for detailed technical specifications.
