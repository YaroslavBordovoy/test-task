import logging
import sys


logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("[%(levelname)8s]: %(message)s")

file_handler = logging.FileHandler("request.log")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

logger.propagate = False
