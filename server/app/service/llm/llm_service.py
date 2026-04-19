from mlx_lm import generate
from app.module.logging_module import logger
from app.module.llm_module import llm_module


def prompt_llm(user_prompt: str, system_prompt: str, max_tokens: int = 1500) -> str:
    """
    Sends a prompt to the Qwen3.6 model and returns the generated text.
    """
    model, tokenizer = llm_module.get_model_and_tokenizer()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # Format for Qwen's Instruct template
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    logger.debug(f"LLM Prompting with: {user_prompt[:50]}...")

    # Execution on M1 GPU
    response = generate(
        model, tokenizer, prompt=prompt, max_tokens=max_tokens, temp=0.7
    )

    return response


def get_llm_status() -> dict:
    """
    Check if the model is currently occupying memory.
    """
    return {"loaded": llm_module.is_loaded, "model_path": llm_module.model_path}
