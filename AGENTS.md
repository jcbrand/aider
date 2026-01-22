# AGENTS.md - Aider Codebase Guide

This document provides guidance for AI coding agents working in the Aider repository.

## Project Overview

Aider is an AI pair programming CLI tool written in Python. It enables developers to pair program with LLMs directly in their terminal.

- **Package name**: `aider-chat` (PyPI)
- **Python versions**: 3.10, 3.11, 3.12
- **Entry point**: `aider.main:main`

## Build & Development Commands

### Setup

```bash
python -m venv /path/to/venv
source /path/to/venv/bin/activate
pip install -e . && pip install -r requirements.txt && pip install -r requirements/requirements-dev.txt
pre-commit install
```

### Testing

```bash
pytest                                                    # Run all tests
pytest tests/basic/test_coder.py                          # Run specific test file
pytest tests/basic/test_coder.py::TestCoder::test_method  # Run single test
pytest -v tests/basic/test_coder.py                       # Verbose output
```

### Linting & Formatting

```bash
pre-commit run --all-files                    # Run all pre-commit hooks
black --line-length 100 --preview <file>      # Format code
isort --profile black <file>                  # Sort imports
flake8 <file>                                 # Lint
```

### Dependency Management

```bash
./scripts/pip-compile.sh            # Regenerate requirements.txt from .in sources
./scripts/pip-compile.sh --upgrade  # Upgrade all dependencies
```

## Code Style Guidelines

### Formatting Rules

- **Line length**: 100 characters maximum
- **Formatter**: Black with `--preview` flag
- **Import sorting**: isort with `profile=black`
- **Linter**: flake8 (ignores E203, W503)

### Type Hints

**Do not use type hints.** The project explicitly avoids type annotations.

### Import Organization

Order: stdlib → third-party → aider imports → relative imports

```python
import os
from pathlib import Path

import git
from rich.console import Console

from aider import models, utils
from aider.coders import Coder

from .dump import dump  # noqa: F401
```

### Naming Conventions

- **Classes**: PascalCase (`Coder`, `InputOutput`, `GitRepo`)
- **Functions/methods**: snake_case (`get_git_root`, `allowed_to_edit`)
- **Constants**: UPPER_SNAKE_CASE (`DEFAULT_MODEL_NAME`, `RETRY_TIMEOUT`)
- **Private members**: Leading underscore (`_load`)

### Error Handling

```python
# Custom exceptions inherit from ValueError or Exception
class UnknownEditFormat(ValueError):
    def __init__(self, edit_format, valid_formats):
        self.edit_format = edit_format
        super().__init__(f"Unknown edit format {edit_format}")

# Optional imports with fallback
try:
    import git
except ImportError:
    git = None

# Tuple exception catching
try:
    repo = git.Repo(search_parent_directories=True)
except (git.InvalidGitRepositoryError, FileNotFoundError):
    return None
```

### Testing Patterns

```python
class TestCoder(unittest.TestCase):
    def setUp(self):
        self.GPT35 = Model("gpt-3.5-turbo")
        self.webbrowser_patcher = patch("aider.io.webbrowser.open")
        self.mock_webbrowser = self.webbrowser_patcher.start()

    def test_allowed_to_edit(self):
        with GitTemporaryDirectory():
            repo = git.Repo()
            fname = Path("added.txt")
            fname.touch()
            # ... test logic
            self.assertTrue(coder.allowed_to_edit("added.txt"))
```

## Project Structure

```
aider/
├── aider/              # Main package
│   ├── coders/         # Coder implementations (edit formats)
│   ├── main.py         # CLI entry point
│   ├── commands.py     # In-chat slash commands
│   ├── models.py       # LLM model handling
│   ├── io.py           # Input/output handling
│   └── repo.py         # Git repository operations
├── tests/              # Test suite
│   ├── basic/          # Core tests
│   ├── browser/        # Browser tests
│   └── help/           # Help system tests
├── benchmark/          # Performance benchmarks
├── requirements/       # Dependency files (.in sources, .txt compiled)
└── scripts/            # Utility scripts
```

## CI/CD

Tests run on GitHub Actions for Ubuntu and Windows (Python 3.10, 3.11, 3.12).
Pre-commit hooks validated via `.github/workflows/pre-commit.yml`.

## Common Patterns

### Optional Dependencies

```python
try:
    from babel import Locale
except ImportError:
    Locale = None
```

### Debug Dumps

```python
from aider.dump import dump  # noqa: F401
```
