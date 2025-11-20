# MCP Server with FastMCP and Starlette

A basic HTTP-streamable MCP server built with FastMCP and Starlette.

## Features

- HTTP-streamable MCP server
- Runs on port 8000
- Custom middleware support (CORS enabled by default)
- Simple hello world tool included

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the server:
```bash
python main.py
```

The server will be available at `http://localhost:8000`

## Adding Custom Middlewares

You can add custom middlewares in `main.py` by modifying the `middlewares` list:

```python
middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    # Add your custom middlewares here
]
```

## Available Tools

### hello_world
A simple greeting tool.

**Parameters:**
- `name` (optional): The name to greet (default: "World")

**Returns:** A greeting message

## Testing the Server

You can test the MCP server using the MCP Inspector or any MCP client that supports HTTP transport.
