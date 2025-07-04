class Progress:
    def __init__(self):
        self.progress: float = 0

    def update_progress(self, progress: float):
        self.progress = progress * 100

    def to_json(self) -> dict:
        return {"progress": self.progress}
