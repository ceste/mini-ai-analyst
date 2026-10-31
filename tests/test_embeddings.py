import pytest
import requests

from unittest.mock import patch, Mock

from app.embeddings.ollama_embeddings import embed, EmbeddingError

def test_embed_success():
    fake_response = Mock()

    fake_response.json.return_value = {
        "embeddings": [[0.1, 0.2, 0.3]]
    }

    with patch(
        "app.embeddings.ollama_embeddings.requests.post",
        return_value=fake_response,
    ) as mock_post:

        result = embed("Hello world")

    assert result == [0.1, 0.2, 0.3]
    mock_post.assert_called_once()

def test_embed_connection_failure():
    with patch(
        "app.embeddings.ollama_embeddings.requests.post",
        side_effect=requests.ConnectionError("Ollama unavailable"),
    ):
        with pytest.raises(EmbeddingError):
            embed("Hello world")
