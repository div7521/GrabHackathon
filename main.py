import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from logging_config import tool_logger

from prompt import system_prompt
from tools import AVAILABLE_TOOLS, get_langchain_tools
import json

#loads environment variables from .env file to applications environment
load_dotenv()

def setup_gemini():
    load_dotenv()

    api_key=os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.1
    )

    # Bind tools to the model
    tools = get_langchain_tools()
    llm_with_tools = llm.bind_tools(tools)

    return llm_with_tools

def execute_tool_call(tool_name, arguments):
    """Execute a tool call with given arguments and return structured results"""
    # Log tool call
    tool_logger.info(f"Calling tool: {tool_name}")

    if tool_name not in AVAILABLE_TOOLS:
        error_msg = f"Tool '{tool_name}' not found in available tools. Available tools: {list(AVAILABLE_TOOLS.keys())}"
        tool_logger.error(f"Tool not found: {tool_name}")
        return {
            "success": False,
            "error": error_msg,
            "tool_name": tool_name,
            "suggestion": "Please use one of the available tools or proceed with manual recommendations."
        }

    try:
        tool_function = AVAILABLE_TOOLS[tool_name]
        result = tool_function(**arguments)
        tool_logger.info(f"Tool {tool_name} executed successfully")
        return {
            "success": True,
            "result": result,
            "tool_name": tool_name
        }
    except Exception as e:
        error_msg = f"Tool execution failed: {str(e)}"
        tool_logger.error(f"Tool {tool_name} failed: {str(e)}")
        return {
            "success": False,
            "error": error_msg,
            "tool_name": tool_name,
            "arguments": arguments,
            "suggestion": f"Tool {tool_name} is temporarily unavailable. Please proceed with alternative approaches or manual recommendations."
        }

def get_ai_response_with_tools(model, user_input, product_type):
    """Get response from Gemini with error-resilient tool calling support"""
    try:
        # Create context-aware prompt based on product type
        contextualized_input = f"""
Product Context: {product_type}

User Scenario: {user_input}

Please analyze this scenario specifically in the context of {product_type} operations and provide appropriate solutions using the available tools.

IMPORTANT: If any tools fail or return errors, continue your analysis and provide alternative solutions. Tool failures should not prevent you from delivering comprehensive recommendations.
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=contextualized_input)
        ]

        # Initial response with potential tool calls
        response = model.invoke(messages)

        # Handle tool calls if present
        if hasattr(response, 'tool_calls') and response.tool_calls:
            tool_results = []
            successful_tools = 0
            failed_tools = 0

            for tool_call in response.tool_calls:
                tool_name = tool_call['name']
                tool_args = tool_call['args']
                result = execute_tool_call(tool_name, tool_args)

                # Format result based on success/failure
                if isinstance(result, dict):
                    if result.get('success'):
                        tool_results.append(f"**{tool_name}({json.dumps(tool_args)}) - SUCCESS**:\n{result['result']}")
                        successful_tools += 1
                    else:
                        tool_results.append(f"**{tool_name}({json.dumps(tool_args)}) - FAILED**:\nError: {result['error']}\nSuggestion: {result.get('suggestion', 'Please proceed with alternative approaches.')}")
                        failed_tools += 1
                else:
                    # Legacy format support
                    if result.startswith("Error"):
                        tool_results.append(f"**{tool_name}({json.dumps(tool_args)}) - FAILED**:\n{result}")
                        failed_tools += 1
                    else:
                        tool_results.append(f"**{tool_name}({json.dumps(tool_args)}) - SUCCESS**:\n{result}")
                        successful_tools += 1

            # If there were failures, give the agent another chance to provide solutions
            if failed_tools > 0:
                # Create follow-up prompt with tool failure context
                tool_failure_context = f"""
Previous tool execution summary:
- Successful tools: {successful_tools}
- Failed tools: {failed_tools}

