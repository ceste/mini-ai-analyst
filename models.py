from typing import Literal
from pydantic import BaseModel

class ToolArguments(BaseModel):
    product: str | None = None


# class ToolDecision(BaseModel):
#     action: Literal[
#         "DIRECT",
#         "GET_PRODUCT_REVENUE"
#     ]

#     arguments: dict = {}

class ToolDecision(BaseModel):
    action: Literal[
        "DIRECT",
        "GET_PRODUCT_REVENUE",
        "GET_TOTAL_REVENUE"
    ]

    arguments: ToolArguments