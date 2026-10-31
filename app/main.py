from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logger import setup_logger
from app.memory.conversation_memory import initialize_memory

logger = setup_logger()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.info("Mini AI Analyst starting")

#     initialize_memory()
#     logger.info("Conversation memory initialized")

#     yield

#     logger.info("Mini AI Analyst shutting down")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Mini AI Analyst starting")

    initialize_memory()
    logger.info("Conversation memory initialized")

    try:
        yield
    finally:
        logger.info("Mini AI Analyst shutting down")


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}
