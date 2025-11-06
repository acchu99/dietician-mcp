
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import logging

logger = logging.getLogger(__name__)


class MongoDBClient:
    def __init__(self, uri: str):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
