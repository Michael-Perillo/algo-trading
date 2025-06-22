# algo-trading

Monorepo for algorithmic trading experiments and infrastructure.

## Project Structure

- **src/trading_bot_mvp/**: Main source code for the trading bot, including:
  - `client/`: API clients (e.g., Alpaca)
  - `service/`: Service and DAO layers (data access, brokerage, etc.)
  - `shared/`: Shared models and mocks
  - `settings.py`: Configuration and environment management
  - `main.py`: Entry point for running the trading bot
- **tests/**: All test modules for the codebase
- **specs/**: OpenAPI and YAML specs for model/code generation
- **scripts/**: Utility scripts (e.g., model generation)

## Getting Started

### Prerequisites
- Python 3.13+ (recommended: use [pyenv](https://github.com/pyenv/pyenv) or similar)
- [PDM](https://pdm.fming.dev/) (Python package/dependency manager)
  - Install with [installation script](https://pdm.fming.dev/latest/#installation) (recommended):
    ```sh
    curl -sSL https://pdm-project.org/install-pdm.py | python3 -
    ```
    - On windows, you may need to run the above command in a PowerShell terminal with administrator privileges:
        ```sh
        powershell -ExecutionPolicy ByPass -c "irm https://pdm-project.org/install-pdm.py | py -"
        ```
  - Or with Homebrew (on macOS):
    ```sh
    brew install pdm
    ```
  - It is recommended to install PDM in an isolated environment (e.g., using the installation script, brew, or `pipx`).

### Setup

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd algo-trading
   ```

2. **Install dependencies:**
   ```sh
   pdm install
   ```

3. **(Recommended) Set up pre-commit hooks:**
   ```sh
   pre-commit install
   ```
   This will ensure formatting, linting, and typechecking are run on every commit.

## Common Commands

All commands below are run via PDM scripts (see `pyproject.toml`):

- **Start the trading bot:**
  ```sh
  pdm run start
  ```
- **Run tests:**
  ```sh
  pdm run test
  ```
- **Run coverage:**
  ```sh
  pdm run coverage
  ```
- **Lint and auto-fix:**
  ```sh
  pdm run lint
  ```
- **Format code:**
  ```sh
  pdm run format
  ```
- **Typecheck (mypy):**
  ```sh
  pdm run typecheck
  ```

## Dependencies
- **ruff**: Linting and formatting (fast, modern Python linter)
- **pytest**: Testing framework
- **mypy**: Static type checking
- **pydantic**: Data validation and settings management
- **pandera**: DataFrame schema validation
- **httpx**: HTTP client for API integrations
- **pre-commit**: Git hook management (optional, but recommended)

## API Model Generation
- See [Alpaca OAS Specs](https://docs.alpaca.markets/openapi) used to generate the client models in `src/client/alpaca/models`.
- Scripts for model generation are in the `scripts/` directory.

## Notes
- The project is structured for extensibility and testability, with clear separation between API clients, services, and data models.
- All code and tests are formatted and linted automatically via pre-commit hooks if enabled.

---
