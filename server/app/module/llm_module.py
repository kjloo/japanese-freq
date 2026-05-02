from app.module.logging_module import logger
from app.module.config_module import _load_yaml_config, _get_env
from app.module.config.llm_config import LLMConfig
from app.module.llm_provider.mlx_provider import MLXProvider
from app.module.llm_provider.openrouter_provider import OpenRouterProvider


class LLMModule:
    def __init__(self):
        """Initialize the LLM module with the configured provider."""
        # Load LLM configuration
        env = _get_env()
        yaml_config = _load_yaml_config(env)
        llm_config = LLMConfig(yaml_config)

        # Validate configuration
        if not llm_config.validate():
            raise ValueError(
                f"Invalid LLM configuration for provider '{llm_config.provider}'. "
                f"Check your environment variables and config files."
            )

        # Instantiate the appropriate provider
        self.provider = self._create_provider(llm_config)
        self.config = llm_config

        logger.info(
            f"✅ LLM Module initialized with provider: {self.provider.get_provider_name()}"
        )

    def _create_provider(self, llm_config: LLMConfig):
        """
        Factory method to create the appropriate LLM provider.

        :param llm_config: The LLM configuration.
        :return: An instance of the configured LLM provider.
        """
        if llm_config.provider == "mlx":
            logger.info(
                f"Creating MLX provider with server: {llm_config.mlx_server_url}"
            )
            return MLXProvider(
                server_url=llm_config.mlx_server_url,
                model_name=llm_config.mlx_model_name,
                temperature=llm_config.temperature,
                timeout=llm_config.timeout,
            )
        elif llm_config.provider == "openrouter":
            logger.info(
                f"Creating OpenRouter provider with model: {llm_config.openrouter_model}"
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

    def generate(self, prompt: str, system_prompt: str, max_tokens: int) -> str | None:
        """
        Generate text using the configured LLM provider.

        :param prompt: The user's prompt.
        :param system_prompt: The system prompt.
        :param max_tokens: Maximum tokens to generate.
        :return: Generated text or None if failed.
        """
        logger.debug(f"LLM Prompting with: {prompt[:50]}...")
        response = self.provider.generate(prompt, system_prompt, max_tokens)
        if response:
            logger.debug(f"LLM Response: {response[:50]}...")
        return response

    @property
    def is_loaded(self) -> bool:
        """
        Check if the LLM provider is available.

        :return: True if the provider is responsive, False otherwise.
        """
        return self.provider.is_loaded()


llm_module = LLMModule()
