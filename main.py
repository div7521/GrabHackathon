import streamlit as st
from agent import setup_model, stream_ai_response, PRODUCT_EXAMPLES, AVAILABLE_PRODUCTS

def show_feedback_controls(message_index):
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

            ""

            if st.form_submit_button("Send feedback"):
                if 'ratings' not in st.session_state:
                    st.session_state.ratings = []

                st.session_state.ratings.append({
                    'message_index': message_index,
                    'rating': rating,
                    'details': details,
                    'history': relevant_history
                })
                st.success("Thank you for your feedback!")

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'ratings' not in st.session_state:
        st.session_state.ratings = []

    if 'product_type' not in st.session_state:
        if not AVAILABLE_PRODUCTS:
            st.error("No product options available")
            st.stop()
        st.session_state.product_type = AVAILABLE_PRODUCTS[0]

    if 'model' not in st.session_state:
        with st.spinner("Initializing Synapse..."):
            try:
                st.session_state.model = setup_model()
                st.success("Synapse initialized successfully!")
            except Exception as e:
                st.error(f"Setup failed. Reason: {e}")
                st.stop()

def get_interaction_state():
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

    return user_first_interaction, has_message_history, user_just_asked_initial_question, user_just_clicked_suggestion

def show_product_interface(product_type):
    product_descriptions = {
        "GrabFood": "🍽️ **How to use:** Describe food delivery issues like 'Restaurant X has 30min delay, customer Y is urgent, driver Z waiting' - I'll analyze and resolve the situation",
        "GrabMart": "🛒 **How to use:** Describe grocery scenarios like 'Customer ordered 5 items, 2 out of stock, driver waiting' - I'll find the best solution",
        "GrabExpress": "📦 **How to use:** Describe package issues like 'High-value item, recipient unavailable, need secure option' - I'll handle delivery coordination",
        "GrabCar": "🚗 **How to use:** Describe ride problems like 'Traffic jam, passenger has flight, need alternative route' - I'll optimize the journey"
    }

    st.info(product_descriptions[product_type])

    with st.container():
        st.chat_input("Describe a delivery disruption scenario with specific IDs and details...", key="initial_question")

        if product_type in PRODUCT_EXAMPLES:
            st.pills(
                label="Example Scenarios (Click to Try)",
                label_visibility="visible",
                options=PRODUCT_EXAMPLES[product_type].keys(),
                key="selected_suggestion",
            )

    st.markdown("---")
    st.markdown("**Synapse** - Autonomous Last-Mile Delivery Coordination")
    st.markdown(f"*Supporting {' | '.join(AVAILABLE_PRODUCTS)}*")

def show_initial_interface():
    st.markdown("### Select Grab Product")
    product_type = st.selectbox(
        "Choose the Grab service for your scenario:",
        options=AVAILABLE_PRODUCTS,
        index=0,
        key="product_selector",
        help="Select the specific Grab product to get contextually relevant solutions"
    )

    st.session_state.product_type = product_type
    show_product_interface(product_type)

def get_user_message(user_just_asked_initial_question, user_just_clicked_suggestion):
    user_message = st.chat_input("Ask a follow-up...")

    if not user_message:
        if user_just_asked_initial_question:
            user_message = st.session_state.initial_question
        if user_just_clicked_suggestion:
            user_message = PRODUCT_EXAMPLES[st.session_state.product_type][st.session_state.selected_suggestion]

    return user_message

def display_chat_history():
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.container()

            st.markdown(message["content"])

            if message["role"] == "assistant":
                show_feedback_controls(i)

def process_user_message(user_message):
    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        st.markdown(f"**Product Context:** {st.session_state.product_type}")

        response_placeholder = st.empty()

        with st.spinner("Analyzing scenario..."):
            pass

        full_response = ""
        for chunk in stream_ai_response(st.session_state.model, user_message, st.session_state.product_type, st.session_state.messages):
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "user", "content": user_message})
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        show_feedback_controls(len(st.session_state.messages) - 1)

def clear_conversation():
    st.session_state.messages = []
    st.session_state.initial_question = None
    st.session_state.selected_suggestion = None

def main():
    st.set_page_config(
        page_title="Synapse",
        layout="wide",
        page_icon="🟢"
    )

    initialize_session_state()

    st.title("Synapse", anchor=False)
    st.caption("Agentic Last-Mile Coordinator")

    user_first_interaction, has_message_history, user_just_asked_initial_question, user_just_clicked_suggestion = get_interaction_state()

    if has_message_history or user_first_interaction:
        st.button(
            "Restart",
            icon=":material/refresh:",
            on_click=clear_conversation,
        )

    if not user_first_interaction and not has_message_history:
        show_initial_interface()
        st.stop()

    user_message = get_user_message(user_just_asked_initial_question, user_just_clicked_suggestion)

    display_chat_history()

    if user_message:
        process_user_message(user_message)

if __name__ == "__main__":
    main()
