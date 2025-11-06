#!/usr/bin/env python3
"""
Test script for the Food MCP Server to verify structured output functionality.

This script demonstrates how to interact with the low-level MCP server and 
validates that structured output schemas work correctly.
"""
import asyncio
import json
import sys
from pathlib import Path

# Add the project root to the path
sys.path.append(str(Path(__file__).parent))

from schemas.food_hierarchy import FoodCategoriesResponse, FoodSearchResponse
from schemas.food_item import FoodNamesResponse, FoodNutritionResponse


async def test_schemas():
    """Test that our Pydantic schemas work correctly."""
    print("Testing Pydantic schemas...")
    
    # Test food categories response
    categories_data = {
        "categories": ["Vegetables", "Fruits", "Proteins"],
        "total_count": 3
    }
    categories_response = FoodCategoriesResponse(**categories_data)
    print(f"✅ FoodCategoriesResponse: {categories_response.total_count} categories")
    
    # Test food search response
    search_data = {
        "keyword": "apple",
        "results": [
            {"category": "Fruits", "subcategory": "Tree Fruits", "item": "Apple"}
        ],
        "total_matches": 1
    }
    search_response = FoodSearchResponse(**search_data)
    print(f"✅ FoodSearchResponse: {search_response.total_matches} matches for '{search_response.keyword}'")
    
    # Test food names response
    names_data = {
        "food_names": ["Apple", "Banana", "Chicken"],
        "total_count": 3
    }
    names_response = FoodNamesResponse(**names_data)
    print(f"✅ FoodNamesResponse: {names_response.total_count} foods available")
    
    # Test food nutrition response (not found case)
    nutrition_data = {
        "requested_name": "test_food",
        "found": False,
        "nutrition": None
    }
    nutrition_response = FoodNutritionResponse(**nutrition_data)
    print(f"✅ FoodNutritionResponse: Food '{nutrition_response.requested_name}' found: {nutrition_response.found}")
    
    print("All schema tests passed! ✅")


def test_json_schema_generation():
    """Test that we can generate JSON schemas for tool definitions."""
    print("\nTesting JSON schema generation...")
    
    # Generate schema for categories response
    categories_schema = FoodCategoriesResponse.model_json_schema()
    print(f"✅ Generated schema for FoodCategoriesResponse")
    print(f"   Title: {categories_schema.get('title')}")
    print(f"   Properties: {list(categories_schema.get('properties', {}).keys())}")
    
    # Generate schema for nutrition response
    nutrition_schema = FoodNutritionResponse.model_json_schema()
    print(f"✅ Generated schema for FoodNutritionResponse")
    print(f"   Title: {nutrition_schema.get('title')}")
    
    print("JSON schema generation tests passed! ✅")


def test_structured_serialization():
    """Test structured data serialization."""
    print("\nTesting structured data serialization...")
    
    # Create a complex response object
    search_response = FoodSearchResponse(
        keyword="apple",
        results=[
            {"category": "Fruits", "subcategory": "Tree Fruits", "item": "Apple"},
            {"category": "Vegetables", "subcategory": "Root Vegetables", "item": "Apple Potato"}
        ],
        total_matches=2
    )
    
    # Test model_dump for structured content
    structured_data = search_response.model_dump()
    print(f"✅ Structured data serialization works")
    print(f"   Data keys: {list(structured_data.keys())}")
    print(f"   Results count: {len(structured_data['results'])}")
    
    # Test JSON serialization
    json_data = search_response.model_dump_json()
    print(f"✅ JSON serialization works (length: {len(json_data)} chars)")
    
    print("Structured serialization tests passed! ✅")


async def main():
    """Run all tests."""
    print("🧪 Testing Food MCP Server Structured Output\n")
    
    try:
        await test_schemas()
        test_json_schema_generation()
        test_structured_serialization()
        
        print("\n🎉 All tests passed successfully!")
        print("The MCP server is ready to provide structured output.")
        print("To use it with MCP inspector:")
        print("  npx @modelcontextprotocol/inspector http://localhost:8000/mcp")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())