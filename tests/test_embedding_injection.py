from unittest.mock import Mock

from app.embeddings.ollama_embeddings import embed


def test_embed_with_injected_http_client():

    fake_response = Mock()

    fake_response.json.return_value = {
        "embeddings": [[0.5, 0.6, 0.7]]
    }

    fake_post = Mock(return_value=fake_response)

    result = embed(
        "Hello world",
        http_post=fake_post,
    )

    assert result == [0.5, 0.6, 0.7]

    fake_post.assert_called_once()
