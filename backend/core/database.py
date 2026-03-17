from pymongo import MongoClient
from pymongo.errors import OperationFailure
import os
from core.logger import get_logger

logger = get_logger(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "trackmyexpenses")
client: MongoClient | None = None
db = None


def init_db():
    """
    Run once at startup (as admin) to create the app DB user if it doesn't exist.
    Safe to call on every boot — skips creation if user already exists.
    Requires MONGO_ADMIN_URI, MONGO_APP_USER, MONGO_APP_PASSWORD in env.
    """
    admin_uri = os.getenv("MONGO_ADMIN_URI")
    app_user = os.getenv("MONGO_APP_USER")
    app_password = os.getenv("MONGO_APP_PASSWORD")

    if not all([admin_uri, app_user, app_password]):
        logger.info("Mongo init vars not set — skipping DB user creation")
        return

    admin_client = MongoClient(admin_uri)
    try:
        app_db = admin_client[DB_NAME]
        result = app_db.command("usersInfo", {"user": app_user, "db": DB_NAME})
        if result.get("users"):
            logger.info("DB user '%s' already exists — skipping creation", app_user)
            return

        app_db.command(
            "createUser",
            app_user,
            pwd=app_password,
            roles=[{"role": "readWrite", "db": DB_NAME}],
        )
        logger.info("Created DB user '%s'", app_user)
    except OperationFailure:
        logger.exception("Failed to create DB user — check MONGO_ADMIN_URI credentials")
        raise
    finally:
        admin_client.close()


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

