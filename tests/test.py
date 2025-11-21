import sys
from pathlib import Path

import pytest
from fastmcp.client import Client

# Add parent directory to path to import main
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import mcp


@pytest.fixture
async def mcp_client():
    """Fixture that provides a FastMCP client for testing."""
    async with Client(mcp) as client:
        yield client


async def test_server_info(mcp_client: Client):
    """Test that server provides basic info."""
    # Initialize the connection to get server info
    result = await mcp_client.initialize()
    assert result is not None
    assert result.serverInfo.name == "MCP Server Template"


async def test_list_tools(mcp_client: Client):
    """Test that server lists available tools."""
    tools = await mcp_client.list_tools()
    assert len(tools) == 1
    assert tools[0].name == "add_numbers"
    assert tools[0].description == "Calculate the square of a number"


@pytest.mark.parametrize(
    "number1, number2, expected",
    [
        (1, 2, 3),
        (2, 3, 5),
        (3, 4, 7),
        (10, 5, 15),
        (0, 0, 0),
        (-5, 5, 0),
        (1.5, 2.5, 4.0),
    ],
)
async def test_add_numbers(
    number1: float,
    number2: float,
    expected: float,
    mcp_client: Client,
):
    """Test add_numbers tool with various inputs."""
    result = await mcp_client.call_tool(
        name="add_numbers", 
        arguments={"number1": number1, "number2": number2}
    )
    
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Result should be a dictionary"
    assert "result" in result.data, "Result should contain 'result' key"
    assert result.data["result"] == expected, f"Expected {expected}, got {result.data['result']}"


async def test_add_numbers_with_negative_numbers(mcp_client: Client):
    """Test add_numbers specifically with negative numbers."""
    result = await mcp_client.call_tool(
        name="add_numbers",
        arguments={"number1": -10, "number2": -20}
    )
    
    assert result.data["result"] == -30


async def test_add_numbers_with_floats(mcp_client: Client):
    """Test add_numbers with floating point precision."""
    result = await mcp_client.call_tool(
        name="add_numbers",
        arguments={"number1": 0.1, "number2": 0.2}
    )
    
    # Account for floating point precision
    assert abs(result.data["result"] - 0.3) < 0.0001


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
