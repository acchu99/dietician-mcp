# MCP Server Template (FastMCP on Starlette)

A Model Context Protocol (MCP) server template built with FastMCP on Starlette. It runs on port `8000` (configurable), supports custom Starlette middlewares, and includes example tools to demonstrate adding functionality.

## Folder Structure

```text
.
├── Dockerfile
├── docker-compose.yml
├── License
├── main.py
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── tools.py
│   └── utils/
└── tests/
    └── test.py
```

## What It Does (Brief)

- Exposes an MCP server using FastMCP + Starlette with both stdio and HTTP transport support.
- Listens on `0.0.0.0:8000` via Uvicorn (configurable via `PORT` env var).
- Lets you inject custom Starlette middlewares (CORS enabled by default).
- Provides custom HTTP endpoints: `/health`, `/info`, `/tools`, and `/docs`.
- Includes example MCP tools in `src/tools.py` (currently `add_numbers`).

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Start the server with HTTP transport:

```bash
python main.py
```

Server will be available at `http://localhost:8000` (or your specified port).

### Docker (optional)

If you prefer containers and your Dockerfile/compose are configured for this app:

#### Option 1: Run tests first, then start the application

Use the provided script to automatically run tests before building and starting:

```bash
./scripts/test-and-run.sh
```

This script will:

1. Build and run tests in a container
2. Exit if tests fail
3. Build and start the application only if tests pass

#### Option 2: Run tests separately

```bash
# Run tests (this will start the server, wait for it to be healthy, then run tests)
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from test

# If tests pass, start the application for production
docker compose up --build -d
```

#### Option 3: Start production server only

```bash
# Start production server
docker compose up --build -d

# Or using the main service directly
docker build -t macrosense-mcp .
docker run --rm -p 8000:8000 macrosense-mcp
```

#### Clean up containers

```bash
docker compose down
docker compose -f docker-compose.test.yml down
```

## Custom Middlewares

Edit the `cors_middleware` in `main.py` to adjust CORS settings or add additional Starlette middlewares to the `middleware` list when creating the app.

## Available HTTP Endpoints

- `GET /` - Redirects to `/docs`
- `GET /health` - Health check endpoint
- `GET /info` - Server information and available tools count
- `GET /tools` - List all available MCP tools with descriptions
- `GET /docs` - Interactive documentation page
- `POST /mcp` - MCP protocol endpoint

## MCP Tools

Tools are defined in `src/tools.py`. The current example tool:

### `add_numbers`

- Purpose: Adds two numbers together
- Parameters:
  - `number1` (float): First number
  - `number2` (float): Second number
- Returns: `{"result": sum}`

To add your own tools, edit `src/tools.py` and use the `@mcp.tool()` decorator.

## Testing

### Running Tests

The project uses pytest with async support for testing. Tests are located in the `tests/` directory.

Run all tests:

```bash
pytest
# or with verbose output
pytest -v
# or using the virtual environment directly
.venv/bin/python -m pytest tests/test.py -v
```

### Test Configuration

The `pyproject.toml` file contains pytest configuration:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

### Test Structure

Tests use FastMCP's in-memory client for fast, deterministic testing:

```python
import pytest
from fastmcp.client import Client
from main import mcp

@pytest.fixture
async def mcp_client():
    """Fixture that provides a FastMCP client for testing."""
    async with Client(mcp) as client:
        yield client

async def test_add_numbers(mcp_client: Client):
    """Test add_numbers tool."""
    result = await mcp_client.call_tool(
        name="add_numbers", 
        arguments={"number1": 1, "number2": 2}
    )
    assert result.data["result"] == 3
```

### Current Test Coverage

- **test_server_info**: Verifies server initialization and metadata
- **test_list_tools**: Checks tool registration
- **test_add_numbers**: Parametrized tests with multiple inputs (7 test cases)
- **test_add_numbers_with_negative_numbers**: Negative number handling
- **test_add_numbers_with_floats**: Floating-point precision

All tests follow FastMCP best practices:

- Single behavior per test
- Self-contained setup
- Clear intent with descriptive names
- Effective assertions with error messages

### Manual Testing

Or use an MCP client (e.g., MCP Inspector) that supports HTTP transport to connect to `http://localhost:8000` and invoke the available tools.

