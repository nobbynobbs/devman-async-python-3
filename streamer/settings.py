import os
import logging

import dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_DELAY = 0.1
DEFAULT_ARCHIVE_PATH = "photos"

LOG_LEVEL = None
DELAY = None
ARCHIVE_PATH = None


def initialize():
    global LOG_LEVEL, DELAY, ARCHIVE_PATH
    dotenv.load_dotenv()
    LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL))
    DELAY = os.getenv("DELAY", DEFAULT_DELAY)
    ARCHIVE_PATH = os.getenv("ARCHIVE_PATH", DEFAULT_ARCHIVE_PATH)
