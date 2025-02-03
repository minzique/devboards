import logging
import os
from datetime import datetime
from src.core.config import Config

class Logger:
    LOGS_DIR = "logs"

    def __init__(self, name=None):
        # If no name is provided, use the calling module's name
        if name is None:
            name = __name__

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Ensure logs directory exists
        os.makedirs(self.LOGS_DIR, exist_ok=True)

        # File handlers (separate files for debug and info logs)
        debug_handler = logging.FileHandler(
            os.path.join(self.LOGS_DIR, f"debug_{datetime.now().strftime('%Y%m%d')}.log")
        )
        debug_handler.setLevel(logging.DEBUG)

        info_handler = logging.FileHandler(
            os.path.join(self.LOGS_DIR, f"info_{datetime.now().strftime('%Y%m%d')}.log")
        )
        info_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
       
        if os.environ.get("ENV") == "production" or Config.DEBUG == False:
            console_handler.setLevel(logging.INFO)
        else:
            console_handler.setLevel(logging.DEBUG)

        # Formatters
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")

        # Assign formatters
        debug_handler.setFormatter(file_formatter)
        info_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)

        # Add handlers (prevent duplicate handlers)
        if not self.logger.hasHandlers():
            self.logger.addHandler(debug_handler)
            self.logger.addHandler(info_handler)
            self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


# Function to get a logger for a module
def get_logger(name=None):
    return Logger(name)