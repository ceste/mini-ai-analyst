from app.memory.conversation_memory import DB_PATH
import sqlite3
from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}





def test_memory_initialized():
    with TestClient(app):
        connection = sqlite3.connect(DB_PATH)

        try:
            tables = connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                """
            ).fetchall()
        finally:
            connection.close()

    table_names = {row[0] for row in tables}

    assert "conversations" in table_names
    assert "memory_facts" in table_names