Tool Results:
{chr(10).join(tool_results)}

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

                    # Combine responses
                    final_response = response.content + "\n\n**Tool Execution Results:**\n\n" + "\n\n".join(tool_results)
                    final_response += f"\n\n**Continued Analysis (Post Tool Execution):**\n\n{follow_up_response.content}"

                except Exception as e:
                    # If follow-up fails, just use original response with tool results
                    final_response = response.content + "\n\n**Tool Execution Results:**\n\n" + "\n\n".join(tool_results)
                    final_response += f"\n\n**Note:** Follow-up analysis failed: {str(e)}"
            else:
                # All tools succeeded
                final_response = response.content + "\n\n**Tool Execution Results:**\n\n" + "\n\n".join(tool_results)

            return final_response
        else:
            return response.content

    except Exception as e:
        error_msg = f"Error in agent processing: {e}"
        tool_logger.error(error_msg)
        return f"I encountered a system error, but I can still help you analyze this {product_type} scenario manually. Please let me provide recommendations based on the situation you described:\n\n{user_input}\n\nBased on typical {product_type} operations, here are some general approaches you could consider... [Error: {error_msg}]"

def show_feedback_controls(message_index):
    """Shows the "How did I do?" control."""
    st.write("")

    with st.popover("How did I do?"):
        with st.form(key=f"feedback-{message_index}", border=False):
            with st.container(gap=None):
                st.markdown(":small[Rating]")
                rating = st.feedback(options="stars")

            details = st.text_area("More information (optional)")

            if st.checkbox("Include chat history with my feedback", True):
                relevant_history = st.session_state.messages[:message_index]
            else:
                relevant_history = []

            ""  # Add some space

            if st.form_submit_button("Send feedback"):
                st.success("Thank you for your feedback!")

# Product-specific examples for quick start
PRODUCT_EXAMPLES = {
    "GrabFood": {
        ":orange[:material/restaurant:] Restaurant Overload": (
            "Restaurant restaurant_002 is overloaded with 40-minute prep time. "
            "Customer CUST_123 has an urgent order and is getting impatient. "
            "The driver DRIVER_456 is waiting idle. What should we do?"
        ),
        ":red[:material/delivery_dining:] Damaged Package": (
            "Food package arrived damaged due to rough handling during delivery. "
            "Customer is upset and demanding full refund. Driver says it was "
            "already damaged when picked up. How to resolve?"
        ),
        ":blue[:material/schedule:] Delivery Delay": (
            "Driver is stuck in traffic with a hot food order that's already "
            "30 minutes late. Customer is calling repeatedly. Restaurant can't "
            "remake the order. What are our options?"
        ),
    },
    "GrabExpress": {
        ":violet[:material/local_shipping:] Recipient Unavailable": (
            "Driver arrived at destination but recipient is unavailable for a "
            "valuable $200 electronics package. Package requires secure handling. "
            "What are the delivery options?"
        ),
        ":green[:material/security:] High-Value Package": (
            "Delivering a $500 jewelry package to a residential area with no "
            "secure drop-off location. Customer won't be home for 3 hours. "
            "How should we handle this?"
        ),
        ":orange[:material/warning:] Package Damage": (
            "Fragile glass items package shows visible damage during transit. "
            "Customer refuses delivery. Sender wants investigation. "
            "What's the proper procedure?"
        ),
    },
    "GrabCar": {
        ":red[:material/flight:] Airport Rush": (
            "Passenger is heading to airport with flight SQ123 departing at 3 PM. "
            "Major accident detected on route_002 causing 30-minute delay. "
            "Current time is 1:30 PM. What should we do?"
        ),
        ":blue[:material/traffic:] Traffic Jam": (
            "Heavy traffic on main route is adding 45 minutes to journey. "
            "Passenger has important business meeting. Driver suggests longer "
            "but faster alternative route. How to handle?"
        ),
        ":yellow[:material/directions_car:] Vehicle Breakdown": (
            "Driver's car broke down mid-journey with passenger inside. "
            "Nearest replacement driver is 20 minutes away. Passenger is "
            "getting anxious about missing appointment. What's the solution?"
        ),
    },
}

