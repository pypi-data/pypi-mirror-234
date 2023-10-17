import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

from colorlog import ColoredFormatter

LOGGER = logging.getLogger(__name__)
LOGGERS = {}


class DuplicateFilter(logging.Filter):
    def filter(self, record):
        repeated_number_exists = getattr(self, "repeated_number", None)
        current_log = (record.module, record.levelno, record.msg)
        if current_log != getattr(self, "last_log", None):
            self.last_log = current_log
            if repeated_number_exists:
                LOGGER.warning(f"Last log repeated {self.repeated_number} times.")

            self.repeated_number = 0
            return True
        if repeated_number_exists:
            self.repeated_number += 1
        else:
            self.repeated_number = 1
        return False


class WrapperLogFormatter(ColoredFormatter):
    def formatTime(self, record, datefmt=None):  # noqa: N802
        return datetime.fromtimestamp(record.created).isoformat()


def get_logger(
    name: str,
    level: int or str = logging.INFO,
    filename: str = None,
    console: bool = True,
    file_max_bytes: int = 104857600,
    file_backup_count: int = 20,
) -> logging.Logger:
    """
    Get logger object for logging.

    Args:
        name (str):): name of the logger
        level (int or str): level of logging
        filename (str): filename (full path) for log file
        console (bool): whether to log to console
        file_max_bytes (int): log file size max size in bytes
        file_backup_count (int): max number of log files to keep

    Returns:
        Logger: logger object

    """
    if LOGGERS.get(name):
        return LOGGERS.get(name)

    logging.SUCCESS = 32
    logging.addLevelName(logging.SUCCESS, "SUCCESS")
    logger_obj = logging.getLogger(name)
    logger_obj.success = lambda msg, *args: logger_obj._log(logging.SUCCESS, msg, args)
    log_formatter = WrapperLogFormatter(
        fmt="%(asctime)s %(name)s %(log_color)s%(levelname)s%(reset)s %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "SUCCESS": "bold_green",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
    )

    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(fmt=log_formatter)
        console_handler.addFilter(filter=DuplicateFilter())

        logger_obj.addHandler(hdlr=console_handler)

    logger_obj.setLevel(level=level)
    logger_obj.addFilter(filter=DuplicateFilter())

    if filename:
        log_handler = RotatingFileHandler(
            filename=filename, maxBytes=file_max_bytes, backupCount=file_backup_count
        )
        log_handler.setFormatter(fmt=log_formatter)
        log_handler.setLevel(level=level)
        logger_obj.addHandler(hdlr=log_handler)

    logger_obj.propagate = False
    LOGGERS[name] = logger_obj
    return logger_obj
