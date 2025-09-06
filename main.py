import os
from dotenv import load_dotenv
import streamlit as st
from google import genai
from google.genai import types
from prompt import system_prompt
from tools import AVAILABLE_TOOLS, TOOL_SCHEMAS

#loads environment variables from .env file to applications environment
load_dotenv()

def setup_gemini():
    load_dotenv()

    api_key=os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")

    client = genai.Client(api_key=api_key)
    return client

def execute_tool_call(tool_name, arguments):
    """Execute a tool call with given arguments"""
    if tool_name not in AVAILABLE_TOOLS:
        return f"Error: Tool '{tool_name}' not found"

    try:
        tool_function = AVAILABLE_TOOLS[tool_name]
        result = tool_function(**arguments)
        return result
    except Exception as e:
        return f"Error executing {tool_name}: {str(e)}"

def get_ai_response_with_tools(model, user_input):
    """Get response from Gemini with tool calling support"""
    try:
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_input)])
        ]

        response = model.models.generate_content(
            model='gemini-1.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[TOOL_SCHEMAS],
            ),
        )

        if response.candidates and response.candidates[0].content:
            return response.candidates[0].content.parts[0].text
        return "No response generated"
    except Exception as e:
        return f"Error getting response: {e}"


def main():
    """Main function to run the AI agent with Streamlit"""

    st.set_page_config(
        page_title="Project Synapse",
        layout="wide"
    )
    st.title("Synapse")
    st.markdown("### Agentic Last-Mile Coordinator")

    st.markdown("""
    **Project Synapse** is an intelligent AI agent that autonomously resolves complex delivery disruptions.
    Describe a delivery scenario with problems, and watch the agent reason through solutions using available tools.
    """)

    # Initialize model in session state
    if 'model' not in st.session_state:
        with st.spinner("Initializing Project Synapse with tools..."):
            try:
                st.session_state.model = setup_gemini()
                st.success("✅ Project Synapse initialized successfully!")
            except Exception as e:
                st.error(f"❌ Setup failed: {e}")
                st.stop()

    st.markdown("### Describe Your Delivery Scenario")
    user_input = st.text_area(
        "Enter a complex delivery disruption scenario:",
        placeholder="Example: Restaurant restaurant_002 is overloaded with 40-minute prep time. Customer CUST_123 has an urgent order and is getting impatient. The driver DRIVER_456 is waiting idle. What should we do?",
        height=100
    )


    # Submit button
    # Submit button
    if st.button("Analyze & Resolve", type="primary"):
        if user_input.strip():
            st.markdown("---")
            st.markdown("### Project Synapse Analysis")

            with st.spinner("Agent is analyzing the scenario and planning actions..."):
                response = get_ai_response_with_tools(st.session_state.model, user_input)

            # Display the response
            st.markdown(response)

        else:
            st.warning("⚠️ Please describe a delivery scenario!")

    # Add footer
    st.markdown("---")
    st.markdown("**Project Synapse** - Autonomous Last-Mile Delivery Coordination")

if __name__ == "__main__":
    main()
