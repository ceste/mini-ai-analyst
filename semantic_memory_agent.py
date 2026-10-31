import os

os.environ["PYDANTIC_AI_NO_BANNER"] = "1"

from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

# from conversation_memory import initialize_memory
from semantic_memory import search_memory


from app.memory.conversation_memory import (
    initialize_memory,
    save_fact,
    load_fact
)

# 1. Initialize memory storage
initialize_memory()


# 2. Configure Qwen
model = OllamaModel(
    "qwen2.5:7b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    )
)

agent = Agent(
    model,
    instructions=(
        "You are a business analytics assistant. "
        "Answer questions only using the supplied memory. "
        "If the memory does not contain the answer, "
        "say that the information is unavailable. "
        "Do not invent business facts."
    )
)


# 3. Questions to test
questions = [
    "What's the minimum revenue for a high-value product?",
    "How do we calculate product revenue?",
    "Who is our CEO?"
]


for question in questions:

    # Retrieve relevant long-term memory
    memory = search_memory(question)

    if memory is None or memory["value"] is None:
        memory_context = "No relevant memory available."
    else:
        memory_context = (
            f"Memory key: {memory['key']}\n"
            f"Memory value: {memory['value']}"
        )

    # Ask Qwen using the selected memory
    result = agent.run_sync(
        f"""
        Retrieved memory:
        {memory_context}

        User question:
        {question}
        """
    )

    print("\nQuestion:", question)
    print("Memory:", memory)
    print("Assistant:", result.output)
    print("Input tokens:", result.usage.input_tokens)
