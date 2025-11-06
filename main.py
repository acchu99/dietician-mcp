"""
FastMCP Food Hierarchy Server

An MCP server that provides tools for querying food hierarchy data from MongoDB.
"""
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from utils.db import MongoDBClient
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

    Parameters:
        name (str): The exact name of the food item to search for (e.g., "Potato Pancake", 
                        "Croquettes", "Brown Rice"). The search is case-insensitive and 
                        supports partial matches.

    Returns:
        dict: A dictionary containing comprehensive nutritional information with the following fields:

        Basic Information:
            name (str): The exact name of the food item as stored in the database
            
        Base Nutritional Data:
            unitCalories100gml (str): Unit of measurement for calories, always "kcal" (kilocalories)
            calories100Gml (str): Calories per 100 grams or 100 milliliters of the food item
            
        Multiple Serving Size Options (up to 5 different serving sizes):
            serving1MlG through serving5MlG (str): Unit of measurement for each serving 
                - "g" for grams, "ml" for milliliters, empty string if serving option not available
            serving1Size through serving5Size (str): Weight or volume of the serving 
                - Numeric value as string (e.g., "37", "120"), empty string if not available
            serving1Unit through serving5Unit (str): Type of serving unit using internationalization keys:
                - "food.serving.label.piece" = individual pieces (1 pancake, 1 slice)
                - "food.serving.label.portion" = standard portion size
                - "food.serving.label.cup" = cup measurement
                - "food.serving.label.tablespoon" = tablespoon measurement
                - "food.serving.label.slice" = sliced items
                - Empty string if serving option not available
            serving1UnitNumber through serving5UnitNumber (str): Number of units in the serving
                - Usually "1" for single servings, empty string if not available
                
        Primary Display Serving (the default/recommended serving shown to users):
            displayPortionCalories (number): Calculated calories for the display serving size
                - Formula: (calories100Gml ÷ 100) × displayServingSize
            displayServingMlG (str): Unit for display serving ("g" for grams, "ml" for milliliters)
            displayServingSize (str): Size/weight of the display serving (numeric value as string)
            displayServingUnit (str): Unit type for display serving (same format as serving units above)
            displayServingUnitNumber (str): Number of units in display serving (usually "1")
            displayServingUnitOption (str): Additional serving size qualifier:
                - "" = standard/default size (no qualifier)
                - "food.serving.option.small" = small version
                - "food.serving.option.medium" = medium version  
                - "food.serving.option.large" = large version
                - "food.serving.option.whole" = whole item
                - "food.serving.option.sliced" = sliced preparation
                - "food.serving.option.shredded" = shredded preparation
                - "food.serving.option.crumbed" = crumbed/breaded preparation
                - "food.serving.option.ground" = ground preparation

    Usage Notes for LLM:
        - All numeric values are stored as strings and need parsing for calculations
        - Empty strings indicate unavailable data or unused serving options
        - The displayPortionCalories field provides pre-calculated calories for the main serving
        - Multiple serving options allow users to choose appropriate portion sizes
        - Serving unit labels use dot notation for internationalization
        - The display serving represents the most common or recommended portion size

    Example Response:
        {
            "name": "Potato Pancake",
            "unitCalories100gml": "kcal",
            "calories100Gml": "268",
            "serving1MlG": "g",
            "serving1Size": "37",
            "serving1Unit": "food.serving.label.piece",
            "serving1UnitNumber": "1",
            "serving2MlG": "g", 
            "serving2Size": "22",
            "serving2Unit": "food.serving.label.piece",
            "serving2UnitNumber": "1",
            "serving3MlG": "g",
            "serving3Size": "100", 
            "serving3Unit": "food.serving.label.portion",
            "serving3UnitNumber": "1",
            "serving4MlG": "",
            "serving4Size": "",
            "serving4Unit": "",
            "serving4UnitNumber": "",
            "serving5MlG": "",
            "serving5Size": "", 
            "serving5Unit": "",
            "serving5UnitNumber": "",
            "displayPortionCalories": 99.16,
            "displayServingMlG": "g",
            "displayServingSize": "37",
            "displayServingUnit": "food.serving.label.piece", 
            "displayServingUnitNumber": "1",
            "displayServingUnitOption": ""
        }

    When interpreting results for users:
        - Convert serving unit labels to human-readable format (remove "food.serving.label." prefix)
        - Use displayPortionCalories for the main calorie information
        - Present multiple serving options when available to give users choices
        - Calculate calories for custom serving sizes using: (calories100Gml ÷ 100) × desired_grams
        - Explain serving size qualifiers (small/medium/large/etc.) in plain language


    Example:
        get_food_nutrition("potato salad, with egg")
    """
    return food_items_service.get_food_nutrition(name)


@mcp.tool()
def search_food_nutrition(keyword: str) -> list[dict]:
    """
    Search food nutrition entries by partial match (case-insensitive).

    Parameters:
        keyword (str): The partial name of the food item to search for (e.g., "potato-pancake", 
                        "hash brown", "hass"). The search is case-insensitive and 
                        supports partial matches.

    Returns:
        dict: A dictionary containing comprehensive nutritional information with the following fields:

        Basic Information:
            name (str): The exact name of the food item as stored in the database
            
        Base Nutritional Data:
            unitCalories100gml (str): Unit of measurement for calories, always "kcal" (kilocalories)
            calories100Gml (str): Calories per 100 grams or 100 milliliters of the food item
            
        Multiple Serving Size Options (up to 5 different serving sizes):
            serving1MlG through serving5MlG (str): Unit of measurement for each serving 
                - "g" for grams, "ml" for milliliters, empty string if serving option not available
            serving1Size through serving5Size (str): Weight or volume of the serving 
                - Numeric value as string (e.g., "37", "120"), empty string if not available
            serving1Unit through serving5Unit (str): Type of serving unit using internationalization keys:
                - "food.serving.label.piece" = individual pieces (1 pancake, 1 slice)
                - "food.serving.label.portion" = standard portion size
                - "food.serving.label.cup" = cup measurement
                - "food.serving.label.tablespoon" = tablespoon measurement
                - "food.serving.label.slice" = sliced items
                - Empty string if serving option not available
            serving1UnitNumber through serving5UnitNumber (str): Number of units in the serving
                - Usually "1" for single servings, empty string if not available
                
        Primary Display Serving (the default/recommended serving shown to users):
            displayPortionCalories (number): Calculated calories for the display serving size
                - Formula: (calories100Gml ÷ 100) × displayServingSize
            displayServingMlG (str): Unit for display serving ("g" for grams, "ml" for milliliters)
            displayServingSize (str): Size/weight of the display serving (numeric value as string)
            displayServingUnit (str): Unit type for display serving (same format as serving units above)
            displayServingUnitNumber (str): Number of units in display serving (usually "1")
            displayServingUnitOption (str): Additional serving size qualifier:
                - "" = standard/default size (no qualifier)
                - "food.serving.option.small" = small version
                - "food.serving.option.medium" = medium version  
                - "food.serving.option.large" = large version
                - "food.serving.option.whole" = whole item
                - "food.serving.option.sliced" = sliced preparation
                - "food.serving.option.shredded" = shredded preparation
                - "food.serving.option.crumbed" = crumbed/breaded preparation
                - "food.serving.option.ground" = ground preparation

    Usage Notes for LLM:
        - All numeric values are stored as strings and need parsing for calculations
        - Empty strings indicate unavailable data or unused serving options
        - The displayPortionCalories field provides pre-calculated calories for the main serving
        - Multiple serving options allow users to choose appropriate portion sizes
        - Serving unit labels use dot notation for internationalization
        - The display serving represents the most common or recommended portion size

    Example Response:
        {
            "name": "Potato Pancake",
            "unitCalories100gml": "kcal",
            "calories100Gml": "268",
            "serving1MlG": "g",
            "serving1Size": "37",
            "serving1Unit": "food.serving.label.piece",
            "serving1UnitNumber": "1",
            "serving2MlG": "g", 
            "serving2Size": "22",
            "serving2Unit": "food.serving.label.piece",
            "serving2UnitNumber": "1",
            "serving3MlG": "g",
            "serving3Size": "100", 
            "serving3Unit": "food.serving.label.portion",
            "serving3UnitNumber": "1",
            "serving4MlG": "",
            "serving4Size": "",
            "serving4Unit": "",
            "serving4UnitNumber": "",
            "serving5MlG": "",
            "serving5Size": "", 
            "serving5Unit": "",
            "serving5UnitNumber": "",
            "displayPortionCalories": 99.16,
            "displayServingMlG": "g",
            "displayServingSize": "37",
            "displayServingUnit": "food.serving.label.piece", 
            "displayServingUnitNumber": "1",
            "displayServingUnitOption": ""
        }

    When interpreting results for users:
        - Convert serving unit labels to human-readable format (remove "food.serving.label." prefix)
        - Use displayPortionCalories for the main calorie information
        - Present multiple serving options when available to give users choices
        - Calculate calories for custom serving sizes using: (calories100Gml ÷ 100) × desired_grams
        - Explain serving size qualifiers (small/medium/large/etc.) in plain language

    Use this when the user doesn't know the exact food name or wants
    related items, e.g.:

        search_food_nutrition("potato")
    """
    return food_items_service.search_food_nutrition(keyword)


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http"
    )

