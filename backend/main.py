import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from middleware.auth import AuthMiddleware
from routers.routes import router
from core.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    try:
        from core.database import init_db, connect_to_db
        init_db()
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

_cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)