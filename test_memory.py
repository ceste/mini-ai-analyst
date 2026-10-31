from app.memory.conversation_memory import (
    initialize_memory,
    save_fact,
    load_fact
)

initialize_memory()

save_fact(
    "high_value_threshold",
    "1000"
)

save_fact(
    "revenue_formula",
    "quantity * price"
)

print(
    "Threshold:",
    load_fact("high_value_threshold")
)

print(
    "Revenue formula:",
    load_fact("revenue_formula")
)

print(
    "Unknown fact:",
    load_fact("company_name")
)
