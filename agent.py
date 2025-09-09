import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage, BaseMessage
from typing import List
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

        messages: List[BaseMessage] = [SystemMessage(content=system_prompt)]
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

                    yield f"\n\nExecuting {tool_name}...\n"

                    result = execute_tool_call(tool_name, tool_args)

                    if isinstance(result, dict):
                        if result.get('success'):
                            tool_output = str(result['result'])
                        else:
                            tool_output = f"Tool failed: {result['error']}"
                    else:
                        tool_output = str(result)

                    # yield f"{tool_output}\n\n"

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
        ":orange[:material/restaurant:] Multi-Restaurant Crisis": (
            "Restaurant MERCHANT_789 has 45-minute delay due to equipment failure. Customer CUST_456 ordered for elderly parent's birthday dinner at 7 PM, it's now 6:15 PM. Driver DRIVER_123 has been waiting 20 minutes and has 3 other pending orders. Customer calls saying parent has diabetes and needs to eat on schedule. Kitchen staff claims food was properly prepared before equipment broke."
        ),
        ":red[:material/delivery_dining:] Delivery Dispute Investigation": (
            "Food arrived 35 minutes late and cold. Customer CUST_890 demands full refund claiming driver DRIVER_567 was rude and food was incorrectly packaged. Driver claims restaurant MERCHANT_234 gave him wrong order initially, causing return trip and delay. Restaurant manager says packaging was fine and driver seemed inexperienced. Customer threatens negative reviews."
        ),
        ":blue[:material/cloud:] Weather Emergency Coordination": (
            "Severe thunderstorm hit delivery zone. Customer CUST_678 ordered hot soup for sick child, storm started after driver DRIVER_890 picked up order. Driver is stuck in traffic due to flooding on main route ROUTE_456. Restaurant MERCHANT_123 can't prepare replacement order due to power outage. Customer desperately needs food for medication timing. Multiple alternative routes flooded."
        ),
    },
    "GrabMart": {
        ":green[:material/shopping_cart:] Supply Chain Disruption": (
            "Customer CUST_345 ordered 8 items including baby formula, fever medicine, and dinner ingredients from store MERCHANT_567. Store reports 4 items out of stock including critical baby formula for 6-month-old with allergies. Driver DRIVER_234 waiting at store. Customer's partner is at work, can't substitute formula brands due to allergies. Three nearby stores might have alternatives but need inventory verification."
        ),
        ":purple[:material/inventory:] Quality Control Crisis": (
            "Customer CUST_123 received grocery order but meat products appear spoiled and vegetables are wilted. Claims packaging was warm and items seem old. Driver DRIVER_789 delivered as instructed but noticed unusual smell. Store MERCHANT_890 insists items were fresh and properly refrigerated. Customer wants immediate refund and replacement but lives 45 minutes away. Pregnant customer concerned about food safety."
        ),
        ":orange[:material/local_grocery_store:] Bulk Order Complications": (
            "Large family gathering order worth $200 for 15 people. Store MERCHANT_456 closed unexpectedly due to staff shortage. Customer CUST_567 guests arriving in 3 hours for celebration. Driver DRIVER_345 already en route when store closure discovered."
        ),
    },
    "GrabExpress": {
        ":violet[:material/local_shipping:] High-Value Authentication Crisis": (
            "Package PKG_456 contains $1500 signed contract documents for urgent business deal. Recipient RECIPIENT_789 unavailable due to emergency hospital visit. Building security won't accept package. Contract deadline is tomorrow morning. Sender SENDER_234 demands proof of delivery. Package requires signature verification. Driver DRIVER_567 has been waiting 30 minutes."
        ),
        ":orange[:material/warning:] Cross-City Delivery Challenge": (
            "Electronics package PKG_890 worth $800 damaged during transport. Customer CUSTOMER_123 refuses delivery claiming driver DRIVER_456 was careless. Driver has photo evidence of pre-existing damage from pickup location. Sender SENDER_567 claims item was perfect condition. Insurance claim needed but requires detailed evidence collection. Customer needs replacement urgently for work presentation tomorrow."
        ),
        ":green[:material/security:] Time-Critical Medical Delivery": (
            "Medical documents PKG_234 for surgery consultation needed by 4 PM today, currently 2:30 PM. Recipient RECIPIENT_345 at hospital but can't leave patient's bedside. Package contains confidential medical records requiring secure handling. Hospital has strict delivery protocols. Driver DRIVER_123 unfamiliar with hospital procedures. Alternative contact CONTACT_678 available but needs authorization."
        ),
    },
    "GrabCar": {
        ":red[:material/flight:] Airport Emergency Coordination": (
            "Passenger PASS_456 needs to catch international flight SQ825 departing at 8:30 PM, currently 6:45 PM. Main route ROUTE_789 blocked due to accident, alternative routes experiencing 40+ minute delays. Flight is overbooked so missing it means 24-hour delay. Passenger has connecting flight in destination city. Driver DRIVER_234 suggests expensive toll road but passenger budget-conscious."
        ),
        ":blue[:material/traffic:] Multi-Stop Business Crisis": (
            "Executive PASS_678 has critical presentations at 3 different locations today. Current trip to location 2 delayed by 25 minutes due to earlier traffic. Locations 3 has strict security requiring 15-minute early arrival. Original schedule now impossible. Passenger willing to pay premium for solution. Driver DRIVER_567 suggests splitting journey between multiple drivers."
        ),
        ":yellow[:material/directions_car:] Vehicle Safety Investigation": (
            "Mid-journey vehicle breakdown on highway. Passenger PASS_890 claims driver DRIVER_345 was driving unsafely before breakdown. Driver claims passenger was distracting him. Both have different versions of events. Passenger late for job interview, stressed and agitated. Driver's vehicle needs towing. Replacement vehicle 20 minutes away. Insurance requires incident documentation."
        ),
    },
}