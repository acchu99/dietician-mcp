
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def mongo_client(uri: str) -> MongoClient | None:
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        return None
