import logging

HEADER = "\033[95m"
OK_BLUE = "\033[94m"
OK_CYAN = "\033[96m"
OK_GREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
END_C = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

logger = logging.getLogger("inv-check")
logger.setLevel(logging.DEBUG)
logging.basicConfig(format="%(asctime)s:[%(levelname)s] %(message)s")


def success(message: str):
    logger.info(f"{OK_GREEN}{message}{END_C}")


def fail(message: str):
    logger.error(f"{FAIL}{message}{END_C}")


def info(message: str):
    logger.info(f"{OK_BLUE}{message}{END_C}")
