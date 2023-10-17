import logging
from logging.config import dictConfig


from pydantic import BaseModel


class LogConfig(BaseModel):
    LOGGER_NAME: str = "wf_honeycomb_rds_client"
    LOG_FORMAT: str = "%(asctime)s,%(msecs)03d | %(levelname)s | %(name)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "format": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


dictConfig(LogConfig().dict())
logger = logging.getLogger("wf_honeycomb_rds_client")
