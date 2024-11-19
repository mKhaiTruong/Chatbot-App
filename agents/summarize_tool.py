from .agent_base import AgentBase

class SummarizeTool(AgentBase):
    def __init__(self, max_retries=3, verbose=True):
        super().__init__(name="Summarize Tool", max_retries=max_retries, verbose=verbose)
    
    def execute(self, text):
        messages = [
            {"role": "system", "content": "You are an AI assistant that summarizes texts."},
            {
                "role": "user",
                "content": (
                    "Please provide a concise summary of the following text:\n\n"
                    f"{text}\n\nSummary:"
                )
            }
        ]
        summary = self.call_llama(messages)
        return summary