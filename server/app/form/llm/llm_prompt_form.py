from typing import override
from app.form.base_form import BaseForm


class LLMPromptForm(BaseForm):
    """
    Form to handle and validate LLM generation requests.
    """

    prompt: str = ""
    system_prompt: str = ""
    max_tokens: int = 1000

    def __init__(self, json_data: dict[str]):
        self.prompt = json_data.get("prompt", "")
        # Default to a Japanese-focused assistant if not provided
        self.system_prompt = json_data.get(
            "system_prompt", "あなたは日本語のプロフェッショナルです。"
        )
        self.max_tokens = json_data.get("max_tokens", 1000)
        super().__init__()

    def to_dict(self) -> dict:
        """
        Returns a clean dictionary for the service layer.
        """
        return {
            "prompt": self.prompt,
            "system_prompt": self.system_prompt,
            "max_tokens": self.max_tokens,
        }

    @override
    def _validate(self):
        if not self.prompt or not isinstance(self.prompt, str):
            raise ValueError("Prompt cannot be empty and must be a string")

        if len(self.prompt.strip()) == 0:
            raise ValueError("Prompt cannot be just whitespace")

        if not isinstance(self.max_tokens, int) or self.max_tokens <= 0:
            raise ValueError("max_tokens must be a positive integer")
