from app.module.logging_module import logger
from app.module.llm_module import llm_config, llm_provider


def generate(prompt: str, system_prompt: str, max_tokens: int) -> str | None:
    """
    Generate text using the configured LLM provider.

    :param prompt: The user's prompt.
    :param system_prompt: The system prompt to set context.
    :param max_tokens: Maximum tokens to generate.
    :return: Generated text or None if failed.
    """
    logger.debug(f"LLM Gateway: Generating with prompt: {prompt[:50]}...")
    response = llm_provider.generate(prompt, system_prompt, max_tokens)
    if response:
        logger.debug(f"LLM Gateway: Response: {response[:50]}...")
    return response


def is_available() -> bool:
    """
    Check if the LLM provider is available and responding.

    :return: True if the provider is responsive, False otherwise.
    """
    return llm_provider.is_loaded()


def get_provider_info() -> dict:
    """
    Get information about the configured LLM provider.

    :return: Dictionary with provider information.
    """
    return {
        "provider": llm_provider.get_provider_name(),
        "available": is_available(),
        "config": {
            "temperature": llm_config.temperature,
            "max_tokens": llm_config.max_tokens,
            "timeout": llm_config.timeout,
        },
    }
