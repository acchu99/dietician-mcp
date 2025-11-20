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

```bash
docker build -t food-mcp .
docker run --rm -p 8000:8000 food-mcp

# or with compose
docker compose up --build
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

Run tests with:

```bash
pytest
```

Or use an MCP client (e.g., MCP Inspector) that supports HTTP transport to connect to `http://localhost:8000` and invoke the available tools.
