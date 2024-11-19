import streamlit as st
from src.logger import logger

def qa_section(agent_manager):
    st.header("Question and Answer with pre-trained NLP model")
    data = st.text_area("Enter question:", height=200)

    if st.button("Send"):
        if data:
            main_agent = agent_manager.get_agent("qa")

            with st.spinner("Query data..."):
                try:
                    ans = main_agent.execute(data)
                    st.subheader("Answer:")
                    st.write(ans)
                except Exception as e:
                    st.error(f"Error: {e}")
                    logger.error(f"SanitizeDataAgent Error: {e}")
                    return

        else:
            st.warning("Please enter medical data to sanitize.")
