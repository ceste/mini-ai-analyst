import re

def sentence_chunk_text(text: str, max_words: int = 20):

    # Split text at sentence boundaries
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    chunks = []
    current_chunk = []
    current_words = 0

    for sentence in sentences:
        sentence_words = len(sentence.split())

        # Start a new chunk if adding this sentence
        # would exceed our limit
        if current_chunk and current_words + sentence_words > max_words:
            chunks.append(" ".join(current_chunk))

            current_chunk = []
            current_words = 0

        current_chunk.append(sentence)
        current_words += sentence_words

    # Save the final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


if __name__ == "__main__":

    document = """
    Revenue is calculated as quantity multiplied by price.
    A high-value product generates more than $1000 in revenue.
    The sales report is refreshed every morning at 7 AM.
    The company does not track individual customer purchases.
    """

    chunks = sentence_chunk_text(
        document,
        max_words=10
    )

    for index, chunk in enumerate(chunks):
        print(f"Chunk {index + 1}: {chunk}")    