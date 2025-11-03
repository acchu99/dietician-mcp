"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from db import mongo_client

load_dotenv()

# Create an MCP server
mcp = FastMCP("Demo")

# Connect to MongoDB
client = mongo_client(uri=os.getenv("MONGODB_URI"))
db = client.food
food_hierarchy_collection = db.food_hierarchy
food_items_collection = db.food_items


@mcp.tool()
def get_all_food_hierarchy() -> any:
    """
    Return the full food hierarchy dataset.

    This retrieves all documents in the food hierarchy collection,
    removes internal database fields (such as `_id`), and returns them
    as a list of category → subcategory → food_items mappings.

    Use when the assistant needs the complete food taxonomy.
    """

    output = food_hierarchy_collection.find({}).to_list()
    for item in output:
        item.pop("_id", None)
    return output

@mcp.tool()
def get_categories() -> list[str]:
    """
    Return a list of all food categories.

    Example output:
    ["fruits & vegetables", "dairy", "grains"]

    Use to discover available top-level food categories.
    """

    return food_hierarchy_collection.distinct("category")

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

    return food_hierarchy_collection.distinct(
        "subcategory", {"category": category}
    )

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

    doc = food_hierarchy_collection.find_one(
        {"category": category, "subcategory": subcategory},
        {"_id": 0, "food_items": 1}
    )
    return doc["food_items"] if doc else []

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

    pipeline = [
        {"$unwind": "$food_items"},
        {
            "$match": {
                "food_items": {"$regex": keyword, "$options": "i"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "category": 1,
                "subcategory": 1,
                "item": "$food_items"
            }
        }
    ]
    return list(food_hierarchy_collection.aggregate(pipeline))

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

    docs = food_hierarchy_collection.find(
        {"food_items": {"$regex": f"^{item}$", "$options": "i"}},
        {"_id": 0, "category": 1, "subcategory": 1}
    )
    return list(docs)

@mcp.tool()
def list_all_foods() -> list[str]:
    """
    Return a deduplicated, flattened list of all food item names across the hierarchy.

    Useful for autocomplete, embeddings, or global search contexts.

    Returns:
        list[str]: All known food names.
    """

    pipeline = [
        {"$unwind": "$food_items"},
        {"$group": {"_id": None, "items": {"$addToSet": "$food_items"}}},
        {"$project": {"_id": 0, "items": 1}}
    ]
    result = list(food_hierarchy_collection.aggregate(pipeline))
    return result[0]["items"] if result else []


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

    total_categories = len(food_hierarchy_collection.distinct("category"))
    total_subcategories = len(food_hierarchy_collection.distinct("subcategory"))

    pipeline = [
        {"$project": {"count": {"$size": "$food_items"}}},
        {"$group": {
            "_id": None,
            "avgItems": {"$avg": "$count"},
            "maxItems": {"$max": "$count"},
            "minItems": {"$min": "$count"}
        }}
    ]
    stats = list(food_hierarchy_collection.aggregate(pipeline))[0]

    return {
        "total_categories": total_categories,
        "total_subcategories": total_subcategories,
        "average_items_per_subcategory": stats["avgItems"],
        "max_items_in_subcategory": stats["maxItems"],
        "min_items_in_subcategory": stats["minItems"]
    }

