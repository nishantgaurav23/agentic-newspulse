"""
Custom logging configuration for debugging multi-agent flows
Provides colored, structured logging with agent context tracking
"""
import logging
import sys
from typing import Optional
from colorlog import ColoredFormatter


class AgentContextFilter(logging.Filter):
    """Add agent context to log records"""

    def __init__(self):
        super().__init__()
        self.agent_context = "SYSTEM"

    def filter(self, record):
        record.agent = self.agent_context
        return True


def setup_logger(name: str = "newspulse", level: str = "INFO") -> logging.Logger:
    """
    Set up a colored, structured logger for the application

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, level.upper()))

    # Add agent context filter
    context_filter = AgentContextFilter()
    handler.addFilter(context_filter)

    # Create colored formatter
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)-8s | [%(agent)s] | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Store filter reference for updating context
    logger.context_filter = context_filter

    return logger


def set_agent_context(logger: logging.Logger, agent_name: str):
    """Update the agent context for logging"""
    if hasattr(logger, "context_filter"):
        logger.context_filter.agent_context = agent_name
