import json
import time
import urllib.parse as up

import pandas as pd
import requests as rqs

from utils.telegram_bot import TelegramBot

class DataLoader:

    ALERTS_URL = "https://docs.google.com/spreadsheets/u/1/d/1gcZX3KCwloO4c4ls0f40lUxYSLBrScswe9uyoXy2TjI/gviz/tq"
    NSE_URL = "https://www.nseindia.com/"
    QUOTES_URL_API = "https://www.nseindia.com/api/quote-equity?symbol="
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }

    cookies = None
    alerts_list = []

    def __init__(self):
        self.telegram_bot = TelegramBot()

    def prepare_headers(self, stock):
        self.HEADERS["referer"] = 'https://www.nseindia.com/get-quotes/equity?symbol=' + up.quote_plus(stock)
        return self.HEADERS

    def set_cookies(self):
        r = rqs.get(self.NSE_URL, headers=self.HEADERS)
        self.cookies = r.cookies.get_dict()
        print("Setting cookies")

    def get_quotes_for(self, stock):
        url = self.QUOTES_URL_API + up.quote_plus(stock)
        # print("Url is : ", url)
        r = rqs.get(url, headers=self.prepare_headers(stock), cookies=self.cookies)
        if r.status_code == 200:
            price = json.loads(r.text)["priceInfo"]["lastPrice"]
            return price
        else:
            print("-"*50)
            print("Error")
            print("Status code : ", r.status_code)
            print("Text : ", r.text[:20])
            print("Headers : ", self.HEADERS)
            print("-"*50)
            self.set_cookies()
            return None

    def load_alerts_data(self):
        self.alerts_list = []
        r = rqs.get(self.ALERTS_URL)
        if r.status_code == 200:
            data = r.text[47:-2]
            data = json.loads(data)
            for row in data['table']['rows']:
                stock_name = row['c'][0]['v']
                price = row['c'][1]['v']
                direction = row['c'][2]['v']
                self.alerts_list.append({
                    'stock_name': stock_name,
                    'price': price,
                    'direction': direction
                })
            return self.alerts_list
        else:
            return None

    def check_for_trigger(self, alert):
        price = self.get_quotes_for(alert['stock_name'])
        if price is None:
            return None
        print(f"{alert['stock_name']} Price : ", price)
        if price >= alert['price'] and alert['direction'] == 'Up':
            message = (f"Crossing Up : {alert['stock_name']}, "
                f"Current Price : {price}, "
                f"Alert Price : {alert['price']}")
            print(message)
            self.telegram_bot.send_message(message)
        elif price <= alert['price'] and alert['direction'] == 'Down':
            message = (f"Crossing Down : {alert['stock_name']}, "
                f"Current Price : {price}, "
                f"Alert Price : {alert['price']}")
            print(message)
            self.telegram_bot.send_message(message)

    def alert_if_trigger(self):
        if self.cookies is None:
            self.set_cookies()

        while True:
            print("-"*50)
            self.load_alerts_data()
            for alert in self.alerts_list:
                self.check_for_trigger(alert)
            time.sleep(10)

    def run(self):
        try:
            self.alert_if_trigger()
        except Exception as e:
            print(f"Error occured : {e}")
