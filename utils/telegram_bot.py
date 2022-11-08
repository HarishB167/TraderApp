import json
import os

import requests as rqs

# Reference
# https://medium.com/codex/using-python-to-send-telegram-messages-in-3-simple-steps-419a8b5e5e2
class TelegramBot:

    def __init__(self):
        self.config = self.load_config()

    def create_url(self, message):
        self.url = (f"https://api.telegram.org/bot"
                    f"{self.config['token']}/"
                    f"sendMessage?chat_id={self.config['chat_id']}&text={message}")
        return self.url


    def load_config(self):  
        if os.path.exists("data/telegram_bot.dat"):
            filepath = os.path.join("data", "telegram_bot.dat")
            with open(filepath, 'r') as file:
                data = file.read()
                try:
                    obj = json.loads(data)
                    return obj
                except json.JSONDecodeError:
                    print("telegram_bot.dat file is not in JSON format.")
                    return None
        print("telegram_bot.dat file doesn't exist.")
        return None

    def get_config(self, key):
        config = self.load_config()        
        return config[key]

    def send_message(self, message):
        r = rqs.get(self.create_url(message))
        if r.status_code == 200:
            return True
        else: 
            print("Unable to send message : status_code : ", r.status_code)
            return False
