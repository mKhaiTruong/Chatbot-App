from .agent_base import AgentBase

class SanitizeDataValidatorAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="Sanitize Data ValidatorAgent", max_retries=max_retries, verbose=verbose)
    
    def execute(self, original_data, sanitized_data):
        system_message = (
            "You are an AI assistant that validates the sanitization of sensitive data. "
            "Your job is to check whether all sensitive information has been successfully removed or anonymized."
        )
        user_content = (
            "Given the original data and the sanitized data, verify whether all sensitive information "
            "has been successfully removed or anonymized.\n"
            "Identify any remaining sensitive information in the sanitized data and provide specific feedback. "
            "Rate the sanitization process on a scale of 1 to 5, where 5 indicates complete and thorough sanitization.\n\n"
            f"Original Data:\n{original_data}\n\n"
            f"Sanitized Data:\n{sanitized_data}\n\n"
            "Validation:"
        )
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_content}
        ]

        validation = self.call_llama(messages)
        return validation