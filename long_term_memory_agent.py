import os

os.environ["PYDANTIC_AI_NO_BANNER"] = "1"

from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

from app.memory.conversation_memory import (
    initialize_memory,
    save_fact,
    load_fact
)

# 1. Initialize memory
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
        "Answer using the provided facts. "
        "Do not invent missing information."
    )
)


# 3. Retrieve a fact from SQLite
threshold = load_fact("high_value_threshold")

print("Retrieved from SQLite:", threshold)


# 4. Build the question with memory
question = "What is our high-value revenue threshold?"

if threshold is None:
    memory_context = "No threshold is available."
else:
    memory_context = (
        f"The stored high-value revenue threshold "
        f"is ${threshold}."
    )


# 5. Ask Qwen
result = agent.run_sync(
    f"""
    Stored memory:
    {memory_context}

    User question:
    {question}
    """
)

print("\nAssistant:", result.output)
print("Input tokens:", result.usage.input_tokens)
