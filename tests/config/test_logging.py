import logging
import unittest
from unittest.mock import mock_open, patch

from tick_manager.config.logging import setup_logging
from tick_manager.config.settings import Settings


class TestLoggingSetup(unittest.TestCase):
    @patch("logging_setup.Path.is_file", return_value=True)
    @patch("logging_setup.open", new_callable=mock_open, read_data="{}")
    @patch("logging.config.dictConfig")
    def loads_logging_configuration_from_file(self, mock_dictConfig, mock_open, mock_is_file):
        settings = Settings(log_config="log_config.yaml", debug=False, log_handler="test_handler")
        logger = setup_logging(settings)
        mock_dictConfig.assert_called_once()
        self.assertEqual(logger.name, "test_handler")

    @patch("logging_setup.Path.is_file", return_value=False)
    @patch("logging.basicConfig")
    def uses_basic_configuration_when_file_not_found(self, mock_basicConfig, mock_is_file):
        settings = Settings(log_config="log_config.yaml", debug=False, log_handler="test_handler")
        logger = setup_logging(settings)
        mock_basicConfig.assert_called_once_with(level=logging.INFO)
        self.assertEqual(logger.name, "root")

    @patch("logging_setup.Path.is_file", return_value=True)
    @patch("logging_setup.open", new_callable=mock_open, read_data="invalid_yaml")
    @patch("logging.basicConfig")
    @patch("logging.exception")
    def uses_basic_configuration_on_exception(self, mock_exception, mock_basicConfig, mock_open, mock_is_file):
        settings = Settings(log_config="log_config.yaml", debug=True, log_handler="test_handler")
        logger = setup_logging(settings)
        mock_basicConfig.assert_called_once_with(level=logging.DEBUG)
        mock_exception.assert_called_once()
        self.assertEqual(logger.name, "root")

    @patch("logging_setup.Path.is_file", return_value=True)
    @patch("logging_setup.open", new_callable=mock_open, read_data="{}")
    @patch("logging.config.dictConfig")
    @patch("logging.getLogger")
    def uses_root_logger_if_handler_not_found(self, mock_getLogger, mock_dictConfig, mock_open, mock_is_file):
        mock_getLogger.return_value.handlers = []
        settings = Settings(log_config="log_config.yaml", debug=False, log_handler="non_existent_handler")
        logger = setup_logging(settings)
        mock_getLogger.assert_called_with("non_existent_handler")
        self.assertEqual(logger.name, "root")
