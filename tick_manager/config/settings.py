import json
import re
from datetime import date
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

from tick_manager.config.exceptions import ConfigurationError

DATE_REGEX = r"^(19|20)\d\d-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"


def get_default_root_dir() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def get_default_env_file() -> Path:
    return get_default_root_dir() / ".env"


class HistoricalIngestorConfig(BaseSettings):
    """Configuration settings for the Historical Ingestor."""

    data_root: Path = Field(default_factory=get_default_root_dir, description="Root directory for historical data.")
    source: str = Field(default="databento", description="Data source for historical ingestion.")
    store_original_format: bool = Field(default=True, description="Flag to store data in original format.")
    output_format: str = Field(default="parquet", description="Output format for ingested data.")
    parquet_partitions: list[str] = Field(
        default=["year", "month", "day", "schema", "symbol"], description="Partitions for Parquet files."
    )
    start_date: str = Field(
        default_factory=lambda: date.today().isoformat(),
        description="Start date for data ingestion in YYYY-MM-DD format.",
    )
    end_date: str = Field(
        default_factory=lambda: date.today().isoformat(),
        description="End date for data ingestion in YYYY-MM-DD format.",
    )

    @field_validator("parquet_partitions", mode="before")
    def parse_parquet_partitions(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            try:
                json_v = json.loads(v)
                if not isinstance(json_v, list):
                    raise ConfigurationError(f"Invalid JSON for HISTORY_PARQUET_PARTITIONS: {v}")
                else:
                    return json_v
            except json.JSONDecodeError as e:
                raise ConfigurationError(f"Invalid JSON for HISTORY_PARQUET_PARTITIONS: {v}") from e
        return v

    @field_validator("start_date", "end_date")
    def validate_date_format(cls, v: str) -> str:
        regex = re.compile(DATE_REGEX)
        print(f"isinstance: {isinstance(v, str)}")
        print(f"regex: {bool(regex.fullmatch(v))}")
        if not isinstance(v, str) or not regex.fullmatch(v):
            raise ConfigurationError(f"{v} must be a string in 'YYYY-MM-DD' format.")
        return v

    class Config:
        env_prefix = "HISTORY_"


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
    root_dir: Path = Field(default_factory=get_default_root_dir)
    log_config: Path = Field(default_factory=lambda: get_default_root_dir() / "logging_config.yaml")
    log_handler: str = "default"
    debug: bool = False

    class ConfigDict:
        """
        Configuration class for Settings.

        Attributes:
            env_file (str): The name of the environment file to load settings from.
            env_file_encoding (str): The encoding of the environment file.
        """

        env_file = get_default_env_file()
        env_file_encoding = "utf-8"

    @field_validator("app_name", "root_dir", "log_config", "log_handler")
    def validate_not_empty(cls, v: str | Path) -> str | Path:
        if isinstance(v, str) and not v.strip():
            raise ValueError("app_name must not be empty")
        if isinstance(v, Path) and not v.name:
            raise ValueError("app_name must not be empty")
        return v
