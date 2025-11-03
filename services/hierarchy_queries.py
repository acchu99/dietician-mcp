from typing import List, Dict, Any
from db import MongoDBClient
import logging

logger = logging.getLogger(__name__)


class FoodHierarchyService:
    def __init__(self, db_client: MongoDBClient):
        self.foods = db_client.client.foods
        self.food_hierarchy_collection = self.foods.food_hierarchy

    def get_all_food_hierarchy(self) -> List[Dict[str, Any]]:
        """
        Return the full food hierarchy dataset.
        
        Returns:
            List[Dict]: List of category → subcategory → food_items mappings.
        """
        logger.debug("Fetching complete food hierarchy")
        output = list(self.food_hierarchy_collection.find({}))
        
        # Remove MongoDB's internal _id field
        for item in output:
            item.pop("_id", None)
        
        logger.info(f"Retrieved {len(output)} food hierarchy documents")
        return output
    
    def get_categories(self) -> List[str]:
        """
        Return a list of all food categories.
        
        Returns:
            List[str]: List of category names.
        """
        logger.debug("Fetching all food categories")
        categories = self.food_hierarchy_collection.distinct("category")
        logger.info(f"Retrieved {len(categories)} categories")
        return categories
    
    def get_subcategories(self, category: str) -> List[str]:
        """
        Return all subcategories for a given category.
        
        Args:
            category (str): The parent food category name.
            
        Returns:
            List[str]: List of subcategory names.
        """
        logger.debug(f"Fetching subcategories for category: {category}")
        subcategories = self.food_hierarchy_collection.distinct(
            "subcategory", {"category": category}
        )
        logger.info(f"Retrieved {len(subcategories)} subcategories for '{category}'")
        return subcategories
    
    def get_food_items(self, category: str, subcategory: str) -> List[str]:
        """
        Return all food items for a given category and subcategory.
        
        Args:
            category (str): The top-level food category.
            subcategory (str): The sub-group inside the category.
            
        Returns:
            List[str]: List of food item names, or empty list if not found.
        """
        logger.debug(f"Fetching food items for {category} - {subcategory}")
        
        doc = self.food_hierarchy_collection.find_one(
            {"category": category, "subcategory": subcategory},
            {"_id": 0, "food_items": 1}
        )
        
        result = doc["food_items"] if doc else []
        logger.info(f"Retrieved {len(result)} food items for '{category}' - '{subcategory}'")
        return result
    
    def search_food(self, keyword: str) -> List[Dict[str, str]]:
        """
        Search food items by keyword (case-insensitive).
        
        Args:
            keyword (str): Text to search inside food item names.
            
        Returns:
            List[Dict]: List of matching food items with their category and subcategory.
        """
        logger.debug(f"Searching food items with keyword: '{keyword}'")
        
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
        
        results = list(self.food_hierarchy_collection.aggregate(pipeline))
        logger.info(f"Found {len(results)} results for keyword '{keyword}'")
        return results
    
    def find_food_category(self, item: str) -> List[Dict[str, str]]:
        """
        Find the category and subcategory for a specific food item.
        
        Args:
            item (str): A food name to look up (case-insensitive exact match).
            
        Returns:
            List[Dict]: Matches containing category and subcategory fields.
        """
        logger.debug(f"Looking up category for food item: '{item}'")
        
        docs = list(self.food_hierarchy_collection.find(
            {"food_items": {"$regex": f"^{item}$", "$options": "i"}},
            {"_id": 0, "category": 1, "subcategory": 1}
        ))
        
        logger.info(f"Found {len(docs)} category matches for '{item}'")
        return docs
    
    def list_all_foods(self) -> List[str]:
        """
        Return a deduplicated, flattened list of all food item names.
        
        Returns:
            List[str]: All known food names.
        """
        logger.debug("Fetching all food items")
        
        pipeline = [
            {"$unwind": "$food_items"},
            {"$group": {"_id": None, "items": {"$addToSet": "$food_items"}}},
            {"$project": {"_id": 0, "items": 1}}
        ]
        
        result = list(self.food_hierarchy_collection.aggregate(pipeline))
        items = result[0]["items"] if result else []
        
        logger.info(f"Retrieved {len(items)} unique food items")
        return items
    
    def get_food_stats(self) -> Dict[str, Any]:
        """
        Return high-level statistics about the food hierarchy dataset.
        
        Returns:
            Dict: Statistics including total categories, subcategories, and item counts.
        """
        logger.debug("Calculating food hierarchy statistics")
        
        total_categories = len(self.food_hierarchy_collection.distinct("category"))
        total_subcategories = len(self.food_hierarchy_collection.distinct("subcategory"))
        
        pipeline = [
            {"$project": {"count": {"$size": "$food_items"}}},
            {"$group": {
                "_id": None,
                "avgItems": {"$avg": "$count"},
                "maxItems": {"$max": "$count"},
                "minItems": {"$min": "$count"}
            }}
        ]
        
        stats_result = list(self.food_hierarchy_collection.aggregate(pipeline))
        stats = stats_result[0] if stats_result else {
            "avgItems": 0, "maxItems": 0, "minItems": 0
        }
        
        result = {
            "total_categories": total_categories,
            "total_subcategories": total_subcategories,
            "average_items_per_subcategory": stats["avgItems"],
            "max_items_in_subcategory": stats["maxItems"],
            "min_items_in_subcategory": stats["minItems"]
        }
        
        logger.info(f"Calculated food hierarchy statistics: {result}")
        return result
