# MCP Server Template (FastMCP on Starlette)

A production-ready Model Context Protocol (MCP) server template built with FastMCP on Starlette. This server runs on port 8000 (configurable), supports custom Starlette middlewares, and includes example tools to demonstrate MCP functionality.

## Architecture Overview

- **Framework**: FastMCP with Starlette
- **Transport**: HTTP and STDIO support
- **Server**: Uvicorn ASGI server
- **Port**: 8000 (configurable via PORT environment variable)
- **Middleware**: CORS enabled by default, extensible middleware stack

## Project Structure

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

## Core Features

- MCP server implementation using FastMCP and Starlette
- HTTP and STDIO transport protocols
- Custom HTTP endpoints for health checks, server info, and tool listing
- Interactive web-based documentation
- Extensible middleware support
- Example MCP tools demonstrating core functionality

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Docker (optional, for containerized deployment)

### Local Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Server

### Local Development

Start the server with HTTP transport:

```bash
python main.py
```

The server will be available at `http://localhost:8000` (or the port specified in your PORT environment variable).

### Docker Deployment

#### Option 1: Automated Test and Deploy

Use the provided script to run automated tests before deployment:

```bash
./scripts/test-and-run.sh
```

This workflow will:

1. Build and execute tests in isolated containers
2. Halt deployment if any tests fail
3. Build and start the production service only if all tests pass

#### Option 2: Manual Test Execution

```bash
# Execute test suite
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from test

# Deploy production service after successful tests
docker compose up --build -d
```

#### Option 3: Direct Production Deployment

```bash
# Deploy without running tests
docker compose up --build -d

# Alternative: Direct Docker commands
docker build -t macrosense-mcp .
docker run --rm -p 8000:8000 macrosense-mcp
```

#### Container Management

```bash
# Stop and remove containers
docker compose down
docker compose -f docker-compose.test.yml down
```

## Configuration

### Middleware Configuration

Edit the `cors_middleware` configuration in `main.py` to customize CORS settings or add additional Starlette middlewares to the middleware stack.

### Environment Variables

- `PORT`: Server port (default: 8000)
- `MONGODB_URI`: MongoDB connection string
- `HOST`: Bind address (default: 0.0.0.0)

## API Endpoints

### Core Endpoints

- `GET /` - Redirects to `/docs`
- `GET /health` - Health check endpoint for monitoring
- `GET /info` - Server metadata and tool information
- `GET /tools` - List all available MCP tools with descriptions
- `GET /docs` - Interactive API documentation
- `POST /mcp` - Primary MCP protocol endpoint

## MCP Tools

### Tool Development

Tools are defined in `src/tools.py`. Use the `@mcp.tool()` decorator to register new tools.

### Available Tools

#### `add_numbers`

Performs addition of two numeric values.

**Parameters:**

- `number1` (float): First operand
- `number2` (float): Second operand

**Returns:**

```json
{
  "result": <sum>
}
```

**Example Usage:**

```python
@mcp.tool()
def add_numbers(number1: float, number2: float) -> dict:
    """Calculate the sum of two numbers"""
    return {"result": sum([number1, number2])}
```

## Testing

### Test Framework

The project uses pytest with asyncio support for asynchronous test execution. All tests are located in the `tests/` directory.

### Running Tests Locally

Execute the complete test suite:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Using virtual environment directly:

```bash
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

### Test Architecture

Tests utilize FastMCP's in-memory client for fast, deterministic testing:

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

### Test Coverage

The test suite includes:

- **test_server_info**: Validates server initialization and metadata
- **test_list_tools**: Verifies tool registration
- **test_add_numbers**: Parametrized tests covering multiple input scenarios (7 test cases)
- **test_add_numbers_with_negative_numbers**: Negative value handling
- **test_add_numbers_with_floats**: Floating-point precision validation

### Testing Best Practices

All tests adhere to FastMCP testing standards:

- Single behavior per test
- Self-contained setup
- Clear intent with descriptive names
- Effective assertions with error messages

### Integration Testing

For integration testing with external MCP clients, use MCP Inspector or similar tools that support HTTP transport to connect to `http://localhost:8000`.
