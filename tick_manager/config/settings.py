import logging.config
import os
from pathlib import Path

# deptry: ignore=DEP004
import yaml
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings class to load the configuration for the application

    Attributes:
        app_name (str): The name of the application.
        root_dir (str): The root directory of the application.
        log_config (str): The path to the logging configuration file.
        log_handler (str): The name of the logger handler to use.
        debug (bool): Flag to enable debug mode.
    """

    app_name: str = "Tick Manager"
    root_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    log_config: str = os.path.abspath(os.path.join(root_dir, "logging_config.yaml"))
    log_handler: str = "default"
    debug: bool = False

    class ConfigDict:
        """
        Configuration class for Settings.

        Attributes:
            env_file (str): The name of the environment file to load settings from.
            env_file_encoding (str): The encoding of the environment file.
        """

        env_file = os.path.abspath(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env")))
        env_file_encoding = "utf-8"

    @field_validator("app_name")
    def validate_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("app_name must not be empty")  # noqa: TRY003
        return v


# Instantiate the Settings class to load the configuration
settings = Settings()
log_config_file = Path(settings.log_config)

if log_config_file.is_file():
    try:
        with log_config_file.open("r") as f:
            config = yaml.safe_load(f)
            logging.config.dictConfig(config)
    except Exception as e:
        # Handle exceptions related to YAML parsing or logging configuration
        logging_level = logging.DEBUG if settings.debug else logging.INFO
        logging.basicConfig(level=logging_level)
        logging.exception(f"Failed to load logging configuration: {e}")  # noqa: TRY401
else:
    # Fallback to basic configuration if YAML file is not found
    logging_level = logging.DEBUG if settings.debug else logging.INFO
    logging.basicConfig(level=logging_level)
    logging.warning(f"Logging configuration file {settings.log_config} not found. Using basic configuration.")

# Retrieve the logger based on the settings
logger = logging.getLogger(settings.log_handler)

# Validate that the logger exists; if not, fallback to the root logger
if not logger.handlers:
    logging.warning(f"Logger '{settings.log_handler}' not found in logging configuration. Using root logger.")
    logger = logging.getLogger()

logger.info(f"Using environment file: {settings.ConfigDict.env_file}")
logger.info(f"Settings:\n {settings.model_dump()}")
