"""
Streamable HTTP MCP server implementation for Food Hierarchy and Nutrition data.

This server uses the MCP Python SDK with StreamableHTTP transport for web-based access.
It provides structured output using Pydantic schemas and follows the MCP specification.
"""
import asyncio
import contextlib
import logging
import os
from typing import Any, Dict, List
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Scope, Receive, Send
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from dotenv import load_dotenv


# Import our services and schemas
from utils.db import MongoDBClient
from services.hierarchy_queries import FoodHierarchyService
from services.item_service import FoodItemsService
from schemas.food_hierarchy import (
    FoodHierarchyResponse, FoodCategoriesResponse, FoodSubcategoriesResponse,
    FoodItemsResponse, FoodSearchResponse, FoodCategoryLookupResponse,
    AllFoodsResponse, FoodStats
)
from schemas.food_item import (
    FoodNamesResponse, FoodNutritionResponse, FoodNutritionSearchResponse,
    FoodNutrition, StructuredFoodNutrition, ServingInfo
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class AppContext:
    """Application context containing initialized services."""
    
    def __init__(self, db_client: MongoDBClient):
        self.db_client = db_client
        self.food_hierarchy_service = FoodHierarchyService(db_client)
        self.food_items_service = FoodItemsService(db_client)


@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[AppContext]:
    """Manage server startup and shutdown lifecycle."""
    logger.info("Initializing Food MCP Server...")
    
    # Initialize MongoDB connection
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        raise ValueError("MONGODB_URI environment variable is required")
    
    try:
        db_client = MongoDBClient(uri=mongodb_uri)
        app_context = AppContext(db_client)
        logger.info("Successfully initialized food services")
        yield app_context
    except Exception as e:
        logger.error(f"Failed to initialize food services: {e}")
        raise
    finally:
        logger.info("Shutting down Food MCP Server")


# Create the server with lifespan management
server = Server("food-mcp-server", lifespan=server_lifespan)


# =============================================================================
# FOOD HIERARCHY TOOLS
# =============================================================================

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List all available tools."""
    return [
        # Food Hierarchy Tools
        types.Tool(
            name="get_all_food_hierarchy",
            description="Return the complete food hierarchy dataset with category → subcategory → food_items mappings",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            outputSchema=FoodHierarchyResponse.model_json_schema()
        ),
        types.Tool(
            name="get_categories",
            description="Return a list of all food categories",
            inputSchema={
                "type": "object", 
                "properties": {},
                "additionalProperties": False
            },
            outputSchema=FoodCategoriesResponse.model_json_schema()
        ),
        types.Tool(
            name="get_subcategories",
            description="Return all subcategories for a given food category",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The name of the parent food category"
                    }
                },
                "required": ["category"],
                "additionalProperties": False
            },
            outputSchema=FoodSubcategoriesResponse.model_json_schema()
        ),
        types.Tool(
            name="get_food_items",
            description="Return all food items for a given category and subcategory",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The top-level food category"
                    },
                    "subcategory": {
                        "type": "string", 
                        "description": "The sub-group inside the category"
                    }
                },
                "required": ["category", "subcategory"],
                "additionalProperties": False
            },
            outputSchema=FoodItemsResponse.model_json_schema()
        ),
        types.Tool(
            name="search_food",
            description="Search food items by keyword (case-insensitive partial matching)",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Text to search inside food item names"
                    }
                },
                "required": ["keyword"],
                "additionalProperties": False
            },
            outputSchema=FoodSearchResponse.model_json_schema()
        ),
        types.Tool(
            name="find_food_category",
            description="Find the category and subcategory for a specific food item",
            inputSchema={
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "A food name to look up (case-insensitive exact match)"
                    }
                },
                "required": ["item"],
                "additionalProperties": False
            },
            outputSchema=FoodCategoryLookupResponse.model_json_schema()
        ),
        types.Tool(
            name="list_all_foods",
            description="Return a deduplicated, flattened list of all food item names across the hierarchy",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            outputSchema=AllFoodsResponse.model_json_schema()
        ),
        types.Tool(
            name="food_stats",
            description="Return high-level statistics about the food hierarchy dataset",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            outputSchema=FoodStats.model_json_schema()
        ),
        
        # Food Nutrition Tools
        types.Tool(
            name="list_food_names",
            description="Return the names of all foods that have nutrition data available",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            outputSchema=FoodNamesResponse.model_json_schema()
        ),
        types.Tool(
            name="get_food_nutrition",
            description="Fetch complete nutritional information for a food item by exact name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The exact name of the food item to search for (case-insensitive)"
                    }
                },
                "required": ["name"],
                "additionalProperties": False
            },
            outputSchema=FoodNutritionResponse.model_json_schema()
        ),
        types.Tool(
            name="search_food_nutrition",
            description="Search food nutrition entries by partial match (case-insensitive)",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "The partial name of the food item to search for"
                    }
                },
                "required": ["keyword"],
                "additionalProperties": False
            },
            outputSchema=FoodNutritionSearchResponse.model_json_schema()
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> types.CallToolResult:
    """Handle tool calls with structured output."""
    # Get the application context
    ctx = server.request_context
    app_ctx: AppContext = ctx.lifespan_context
    
    try:
        if name == "get_all_food_hierarchy":
            hierarchy_data = app_ctx.food_hierarchy_service.get_all_food_hierarchy()
            response = FoodHierarchyResponse(hierarchy=[
                {
                    "category": item.get("category", ""),
                    "subcategory": item.get("subcategory", ""),
                    "food_items": item.get("food_items", [])
                }
                for item in hierarchy_data
            ])
            
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Retrieved complete food hierarchy with {len(response.hierarchy)} category-subcategory combinations"
                    )
                ],
                structuredContent=response.model_dump()
            )
            
        elif name == "get_categories":
            categories = app_ctx.food_hierarchy_service.get_categories()
            response = FoodCategoriesResponse(categories=categories, total_count=len(categories))
            
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Found {len(categories)} food categories: {', '.join(categories)}"
                    )
                ],
                structuredContent=response.model_dump()
            )
            
        elif name == "get_subcategories":
            category = arguments["category"]
            subcategories = app_ctx.food_hierarchy_service.get_subcategories(category)
            response = FoodSubcategoriesResponse(category=category, subcategories=subcategories)
            
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Found {len(subcategories)} subcategories in '{category}': {', '.join(subcategories)}"
                    )
                ],
                structuredContent=response.model_dump()
            )
            
        elif name == "get_food_items":
            category = arguments["category"]
            subcategory = arguments["subcategory"] 
            food_items = app_ctx.food_hierarchy_service.get_food_items(category, subcategory)
            response = FoodItemsResponse(category=category, subcategory=subcategory, food_items=food_items)
            
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Found {len(food_items)} food items in '{category}' → '{subcategory}'"
                    )
                ],
                structuredContent=response.model_dump()
            )
            
        elif name == "search_food":
            keyword = arguments["keyword"]
            search_results = app_ctx.food_hierarchy_service.search_food(keyword)
            response = FoodSearchResponse(
                keyword=keyword,
                results=[
                    {
                        "category": result.get("category", ""),
                        "subcategory": result.get("subcategory", ""),
                        "item": result.get("item", "")
                    }
                    for result in search_results
                ],
                total_matches=len(search_results)
            )
            
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Found {len(search_results)} food items matching '{keyword}'"
                    )
                ],
                structuredContent=response.model_dump()
            )
            
        elif name == "find_food_category":
            item = arguments["item"]
            matches = app_ctx.food_hierarchy_service.find_food_category(item)
            response = FoodCategoryLookupResponse(
                item=item,
                matches=[
                    {
                        "category": match.get("category", ""),
                        "subcategory": match.get("subcategory", "")
                    }
                    for match in matches
                ]
            )
            
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Found {len(matches)} category matches for '{item}'"
                    )
                ],
                structuredContent=response.model_dump()
            )
            
        elif name == "list_all_foods":
            foods = app_ctx.food_hierarchy_service.list_all_foods()
            response = AllFoodsResponse(foods=foods)
            
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Retrieved {len(foods)} unique food names from the hierarchy"
                    )
                ],
                structuredContent=response.model_dump()
            )
            
        elif name == "food_stats":
            stats = app_ctx.food_hierarchy_service.get_food_stats()
            response = FoodStats(**stats)
            
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Food hierarchy contains {stats['total_categories']} categories, "
                             f"{stats['total_subcategories']} subcategories"
                    )
                ],
                structuredContent=response.model_dump()
            )
            
        elif name == "list_food_names":
            food_names = app_ctx.food_items_service.list_food_names()
            response = FoodNamesResponse(food_names=food_names, total_count=len(food_names))
            
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Found {len(food_names)} foods with nutrition data available"
                    )
                ],
                structuredContent=response.model_dump()
            )
            
        elif name == "get_food_nutrition":
            name_arg = arguments["name"]
            nutrition_data = app_ctx.food_items_service.get_food_nutrition(name_arg)
            
            if nutrition_data:
                # Convert the raw nutrition data to our Pydantic model
                nutrition = FoodNutrition(**nutrition_data)
                response = FoodNutritionResponse(
                    requested_name=name_arg,
                    found=True,
                    nutrition=nutrition
                )
                
                return types.CallToolResult(
                    content=[
                        types.TextContent(
                            type="text",
                            text=f"Found nutrition data for '{nutrition.name}': "
                                 f"{nutrition.display_portion_calories} calories per serving"
                        )
                    ],
                    structuredContent=response.model_dump()
                )
            else:
                response = FoodNutritionResponse(
                    requested_name=name_arg,
                    found=False,
                    nutrition=None
                )
                
                return types.CallToolResult(
                    content=[
                        types.TextContent(
                            type="text",
                            text=f"No nutrition data found for '{name_arg}'"
                        )
                    ],
                    structuredContent=response.model_dump()
                )
                
        elif name == "search_food_nutrition":
            keyword = arguments["keyword"]
            search_results = app_ctx.food_items_service.search_food_nutrition(keyword)
            
            # Convert search results to structured format
            structured_results = []
            for result in search_results:
                nutrition = FoodNutrition(**result)
                structured_results.append({
                    "name": nutrition.name,
                    "relevance_score": None,  # Could implement relevance scoring
                    "nutrition": nutrition.model_dump()
                })
            
            response = FoodNutritionSearchResponse(
                search_keyword=keyword,
                results=structured_results,
                total_matches=len(structured_results)
            )
            
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Found {len(search_results)} nutrition entries matching '{keyword}'"
                    )
                ],
                structuredContent=response.model_dump()
            )
            
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Error in tool '{name}': {e}")
        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=f"Error executing tool '{name}': {str(e)}"
                )
            ],
            isError=True
        )


def run_server():
    """Run the MCP server with StreamableHTTP transport."""
    logger.info("Starting Food MCP Server with StreamableHTTP transport...")
    
    # Configure host and port
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    json_response = os.getenv("JSON_RESPONSE", "false").lower() == "true"
    
    logger.info(f"MCP Server starting on http://{host}:{port}")
    
    # Create the StreamableHTTP session manager with stateless mode for inspector compatibility
    session_manager = StreamableHTTPSessionManager(
        app=server,
        event_store=None,  # No event store for now
        json_response=json_response,  # Use JSON responses for inspector
        stateless=True,  # Stateless mode for inspector compatibility
    )
    
    # Handle StreamableHTTP requests
    async def handle_streamable_http(scope: Scope, receive: Receive, send: Send) -> None:
        await session_manager.handle_request(scope, receive, send)
    
    # Lifespan manager for the session manager
    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        async with session_manager.run():
            logger.info("Application started with StreamableHTTP session manager!")
            try:
                yield
            finally:
                logger.info("Application shutting down...")
    
    # Create Starlette ASGI app with proper MCP endpoint
    starlette_app = Starlette(
        debug=True,
        routes=[
            Mount("/mcp", app=handle_streamable_http)
        ],
        lifespan=lifespan,
    )
    
    # Add CORS middleware for browser/inspector access
    starlette_app = CORSMiddleware(
        starlette_app,
        allow_origins=["*"],
        allow_methods=["GET", "POST", "DELETE"],
        allow_headers=["*"],
        expose_headers=["Mcp-Session-Id"],
    )
    
    # Run with uvicorn
    uvicorn.run(
        starlette_app,
        host=host,
        port=port,
        log_level="info"
    )


if __name__ == "__main__":
    run_server()