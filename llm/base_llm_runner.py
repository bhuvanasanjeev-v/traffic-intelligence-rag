from abc import ABC, abstractmethod


class BaseLLMRunner(ABC):
    """Common interface for all LLM runners."""

    @abstractmethod
    def run_prompt(self, prompt: str) -> str:
        """Execute a prompt and return the model response text."""
        raise NotImplementedError
