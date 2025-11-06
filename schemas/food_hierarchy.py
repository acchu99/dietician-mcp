"""
Pydantic schemas for food hierarchy data structures.
"""
from typing import List, Dict, Any
from pydantic import BaseModel, Field


class FoodHierarchyItem(BaseModel):
    """Individual food hierarchy item with category, subcategory and food items."""
    
    category: str = Field(description="Top-level food category name")
    subcategory: str = Field(description="Subcategory within the category") 
    food_items: List[str] = Field(description="List of food item names in this subcategory")


class FoodSearchResult(BaseModel):
    """Result of searching food items by keyword."""
    
    category: str = Field(description="Food category containing the item")
    subcategory: str = Field(description="Food subcategory containing the item")
    item: str = Field(description="Name of the food item that matched")


class FoodCategoryResult(BaseModel):
    """Result of finding category information for a food item."""
    
    category: str = Field(description="Food category containing the item")
    subcategory: str = Field(description="Food subcategory containing the item")


class FoodStats(BaseModel):
    """Statistics about the food hierarchy dataset."""
    
    total_categories: int = Field(description="Total number of food categories")
    total_subcategories: int = Field(description="Total number of food subcategories")
    average_items_per_subcategory: float = Field(description="Average number of food items per subcategory")
    max_items_in_subcategory: int = Field(description="Maximum number of items in any subcategory")
    min_items_in_subcategory: int = Field(description="Minimum number of items in any subcategory")


class FoodHierarchyResponse(BaseModel):
    """Response containing complete food hierarchy data."""
    
    hierarchy: List[FoodHierarchyItem] = Field(description="Complete food hierarchy dataset")


class FoodCategoriesResponse(BaseModel):
    """Response containing list of food categories."""
    
    categories: List[str] = Field(description="List of all food category names")
    total_count: int = Field(description="Total number of categories")


class FoodSubcategoriesResponse(BaseModel):
    """Response containing list of subcategories for a category."""
    
    category: str = Field(description="The category these subcategories belong to")
    subcategories: List[str] = Field(description="List of subcategory names")


class FoodItemsResponse(BaseModel):
    """Response containing list of food items for a category/subcategory."""
    
    category: str = Field(description="The category these items belong to")
    subcategory: str = Field(description="The subcategory these items belong to")
    food_items: List[str] = Field(description="List of food item names")


class FoodSearchResponse(BaseModel):
    """Response containing search results for food items."""
    
    keyword: str = Field(description="The search keyword used")
    results: List[FoodSearchResult] = Field(description="List of matching food items")
    total_matches: int = Field(description="Total number of matches found")


class FoodCategoryLookupResponse(BaseModel):
    """Response containing category lookup results for a food item."""
    
    item: str = Field(description="The food item that was searched for")
    matches: List[FoodCategoryResult] = Field(description="List of category matches")


class AllFoodsResponse(BaseModel):
    """Response containing all unique food names."""
    
    foods: List[str] = Field(description="Complete list of all unique food names")
