"""Top-level package for argus_dynamixel."""

__author__ = """Alan Vasquez"""
__email__ = "vasqua@unc.edu"
__version__ = "0.1.2"

import logging
import os

from dotenv import load_dotenv

from .argus_dynamixel import DXLMotorSDK

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

__all__ = ["DXLMotorSDK"]


class Config(object):
    LOCAL_ADDR = os.environ.get("LOCAL_ADDR") or "127.0.0.1"


c = Config()


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Prevent logging from propagating to the root logger
        logger.propagate = 0
        logger.setLevel(("INFO"))
        console = logging.StreamHandler()
        logger.addHandler(console)
        formatter = logging.Formatter(
            "%(asctime)s — %(levelname)s — %(message)s"
        )
        console.setFormatter(formatter)
    return logger


# For testing
base_log = get_logger(__name__).addHandler(logging.StreamHandler())
