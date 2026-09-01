# Documentation Index

This folder contains all documentation for the Iterated Prisoner's Dilemma course project.

## Files

### Project Management
- **[implementation_plan.md](implementation_plan.md)** — Development blueprint approved before coding started. Lists all deliverables, folder structure, and verification steps.
- **[original_prompt.md](original_prompt.md)** — The original user prompt in Spanish (historical record).

### For Students
- **[student_guide.md](student_guide.md)** — Step-by-step guide to writing your first agent. **Start here if you're a student.**
- **[game_rules.md](game_rules.md)** — Detailed explanation of the Prisoner's Dilemma payoff matrix, ida/vuelta structure, and tournament rules.

### For Instructors & Developers
- **[architecture.md](architecture.md)** — Technical design: folder layout, component descriptions, agent interface, CLI tools, and configuration.
- **[installation.md](installation.md)** — Python environment setup: venv, pyenv (optional), dependency installation.

---

## Quick Navigation

### "I'm a student and want to write an agent"
1. Read [game_rules.md](game_rules.md) to understand how the game works.
2. Follow [student_guide.md](student_guide.md) to write your first strategy.
3. Test it locally using the match runner.

### "I'm an instructor and want to run a tournament"
1. Read [architecture.md](architecture.md) to understand the system.
2. Collect student agents using `collect_agents.py` (described in architecture).
3. Run `tournament_runner.py` to generate results.
4. Open the CSV to analyze performance.

### "I'm a developer and want to understand the system"
1. Read [implementation_plan.md](implementation_plan.md) for the overall design.
2. Read [architecture.md](architecture.md) for technical details.
3. Check the code comments and docstrings in `utils/` and `agents/`.

---

## Key Concepts

- **Ida & Vuelta:** The two-leg match structure. See [game_rules.md](game_rules.md).
- **Agent Interface:** All agents inherit from `Agent` and implement `play()`. See [architecture.md](architecture.md).
- **Tournament CSV:** Detailed statistics per agent per match. Schema in [architecture.md](architecture.md).
- **Configuration:** Game payoffs and round counts in `config.json` (root). See [architecture.md](architecture.md).

---

## Documentation Quality Notes

All documentation was written to be:
- **Complete:** Covers all major concepts and workflows.
- **Accessible:** Uses clear language and examples for different audiences (students, instructors, developers).
- **Accurate:** Reflects the implementation plan and project constraints.
- **Indexable:** Links and references make navigation easy.
