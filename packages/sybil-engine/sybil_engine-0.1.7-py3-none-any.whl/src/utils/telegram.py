import telebot

from config import telegram_api_chat_id, telegram_api_key


def send_to_bot(msg):
    try:
        bot = telebot.TeleBot(telegram_api_key)
        bot.send_message(telegram_api_chat_id, msg)
    except Exception as error:
        print(f"Fail to send {msg}")
        print(error)