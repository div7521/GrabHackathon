import logging
import sys
from datetime import datetime

def setup_tool_logging():
    """Set up simple CLI logging for tool calls"""

    # Create logger
    logger = logging.getLogger("tool_calls")
    logger.setLevel(logging.INFO)

    # Clear any existing handlers
    logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Create simple formatter
    formatter = logging.Formatter('%(asctime)s - TOOL_CALL - %(message)s')
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger

# Initialize the logger
tool_logger = setup_tool_logging()
