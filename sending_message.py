import requests
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("telegram_api_key")
CHAT_ID = os.getenv("CHAT_ID")


class Message():
    def __init__(self, message):
        self.send_message(message)
        pass

    def send_message(self, message):
        token = TOKEN
        chat_id = CHAT_ID
        url_req = "https://api.telegram.org/bot" + token + \
            f"/sendMessage?chat_id={chat_id}&text={message}"
        res = requests.get(url_req)
        res.raise_for_status()
        print(res.text)
