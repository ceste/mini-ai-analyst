from app.memory.conversation_memory import (
    initialize_memory,
    save_fact,
    load_fact
)
from semantic_memory import (
    initialize_semantic_memory,
    search_memory
)


initialize_memory()
initialize_semantic_memory()

questions = [
    "What's the minimum revenue for a high-value product?",
    "How much money does a product generate from its quantity and price?",
    "Who is our CEO?"
]

for question in questions:

    result = search_memory(question)
from app.memory.conversation_memory import (
    initialize_memory,
    save_fact,
    load_fact
)
    print("\nQuestion:", question)
    print("Retrieved memory:", result)
