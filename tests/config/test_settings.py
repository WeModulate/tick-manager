import logging
import os
from unittest.mock import MagicMock, mock_open, patch

import pytest
from pydantic import ValidationError

from tick_manager.config.settings import Settings


def test_default_values():
    settings = Settings()
    assert settings.app_name == "Tick Manager"
    assert isinstance(settings.root_dir, str)
    assert isinstance(settings.log_config, str)
    assert settings.log_handler == "default"
    assert settings.debug is False


def test_app_name_validation():
    with pytest.raises(ValidationError) as exc_info:
        Settings(app_name="   ")
    assert "app_name must not be empty" in str(exc_info.value)


@patch.dict(os.environ, {"APP_NAME": "Test App", "DEBUG": "true", "LOG_HANDLER": "debug"})
def test_settings_from_env():
    settings = Settings()
    assert settings.app_name == "Test App"
    assert settings.debug is True
    assert settings.log_handler == "debug"


@patch("tick_manager.config.settings.Path.is_file", return_value=True)
@patch("tick_manager.config.settings.Path.open", new_callable=mock_open, read_data="logging: config")
@patch("tick_manager.config.settings.yaml.safe_load", return_value={"version": 1})
def test_logging_config_loaded(mock_safe_load, mock_file, mock_is_file):
    # settings = Settings()
    with patch("tick_manager.config.settings.logging.config.dictConfig") as mock_dict_config:
        # Re-import the module to trigger the logging configuration
        import importlib

        importlib.reload(importlib.import_module("tick_manager.config.settings"))
        mock_dict_config.assert_called_once_with({"version": 1})


@patch("tick_manager.config.settings.Path.is_file", return_value=False)
def test_logging_config_fallback(mock_is_file, caplog):
    settings = Settings()
    with patch("tick_manager.config.settings.logging.basicConfig") as mock_basic_config:
        # Re-import the module to trigger the logging fallback
        import importlib

        importlib.reload(importlib.import_module("tick_manager.config.settings"))
        mock_basic_config.assert_called_once()
        assert f"Logging configuration file {settings.log_config} not found. Using basic configuration." in caplog.text


def test_env_file_path():
    settings = Settings()
    expected_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
    assert settings.ConfigDict.env_file == expected_path
    assert settings.ConfigDict.env_file_encoding == "utf-8"


def test_logger_exists():
    with patch("tick_manager.config.settings.logging.getLogger") as mock_get_logger:
        mock_logger = mock_get_logger.return_value
        mock_logger.handlers = [object()]
        settings = Settings()
        import importlib

        importlib.reload(importlib.import_module("tick_manager.config.settings"))
        mock_get_logger.assert_called_with(settings.log_handler)


def test_logger_fallback(caplog):
    with (
        patch("tick_manager.config.settings.logging.getLogger") as mock_get_logger,
        patch("tick_manager.config.settings.logging.basicConfig"),
        patch("tick_manager.config.settings.Path.is_file", return_value=False),
    ):
        mock_logger = mock_get_logger.return_value
        mock_logger.handlers = []
        mock_logger.manager = MagicMock()
        mock_logger.manager.disable = logging.NOTSET  # Ensure this is a valid log level
        # settings = Settings()

        # Start capturing logs
        with caplog.at_level(logging.WARNING):
            import importlib

            importlib.reload(importlib.import_module("tick_manager.config.settings"))

            # Ensure the warning was called
            assert "Logger 'default' not found in logging configuration. Using root logger." in caplog.text
            # mock_get_logger.assert_called_with()
