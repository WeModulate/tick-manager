import os
import unittest
from datetime import date
from unittest.mock import patch

from pydantic import ValidationError

from tick_manager.config.exceptions import ConfigurationError
from tick_manager.config.settings import HistoricalIngestorConfig, Settings, get_default_env_file, get_default_root_dir


class TestHistoricalIngestorConfig(unittest.TestCase):
    def test_default_values(self):
        config = HistoricalIngestorConfig()
        self.assertEqual(config.data_root, get_default_root_dir())
        self.assertEqual(config.source, "databento")
        self.assertTrue(config.store_original_format)
        self.assertEqual(config.output_format, "parquet")
        self.assertEqual(config.parquet_partitions, ["year", "month", "day", "schema", "symbol"])
        self.assertEqual(config.start_date, date.today().isoformat())
        self.assertEqual(config.end_date, date.today().isoformat())

    @patch.dict(os.environ, {"HISTORY_SOURCE": "env_source_value"})
    def test_settings_from_env(self):
        config = HistoricalIngestorConfig()
        self.assertEqual(config.source, "env_source_value")

    def test_parquet_partitions_parsing(self):
        config = HistoricalIngestorConfig(parquet_partitions='["year", "month", "day"]')
        self.assertEqual(config.parquet_partitions, ["year", "month", "day"])

    def test_invalid_parquet_partitions(self):
        with self.assertRaises(ConfigurationError):
            HistoricalIngestorConfig(parquet_partitions="invalid json")

    def test_invalid_date_format(self):
        with self.assertRaises(ConfigurationError):
            HistoricalIngestorConfig(start_date="2022-13-01")

        with self.assertRaises(ConfigurationError):
            HistoricalIngestorConfig(end_date="01-01-2022")


class TestSettings(unittest.TestCase):
    def test_default_settings(self):
        settings = Settings()
        self.assertEqual(settings.app_name, "Tick Manager")
        self.assertEqual(settings.root_dir, get_default_root_dir())
        self.assertEqual(settings.log_config, get_default_root_dir() / "logging_config.yaml")
        self.assertEqual(settings.log_handler, "default")
        self.assertFalse(settings.debug)

    def test_env_file_location(self):
        self.assertEqual(Settings.ConfigDict.env_file, get_default_env_file())

    def test_validate_not_empty(self):
        with self.assertRaises(ValidationError):
            Settings(app_name="")
