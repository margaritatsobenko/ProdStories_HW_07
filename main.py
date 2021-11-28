import json
import random

import requests
import telebot

from handler import Handler

model = Handler()


def bot_run():
    bot_name = ""
    bot = telebot.TeleBot(bot_name)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Привет, рад видеть тебя!')
        bot.send_message(message.chat.id, 'Мой список команд:\n/start - Начать диалог\n' \
                                          '/get_news - Узнать любую новость\n/get_last_news - Узнать последнюю новость')
        bot.send_message(message.chat.id, 'Также ты можешь поприветствовать меня, попрощаться со мной '
                                          'и узнать несколько последних новостей, например: '
                                          'Хочу 3 новости')

    @bot.message_handler(commands=['get_news'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Хочешь новость?')

        response = json.loads(requests.get("https://meduza.io/api/w5/screens/news").text)
        keys = list(response["documents"].keys())
        le_keys = len(keys)
        while True:
            rand_ind = random.randint(0, le_keys - 1)
            news = response["documents"][keys[rand_ind]]
            if 'url' not in news:
                continue
            else:
                bot.send_message(message.chat.id, 'https://meduza.io/' + news["url"])
                break

    @bot.message_handler(commands=['get_last_news'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Хочешь последнюю новость?')

        response = json.loads(requests.get("https://meduza.io/api/w5/screens/news").text)
        keys = list(response["documents"].keys())
        while True:
            ind = 0
            news = response["documents"][keys[ind]]
            if 'url' not in news:
                ind += 1
                continue
            else:
                bot.send_message(message.chat.id, 'https://meduza.io/' + news["url"])
                break

    @bot.message_handler(content_types=["text"])
    def send_message(message):
        res = model.handle(message.text)

        for ans in res:
            bot.send_message(message.chat.id, ans)

    bot.polling()


if __name__ == '__main__':
    bot_run()
