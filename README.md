# Iterated Prisoner's Dilemma: Course Project

A tournament platform where students implement strategies for the Iterated Prisoner's Dilemma and compete against each other.

---

## 🚀 Quick Start Guide

Follow these steps to clone the repository and run your first match between example agents.

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/gameTheory.git
cd gameTheory
```

### Step 2: Set Up Python Environment

**Option A: Basic Setup (venv)**

```bash
python -m venv .venv

# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# macOS/Linux:
source .venv/bin/activate

# Install dependencies:
pip install -r requirements.txt
```

**Option B: Using pyenv (Optional)**

For detailed pyenv setup instructions, see [`docs/installation.md`](docs/installation.md)

### Step 3: Run Your First Match

The project comes with three example agents. Let's watch them compete:

```bash
python utils/match_runner/run_match.py copycat_agent random_agent --rounds 50
```

**Expected output:**
```
============================================================
First Leg: copycat_agent (Player 1) vs random_agent (Player 2)
Rounds: 50
============================================================

First Leg Results:
  copycat_agent: 145 points
  random_agent: 68 points

============================================================
Second Leg: random_agent (Player 1) vs copycat_agent (Player 2)
Rounds: 50
============================================================

Second Leg Results:
  random_agent: 72 points
  copycat_agent: 143 points

============================================================
SUMMARY
============================================================

copycat_agent:
  First Leg:  145 points
  Second Leg: 143 points
  Average: 144.0 points

random_agent:
  First Leg:  68 points
  Second Leg: 72 points
  Average: 70.0 points

============================================================
RESULT: copycat_agent WINS by 74.0 points on average
============================================================
```

### Step 4: Run a Full Tournament

Play all agents against each other and generate a CSV with detailed statistics:

```bash
python utils/tournament_runner/run_tournament.py --verbose
```

This creates `results/tournament.csv` with comprehensive statistics for each agent.

### Step 5: Write Your First Agent

Follow the step-by-step guide in [`docs/student_guide.md`](docs/student_guide.md):

1. Copy `agents/copycat_agent/` to `agents/my_agent/`
2. Edit `my_agent/agent.py` to implement your strategy
3. Test against example agents: `python utils/match_runner/run_match.py my_agent random_agent --rounds 50`
4. Update `my_agent/README.md` with your strategy description (include a Mermaid diagram)

---

## 📖 Full Documentation

For detailed information, see the documentation folder:

### For Students
- **[Student Guide](docs/student_guide.md)** — Step-by-step: write and test your first agent
- **[Game Rules](docs/game_rules.md)** — How the game works, payoff matrix, first leg / second leg structure
- **[Installation Guide](docs/installation.md)** — Detailed environment setup

### For Instructors
- **[Architecture Guide](docs/architecture.md)** — Technical design, components, and CLI tools
- **[How to Run Tournaments](docs/architecture.md#tournament-runner)** — Collect student agents and run tournaments
- **[Agent Collector Guide](utils/agent_collector/README.md)** — Import student agents from repositories

### For Developers
- **[Technical Requirements](docs/requirements.md)** — Complete technical specifications
- **[Implementation Plan](docs/implementation_plan.md)** — Development blueprint
- **[Project Rules](CLAUDE.md)** — Code style, constraints, best practices

### Reference
- **[Documentation Index](docs/README.md)** — Complete list of all documentation
- **[Original Specification](docs/original_prompt.md)** — Original requirements (Spanish)
- **[Development History](docs/prompts.md)** — All prompts that shaped this project

---

## 🎮 The Three Example Agents

The repository includes three example agents to learn from:

### 1. Random Agent
**Strategy:** Play random moves (50% cooperate, 50% defect)  
**Purpose:** Baseline test opponent  
**File:** `agents/random_agent/`  
**README:** Includes Mermaid decision tree

### 2. Copycat Agent (Template for Students)
**Strategy:** Tit-for-tat — cooperate on round 1, then copy opponent's last move  
**Purpose:** Famous strategy and template for student submissions  
**File:** `agents/copycat_agent/`  
**README:** Includes Mermaid decision tree  
**Note:** This is the recommended starting point for students

### 3. Second Chance Agent
**Strategy:** Cooperate by default; forgive first defection; retaliate only on second  
**Purpose:** Demonstrate stateful strategy with memory  
**File:** `agents/second_chance_agent/`  
**README:** Includes Mermaid state machine diagram

---

## 🛠️ Available CLI Tools

### Match Runner
Play two agents head-to-head (first leg + second leg):

```bash
python utils/match_runner/run_match.py <agent1> <agent2> [--rounds N] [--unknown-horizon]
```

See [`utils/match_runner/README.md`](utils/match_runner/README.md) for details.

### Tournament Runner
Run round-robin tournament with all agents:

```bash
python utils/tournament_runner/run_tournament.py [--rounds N] [--verbose]
```

Outputs CSV to `results/tournament.csv`  
See [`utils/tournament_runner/README.md`](utils/tournament_runner/README.md) for details.

### Agent Collector
Import student agents from repositories or files:

```bash
python utils/agent_collector/collect_agents.py --sources sources.json
```

See [`utils/agent_collector/README.md`](utils/agent_collector/README.md) for details.

---

## 📁 Project Structure

```
gameTheory/
├── agents/                    # Agent implementations
│   ├── random_agent/          # Example: random moves
│   ├── copycat_agent/         # Example: tit-for-tat (student template)
│   └── second_chance_agent/   # Example: forgiving strategy
│
├── utils/                     # Core library & CLI tools
│   ├── game_core/             # Game engine library
│   ├── match_runner/          # CLI: play two agents
│   ├── tournament_runner/     # CLI: run tournament
│   └── agent_collector/       # CLI: import student agents
│
├── docs/                      # Complete documentation
├── tests/                     # Test suite (in progress)
├── results/                   # Tournament outputs (generated)
│
├── README.md                  # This file
├── CLAUDE.md                  # Project rules & style
├── config.json                # Game configuration
└── requirements.txt           # Python dependencies
```

---

## 📋 Key Concepts

- **First Leg:** Agent A vs Agent B, with A as Player 1
- **Second Leg:** Agent B vs Agent A, with B as Player 1  
  (This fairness mechanism accounts for any first-mover advantages)
- **Match:** Complete competition = First Leg + Second Leg + Average scoring
- **Tournament:** Round-robin where every agent plays every other agent
- **Unknown Horizon:** Agents see `num_rounds=None`; actual match length is random

---

## 🤝 Getting Help

- **I'm a student:** Start with [`docs/student_guide.md`](docs/student_guide.md)
- **I'm running a tournament:** See [`utils/tournament_runner/README.md`](utils/tournament_runner/README.md)
- **I need to set up the environment:** See [`docs/installation.md`](docs/installation.md)
- **I want to understand the game:** See [`docs/game_rules.md`](docs/game_rules.md)
- **Full documentation index:** See [`docs/README.md`](docs/README.md)

---

## 📝 Project Status

- ✅ **Core Library** — Complete (game engine, agent interface, payoff scoring)
- ✅ **Example Agents** — Complete (random, copycat, second_chance)
- ✅ **CLI Tools** — Complete (match_runner, tournament_runner, agent_collector)
- ⏳ **Test Suite** — In progress
