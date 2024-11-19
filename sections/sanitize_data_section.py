import streamlit as st
from src.logger import logger

def sanitize_data_section(agent_manager):
    st.header("Sanitize Medical Data (PHI)")
    data = st.text_area("Enter data to sanitize:", height=200)

    if st.button("Sanitize Data"):
        if data:
            main_agent = agent_manager.get_agent("sanitize_data")
            validator_agent = agent_manager.get_agent("sanitize_data_validator")

            with st.spinner("Sanitizing data..."):
                try:
                    sanitized_data = main_agent.execute(data)
                    st.subheader("Sanitized Data:")
                    st.write(sanitized_data)
                except Exception as e:
                    st.error(f"Error: {e}")
                    logger.error(f"SanitizeDataAgent Error: {e}")
                    return
            
            with st.spinner("Validating sanitized data..."):
                try:
                    validation = validator_agent.execute(original_data=data, sanitized_data=sanitized_data)
                    st.subheader("Validation:")
                    st.write(validation)
                except Exception as e:
                    st.error(f"Validation Error: {e}")
                    logger.error(f"SanitizeDataValidatorAgent Error: {e}")

        else:
            st.warning("Please enter medical data to sanitize.")
