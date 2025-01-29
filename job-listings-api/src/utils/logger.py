import logging
import os
from datetime import datetime


class Logger:
    def __init__(self, name="job_listings"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Create logs directory if it doesn't exist
        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # File handler for debug logs
        debug_handler = logging.FileHandler(
            f"logs/debug_{datetime.now().strftime('%Y%m%d')}.log"
        )
        debug_handler.setLevel(logging.DEBUG)

        # File handler for info logs
        info_handler = logging.FileHandler(
            f"logs/info_{datetime.now().strftime('%Y%m%d')}.log"
        )
        info_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create formatters and add it to the handlers
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )

        debug_handler.setFormatter(file_formatter)
        info_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)

        # Add handlers to the logger
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

logger = Logger()
