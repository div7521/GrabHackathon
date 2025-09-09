import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from config import MODEL_NAME, MAX_ITERS

from prompt import system_prompt
from tools import AVAILABLE_TOOLS
import time

AVAILABLE_PRODUCTS = ["GrabFood", "GrabMart", "GrabExpress", "GrabCar"]

def setup_model(model_name=MODEL_NAME):
    load_dotenv()
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise ValueError("API_KEY not found in environment variables")

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0.1
    )

    llm_with_tools = llm.bind_tools(list(AVAILABLE_TOOLS.values()))
    return llm_with_tools

def execute_tool_call(tool_name, arguments):
    print(f"[CLI] Tool call started: {tool_name}")

    if tool_name not in AVAILABLE_TOOLS:
        error_msg = f"Tool '{tool_name}' not found in available tools. Available tools: {list(AVAILABLE_TOOLS.keys())}"
        print(f"[CLI] Tool call failed: {tool_name} - Tool not found")
        return {
            "success": False,
            "error": error_msg,
            "tool_name": tool_name,
            "suggestion": "Please use one of the available tools or proceed with manual recommendations."
        }

    try:
        tool_function = AVAILABLE_TOOLS[tool_name]
        result = tool_function(**arguments)
        print(f"[CLI] Tool call completed: {tool_name}")
        return {
            "success": True,
            "result": result,
            "tool_name": tool_name
        }

    except Exception as e:
        error_msg = f"Tool execution failed: {str(e)}"
        print(f"[CLI] Tool call failed: {tool_name} - {str(e)}")
        return {
            "success": False,
            "error": error_msg,
            "tool_name": tool_name,
            "arguments": arguments,
            "suggestion": f"Tool {tool_name} is temporarily unavailable. Please proceed with alternative approaches or manual recommendations."
        }

def convert_conversation_history(conversation_history):
    messages = []
    if conversation_history:
        for msg in conversation_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
    return messages

def stream_ai_response(model, user_input, product_type, conversation_history=None):
    try:
        contextualized_input = f"""
        Product: {product_type}
        Scenario: {user_input}
        """

        messages = [SystemMessage(content=system_prompt)]
        messages.extend(convert_conversation_history(conversation_history))
        messages.append(HumanMessage(content=contextualized_input))

        iteration = 0

        while iteration < MAX_ITERS:
            iteration += 1

            response = model.invoke(messages)

            if hasattr(response, 'tool_calls') and response.tool_calls:
                if response.content:
                    for chunk in response.content.split(' '):
                        yield chunk + ' '
                        time.sleep(0.02)

                messages.append(AIMessage(content=response.content, tool_calls=response.tool_calls))

                tool_results = []

                for tool_call in response.tool_calls:
                    tool_name = tool_call['name']
                    tool_args = tool_call['args']
                    tool_call_id = tool_call.get('id', f"{tool_name}_{iteration}")

                    yield f"Executing {tool_name}...\n"

                    result = execute_tool_call(tool_name, tool_args)

                    if isinstance(result, dict):
                        if result.get('success'):
                            tool_output = str(result['result'])
                        else:
                            tool_output = f"Tool failed: {result['error']}"
                    else:
                        tool_output = str(result)

                    yield f"{tool_output}\n\n"

                    tool_message = ToolMessage(
                        content=tool_output,
                        tool_call_id=tool_call_id
                    )
                    tool_results.append(tool_message)

                messages.extend(tool_results)
                continue

            else:
                if response.content:
                    for chunk in response.content.split(' '):
                        yield chunk + ' '
                        time.sleep(0.02)
                break

        if iteration >= MAX_ITERS:
            yield "\nMaximum iterations reached.\n"

    except Exception as e:
        yield f"\nError occurred: {str(e)}\n"

PRODUCT_EXAMPLES = {
    "GrabFood": {
        "Restaurant Overload": (
            "Example: Restaurant restaurant_002 shows 40-minute prep time. "
            "Customer CUST_123 has urgent order, driver DRIVER_456 waiting idle. "
            "Try using: get_merchant_status(), notify_customer(), re_route_driver()"
        ),
        "Damaged Package": (
            "Example: Food arrives damaged, customer wants refund, driver claims pre-damage. "
            "Try using: issue_instant_refund(), initiate_mediation_flow(), collect_evidence()"
        ),
        "Delivery Delay": (
            "Example: Driver stuck in traffic, 30min late hot food, customer calling. "
            "Try using: check_traffic(), calculate_alternative_route(), notify_customer()"
        ),
    },
    "GrabMart": {
        "Out of Stock Items": (
            "Example: 5 items ordered, 2 essential out of stock, driver waiting, customer needs for dinner. "
            "Try using: get_nearby_merchants(), contact_recipient_via_chat(), notify_customer()"
        ),
        "Wrong Item Picked": (
            "Example: Wrong baby formula brand picked (allergic baby), store 15min away. "
            "Try using: contact_recipient_via_chat(), re_route_driver(), issue_instant_refund()"
        ),
        "Store Closure": (
            "Example: Store closed due to power outage, large order, guests coming in 2 hours. "
            "Try using: get_nearby_merchants(), notify_customer(), calculate_alternative_route()"
        ),
    },
    "GrabExpress": {
        "Recipient Unavailable": (
            "Example: $200 electronics package, recipient unavailable, secure handling required. "
            "Try using: suggest_safe_drop_off(), find_nearby_locker(), contact_recipient_via_chat()"
        ),
        "High-Value Package": (
            "Example: $500 jewelry, no secure drop-off, customer away 3 hours. "
            "Try using: find_nearby_locker(), suggest_safe_drop_off(), contact_recipient_via_chat()"
        ),
        "Package Damage": (
            "Example: Visible damage to fragile glass items, customer refuses, sender wants investigation. "
            "Try using: collect_evidence(), initiate_mediation_flow(), issue_instant_refund()"
        ),
    },
    "GrabCar": {
        "Airport Rush": (
            "Example: Flight SQ123 at 3PM, route_002 has 30min delay, current time 1:30PM. "
            "Try using: check_flight_status(), check_traffic(), calculate_alternative_route()"
        ),
        "Traffic Jam": (
            "Example: 45min delay on main route, business meeting, driver suggests longer alternative. "
            "Try using: check_traffic(), calculate_alternative_route(), notify_passenger_and_driver()"
        ),
        "Vehicle Breakdown": (
            "Example: Car breakdown mid-journey, replacement 20min away, passenger anxious about appointment. "
            "Try using: re_route_driver(), notify_passenger_and_driver(), calculate_alternative_route()"
        ),
    },
}
