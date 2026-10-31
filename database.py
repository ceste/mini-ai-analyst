import sqlite3


def get_connection():
    return sqlite3.connect("analyst.db")


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM sales")

    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            """
            INSERT INTO sales (product, quantity, price)
            VALUES (?, ?, ?)
            """,
            [
                ("Laptop", 2, 1200),
                ("Mouse", 10, 25),
                ("Keyboard", 5, 70),
                ("Monitor", 3, 300),
            ],
        )

    conn.commit()
    conn.close()