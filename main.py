"""
FastMCP Food Hierarchy Server

An MCP server that provides tools for querying food hierarchy data from MongoDB.
"""
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from db import MongoDBClient
from services.hierarchy_queries import FoodHierarchyService
from services.item_service import FoodItemsService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Create an MCP server
mcp = FastMCP("Calorie Server")

# Initialize database client and service
try:
    db_client = MongoDBClient(uri=os.getenv("MONGODB_URI"))
    food_hierarchy_service = FoodHierarchyService(db_client)
    food_items_service = FoodItemsService(db_client)
    logger.info("Successfully initialized food services")
except Exception as e:
    logger.error(f"Failed to initialize food services: {e}")
    raise


# Food Hierarchy Service Tools
@mcp.tool()
def get_all_food_hierarchy() -> list[dict]:
    """
    Return the full food hierarchy dataset.

    This retrieves all documents in the food hierarchy collection,
    removes internal database fields (such as `_id`), and returns them
    as a list of category → subcategory → food_items mappings.

    Use when the assistant needs the complete food taxonomy.
    """
    return food_hierarchy_service.get_all_food_hierarchy()


@mcp.tool()
def get_categories() -> list[str]:
    """
    Return a list of all food categories.

    Example output:
    ["fruits & vegetables", "dairy", "grains"]

    Use to discover available top-level food categories.
    """
    return food_hierarchy_service.get_categories()


@mcp.tool()
def get_subcategories(category: str) -> list[str]:
    """
    Return all subcategories for a given category.

    Args:
        category (str): The name of the parent food category.

    Returns:
        list[str]: A list of subcategory names.

    Example:
    Input -> "fruits & vegetables"
    Output -> ["potatoes & potato products", "leafy greens", ...]
    """
    return food_hierarchy_service.get_subcategories(category)


@mcp.tool()
def get_food_items(category: str, subcategory: str) -> list[str]:
    """
    Return all food items for a given category and subcategory.

    Args:
        category (str): The top-level food category.
        subcategory (str): The sub-group inside the category.

    Returns:
        list[str]: A list of food item names, or an empty list if not found.

    Use when the user specifies a category + subcategory and wants the foods.
    """
    return food_hierarchy_service.get_food_items(category, subcategory)


@mcp.tool()
def search_food(keyword: str) -> list[dict]:
    """
    Search food items by keyword (case-insensitive).

    Args:
        keyword (str): Text to search inside food item names.

    Returns:
        list[dict]: A list of matching food items with their category and subcategory.

    Useful for partial text matches, e.g.:
    Input -> "fries"
    Output -> [{ "category": "...", "subcategory": "...", "item": "curly fries" }, ...]
    """
    return food_hierarchy_service.search_food(keyword)


@mcp.tool()
def find_food_category(item: str) -> list[dict]:
    """
    Find the category and subcategory for a specific food item (case-insensitive exact match).

    Args:
        item (str): A food name to look up.

    Returns:
        list[dict]: One or more matches containing category and subcategory fields.

    Use when given a specific food and you want to know where it belongs
    in the hierarchy — e.g. "sweet potato fries".
    """
    return food_hierarchy_service.find_food_category(item)


@mcp.tool()
def list_all_foods() -> list[str]:
    """
    Return a deduplicated, flattened list of all food item names across the hierarchy.

    Useful for autocomplete, embeddings, or global search contexts.

    Returns:
        list[str]: All known food names.
    """
    return food_hierarchy_service.list_all_foods()


@mcp.tool()
def food_stats() -> dict:
    """
    Return high-level statistics about the food hierarchy dataset.

    Includes:
    - total categories
    - total subcategories
    - average number of foods per subcategory
    - min/max foods in a subcategory

    Useful for diagnostics, dashboards, or summarization.
    """
    return food_hierarchy_service.get_food_stats()


# Food Items Service Tools
@mcp.tool()
def list_food_names() -> list[str]:
    """
    Return the names of all foods that have nutrition data.

    Useful for autocomplete, validation, or checking whether a food exists
    in the nutrition database.
    """
    return food_items_service.list_food_names()


@mcp.tool()
def get_food_nutrition(name: str) -> dict | None:
    """
    Fetch complete nutritional information for a food item by exact name (case-insensitive).

    Returns macro calories per 100g/ml, all serving sizes, and the default
    display serving calories.

    Example:
        get_food_nutrition("potato salad, with egg")
    """
    return food_items_service.get_food_nutrition(name)


@mcp.tool()
def search_food_nutrition(keyword: str) -> list[dict]:
    """
    Search food nutrition entries by partial match (case-insensitive).

    Use this when the user doesn't know the exact food name or wants
    related items, e.g.:

        search_food_nutrition("potato")
    """
    return food_items_service.search_food_nutrition(keyword)


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http"
    )

