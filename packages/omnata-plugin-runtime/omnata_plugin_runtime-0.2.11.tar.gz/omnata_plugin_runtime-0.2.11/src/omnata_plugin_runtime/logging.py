"""
Custom logging functionality for Omnata
"""
import logging
import logging.handlers
import traceback
from logging import Logger
from typing import Dict, List, Optional
from snowflake.snowpark import Session
from pydantic import ValidationError


def log_exception(exception: Exception, logger_instance: Logger):
    """
    Logs an exception to a logger
    """
    # if the exception is a ValidationError, log the errors
    if isinstance(exception, ValidationError):
        logger_instance.error(
            f"""Validation error occurred: {exception.json()}
Stack trace: {traceback.format_exc()}"""
        )  # pylint: disable=no-member
    else:
        try:
            logger_instance.error(exception, exc_info=True, stack_info=True)
        except Exception as exception2:  # pylint: disable=broad-except
            # fall back on just logging a string representation of the exception
            logger_instance.error(str(exception))


class CustomLogger(logging.getLoggerClass()):
    """
    Custom logger that can handle pydantic validation errors.
    Without this, you get "Object of type ErrorWrapper is not JSON serializable"
    when logging the exception.
    """

    def handleError(self, record):
        if record.exc_info:
            exc_type, exc_value, tb = record.exc_info
            if isinstance(exc_value, ValidationError):
                record.msg = exc_value.errors()
                record.exc_info = (exc_type, None, tb)
        super().handleError(record)  # type: ignore


class OmnataPluginLogHandler(logging.Handler):
    """
    A logging handler which does two things:
    1) For inbound syncs, keeps a track of how many errors have occurred per stream
    2)
    Additional information about the current sync and run is included, so that logs can be filtered easily.
    """

    def __init__(
        self,
        session: Session,
        sync_id: int,
        sync_branch_id: Optional[int],
        connection_id: int,
        sync_run_id: int,
    ):
        logging.Handler.__init__(self)
        self.session = session
        self.sync_id = sync_id
        self.sync_branch_id = sync_branch_id
        self.connection_id = connection_id
        self.sync_run_id = sync_run_id
        self.stream_has_errors: Dict[str, bool] = {}

    def emit(self, record: logging.LogRecord):
        if hasattr(record, "stream_name"):
            stream_name: str = record.stream_name  # type: ignore
            if record.levelno >= logging.ERROR:
                self.stream_has_errors[stream_name] = True

    def register(
        self, logging_level: str, additional_loggers: Optional[List[str]] = None
    ):
        """
        Register the handler with the omnata_plugin namespace
        """
        self.setLevel(logging_level)
        logger = logging.getLogger("omnata_plugin")
        logger.addHandler(self)
        if additional_loggers is not None:
            for additional_logger in additional_loggers:
                logger = logging.getLogger(additional_logger)
                logger.addHandler(self)

    def unregister(self):
        """
        Removes the handler
        """
        logger = logging.getLogger("omnata_plugin")
        logger.removeHandler(self)
