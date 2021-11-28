import json
import spacy
from typing import List


class IntentFinder:
    def __init__(self):
        self._nlp = spacy.load("ru_core_news_sm")

        with open("./corpus.json") as file:
            self._corpus = json.load(file)

    def _has_intent(self, sentence: List[str], key_words: List[str]) -> bool:
        return len(set(sentence).intersection(set(key_words))) > 0

    def get_intents(self, sentence: str) -> List[str]:
        processed_sent = [str(token.lemma_) for token in self._nlp(sentence)]
        return [intent for intent, words in self._corpus.items() if self._has_intent(processed_sent, words)]
