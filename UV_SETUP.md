# UV Setup Guide

This project uses [uv](https://docs.astral.sh/uv/) for fast and reliable Python package management with Python 3.12.

## Quick Start

### Prerequisites

Install `uv` if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or on macOS with Homebrew:
```bash
brew install uv
```

### Setup the Project

1. **Create virtual environment and install dependencies:**
   ```bash
   uv sync
   ```

2. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

## Common Commands

### Managing Dependencies

**Install a new dependency:**
```bash
uv add package-name
```

**Install a development dependency:**
```bash
uv add --dev package-name
```

**Remove a dependency:**
```bash
uv remove package-name
```

**Update all dependencies:**
```bash
uv sync --upgrade
```

**Lock dependencies without installing:**
```bash
uv lock
```

### Running Commands

**Run a Python script:**
```bash
uv run python script.py
```

**Run the CLI:**
```bash
uv run python cli.py
```

**Run the API server:**
```bash
uv run python run_api.py
```

**Run the web UI:**
```bash
uv run python app/main.py
```

### Running Tests

**Run all tests:**
```bash
uv run pytest
```

**Run tests with coverage:**
```bash
uv run pytest --cov=src --cov=app
```

### Code Quality

**Format code with Black:**
```bash
uv run black .
```

**Lint with flake8:**
```bash
uv run flake8 src app tests
```

**Type check with mypy:**
```bash
uv run mypy src app
```

## Using uv Scripts

You can also run the project's scripts directly:

```bash
# Run the interview assistant
uv run interview-assistant

# Run the API server
uv run interview-api
```

## Benefits of uv

- **Fast**: 10-100x faster than pip
- **Reliable**: Deterministic dependency resolution
- **Compatible**: Works with existing pip/requirements.txt projects
- **All-in-one**: Manages Python versions, virtual environments, and packages
- **No pip needed**: Direct installation from PyPI

## Troubleshooting

**Virtual environment not found:**
```bash
uv venv --python 3.12
uv sync
```

**Clear cache:**
```bash
uv cache clean
```

**Verify Python version:**
```bash
uv run python --version
```

## Migration from pip

The project has been migrated from `requirements.txt` to `pyproject.toml`. All dependencies are now managed through:
- `[project.dependencies]` - Main dependencies
- `[project.optional-dependencies.dev]` - Development dependencies

The old `requirements.txt` and `requirements-dev.txt` files can be kept for reference or removed.
