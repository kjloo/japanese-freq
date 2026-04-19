from mlx_lm import load
from app.module.logging_module import logger

# Using the Qwen3.6 MoE model optimized for 16GB RAM
MODEL_PATH = "mlx-community/Qwen3.6-35B-A3B-4bit"


class LLMModule:
    def __init__(self):
        self._model = None
        self._tokenizer = None

    def get_model_and_tokenizer(self):
        """Lazy loader to ensure model is only loaded when needed."""
        if self._model is None:
            logger.info(f"🚀 Initializing Qwen3.6 via MLX: {MODEL_PATH}")
            self._model, self._tokenizer = load(MODEL_PATH)
        return self._model, self._tokenizer

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    @property
    def model_path(self) -> str:
        return MODEL_PATH


# Instantiate the module as a singleton
llm_module = LLMModule()
