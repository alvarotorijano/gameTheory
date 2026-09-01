# Project Instructions & Constraints

This document captures the durable rules and constraints for the Iterated Prisoner's Dilemma
course project. These rules override any default behavior and must be followed exactly.

## File Paths

- **Never commit or reference absolute/local machine paths** in any project file.
- **Always use relative paths** from the project root.
- Example ✅: `./utils/game_core/agent_base.py`, `docs/game_rules.md`
- Example ❌: `c:\Users\The_menda14\Desktop\ICAI\gameTheory\utils\game_core\agent_base.py`
- This ensures the project is portable and works on any machine/environment.

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

## Style Guidelines

### Python Code Style

- **Naming:** Use `snake_case` for functions and variables, `PascalCase` for classes.
- **Imports:** Organize as: stdlib → third-party → local imports (one blank line between groups).
- **Line length:** Prefer under 100 characters; break long lines for readability.
- **Type hints:** Use type annotations for function signatures (e.g., `def play(...) -> str:`).
- **Comments:** Avoid obvious comments. Comment *why*, not *what*.
  - ✅ `# Random choice prevents predictable agent behavior`
  - ❌ `# Pick a random move`

### Docstring Format

Every function must have a docstring. Use this format:

```python
def function_name(param1: Type, param2: Type) -> ReturnType:
    """
    Brief description of what the function does.
    
    Parameters:
        param1: Description of param1.
        param2: Description of param2.
    
    Returns:
        Description of return value.
    """
```

Keep docstrings **concise and complete**. One or two sentences for the description; list parameters and returns even if brief.

### Folder & File Organization

- **One agent per folder:** `agents/<agent_name>/agent.py` (lowercase, underscore-separated).
- **One tool per folder:** `utils/<tool_name>/run_<tool_name>.py` + `README.md`.
- **Tests mirror structure:** `tests/test_<component>.py` for each major component.
- **No deeply nested folders:** Maximum 3 levels (e.g., `utils/game_core/agent_loader.py` is ok; `utils/a/b/c/d` is not).

### CLI Scripts

- Use `argparse` for command-line argument parsing.
- Provide `--help` with clear usage examples.
- Exit with status code 0 on success, 1 on error.
- Print results to stdout; errors to stderr.

### CSV Output

- Use CSV format (comma-separated, quoted strings for safety).
- Include headers (column names as first row).
- One row per logical unit (one row per agent per leg in tournament results).
- Ensure consistency: same column order, same column types across all rows.

### Error Handling

- **Do not silence errors.** Let exceptions propagate or log them explicitly.
- **Do not validate impossible scenarios.** Trust framework contracts and types.
- **Validate only at boundaries:** CLI inputs, external files, user-provided agent discovery.
- **Use assertions for internal invariants:** `assert len(history) <= num_rounds`.

## Documentation Standards

### File Structure
- Every major component has a `README.md` explaining its purpose and usage.
- Each script has example CLI invocations in its README.
- Technical docs are in `docs/`; prose is user-facing.

### Content Quality
- **Accuracy:** Docs must match the code. Update docs when code changes.
- **Completeness:** Explain *what*, *why*, and *how*.
- **Clarity:** Use plain language. Define jargon (e.g., "ida: first leg of the match").
- **Examples:** Provide realistic examples in every README and guide.

### Relative References
- Always use relative paths in documentation: `./utils/game_core/agent_base.py`, `docs/game_rules.md`.
- Do not reference absolute machine paths (e.g., no `C:\Users\...`).

## Workflow & Versioning

### Implementation Phases
1. **Planning:** Create detailed plan, document requirements, get approval.
2. **Implementation:** Write code (core library → agents → tools → tests).
3. **Testing:** Run full test suite; verify manually with example matchups.
4. **Documentation:** Finalize README/docstring; ensure accuracy.

### Prompt Tracking
- All user prompts are saved in `prompts.md` (verbatim).
- Each new prompt is added with timestamp and language.
- Prompts form the historical record of requirements.

### Avoiding Drift
- Docstrings describe *why*, not *what* the code does.
- Comments explain non-obvious logic or constraints.
- No comments needed for self-explanatory code (good naming + clear structure = self-documenting).

## Project Assumptions

- Students have basic Python knowledge but may not understand game theory or advanced patterns.
- Agents will be submitted with various code styles and quality levels; the system must discover them robustly (AST-based discovery handles this).
- The instructor may adjust payoff values and round counts; all such values go in `config.json`.
- No internet or external services are available during tournament runs (everything is local).
