from .summarize_tool import SummarizeTool
from .summarize_validation_agent import SummarizeValidatorAgent
from .sanitize_data_tool import SanitizeDataTool
from .sanitize_data_validation_agent import SanitizeDataValidatorAgent
from .write_article_tool import WriteArticleTool
from .write_article_validation_agent import WriteArticleValidatorAgent

from .refiner_agent import RefinerAgent
from .validator_agent import ValidatorAgent
from .q_and_a_tool import QandATool

class AgentManager:
    def __init__(self, max_retries=2, verbose=True):
        self.agents = {
            "summarize": SummarizeTool(max_retries=max_retries, verbose=verbose),
            "summarize_validator": SummarizeValidatorAgent(max_retries=max_retries, verbose=verbose),
            "sanitize_data": SanitizeDataTool(max_retries=max_retries, verbose=verbose),
            "sanitize_data_validator": SanitizeDataValidatorAgent(max_retries=max_retries, verbose=verbose),
            "write_article": WriteArticleTool(max_retries=max_retries, verbose=verbose),
            "write_article_validator": WriteArticleValidatorAgent(max_retries=max_retries, verbose=verbose),

            "refiner": RefinerAgent(max_retries=max_retries, verbose=verbose),
            "validator": ValidatorAgent(max_retries=max_retries, verbose=verbose),
            "qa": QandATool(max_retries=max_retries, verbose=verbose),
        }
        

    def get_agent(self, agent_name):
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found.")
        return agent    