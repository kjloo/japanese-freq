from flask import Blueprint, jsonify, Response, request
from app.form.llm.llm_prompt_form import LLMPromptForm
from app.service.llm import llm_service
from app.module.logging_module import logger

llm_routes = Blueprint("llm_routes", __name__)


@llm_routes.route("/api/llm/generate", methods=["POST"])
def generate_response() -> Response:
    data = request.get_json()

    try:
        form = LLMPromptForm(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    try:
        response_text = llm_service.prompt_llm(
            user_prompt=form.prompt,
            system_prompt=form.system_prompt,
            max_tokens=form.max_tokens,
        )

        return (
            jsonify(
                {
                    "model": llm_service.get_llm_status()["model_path"],
                    "response": response_text,
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"LLM Generation failed: {str(e)}")
        return jsonify({"error": "Internal model error"}), 500


@llm_routes.route("/api/llm/status", methods=["GET"])
def get_status() -> Response:
    return jsonify(llm_service.get_llm_status()), 200
