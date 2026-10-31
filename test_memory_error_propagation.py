from unittest.mock import patch

from app.embeddings.ollama_embeddings import EmbeddingError
from semantic_memory import search_memory


with patch(
    "semantic_memory.embed",
    side_effect=EmbeddingError("Ollama unavailable"),
):
    try:
        result = search_memory(
            "What is our high-value revenue threshold?"
        )

        if result is None:
            print("No relevant memory found")
        else:
            print("Memory found:", result)

    except EmbeddingError as error:
        print("Memory search failed:", error)
        print("The application should not treat this as missing memory.")
