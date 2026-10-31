from unittest.mock import patch

import requests

from app.embeddings.ollama_embeddings import (
    embed,
    EmbeddingError,
)


with patch(
    "app.embeddings.ollama_embeddings.requests.post",
    side_effect=requests.ConnectionError("Ollama unavailable"),
):
    try:
        embed("What is our revenue threshold?")

    except EmbeddingError as error:
        print("Caught application error:", error)
        print("Original cause:", type(error.__cause__).__name__)
