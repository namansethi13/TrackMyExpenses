import logging
import os
import sys
from logging.handlers import RotatingFileHandler

DEFAULT_LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", 10 * 1024 * 1024))
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", 5))


def configure_logging() -> None:
    """Configure root logging for the application.

    - Console (stdout) handler
    - Rotating file handler at LOG_FILE
    - Sets uvicorn loggers to propagate to the root logger
    """
    # Basic root logger setup
    level = getattr(logging, DEFAULT_LOG_LEVEL, logging.INFO)

    # Clear existing handlers to avoid duplicate logs when re-importing
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)

    root.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    root.addHandler(console_handler)

    # File handler
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    root.addHandler(file_handler)

    # Make uvicorn logs propagate to root (so they use our handlers/format)
    for name in ("uvicorn.error", "uvicorn.access", "uvicorn.asgi"):
        uvlogger = logging.getLogger(name)
        uvlogger.handlers = []
        uvlogger.propagate = True
        uvlogger.setLevel(level)


# Configure logging immediately on import so other modules can log right away
configure_logging()


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
