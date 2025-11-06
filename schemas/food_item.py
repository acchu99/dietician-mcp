"""
Pydantic schemas for food nutrition data structures.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class FoodNutrition(BaseModel):
    """Complete nutritional information for a food item."""
    
    # Basic Information
    name: str = Field(description="The exact name of the food item as stored in the database")
    
    # Base Nutritional Data
    unit_calories_100g_ml: str = Field(
        description="Unit of measurement for calories, always 'kcal' (kilocalories)",
        alias="unitCalories100gml"
    )
    calories_100g_ml: str = Field(
        description="Calories per 100 grams or 100 milliliters of the food item",
        alias="calories100Gml"
    )
    
    # Multiple Serving Size Options (up to 5 different serving sizes)
    serving1_ml_g: str = Field(
        description="Unit of measurement for serving 1: 'g' for grams, 'ml' for milliliters, empty string if not available",
        alias="serving1MlG"
    )
    serving1_size: str = Field(
        description="Weight or volume of serving 1 as numeric string (e.g., '37', '120'), empty string if not available",
        alias="serving1Size"
    )
    serving1_unit: str = Field(
        description="Type of serving unit using internationalization keys (e.g., 'food.serving.label.piece'), empty string if not available",
        alias="serving1Unit"
    )
    serving1_unit_number: str = Field(
        description="Number of units in serving 1 (usually '1'), empty string if not available",
        alias="serving1UnitNumber"
    )
    
    serving2_ml_g: str = Field(default="", alias="serving2MlG")
    serving2_size: str = Field(default="", alias="serving2Size")
    serving2_unit: str = Field(default="", alias="serving2Unit")
    serving2_unit_number: str = Field(default="", alias="serving2UnitNumber")
    
    serving3_ml_g: str = Field(default="", alias="serving3MlG")
    serving3_size: str = Field(default="", alias="serving3Size")
    serving3_unit: str = Field(default="", alias="serving3Unit")
    serving3_unit_number: str = Field(default="", alias="serving3UnitNumber")
    
    serving4_ml_g: str = Field(default="", alias="serving4MlG")
    serving4_size: str = Field(default="", alias="serving4Size")
    serving4_unit: str = Field(default="", alias="serving4Unit")
    serving4_unit_number: str = Field(default="", alias="serving4UnitNumber")
    
    serving5_ml_g: str = Field(default="", alias="serving5MlG")
    serving5_size: str = Field(default="", alias="serving5Size")
    serving5_unit: str = Field(default="", alias="serving5Unit")
    serving5_unit_number: str = Field(default="", alias="serving5UnitNumber")
    
    # Primary Display Serving
    display_portion_calories: float = Field(
        description="Calculated calories for the display serving size",
        alias="displayPortionCalories"
    )
    display_serving_ml_g: str = Field(
        description="Unit for display serving ('g' for grams, 'ml' for milliliters)",
        alias="displayServingMlG"
    )
    display_serving_size: str = Field(
        description="Size/weight of the display serving (numeric value as string)",
        alias="displayServingSize"
    )
    display_serving_unit: str = Field(
        description="Unit type for display serving (same format as serving units)",
        alias="displayServingUnit"
    )
    display_serving_unit_number: str = Field(
        description="Number of units in display serving (usually '1')",
        alias="displayServingUnitNumber"
    )
    display_serving_unit_option: str = Field(
        description="Additional serving size qualifier (e.g., 'food.serving.option.small')",
        alias="displayServingUnitOption"
    )

    class Config:
        allow_population_by_field_name = True


class FoodNutritionSearchResult(BaseModel):
    """Search result for food nutrition entries."""
    
    name: str = Field(description="Name of the food item found in search")
    relevance_score: Optional[float] = Field(
        None, 
        description="Optional relevance score for search ranking"
    )
    nutrition: FoodNutrition = Field(description="Complete nutritional information")


class FoodNamesResponse(BaseModel):
    """Response containing list of all food names with nutrition data."""
    
    food_names: List[str] = Field(description="List of all food names that have nutrition data available")
    total_count: int = Field(description="Total number of foods with nutrition data")


class FoodNutritionResponse(BaseModel):
    """Response containing nutrition information for a specific food."""
    
    requested_name: str = Field(description="The food name that was requested")
    found: bool = Field(description="Whether the food was found in the database")
    nutrition: Optional[FoodNutrition] = Field(
        None, 
        description="Nutritional information if food was found"
    )
    suggestions: Optional[List[str]] = Field(
        None,
        description="Suggested similar food names if exact match not found"
    )


class FoodNutritionSearchResponse(BaseModel):
    """Response containing search results for food nutrition entries."""
    
    search_keyword: str = Field(description="The keyword used for searching")
    results: List[FoodNutritionSearchResult] = Field(description="List of matching food nutrition entries")
    total_matches: int = Field(description="Total number of matches found")


class ServingInfo(BaseModel):
    """Structured information about a food serving."""
    
    size: str = Field(description="Serving size as numeric string")
    unit: str = Field(description="Serving unit type")
    unit_number: str = Field(description="Number of units in serving")
    measurement_unit: str = Field(description="'g' for grams or 'ml' for milliliters")
    calories: Optional[float] = Field(None, description="Calculated calories for this serving")


class StructuredFoodNutrition(BaseModel):
    """Structured version of food nutrition with parsed serving information."""
    
    name: str = Field(description="Food item name")
    calories_per_100g: float = Field(description="Calories per 100g/ml as numeric value")
    
    # Structured serving information
    servings: List[ServingInfo] = Field(description="List of available serving sizes")
    
    # Primary display serving
    primary_serving: ServingInfo = Field(description="Primary/recommended serving size")
    primary_serving_calories: float = Field(description="Calories in the primary serving")
    
    # Additional metadata
    serving_unit_option: str = Field(description="Serving size qualifier (small/medium/large/etc.)")
    
    class Config:
        json_encoders = {
            float: lambda v: round(v, 2)  # Round calories to 2 decimal places
        }
