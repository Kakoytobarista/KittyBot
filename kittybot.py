import logging
import os

import requests

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

from dotenv import load_dotenv


load_dotenv()

secret_token = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


URL_CAT_API = 'https://api.thecatapi.com/v1/images/search'
URL_DOG_API = 'https://api.thedogapi.com/v1/images/search'


def get_cat_image():
    try:
        response = requests.get(URL_CAT_API)
    except Exception as error:

        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(URL_DOG_API)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def get_dog_image():
    try:
        response = requests.get(URL_DOG_API)
    except Exception as error:

        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(URL_CAT_API)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_cat_image())


def new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_dog_image())


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    if not name:
        name = update.message.chat.title
    button = ReplyKeyboardMarkup([['/Give_me_new_cat', '/Give_me_new_dog']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри какого котика я тебе нашел'.format(name),
        reply_markup=button
    )

    context.bot.send_photo(chat.id, get_cat_image())


def main():
    updater = Updater(token=secret_token)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('Give_me_new_cat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('Give_me_new_dog', new_dog))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
