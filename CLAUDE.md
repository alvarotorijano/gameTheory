# Project Instructions & Constraints

This document captures the durable rules and constraints for the Iterated Prisoner's Dilemma
course project. These rules override any default behavior and must be followed exactly.

## Code & Documentation Language

- **All code** (function names, variables, imports, comments, docstrings, log output, CLI messages)
  must be written in **English**.
- Documentation that is historical (e.g., `docs/original_prompt.md`) may remain in its original language
  for archival purposes.

## Git Operations

- **Claude must never perform git write operations** in this repository.
  - No `git add`, `git commit`, `git push`, or any other commands that modify git state.
  - The user retains all responsibility for git operations and repository management.
  - This is a hard constraint, even if it would be convenient for the workflow.

## Code Quality

- **Every function and method must have a docstring.**
  - Docstrings should explain the purpose, parameters, return value, and any notable behavior.
  - Keep docstrings concise; prefer clarity over verbosity.
- **Implementation approach:**
  - Always create an implementation plan and get user approval before writing code.
  - Don't add features or abstractions beyond what the specification requires.
  - Avoid unnecessary error handling, fallbacks, or validation for impossible scenarios.

## Architecture & Structure

- **Run locally only.** No external services or cloud dependencies.
- **Agent isolation:** Each agent is a separate module/file, allowing students to add their own
  without modifying core code.
- **Configuration externalization:** Scoring payoffs and round limits are defined in `config.json`
  and loaded at runtime, not hard-coded.

## Semantics

- **Ida and Vuelta:** The two-leg match structure where the order of player precedence (for
  record-keeping and CSV output) alternates:
  - **Ida:** Agent A is Player 1, Agent B is Player 2.
  - **Vuelta:** Agent B is Player 1, Agent A is Player 2.
  - The game itself is simultaneous; these labels are for consistent CSV/output ordering only.
- **Unknown Horizon:** When an agent is told `num_rounds=None`, it does not know how many rounds
  it will play. The engine still runs a finite number of rounds (randomly chosen from a configured
  range in `config.json`), but the agent never learns the actual count.
- **Moves:** Represented as simple strings: `"C"` for cooperate, `"D"` for defect.

## Testing & Verification

- All functionality must have corresponding tests in the `tests/` folder.
- Tests must use pytest.
- A `tests/run_tests.py` convenience wrapper should exist to run the full test suite.
- Tests should verify:
  - Payoff scoring correctness.
  - Example agents' move sequences against known histories.
  - Match runner output (ida, vuelta, averages).
  - Tournament runner CSV schema and plausible values.
  - Agent discovery and collection logic.
