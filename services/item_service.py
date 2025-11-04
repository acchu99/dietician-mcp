from typing import List, Dict, Any, Optional
from db import MongoDBClient
import logging

logger = logging.getLogger(__name__)

class FoodItemsService:
    def __init__(self, db_client: MongoDBClient):
        self.foods = db_client.client.foods
        self.food_items_collection = self.foods.food_items

    def get_all_food_items(self) -> List[Dict[str, Any]]:
        """
        Return all food nutrition documents.
        Removes internal _id field.
        """
        logger.debug("Fetching all food nutrition documents")
        data = list(self.food_items_collection.find({}, {"_id": 0}))
        logger.info(f"Retrieved {len(data)} food nutrition entries")
        return data

    def list_food_names(self) -> List[str]:
        """
        Return a list of all food names present in the nutrition database.
        """
        logger.debug("Fetching food names from nutrition collection")
        names = self.food_items_collection.distinct("name")
        logger.info(f"Retrieved {len(names)} food names")
        return names

    def get_food_nutrition(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get full nutrition + serving data for a food item by exact name (case-insensitive).
        """
        logger.debug(f"Looking up nutrition information for: {name}")
        doc = self.food_items_collection.find_one(
            {"name": {"$regex": f"^{name}$", "$options": "i"}},
            {"_id": 0}
        )
        logger.info(f"Nutrition found: {bool(doc)} for '{name}'")
        return doc

    def search_food_nutrition(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Search food nutrition docs by partial name (case-insensitive).
        """
        logger.debug(f"Searching nutrition collection for keyword: {keyword}")
        pipeline = [
            {"$match": {"name": {"$regex": keyword, "$options": "i"}}},
            {"$project": {"_id": 0}}
        ]
        results = list(self.food_items_collection.aggregate(pipeline))
        logger.info(f"Found {len(results)} matches for keyword '{keyword}'")
        return results

    def get_display_calories(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Return food name + default serving size + calories for that serving.
        """
        logger.debug(f"Fetching display calories for: {name}")
        doc = self.get_food_nutrition(name)
        if not doc:
            logger.info(f"No display calories found for '{name}'")
            return None

        return {
            "name": doc["name"],
            "displayServingSize": doc.get("displayServingSize"),
            "displayServingUnit": doc.get("displayServingUnit"),
            "displayServingUnitNumber": doc.get("displayServingUnitNumber"),
            "displayPortionCalories": doc.get("displayPortionCalories")
        }
