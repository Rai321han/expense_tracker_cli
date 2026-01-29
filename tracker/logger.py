import logging
from logging.handlers import RotatingFileHandler
import os

# Ensure logs directory exists
os.makedirs("./logs", exist_ok=True)

# Configure a reusable logger
logger = logging.getLogger("tracker")
logger.setLevel(logging.INFO)  # default level

# Rotating file handler: prevents log file from growing indefinitely
file_handler = RotatingFileHandler(
    "./logs/tracker.log",
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=3,  # keep 3 old logs
)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
