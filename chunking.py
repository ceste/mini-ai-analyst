# def chunk_text(text: str, chunk_size: int = 100):
#     words = text.split()

#     chunks = []

#     for i in range(0, len(words), chunk_size):
#         chunk = " ".join(words[i:i + chunk_size])
#         chunks.append(chunk)

#     return chunks

def chunk_text(
    text: str,
    chunk_size: int = 10,
    overlap: int = 3
):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if not 0 <= overlap < chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    words = text.split()
    chunks = []

    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

        if i + chunk_size >= len(words):
            break

    return chunks

if __name__ == "__main__":

    document = """
    Revenue is calculated as quantity multiplied by price.
    A high-value product generates more than $1000 in revenue.
    The sales report is refreshed every morning at 7 AM.
    The company does not track individual customer purchases.
    """

    # chunks = chunk_text(document, chunk_size=10)
    chunks = chunk_text(
        document,
        chunk_size=10,
        overlap=3
    )
    
    for index, chunk in enumerate(chunks):
        print(f"Chunk {index + 1}: {chunk}")