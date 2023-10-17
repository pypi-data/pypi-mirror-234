import logging

from simple_logger.logger import get_logger


class TestGetLogger:
    def test_existing_logger(self):
        logger1 = get_logger(name="test_logger")
        logger2 = get_logger(name="test_logger")
        assert logger1 == logger2

    def test_valid_name(self):
        logger = get_logger(name="test_logger")
        assert isinstance(logger, logging.Logger)

    def test_disable_console_logging(self):
        logger = get_logger(name="test_logger", console=False)
        assert isinstance(logger, logging.Logger)
