def setup_mcp_tools(mcp):
    """Setup MCP tools for the server"""
    
    @mcp.tool()
    def add_numbers(number1: float, number2: float) -> dict:
        """Calculate the square of a number"""
        return {"result": sum([number1, number2])}