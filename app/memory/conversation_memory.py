import sqlite3

#DB_PATH = "conversation.db"

# import os
# from pathlib import Path

# DATA_DIR = Path(os.getenv("DATA_DIR", "."))
# DATA_DIR.mkdir(parents=True, exist_ok=True)

# DB_PATH = str(DATA_DIR / "conversation.db")


import os
from pathlib import Path

DATA_DIR = Path(os.getenv("DATA_DIR", "."))
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = str(DATA_DIR / "conversation.db")

def initialize_memory():

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                conversation_id TEXT PRIMARY KEY,
                messages TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS memory_facts (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)


def save_history(conversation_id, messages):

    # Convert PydanticAI messages into JSON.
    from pydantic_ai.messages import ModelMessagesTypeAdapter

    messages_json = ModelMessagesTypeAdapter.dump_json(messages).decode("utf-8")

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO conversations (
                conversation_id,
                messages
            )
            VALUES (?, ?)
            ON CONFLICT(conversation_id)
            DO UPDATE SET messages = excluded.messages
        """,
            (conversation_id, messages_json),
        )


def load_history(conversation_id):

    from pydantic_ai.messages import ModelMessagesTypeAdapter

    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            """
            SELECT messages
            FROM conversations
            WHERE conversation_id = ?
        """,
            (conversation_id,),
        ).fetchone()

    if row is None:
        return []

    return ModelMessagesTypeAdapter.validate_json(row[0])


def save_fact(key, value):

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO memory_facts (key, value)
            VALUES (?, ?)
            ON CONFLICT(key)
            DO UPDATE SET value = excluded.value
        """,
            (key, value),
        )


def load_fact(key):

    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            """
            SELECT value
            FROM memory_facts
            WHERE key = ?
        """,
            (key,),
        ).fetchone()

    if row is None:
        return None

    return row[0]


def select_memory(question):

    question = question.lower()

    if "threshold" in question:
        return load_fact("high_value_threshold")

    elif "calculate revenue" in question:
        return load_fact("revenue_formula")

    return None
