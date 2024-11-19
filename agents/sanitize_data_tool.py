from .agent_base import AgentBase

class SanitizeDataTool(AgentBase):
    def __init__(self, max_retries=3, verbose=True):
        super().__init__(name="Sanitize Data Tool", max_retries=max_retries, verbose=verbose)
    
    def execute(self, data):
        messages = [
            {"role": "system", "content": "You are an AI assistant that sanitizes sensitive data."},
            {
                "role": "user", 
                "content": (
                    "Remove all sensitive from the following data:\n\n"
                    f"{data}\n\nSanitized Data:"
                )
            }
        ]

        sanitized_data = self.call_llama(messages)
        return sanitized_data