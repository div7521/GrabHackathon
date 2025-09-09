import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from config import MODEL_NAME

from prompt import system_prompt
from tools import AVAILABLE_TOOLS
import json
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
    if tool_name not in AVAILABLE_TOOLS:
        error_msg = f"Tool '{tool_name}' not found in available tools. Available tools: {list(AVAILABLE_TOOLS.keys())}"
        return {
            "success": False,
            "error": error_msg,
            "tool_name": tool_name,
            "suggestion": "Please use one of the available tools or proceed with manual recommendations."
        }

    try:
        tool_function = AVAILABLE_TOOLS[tool_name]
        result = tool_function(**arguments)
        return {
            "success": True,
            "result": result,
            "tool_name": tool_name
        }

    except Exception as e:
        error_msg = f"Tool execution failed: {str(e)}"
        return {
            "success": False,
            "error": error_msg,
            "tool_name": tool_name,
            "arguments": arguments,
            "suggestion": f"Tool {tool_name} is temporarily unavailable. Please proceed with alternative approaches or manual recommendations."
        }

def stream_ai_response(model, user_input, product_type):
    try:
        contextualized_input = f"""
        Product: {product_type}
        Scenario: {user_input}
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=contextualized_input)
        ]

        # Initial response with potential tool calls
        response = model.invoke(messages)

        # Stream the initial response
        response_text = response.content

        # Handle tool calls if present
        if hasattr(response, 'tool_calls') and response.tool_calls:
            tool_results = []
            successful_tools = 0
            failed_tools = 0

            # First yield the initial response
            for chunk in response_text.split(' '):
                yield chunk + ' '
                time.sleep(0.02)  # Small delay for streaming effect

            yield "\n\n**🔧 Executing Tools:**\n\n"

            for tool_call in response.tool_calls:
                tool_name = tool_call['name']
                tool_args = tool_call['args']

                yield f"⏳ Running {tool_name}...\n"

                result = execute_tool_call(tool_name, tool_args)

                # Format result based on success/failure
                if isinstance(result, dict):
                    if result.get('success'):
                        tool_result = f"✅ **{tool_name}({json.dumps(tool_args)}) - SUCCESS**:\n{result['result']}\n\n"
                        successful_tools += 1
                    else:
                        tool_result = f"❌ **{tool_name}({json.dumps(tool_args)}) - FAILED**:\nError: {result['error']}\nSuggestion: {result.get('suggestion', 'Please proceed with alternative approaches.')}\n\n"
                        failed_tools += 1
                else:
                    # Legacy format support
                    if result.startswith("Error"):
                        tool_result = f"❌ **{tool_name}({json.dumps(tool_args)}) - FAILED**:\n{result}\n\n"
                        failed_tools += 1
                    else:
                        tool_result = f"✅ **{tool_name}({json.dumps(tool_args)}) - SUCCESS**:\n{result}\n\n"
                        successful_tools += 1

                # Stream tool result
                for chunk in tool_result.split(' '):
                    yield chunk + ' '
                    time.sleep(0.01)

            # If there were failures, provide follow-up analysis
            if failed_tools > 0:
                yield f"\n**📋 Analysis Summary:** {successful_tools} tools succeeded, {failed_tools} failed\n\n"

                # Create follow-up prompt with tool failure context
                tool_failure_context = f"""
Previous tool execution summary:
- Successful tools: {successful_tools}
- Failed tools: {failed_tools}

Some tools failed, but please continue with your analysis and provide comprehensive solutions using:
1. Information from successful tools
2. Your domain knowledge of {product_type} operations
3. Alternative approaches that don't rely on failed tools
4. Manual procedures and recommendations

