import argparse
import os
import warnings

import uvicorn
from fastmcp import FastMCP
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from src.tools import setup_mcp_tools

# Suppress websockets deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="websockets")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="uvicorn.protocols.websockets")

mcp = FastMCP("MCP Server Template")

# Register the example tool
setup_mcp_tools(mcp)

@mcp.custom_route("/", methods=["GET"])
async def root(request):
    return RedirectResponse(url="/docs")

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "ok"})

@mcp.custom_route("/info", methods=["GET"])
async def mcp_info(request):
    tools_list = await mcp.get_tools()
    return JSONResponse(
        {
            "status": "running",
            "protocol": "mcp",
            "server_name": "MCP Server Template",
            "description": "Template for building custom Model Context Protocol servers",
            "mcp_endpoint": "/mcp",
            "tools_available": len(tools_list),
            "note": "This is an MCP server template. Customize the tools in src/tools.py",
        }
    )

@mcp.custom_route("/tools", methods=["GET"])
async def list_tools(request):
    tools = []
    tools_list = await mcp.get_tools()
    for tool_name, tool in tools_list.items():
        tools.append(
            {
                "name": tool_name,
                "description": getattr(tool, "description", None) or "No description available",
                "parameters": getattr(tool, "parameters", None) or {},
            }
        )
    return JSONResponse({"tools": tools})

@mcp.custom_route("/docs", methods=["GET"])
async def docs(request):
    from pathlib import Path
    
    tools_list = await mcp.get_tools()
    
    # Generate tools HTML
    tools_html = ""
    for tool_name, tool in tools_list.items():
        description = getattr(tool, "description", None) or "No description available"
        tools_html += f"""
                    <div class="bg-slate-800/50 rounded-lg p-5 border border-slate-700 hover:border-indigo-500 transition-colors">
                        <h3 class="font-semibold text-base mb-2 text-indigo-300">{tool_name}</h3>
                        <p class="text-gray-400 text-sm leading-relaxed">{description}</p>
                    </div>
        """
    
    # Read template and replace placeholders
    template_path = Path(__file__).parent / "src" / "templates" / "docs.html"
    with open(template_path, "r") as f:
        template = f.read()
    
    html_content = template.replace("{{ tools_count }}", str(len(tools_list)))
    html_content = html_content.replace("{{ tools_html }}", tools_html)
    
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP Server Template")
    args = parser.parse_args()

    port = int(os.environ.get("PORT", 8000))

    cors_middleware = Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["mcp-session-id"],
        max_age=86400,
    )
    
    app = mcp.http_app(middleware=[cors_middleware])

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")