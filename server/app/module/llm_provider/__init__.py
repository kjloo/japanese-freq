from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    Defines the interface that all LLM implementations must follow.
    """

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str, max_tokens: int) -> str | None:
        """
        Generate text from the LLM.

        :param prompt: The user's prompt.
        :param system_prompt: The system prompt to set context.
        :param max_tokens: Maximum tokens to generate.
        :return: Generated text or None if failed.
        """
        pass

    @abstractmethod
    def is_loaded(self) -> bool:
        """
        Check if the LLM provider is available and responding.

        :return: True if the provider is available, False otherwise.
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get the name of the provider.

        :return: Provider name (e.g., "mlx", "openrouter").
        """
        pass
