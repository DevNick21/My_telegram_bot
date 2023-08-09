import requests
import os
import telegram.ext
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("telegram_api_key")


# def send_msg(text):
#     token = TOKEN
#     chat_id = "1382061833"
#     url_req = "https://api.telegram.org/bot" + token + \
#         "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
#     results = requests.get(url_req)
#     print(results.status_code)


# send_msg("Hello there!")
def start(update, context):
    update.message.reply_text(
        "Hello! Welcome to Nicholas's bot!\nIt is still in development though but i hope you are excited to use it")


def help(update, context):
    update.message.reply_text()


updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher
