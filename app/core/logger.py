import logging
import sys

from app.core.config.settings import settings

log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler(settings.LOG_FILE)
file_handler.setFormatter(log_formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)

logger = logging.getLogger("app")
logger.setLevel(getattr(logging, settings.LOG_LEVEL))
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.propagate = False
