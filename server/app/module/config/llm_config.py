import os


class LLMConfig:
    def __init__(self, config: dict):
        """
        Initialize the LLMConfig class by loading configuration from a YAML file.

        :param config: The configuration dictionary from YAML.
        """
        llm_config = config.get("llm", {})

        # Provider type: "mlx" or "openrouter"
        self.provider = os.getenv("LLM_PROVIDER", llm_config.get("provider", "mlx"))

        # MLX-specific configuration
        self.mlx_server_url = os.getenv(
            "LLM_SERVER_URL",
            llm_config.get("mlx_server_url", "http://localhost:8080/v1"),
        )
        self.mlx_model_name = os.getenv(
            "LLM_MODEL_NAME",
            llm_config.get("mlx_model_name", "mlx-community/Qwen3.5-9B-MLX-4bit"),
        )

        # OpenRouter-specific configuration
        self.openrouter_api_key = os.getenv(
            "OPENROUTER_API_KEY", llm_config.get("openrouter_api_key")
        )
        self.openrouter_model = os.getenv(
            "OPENROUTER_MODEL", llm_config.get("openrouter_model", "openai/gpt-4-turbo")
        )
        self.openrouter_base_url = llm_config.get(
            "openrouter_base_url", "https://openrouter.ai/api/v1"
        )

        # Common configuration
        self.temperature = float(llm_config.get("temperature", 0.7))
        self.max_tokens = int(llm_config.get("max_tokens", 2000))
        self.timeout = int(llm_config.get("timeout", 120))

    def validate(self) -> bool:
        """
        Validate the configuration for the selected provider.

        :return: True if valid, False otherwise.
        """
        if self.provider == "mlx":
            return bool(self.mlx_server_url)
        elif self.provider == "openrouter":
            return bool(self.openrouter_api_key)
        else:
            return False
