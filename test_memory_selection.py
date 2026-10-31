from app.memory.conversation_memory import (
    initialize_memory,
    save_fact,
    load_fact
)

initialize_memory()

questions = [
    "What is our high-value revenue threshold?",
    "How do we calculate revenue?",
    "Who is our CEO?"
]

for question in questions:

    memory = select_memory(question)

    print("\nQuestion:", question)
    print("Selected memory:", memory)
