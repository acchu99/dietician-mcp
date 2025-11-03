import os
from dotenv import load_dotenv
from db import MongoDBClient, FoodHierarchyService

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

try:
    db_client = MongoDBClient(uri=os.getenv("MONGODB_URI"))
    food_service = FoodHierarchyService(db_client)
    logger.info("Successfully initialized food service")
except Exception as e:
    logger.error(f"Failed to initialize food service: {e}")
    raise


if __name__ == "__main__":
    food_service.get_all_food_hierarchy()
    food_service.get_categories()
    food_service.get_subcategories("fruits & vegetables")
    food_service.get_food_items("fruits & vegetables", "potatoes & potato products")
    food_service.search_food("apple")
    food_service.find_food_category("potato pancake")
    food_service.list_all_foods()
    food_service.get_food_stats()