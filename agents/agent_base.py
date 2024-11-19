from langchain_ollama import OllamaLLM
from abc import ABC, abstractmethod
from loguru import logger
import os

class AgentBase(ABC):
    def __init__(self, name, model="llama3.2", max_tokens=2048, temperature=0.5, max_retries=2, verbose=True):
        self.name = name
        self.max_retries = max_retries
        self.verbose = verbose
        self.llama = OllamaLLM(model=model, max_tokens=max_tokens, temperature=temperature)

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def call_llama(self, messages):
        retries = 0
        while retries < self.max_retries:
            try:
                combined_prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

                if self.verbose:
                    logger.info(f"[{self.name}] Sending combined prompt to OLlama:")
                    logger.debug(combined_prompt)

                response = self.llama.invoke(input=combined_prompt)

                if isinstance(response, str):
                    reply = response
                else:
                    try:
                        reply = response["choices"][0]["message"]
                    except (IndexError, KeyError) as e:
                        logger.error(f"[{self.name}] Unexpected response structure: {response}")
                        raise Exception(f"[{self.name}] Failed to parse response: {e}")

                if self.verbose:
                    logger.info(f"[{self.name}] Received response: {reply[:200]}...")  # Truncated for readability
                return reply

            except Exception as e:
                retries += 1
                logger.error(f"[{self.name}] Error during OLlama call: {e}. Retry {retries}/{self.max_retries}")
                if retries < self.max_retries:
                    logger.info(f"[{self.name}] Retrying...")

        raise Exception(f"[{self.name}] Failed to get response from OLlama after {self.max_retries} retries.")
