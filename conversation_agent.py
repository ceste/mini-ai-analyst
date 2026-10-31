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


model = OllamaModel(
    "qwen2.5:7b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    ),
)

agent = Agent(
    model,
    instructions=(
        "You are a helpful business analytics assistant. "
        "Answer questions using the information provided. "
        "If information is missing, say so. "
        "Do not invent revenue figures."
    ),
)




# # First question
# result1 = agent.run_sync(
#     "Laptop revenue is $2400 and Monitor revenue is $900. "
#     "Which product has higher revenue?"
# )

# print("\nFirst answer:")
# print(result1.output)


# # Follow-up WITHOUT history
# result2 = agent.run_sync(
#     "What is its revenue?"
# )

# print("\nWithout history:")
# print(result2.output)


# # Follow-up WITH history
# result3 = agent.run_sync(
#     "What is its revenue?",
#     message_history=result1.all_messages()
# )

# print("\nWith history:")
# print(result3.output)



# print("\nConversation history:")

# for message in result3.all_messages():
#     print(type(message).__name__)

#     for part in message.parts:
#         print("  ", type(part).__name__)



# questions = [
#     "Laptop revenue is $2400 and Monitor revenue is $900. "
#     "Which product has higher revenue?",

#     "What is its revenue?",

#     "How much higher is it than Monitor?",

#     "Which product has the lower revenue?"
# ]

# history = []

# for turn, question in enumerate(questions, start=1):

#     result = agent.run_sync(
#         question,
#         message_history=history
#     )

#     print(f"\nTurn {turn}")
#     print("Question:", question)
#     print("Answer:", result.output)

#     print("Input tokens:", result.usage.input_tokens)
#     print("Output tokens:", result.usage.output_tokens)
#     print("Model requests:", result.usage.requests)

#     history = result.all_messages()



# questions = [
    # "Laptop revenue is $2400 and Monitor revenue is $900. "
    # "Which product has higher revenue?",

#     # "What is its revenue?",
#     "What is the revenue of the product you just identified as having higher revenue?",

#     "How much higher is it than Monitor?",

#     "Which product has the lower revenue?",

#     "What was Laptop's revenue again?"
# ]

# history = []

# for turn, question in enumerate(questions, start=1):

#     result = agent.run_sync(
#         question,
#         message_history=history
#     )

#     print(f"\nTurn {turn}")
#     print("Question:", question)
#     print("Answer:", result.output)
#     print("Input tokens:", result.usage.input_tokens)

#     # Keep only the last 2 completed exchanges.
#     history = result.all_messages()[-4:]


# 3. Initialize persistent memory
initialize_memory()

conversation_id = "demo_conversation"

history = load_history(conversation_id)

print("Loaded messages:", len(history))


# 4. Ask a question
question = input("\nYour question: ")

result = agent.run_sync(
    question,
    message_history=history
)

print("\nAssistant:", result.output)


# 5. Save the updated conversation
save_history(
    conversation_id,
    result.all_messages()
)

print("\nConversation saved.")