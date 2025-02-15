import logging
import sys


logger = logging.getLogger("task_manager_logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("[%(levelname)8s]: %(message)s")

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)

logger.propagate = False
