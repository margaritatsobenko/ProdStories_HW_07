from intent_finder import IntentFinder
import random
from news import NewsFeature


class Handler:

    def __init__(self):
        self.model = IntentFinder()
        self.news = NewsFeature()

    def handle(self, text):
        intents = self.model.get_intents(text)

        if len(intents) != 1:
            return [random.choice(['Прости, я тебя не понял.', 'Можешь еще раз повторить?'])]

        if intents[0] == 'hi':
            return [random.choice(['Здравствуй!', 'Привет!', 'Hello!'])]
        if intents[0] == 'end':
            return [random.choice(['Пока!', 'До свидания!', 'До встречи!', "Буду ждать новой встречи!"])]

        return self.news.handle(text)

