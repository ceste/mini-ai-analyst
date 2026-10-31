import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logger = logging.getLogger("rotation_test")
logger.setLevel(logging.INFO)
logger.propagate = False

handler = RotatingFileHandler(
    log_dir / "rotation_test.log",
    maxBytes=200,
    backupCount=2,
    encoding="utf-8",
)

handler.setFormatter(
    logging.Formatter("%(levelname)s | %(message)s")
)

logger.addHandler(handler)

for i in range(20):
    logger.info(f"Test message number {i}")

handler.close()
logger.removeHandler(handler)

print("Rotation experiment completed")
