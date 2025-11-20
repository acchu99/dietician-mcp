from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn

# Initialize FastMCP server
mcp = FastMCP("Hello World MCP Server")

# Define a simple hello world tool
@mcp.tool()
def hello_world(name: str = "World") -> str:
    """
    A simple hello world tool that greets the user.
    
    Args:
        name: The name to greet (default: "World")
    
    Returns:
        A greeting message
    """
    return f"Hello, {name}! This is your MCP server running on Starlette."

# Configure custom middlewares
middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]

# Create Starlette app with middlewares
app = mcp.get_starlette_app(middlewares=middlewares)

if __name__ == "__main__":
    # Run the server on port 8000
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
