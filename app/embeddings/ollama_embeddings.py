import requests

from app.core.config import (
    EMBEDDING_MODEL,
    EMBEDDING_TIMEOUT,
    OLLAMA_BASE_URL,
)
from app.core.logger import setup_logger

logger = setup_logger()


class EmbeddingError(Exception):
    """Raised when embedding generation fails."""

    pass


# def embed(text: str) -> list[float]:
#     try:
#         response = requests.post(
#             "http://localhost:11434/api/embed",
#             json={
#                 "model": "nomic-embed-text",
#                 "input": text
#             },
#             timeout=60
#         )

#         response.raise_for_status()

#         return response.json()["embeddings"][0]

#     except (requests.RequestException, ValueError, KeyError, IndexError, TypeError) as error:
#         raise EmbeddingError(
#             "Failed to generate embedding using Ollama"
#         ) from error

# def embed(text: str) -> list[float]:
#     try:
#         response = requests.post(
#             f"{OLLAMA_BASE_URL.rstrip('/')}/api/embed",
#             json={
#                 "model": EMBEDDING_MODEL,
#                 "input": text
#             },
#             timeout=EMBEDDING_TIMEOUT
#         )

#         response.raise_for_status()

#         return response.json()["embeddings"][0]

#     except (
#         requests.RequestException,
#         ValueError,
#         KeyError,
#         IndexError,
#         TypeError,
#     ) as error:

#         logger.error(
#             "Embedding generation failed: %s",
#             error,
#         )

#         raise EmbeddingError(
#             "Failed to generate embedding using Ollama"
#         ) from error


def embed(text: str, http_post=None) -> list[float]:

    if http_post is None:
        http_post = requests.post

    try:
        response = http_post(
            f"{OLLAMA_BASE_URL.rstrip('/')}/api/embed",
            json={
                "model": EMBEDDING_MODEL,
                "input": text,
            },
            timeout=EMBEDDING_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()["embeddings"][0]

    except (
        requests.RequestException,
        ValueError,
        KeyError,
        IndexError,
        TypeError,
    ) as error:
        logger.error(
            "Embedding generation failed: %s",
            error,
        )

        raise EmbeddingError("Failed to generate embedding using Ollama") from error
