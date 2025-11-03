from typing import List, Dict, Any
from db import MongoDBClient
import logging

logger = logging.getLogger(__name__)


class FoodItemService:
    def __init__(self, db_client: MongoDBClient):
        self.foods = db_client.client.foods
        self.food_items_collection = self.foods.food_items

    def get_food_items(self, category: str, subcategory: str) -> List[dict]:
        """
        Return all food items for a given category and subcategory.

        Args:
            category (str): The parent food category name.
            subcategory (str): The food subcategory name.

        Returns:
            List[dict]: A list of food items matching the category and subcategory.
        """
        logger.debug(f"Fetching food items for {category} - {subcategory}")

        food_items = list(self.food_items_collection.find({
            "category": category,
            "subcategory": subcategory
        }))

        logger.info(f"Retrieved {len(food_items)} food items for '{category}' - '{subcategory}'")
        return food_items
