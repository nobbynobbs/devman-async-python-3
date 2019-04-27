import argparse
import os

import dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_DELAY = 0.01
DEFAULT_STORAGE = "./photos"


def get_args():
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser(
        description="Aiohttp based streaming service",
    )

    parser.add_argument(
        "-s", "--storage",
        help="Path to photo storage root directory",
        required=False,
        type=str,
        default=os.getenv("STORAGE", DEFAULT_STORAGE),
    )

    parser.add_argument(
        "-d", "--delay",
        help="Interval between sending the chunks  in seconds",
        required=False,
        type=float,
        default=os.getenv("DELAY", DEFAULT_DELAY),
    )

    parser.add_argument(
        "-l", "--log",
        help="Loging level",
        required=False,
        type=str,
        default=os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL),
    )

    args = parser.parse_args()
    return args
