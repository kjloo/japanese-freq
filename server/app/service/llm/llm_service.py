from app.module.logging_module import logger
from app.gateway.llm import llm_gateway


def prompt_llm(user_prompt: str, system_prompt: str, max_tokens: int) -> str:
    """
    Sends a prompt to the LLM and returns the generated text.
    Delegates to the configured LLM provider via the gateway.
    """
    logger.debug(f"LLM Prompting with: {user_prompt[:50]}...")

    # Use the gateway function from llm_module.py
    response = llm_gateway.generate(
        prompt=user_prompt, system_prompt=system_prompt, max_tokens=max_tokens
    )

    if response is None:
        raise Exception("LLM provider returned no response. Check logs.")

    logger.debug(f"LLM Response: {response[:50]}...")
    return response


def get_llm_status() -> dict:
    """
    Get the status of the LLM provider.
    """
    return llm_gateway.get_provider_info()
