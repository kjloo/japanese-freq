import json

from app.module.file_module import file_manager
from app.serde.encoder import CustomJSONEncoder


def get_inputs() -> list[str]:
    return [f.get_name() for f in file_manager.source_content]


def write_to_json(data: dict, output_file: str):
    with open(output_file, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, cls=CustomJSONEncoder)
