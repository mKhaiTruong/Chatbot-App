import streamlit as st
from agents import AgentManager
from sections.qa_section import qa_section, initialize_session_state  
from sections.summarise_section import summarize_section
from sections.sanitize_data_section import sanitize_data_section
from sections.write_article_section import write_and_refine_article_section

def main():
    st.set_page_config(page_title="Multi-Agent AI System", layout="wide")
    initialize_session_state()
    st.title("Multi-Agent AI System with Collaboration and Validation")

    st.sidebar.title("Select Task")
    task = st.sidebar.selectbox("Choose a task:", [
        "Question and Answer with Pre trained Model",
        "Summarize Text",
        "Write and Refine Research Article",
        "Sanitize Data (PHI)"
    ])

    agent_manager = AgentManager(max_retries=2, verbose=True)

    if task == "Question and Answer with Pre trained Model":
        qa_section(agent_manager)
    elif task == "Summarize Text":
        summarize_section(agent_manager)
    elif task == "Write and Refine Research Article":
        write_and_refine_article_section(agent_manager)
    elif task == "Sanitize Data (PHI)":
        sanitize_data_section(agent_manager)


if __name__ == "__main__":
    main()