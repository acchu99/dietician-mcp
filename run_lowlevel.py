#!/usr/bin/env python3
"""
Entry point for the low-level Food MCP Server.

This script runs the low-level MCP server with proper stdio transport for 
MCP client communication. The server provides structured output using 
Pydantic schemas and follows the MCP specification.
"""
import asyncio
import sys
from lowlevel_server import run_server

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("Server stopped by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)