def main():
    """Main function to run the AI agent with Streamlit"""

    st.set_page_config(
        page_title="Project Synapse",
        layout="wide",
        page_icon="🧠"
    )

    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'product_type' not in st.session_state:
        st.session_state.product_type = "GrabFood"

    # Initialize model in session state
    if 'model' not in st.session_state:
        with st.spinner("Initializing Project Synapse with tools..."):
            try:
                st.session_state.model = setup_gemini()
                st.success("Project Synapse initialized successfully!")
            except Exception as e:
                st.error(f"Setup failed: {e}")
                st.stop()

    # Header with title and restart button
    title_row = st.container(horizontal=True, vertical_alignment="bottom")
    
    with title_row:
        st.title("🧠 Project Synapse", anchor=False, width="stretch")
        st.caption("Agentic Last-Mile Coordinator")

        def clear_conversation():
            st.session_state.messages = []
            st.session_state.initial_question = None
            st.session_state.selected_suggestion = None

        st.button(
            "Restart",
            icon=":material/refresh:",
            on_click=clear_conversation,
        )

    # Check for initial interactions
    user_just_asked_initial_question = (
        "initial_question" in st.session_state and st.session_state.initial_question
    )

    user_just_clicked_suggestion = (
        "selected_suggestion" in st.session_state and st.session_state.selected_suggestion
    )

    user_first_interaction = (
        user_just_asked_initial_question or user_just_clicked_suggestion
    )

    has_message_history = len(st.session_state.messages) > 0

    # Show initial interface when no conversation exists
    if not user_first_interaction and not has_message_history:
        # Product selection
        st.markdown("### Select Grab Product")
        product_type = st.selectbox(
            "Choose the Grab service for your scenario:",
            options=["GrabFood", "GrabExpress", "GrabCar"],
            index=0,
            key="product_selector",
            help="Select the specific Grab product to get contextually relevant solutions"
        )
        
        st.session_state.product_type = product_type

        # Product-specific descriptions
        product_descriptions = {
            "GrabFood": "🍽️ Food delivery scenarios: Restaurant delays, damaged packaging, merchant issues, driver routing",
            "GrabExpress": "📦 Package delivery scenarios: Recipient unavailability, valuable packages, secure drop-offs",
            "GrabCar": "🚗 Ride scenarios: Traffic disruptions, route optimization, passenger urgency, flight connections"
        }

        st.info(product_descriptions[product_type])

        with st.container():
            st.chat_input("Describe a complex delivery disruption scenario...", key="initial_question")

            # Show product-specific examples
            if product_type in PRODUCT_EXAMPLES:
                selected_suggestion = st.pills(
                    label="Example Scenarios",
                    label_visibility="visible", 
                    options=PRODUCT_EXAMPLES[product_type].keys(),
                    key="selected_suggestion",
                )

        st.markdown("---")
        st.markdown("**Project Synapse** - Autonomous Last-Mile Delivery Coordination")
        st.markdown("*Supporting GrabFood | GrabExpress | GrabCar*")

        st.stop()

    # Handle user input
    user_message = st.chat_input("Ask a follow-up...")

    if not user_message:
        if user_just_asked_initial_question:
            user_message = st.session_state.initial_question
        if user_just_clicked_suggestion:
            user_message = PRODUCT_EXAMPLES[st.session_state.product_type][st.session_state.selected_suggestion]

    # Display chat messages from history
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.container()  # Fix ghost message bug

            st.markdown(message["content"])

            if message["role"] == "assistant":
                show_feedback_controls(i)

    # Process new user message
    if user_message:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_message)

        # Display assistant response
        with st.chat_message("assistant"):
            # Show selected product context
            st.markdown(f"**Product Context:** {st.session_state.product_type}")
            
            with st.spinner(f"Agent is analyzing the {st.session_state.product_type} scenario and planning actions..."):
                response = get_ai_response_with_tools(st.session_state.model, user_message, st.session_state.product_type)

            # Put everything after the spinner in a container to fix ghost message bug
            with st.container():
                # Display the response exactly as your original code did
                st.markdown(response)

                # Add messages to chat history
                st.session_state.messages.append({"role": "user", "content": user_message})
                st.session_state.messages.append({"role": "assistant", "content": response})

                # Show feedback controls
                show_feedback_controls(len(st.session_state.messages) - 1)

if __name__ == "__main__":
    main()