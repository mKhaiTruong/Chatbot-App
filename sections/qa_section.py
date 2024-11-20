import streamlit as st
from streamlit_chat import message
from src.logger import logger
import time

def qa_section(agent_manager):
    reply_container = st.container()
    container = st.container()

    with container:
        st.markdown(
            """
            <style>
            .centered-container {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-top: 10px;
                margin-bottom: 10px;
            }
            .custom-input {
                width: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        with st.form(key='my_form'):
            # Center the columns using a container with custom CSS
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown('<div class="centered-container">', unsafe_allow_html=True)
                user_input = st.text_input("", placeholder="Write your question here...", key='input', label_visibility="collapsed")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="centered-container">', unsafe_allow_html=True)
                submit_button = st.form_submit_button(label='Send', use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        if submit_button and user_input:
            main_agent = agent_manager.get_agent("qa")

            with st.spinner("Generating response..."):
                try:
                    ans = main_agent.execute(user_input)
                    st.session_state['past'].append(user_input)
                    st.session_state['generated'].append(ans)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    logger.error(f"SanitizeDataAgent Error: {e}")
                    return

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated']) - 1):
                message(st.session_state["past"][i], is_user=True, key=f"{i}_user", avatar_style="thumbs")
                message(st.session_state['generated'][i], is_user=False, key=f"{i}_bot")

            # Handle animation for the latest response only
            if st.session_state['generated']:
                latest_index = len(st.session_state['generated']) - 1
                message(st.session_state["past"][latest_index], is_user=True, key=f"{latest_index}_user", avatar_style="thumbs")
                message(st.session_state['generated'][latest_index], is_user=False, key=f"{latest_index}_bot")
                
                # response = st.empty()
                # full_response = st.session_state["generated"][latest_index]
                # typed_response = ""

                # for char in full_response:
                #     typed_response += char
                #     response.markdown(f"{typed_response}")
                #     time.sleep(0.008)  # Adjust speed by changing the sleep duration

def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]