Please provide a complete solution despite the tool failures.
"""

                # Get follow-up response
                follow_up_messages = messages + [
                    response,
                    HumanMessage(content=tool_failure_context)
                ]

                try:
                    follow_up_response = model.invoke(follow_up_messages)
                    yield "**🔄 Continued Analysis:**\n\n"

                    # Stream follow-up response
                    for chunk in follow_up_response.content.split(' '):
                        yield chunk + ' '
                        time.sleep(0.02)

                except Exception as e:
                    yield f"\n\n**Note:** Follow-up analysis failed: {str(e)}"
        else:
            # No tool calls, just stream the response
            for chunk in response_text.split(' '):
                yield chunk + ' '
                time.sleep(0.02)

    except Exception as e:
        error_msg = f"Error in agent processing: {e}"
        yield f"I encountered a system error, but I can still help you analyze this {product_type} scenario manually. Please let me provide recommendations based on the situation you described:\n\n{user_input}\n\nBased on typical {product_type} operations, here are some general approaches you could consider... [Error: {error_msg}]"

PRODUCT_EXAMPLES = {
    "GrabFood": {
        ":orange[:material/restaurant:] Restaurant Overload": (
            "Example: Restaurant restaurant_002 shows 40-minute prep time. "
            "Customer CUST_123 has urgent order, driver DRIVER_456 waiting idle. "
            "Try using: get_merchant_status(), notify_customer(), re_route_driver()"
        ),
        ":red[:material/delivery_dining:] Damaged Package": (
            "Example: Food arrives damaged, customer wants refund, driver claims pre-damage. "
            "Try using: issue_instant_refund(), initiate_mediation_flow(), collect_evidence()"
        ),
        ":blue[:material/schedule:] Delivery Delay": (
            "Example: Driver stuck in traffic, 30min late hot food, customer calling. "
            "Try using: check_traffic(), calculate_alternative_route(), notify_customer()"
        ),
    },
    "GrabMart": {
        ":green[:material/shopping_cart:] Out of Stock Items": (
            "Example: 5 items ordered, 2 essential out of stock, driver waiting, customer needs for dinner. "
            "Try using: get_nearby_merchants(), contact_recipient_via_chat(), notify_customer()"
        ),
        ":purple[:material/inventory:] Wrong Item Picked": (
            "Example: Wrong baby formula brand picked (allergic baby), store 15min away. "
            "Try using: contact_recipient_via_chat(), re_route_driver(), issue_instant_refund()"
        ),
        ":orange[:material/local_grocery_store:] Store Closure": (
            "Example: Store closed due to power outage, large order, guests coming in 2 hours. "
            "Try using: get_nearby_merchants(), notify_customer(), calculate_alternative_route()"
        ),
    },
    "GrabExpress": {
        ":violet[:material/local_shipping:] Recipient Unavailable": (
            "Example: $200 electronics package, recipient unavailable, secure handling required. "
            "Try using: suggest_safe_drop_off(), find_nearby_locker(), contact_recipient_via_chat()"
        ),
        ":green[:material/security:] High-Value Package": (
            "Example: $500 jewelry, no secure drop-off, customer away 3 hours. "
            "Try using: find_nearby_locker(), suggest_safe_drop_off(), contact_recipient_via_chat()"
        ),
        ":orange[:material/warning:] Package Damage": (
            "Example: Visible damage to fragile glass items, customer refuses, sender wants investigation. "
            "Try using: collect_evidence(), initiate_mediation_flow(), issue_instant_refund()"
        ),
    },
    "GrabCar": {
        ":red[:material/flight:] Airport Rush": (
            "Example: Flight SQ123 at 3PM, route_002 has 30min delay, current time 1:30PM. "
            "Try using: check_flight_status(), check_traffic(), calculate_alternative_route()"
        ),
        ":blue[:material/traffic:] Traffic Jam": (
            "Example: 45min delay on main route, business meeting, driver suggests longer alternative. "
            "Try using: check_traffic(), calculate_alternative_route(), notify_passenger_and_driver()"
        ),
        ":yellow[:material/directions_car:] Vehicle Breakdown": (
            "Example: Car breakdown mid-journey, replacement 20min away, passenger anxious about appointment. "
            "Try using: re_route_driver(), notify_passenger_and_driver(), calculate_alternative_route()"
        ),
    },
}
