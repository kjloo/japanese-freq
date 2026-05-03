from app.module.app_module import app
from app.module.logging_module import logger
from app.gateway.llm.mlx_provider import MLXProvider
from app.gateway.llm.openrouter_provider import OpenRouterProvider

# LLM configuration and provider
llm_config = app.config["LLM_CONFIG"]


def _create_llm_provider():
    """
    Factory function to create the appropriate LLM provider.

    :return: An instance of the configured LLM provider.
    """
    if llm_config.provider == "mlx":
        logger.info(
            f"Initializing MLX provider with server: {llm_config.mlx_server_url}"
        )
        return MLXProvider(
            server_url=llm_config.mlx_server_url,
            model_name=llm_config.mlx_model_name,
            temperature=llm_config.temperature,
            timeout=llm_config.timeout,
        )
    elif llm_config.provider == "openrouter":
        logger.info(
            f"Initializing OpenRouter provider with model: {llm_config.openrouter_model}"
        )
        return OpenRouterProvider(
            api_key=llm_config.openrouter_api_key,
            model=llm_config.openrouter_model,
            temperature=llm_config.temperature,
            timeout=llm_config.timeout,
            base_url=llm_config.openrouter_base_url,
        )
    else:
        raise ValueError(f"Unknown LLM provider: {llm_config.provider}")


llm_provider = _create_llm_provider()
logger.info(
    f"✅ LLM Gateway initialized with provider: {llm_provider.get_provider_name()}"
)
