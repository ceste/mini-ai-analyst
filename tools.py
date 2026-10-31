from database import get_connection


# def get_product_revenue():
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT
#             product,
#             quantity * price AS revenue
#         FROM sales
#         ORDER BY revenue DESC
#     """)

#     rows = cursor.fetchall()
#     conn.close()

#     return [
#         {
#             "product": row[0],
#             "revenue": row[1]
#         }
#         for row in rows
#     ]


def get_product_revenue(product: str | None = None):

    conn = get_connection()
    cursor = conn.cursor()

    if product:
        cursor.execute(
            """
            SELECT
                product,
                quantity * price AS revenue
            FROM sales
            WHERE LOWER(product) = LOWER(?)
            """,
            (product,)
        )
    else:
        cursor.execute("""
            SELECT
                product,
                quantity * price AS revenue
            FROM sales
            ORDER BY revenue DESC
        """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "product": row[0],
            "revenue": row[1]
        }
        for row in rows
    ]    

def get_total_revenue():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(quantity * price)
        FROM sales
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return {
        "total_revenue": result
    }