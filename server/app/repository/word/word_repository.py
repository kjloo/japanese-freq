from app.model.word.word_list import WordList


class WordRepository:
    def add_words(self, words: list[str]) -> WordList:
        # Add a list of words to the WordList document in MongoDB
        word_list: WordList = WordList.objects.first()
        if not word_list:
            word_list = WordList(words=[])
        # Add only unique new words
        word_list.words = list(set(word_list.words) | set(words))
        word_list.save()
        return word_list

    def get_words(self) -> list[str]:
        # Retrieve the current list of words from MongoDB
        word_list: WordList = WordList.objects.first()
        return word_list.words if word_list else []

    def remove_word(self, word: str) -> WordList:
        # Remove a word from the WordList document in MongoDB
        word_list: WordList = WordList.objects.first()
        if word_list and word in word_list.words:
            word_list.words.remove(word)
            word_list.save()
        return word_list


word_repository = WordRepository()
