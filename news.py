import json
import random
from typing import Union, List

import spacy
from requests import get


class NewsNEExtractor:
    def __init__(self):
        self.__nlp = spacy.load("ru_core_news_sm")

    def __get_news_count(self, message: str):
        text2number = {'один': 1, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5,
                       'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9, 'десять': 10}

        tokens = self.__nlp(message.lower())
        lemmas = [token.lemma_ for token in tokens]

        for lemma in lemmas:
            if lemma in text2number:
                return text2number[lemma]
            elif lemma.isdigit():
                return int(lemma)

        return 1

    def extract_ne(self, message: str):
        return self.__get_news_count(message)


class NewsFeature:
    __api_url = "https://meduza.io/api/w5/screens/news"
    __domain = "https://meduza.io/"
    __error_responses = [
        "Извини, что-то не могу получить список новостей :(",
        "У меня проблемы, пожалуйста, попробуй ещё раз"
    ]

    def __init__(self):
        self.__extractor = NewsNEExtractor()

    def __handle_error_status_code(self) -> str:
        return random.choice(self.__error_responses)

    def __get_news(self, count):
        response = json.loads(get(self.__api_url).text)
        keys = list(response["documents"].keys())

        news_lst = []
        step, max_step = 0, 50
        ind = 0
        while len(news_lst) < count and step < max_step:

            news = response["documents"][keys[ind]]
            if 'url' not in news:
                ind += 1
                continue
            else:
                news_lst.append(self.__domain + news["url"])

            ind += 1
            step += 1

        if news_lst:
            return news_lst

        return self.__handle_error_status_code()

    def handle(self, message: str) -> Union[str, List[str]]:
        num_news = self.__extractor.extract_ne(message)

        news = self.__get_news(count=num_news)

        if isinstance(news, str):
            news = [news]
        return news
