from llm.base_llm_runner import BaseLLMRunner
from llm.gemini_llm_runner import GeminiLLMRunner


class LLMRunnerFactory:
    """Factory for creating LLM runner instances."""

    @staticmethod
    def create_runner(provider: str = "gemini", **kwargs) -> BaseLLMRunner:
        provider_name = provider.lower().strip()

        if provider_name == "gemini":
            return GeminiLLMRunner(**kwargs)

        raise ValueError(
            f"Unsupported LLM provider: {provider}. Supported providers: gemini"
        )
