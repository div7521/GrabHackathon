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


def main():
    """Main function to run the AI agent with Streamlit"""

    st.set_page_config(
        page_title="Project Synapse",
        layout="wide"
    )
    st.title("Synapse")
    st.markdown("### Agentic Last-Mile Coordinator")

    st.markdown("""
    **Project Synapse** is an intelligent AI agent that autonomously resolves complex delivery disruptions across
    GrabFood, GrabExpress, and GrabCar services. Select your product type and describe a delivery scenario with problems,
    and watch the agent reason through solutions using available tools.
    """)

    # Initialize model in session state
    if 'model' not in st.session_state:
        with st.spinner("Initializing Project Synapse with tools..."):
            try:
                st.session_state.model = setup_gemini()
                st.success("Project Synapse initialized successfully!")
            except Exception as e:
                st.error(f"Setup failed: {e}")
                st.stop()

    # Product selection
    st.markdown("### Select Grab Product")
    product_type = st.selectbox(
        "Choose the Grab service for your scenario:",
        options=["GrabFood", "GrabExpress", "GrabCar"],
        index=0,
        help="Select the specific Grab product to get contextually relevant solutions"
    )

    # Product-specific descriptions
    product_descriptions = {
        "GrabFood": "Food delivery scenarios: Restaurant delays, damaged packaging, merchant issues, driver routing",
        "GrabExpress": "Package delivery scenarios: Recipient unavailability, valuable packages, secure drop-offs",
        "GrabCar": "Ride scenarios: Traffic disruptions, route optimization, passenger urgency, flight connections"
    }

    st.info(product_descriptions[product_type])

    st.markdown("### Describe Your Delivery Scenario")

    # Product-specific placeholders
    placeholders = {
        "GrabFood": "Example: Restaurant restaurant_002 is overloaded with 40-minute prep time. Customer CUST_123 has an urgent order and is getting impatient. The driver DRIVER_456 is waiting idle. What should we do?",
        "GrabExpress": "Example: Driver arrived at destination but recipient is unavailable for a valuable $200 electronics package. Package requires secure handling. What are the options?",
        "GrabCar": "Example: Passenger is heading to airport with flight SQ123 departing at 3 PM. Major accident detected on route_002 causing 30-minute delay. Current time is 1:30 PM. What should we do?"
    }

    user_input = st.text_area(
        "Enter a complex delivery disruption scenario:",
        placeholder=placeholders[product_type],
        height=120
    )


    # Submit button
    if st.button("Analyze & Resolve", type="primary"):
        if user_input.strip():
            st.markdown("---")
            st.markdown(f"### Project Synapse Analysis - {product_type}")

            # Show selected product context
            st.markdown(f"**Product Context:** {product_type}")

            with st.spinner(f"Agent is analyzing the {product_type} scenario and planning actions..."):
                response = get_ai_response_with_tools(st.session_state.model, user_input, product_type)

            # Display the response
            st.markdown(response)

        else:
            st.warning("Please describe a delivery scenario!")

    # Add footer with product info
    st.markdown("---")
    st.markdown("**Project Synapse** - Autonomous Last-Mile Delivery Coordination")
    st.markdown("*Supporting GrabFood | GrabExpress | GrabCar*")

if __name__ == "__main__":
    main()
