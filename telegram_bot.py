from telegram import Update, Bot
import requests
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
from telegram.utils.request import Request

from Opechatka import *
import symspell
symspell.init()

def log_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            print(f'Error: {exc}')
            raise exc

    return wrapper


def message_handler(update: Update, context: CallbackContext):
    update.message.reply_text(text='Example')
requests.post('http://130.193.51.51:5000/predict2', data='я иду'.encode()).text

@log_error
def symspell_ans(update: Update, context: CallbackContext):
    q = update.message['text'][10::]
    answer = symspell.solve_with_symspell(q)
    print(q)
    update.message.reply_text(text='Ответ с помощью симспелла = ' + answer)

@log_error
def trie_ans(update: Update, context: CallbackContext):
    q = update.message['text'][5::]
    answer = fix_text(q)
    print(q)
    update.message.reply_text(text='Ответ с помощью бора = ' + answer)

@log_error
def greet_user(update: Update, context: CallbackContext):
    update.message.reply_text("Я умею отвечать на запросы /symspell(с помощью symspell), /trie(с бором)")

def main():
    req = Request(connect_timeout=0.5)
    t_bot = Bot(
        request=req,
        token='1442678411:AAFIyGJ1KgFetSEErnLuvugXjTG7E1dXSxM',
        base_url='https://telegg.ru/orig/bot',
    )
    updater = Updater(bot=t_bot, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('help', greet_user))
    dp.add_handler(CommandHandler('symspell', symspell_ans))
    dp.add_handler(CommandHandler('trie', trie_ans))
    dp.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
