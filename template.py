import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    "src/logger.py",
    "sections/summarise_section.py",
    "sections/sanitize_data_section.py",
    "sections/write_article_section.py",
    "agents/__init__.py",
    "agents/agent_base.py",
    "agents/refiner_agent.py",
    "agents/validator_agent.py",
    "agents/sanitize_data_tool.py",
    "agents/sanitize_data_validation_agent.py",
    "agents/summarize_tool.py",
    "agents/summarize_validation_agent.py",
    "agents/write_article_tool.py",
    "agents/write_article_validation_agent.py",
    "agents/q_and_a_tool.py",
    ".env",
    "setup.py",
    "app.py",
    "store_index.py",
    "research/trials.ipynb",
]

for file in list_of_files:
    file_path = Path(file)
    file_dir, file_name = os.path.split(file_path)

    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Creating directory: {file_dir} for the file {file_name}")
    
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, 'w') as f:
            pass
            logging.info(f"Creating empty file: {file_path}")
    
    else:
        logging.info(f"{file_path} is already exists")