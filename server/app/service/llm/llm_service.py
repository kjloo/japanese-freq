from app.module.logging_module import logger
from app.module.llm_module import llm_module


def prompt_llm(user_prompt: str, system_prompt: str, max_tokens: int) -> str:
    """
    Sends a prompt to the Sidecar MLX server and returns the generated text.
    """
    logger.debug(f"LLM Prompting with: {user_prompt[:50]}...")

    # Use the new generate method in llm_module.py
    response = llm_module.generate(
        prompt=user_prompt, system_prompt=system_prompt, max_tokens=max_tokens
    )

    if response is None:
        raise Exception("LLM Sidecar returned no response. Check sidecar.log.")

    logger.debug(f"LLM Response: {response[:50]}...")
    return response


def get_llm_status() -> dict:
    """
    Check if the sidecar is responsive.
    """
    # Note: model_path logic moved to sidecar server,
    # but we can return the URL for status.
    return {"loaded": llm_module.is_loaded, "endpoint": llm_module.base_url}
