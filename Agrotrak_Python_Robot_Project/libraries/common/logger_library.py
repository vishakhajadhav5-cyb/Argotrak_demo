import logging
import os
from datetime import datetime

class logger_library:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self.logger = None

    def initialize_logger(self, log_file_path):
        """Initialize a dedicated logger with file + console output."""
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        # ✅ Create unique log file for each test run
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_path = log_file_path.replace(".log", f"_{timestamp}.log")

        # ✅ Create new logger (don't rely on basicConfig)
        self.logger = logging.getLogger("AgroTrakLogger")
        self.logger.setLevel(logging.INFO)

        # Remove existing handlers to prevent duplication
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # ✅ File handler
        file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # ✅ Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # ✅ Log initialization message
        self.logger.info(f"🚀 Logger initialized successfully at: {log_file_path}")

    def log_info(self, message):
        """Log informational message."""
        if self.logger:
            self.logger.info(message)
        else:
            print(f"[INFO] {message}")

    def log_error(self, message):
        """Log error message."""
        if self.logger:
            self.logger.error(message)
        else:
            print(f"[ERROR] {message}")


