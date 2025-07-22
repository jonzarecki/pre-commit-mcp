# Contributing

Thanks for wanting to contribute! Follow these guidelines to set up your environment and run checks locally.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install the project with development dependencies:
   ```bash
pip install -e .[dev]
   ```
3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Running checks

- Run the linters on changed files:
  ```bash
  pre-commit run --files <file1> <file2> ...
  ```
- Compile the code and run tests:
  ```bash
  python -m py_compile fast_precommit_mcp/*.py
  pytest --cov=fast_precommit_mcp --cov-report=term-missing
  ```

GitHub Actions will run these same checks on every pull request.
