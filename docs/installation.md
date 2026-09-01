# Installation Guide

This project requires **Python 3.7+** and uses a virtual environment to isolate dependencies.
Only one external package is needed: `pytest` (for running tests).

---

## Quick Start (All Platforms)

### 1. Install Python 3.7+

**Windows:**
- Download from https://www.python.org/downloads/
- During installation, **check "Add Python to PATH"**.
- Verify: open PowerShell and run `python --version`.

**macOS/Linux:**
- Use your package manager or https://www.python.org/downloads/
- Verify: `python3 --version`

### 2. Create a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Git Bash / WSL):**
```bash
python -m venv .venv
source .venv/Scripts/activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` at the start of your terminal prompt when active.

### 3. Install Dependencies

With the virtual environment activated:
```bash
pip install -r requirements.txt
```

This installs `pytest` (only external dependency).

### 4. Verify Installation

```bash
python --version
pip list
```

You should see `pytest` in the list.

---

## (Optional) Using pyenv for Version Management

If you have multiple Python versions or want to manage versions across projects, use **pyenv**.

### Windows (pyenv-win)

#### Installation

1. Open PowerShell **as Administrator**.
2. Run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   # Then:
   git clone https://github.com/pyenv-win/pyenv-win.git "$HOME\.pyenv"
   ```
3. Add pyenv to your PATH:
   - Open "Environment Variables" (search in Start menu).
   - Add `%USERPROFILE%\.pyenv\pyenv-win\bin` and `%USERPROFILE%\.pyenv\pyenv-win\shims`.
   - Close and reopen PowerShell.
4. Verify: `pyenv --version`

#### Usage

```powershell
# List available versions
pyenv install --list

# Install Python 3.11
pyenv install 3.11.0

# Set local version for this project
pyenv local 3.11.0

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### macOS/Linux (pyenv)

#### Installation

**macOS (Homebrew):**
```bash
brew install pyenv
```

**Linux (Ubuntu/Debian):**
```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
exec $SHELL
```

#### Usage

```bash
# List available versions
pyenv versions

# Install Python 3.11
pyenv install 3.11.0

# Set local version for this project
pyenv local 3.11.0

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Troubleshooting

### Issue: "python: command not found"
- **Windows:** Make sure Python is in your PATH. Reinstall Python and check "Add Python to PATH".
- **macOS/Linux:** Use `python3` instead of `python`.

### Issue: "venv module not found"
- Python 3.3+ includes `venv` by default. If missing, install python3-venv:
  ```bash
  sudo apt-get install python3-venv  # Ubuntu/Debian
  brew install python@3.11           # macOS
  ```

### Issue: Virtual environment not activating
- **Windows (PowerShell):** You may need to allow script execution:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- Try activating again: `.\.venv\Scripts\Activate.ps1`

### Issue: "pip: command not found"
- Make sure your virtual environment is **activated** (you should see `(.venv)` in your prompt).
- If not, run the activate command for your OS (see Quick Start section 2).

### Issue: pytest not found after install
- Verify pytest is installed: `pip list`
- If not in the list, run `pip install pytest` explicitly.
- Try running tests with `python -m pytest tests/` instead of `pytest tests/`.

---

## Verifying the Setup

Once installation is complete, run:

```bash
python tests/run_tests.py
```

Or directly with pytest:

```bash
pytest tests/ -v
```

You should see all tests pass (or display their status).

---

## Deactivating the Virtual Environment

When you're done working, deactivate the virtual environment:

**All platforms:**
```bash
deactivate
```

You can reactivate it anytime by running the activation command again (see Quick Start section 2).

---

## Next Steps

1. Read the [README.md](../README.md) for project overview and usage.
2. Follow the [Student Guide](student_guide.md) to write your first agent.
3. Test locally: `python utils/match_runner/run_match.py copycat_agent random_agent --rounds 50`
