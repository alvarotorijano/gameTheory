# Iterated Prisoner's Dilemma: Course Project

A tournament platform where students implement strategies for the Iterated Prisoner's Dilemma and compete against each other.

---

## 📁 Project Structure

```
gameTheory/
├── README.md                  # This file (entry point)
├── config.json                # Game configuration (payoffs, round counts)
├── requirements.txt           # Python dependencies (pytest only)
├── .gitignore                 # Git exclusions
├── agents/                    # Student agents (add yours here)
├── utils/                     # Core library & CLI tools (will be implemented)
├── tests/                     # Test suite (will be implemented)
├── results/                   # Generated tournament CSVs (gitignored)
└── docs/                      # Complete documentation
    ├── README.md              # Documentation index (START HERE)
    ├── README_MAIN.md         # Full project overview
    ├── requirements.md        # Technical specifications
    ├── CLAUDE.md              # Project rules & style guidelines
    ├── prompts.md             # User prompts (historical record)
    ├── game_rules.md          # Game mechanics explained
    ├── architecture.md        # Technical design & components
    ├── student_guide.md       # How to write your first agent
    ├── installation.md        # Python environment setup
    ├── implementation_plan.md # Development blueprint
    └── [more docs...]         # Additional documentation
```

---

## 🚀 Quick Start

### For Students
1. **Read:** [`docs/game_rules.md`](docs/game_rules.md) to understand the game
2. **Follow:** [`docs/student_guide.md`](docs/student_guide.md) to write your first agent
3. **Test:** `python utils/match_runner/run_match.py my_agent random_agent --rounds 50`

### For Instructors
1. **Collect:** Student agent submissions using `collect_agents.py`
2. **Run:** `python utils/tournament_runner/run_tournament.py`
3. **Analyze:** Open the generated CSV to see results

### For Developers
1. **Read:** [`docs/requirements.md`](docs/requirements.md) for technical specs
2. **Check:** [`docs/CLAUDE.md`](docs/CLAUDE.md) for project rules & style
3. **Review:** [`docs/architecture.md`](docs/architecture.md) for design details

---

## 📚 Documentation

**Start here:** [`docs/README.md`](docs/README.md) — Complete documentation index

Key documents:
- **[Project Overview](docs/README_MAIN.md)** — Full project description
- **[Game Rules](docs/game_rules.md)** — How the game works (ida, vuelta, payoffs)
- **[Technical Requirements](docs/requirements.md)** — What needs to be implemented
- **[Student Guide](docs/student_guide.md)** — Write your first strategy
- **[Installation](docs/installation.md)** — Python setup (venv, pyenv)
- **[Project Rules](docs/CLAUDE.md)** — Constraints, style, best practices
- **[Architecture](docs/architecture.md)** — Technical design & components

---

## ⚙️ Installation

```bash
python -m venv .venv

# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# macOS/Linux:
source .venv/bin/activate

# Install dependencies:
pip install -r requirements.txt
```

See [`docs/installation.md`](docs/installation.md) for detailed instructions.

---

## 📝 Project Status

**Documentation Phase:** ✅ Complete  
**Implementation Phase:** ⏳ Pending

All project rules, specifications, and documentation are finalized. Ready to implement the core library, agents, tools, and tests.

---

## 📖 More Information

For any questions or to learn more, see the documentation in [`docs/`](docs/) folder.
