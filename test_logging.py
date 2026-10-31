import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

logger.debug("This is a debug message")
logger.info("Memory search started")
logger.warning("No relevant memory found")
logger.error("Ollama connection failed")
