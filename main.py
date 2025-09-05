import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

#loads environment variables from .env file to applications environment
load_dotenv()

def setup_gemini():
    load_dotenv()

    api_key=os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    genai.configure(api_key=api_key)

    model=genai.GenerativeModel('gemini-1.5-flash')
    return model

def get_ai_response(model, user_input):
    """Get response from Gemini for given input"""
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"Error getting response: {e}"


def main():
    """Main function to run the AI agent with Streamlit"""
    st.title("AI Agent")
    
    # Initialize model in session state
    if 'model' not in st.session_state:
        st.session_state.model = setup_gemini()
    
    # Text input
    user_input = st.text_input("Ask me anything:")
    
    # Submit button
    if st.button("Get Answer"):
        if user_input:
            with st.spinner("Thinking..."):
                response = get_ai_response(st.session_state.model, user_input)
            st.write(response)
        else:
            st.warning("Please enter a question!")

if __name__ == "__main__":
    main()


