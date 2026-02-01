from fastapi import FastAPI
from middleware.auth import AuthMiddleware
from routers.routes import router
from core.logger import get_logger
from contextlib import asynccontextmanager

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    try:
        from core.database import connect_to_db
        connect_to_db()
        logger.info("Connected to database")
    except Exception:
        logger.exception("Failed to connect to database")
    yield
    logger.info("Shutting down application")
    try:
        from core.database import close_db_connection
        close_db_connection()
        logger.info("Closed database connection")
    except Exception:
        logger.exception("Error during shutdown")


app = FastAPI(lifespan=lifespan)
app.add_middleware(AuthMiddleware)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)