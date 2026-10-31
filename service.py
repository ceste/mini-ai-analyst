from llm import ask_llm, choose_action
from tools import get_product_revenue
from models import ToolDecision
from pydantic import ValidationError
from tools import get_product_revenue, get_total_revenue

# async def answer_question(question: str):

#     action = await choose_action(question)

#     if action == "GET_PRODUCT_REVENUE":

#         sales_data = get_product_revenue()

#         prompt = f"""
#                 Answer the user's question using ONLY the sales data below.

#                 User question:
#                 {question}

#                 Sales data:
#                 {sales_data}
#                 """

#         return await ask_llm(prompt)

#     return await ask_llm(question)


# async def answer_question(question: str):

#     decision_json = await choose_action(question)

#     decision = ToolDecision.model_validate_json(
#         decision_json
#     )

#     if decision.action == "GET_PRODUCT_REVENUE":

#         sales_data = get_product_revenue()

#         prompt = f"""
#                     Answer the user's question using ONLY the sales data below.

#                     If the data does not contain enough information to answer,
#                     say that the available data is insufficient.
#                     Do not infer information that is not present.

#                     User question:
#                     {question}

#                     Sales data:
#                     {sales_data}
#                     """

#         return await ask_llm(prompt)

#     return await ask_llm(question)


async def answer_question(question: str):

    decision_json = await choose_action(question)

    # decision = ToolDecision.model_validate_json(
    #     decision_json
    # )

    print("RAW DECISION:", decision_json)

    try:
        decision = ToolDecision.model_validate_json(decision_json)
    except ValidationError as e:
        raise RuntimeError(
        f"Invalid LLM tool decision: {e}"
    )

    if decision.action == "GET_PRODUCT_REVENUE":

        product = decision.arguments.product
        sales_data = get_product_revenue()

        prompt = f"""
                Answer the user's question using ONLY the sales data below.

                If the data does not contain enough information to answer,
                say that the available data is insufficient.

                Do not infer information that is not present.

                User question:
                {question}

                Sales data:
                {sales_data}
                """


        return await ask_llm(prompt)

    if decision.action == "GET_TOTAL_REVENUE":

        revenue_data = get_total_revenue()

        prompt = f"""
                Answer the user's question using ONLY the data below.

                User question:
                {question}

                Revenue data:
                {revenue_data}
                """

        return await ask_llm(prompt)

    return await ask_llm(question)