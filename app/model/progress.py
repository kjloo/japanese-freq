from flask import Response, jsonify


class Progress:
    def __init__(self):
        self.progress: float = 0

    def update_progress(self, progress: float):
        self.progress = progress

    def to_json(self) -> Response:
        return jsonify({'progress': self.progress})
