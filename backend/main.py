from fastapi import FastAPI
from middleware.auth import AuthMiddleware
from routers.routes import router
from core.logger import get_logger
from contextlib import asynccontextmanager
import os

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
    
    # Set up Telegram webhook for local development if dev mode is enabled
    dev_mode = os.getenv("DEV", "0") == "1"
    if dev_mode:
        logger.info("Dev mode enabled. Setting up Telegram webhook...")
        try:
            from dev_util_scripts.localhost_webhook_to_tg import LocalhostWebhookManager
            
            bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
            if bot_token:
                webhook_manager = LocalhostWebhookManager(local_port=8000)
                success = webhook_manager.setup_telegram_webhook(bot_token)
                if success:
                    app.state.webhook_manager = webhook_manager
                    logger.info("Telegram webhook setup completed")
                else:
                    logger.warning("Failed to set up Telegram webhook")
            else:
                logger.warning("TELEGRAM_BOT_TOKEN not set, skipping webhook setup")
        except Exception as e:
            logger.warning(f"Error setting up Telegram webhook: {e}")
    
    yield
    logger.info("Shutting down application")
    
    # Cleanup webhook manager if it exists
    if dev_mode and hasattr(app.state, "webhook_manager"):
        try:
            app.state.webhook_manager.cleanup()
        except Exception as e:
            logger.error(f"Error cleaning up webhook manager: {e}")
    
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