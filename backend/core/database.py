from pymongo import MongoClient
import os
from core.logger import get_logger

logger = get_logger(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "trackmyexpenses")
client : MongoClient | None = None
db  = None

def connect_to_db():
    global client, db
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        logger.info("Connected to MongoDB at %s/%s", MONGO_URI, DB_NAME)
    except Exception:
        logger.exception("Failed to connect to MongoDB")
        raise

def close_db_connection():
    global client
    if client:
        client.close()
        client = None
        logger.info("Closed MongoDB connection")

