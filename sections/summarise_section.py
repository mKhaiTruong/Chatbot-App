import streamlit as st
from src.logger import logger

def summarize_section(agent_manager):
    st.header("Summarize Text")
    text = st.text_area("Enter text to summarize:", height=200)

    if st.button("Summarize"):
        if text:
            main_agent = agent_manager.get_agent("summarize")
            validator_agent = agent_manager.get_agent("summarize_validator")

            with st.spinner("Summarizing..."):
                try:
                    summary = main_agent.execute(text)
                    st.subheader("Summary:")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error: {e}")
                    logger.error(f"SummarizeAgent Error: {e}")
                    return
                
            with st.spinner("Validating summary..."):
                try:
                    validation = validator_agent.execute(original_text=text, summary=summary)
                    st.subheader("Validation:")
                    st.write(validation)
                except Exception as e:
                    st.error(f"Validation Error: {e}")
                    logger.error(f"SummarizeValidatorAgent Error: {e}")   

        else:
            st.warning("Please enter some text to summarize.")           