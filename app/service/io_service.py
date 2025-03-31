import json

from model.file_manager import FileManager

input_dir: str = 'input'
output_dir: str = 'output'


def get_inputs() -> list[str]:
    file_manager = get_file_manager()
    return [f.get_name() for f in file_manager.source_content]


def get_file_manager() -> FileManager:
    return FileManager(input_dir, output_dir)


def write_to_json(data: dict, output_file: str):
    with open(output_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
