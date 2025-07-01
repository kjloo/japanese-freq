from app.repository.base_repository import BaseRepository


class WordRepository(BaseRepository):
    def __init__(self):
        super().__init__("words")

    def add_words(self, words: list[str]):
        # Add a list of words to the list in MongoDB
        self.collection.update_one(
            {"_id": "word_list"},
            {"$addToSet": {"words": {"$each": words}}},
            upsert=True,
        )

    def remove_word(self, word: str):
        # Remove a word from the list in MongoDB
        self.collection.update_one(
            {"_id": "word_list"},
            {"$pull": {"words": word}},  # `$pull` removes the item from the array
        )

    def get_words(self) -> list[str]:
        # Retrieve the current list of words from MongoDB
        result = self.collection.find_one({"_id": "word_list"})
        return result.get("words", [])


word_repository = WordRepository()
