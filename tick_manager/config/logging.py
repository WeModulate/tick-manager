# logging_setup.py

import logging
from pathlib import Path

import yaml

from tick_manager.config.settings import Settings


def setup_logging(settings: Settings) -> logging.Logger:
    log_config_file = Path(settings.log_config)

    if log_config_file.is_file():
        try:
            with log_config_file.open("r") as f:
                config = yaml.safe_load(f)
                logging.config.dictConfig(config)
        except Exception:
            logging_level = logging.DEBUG if settings.debug else logging.INFO
            logging.basicConfig(level=logging_level)
            logging.exception("Failed to load logging configuration")
    else:
        logging_level = logging.DEBUG if settings.debug else logging.INFO
        logging.basicConfig(level=logging_level)
        logging.warning(f"Logging configuration file {settings.log_config} not found. Using basic configuration.")

    logger = logging.getLogger(settings.log_handler)

    if not logger.handlers:
        logging.warning(f"Logger '{settings.log_handler}' not found in logging configuration. Using root logger.")
        logger = logging.getLogger()

    return logger
