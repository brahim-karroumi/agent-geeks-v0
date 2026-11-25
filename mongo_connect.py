import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

load_dotenv()

_client = None


def get_mongo_client():
    global _client

    if _client is not None:
        return _client

    uri = os.getenv("MONGODB_URI")
    if not uri or not uri.strip():
        raise ValueError("MONGODB_URI is not set in .env")

    client = MongoClient(uri.strip(), serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    _client = client
    return _client


def get_database(name=None):
    client = get_mongo_client()
    db_name = name or os.getenv("MONGODB_DB", "agent_v1")
    return client[db_name]


def get_collection(collection_name, db_name=None):
    if not isinstance(collection_name, str) or not collection_name.strip():
        raise ValueError("collection_name must be a non-empty string.")
    return get_database(db_name)[collection_name.strip()]


if __name__ == "__main__":
    try:
        client = get_mongo_client()
        db = get_database()
        print("MongoDB connection succeeded!")
        print(f"Database: {db.name}")
        print(f"Collections: {db.list_collection_names()}")
        client.close()
    except (ConnectionFailure, PyMongoError, ValueError) as error:
        print(f"MongoDB connection failed: {error}")
